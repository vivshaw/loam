"""tests for continue-autonomous-run.py Stop hook."""

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest

SCRIPT = os.path.join(os.path.dirname(__file__), "continue-autonomous-run.py")

SESSION = "sess-0001"
PLAN_DIR = ".loam/tasks/2026-08-09-widgets"


def write_run(root: Path, **overrides: Any) -> Path:
    """Write .loam/run.json with sensible defaults, returning its path."""
    run = {
        "plan_dir": PLAN_DIR,
        "session_id": SESSION,
        "status": "active",
        "continuations": 0,
        "last_remaining": None,
        "stalls": 0,
    }
    run.update(overrides)
    path = root / ".loam" / "run.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(run))
    return path


def write_plan(root: Path, body: str) -> None:
    """Write the plan's `plan.md`, the hook's only source of progress."""
    plan_dir = root / PLAN_DIR
    plan_dir.mkdir(parents=True, exist_ok=True)
    (plan_dir / "plan.md").write_text(body)


def read_run(root: Path) -> dict[str, Any]:
    return json.loads((root / ".loam" / "run.json").read_text())


def run_hook(root: Path, *, session_id: str = SESSION, stop_hook_active: bool = False) -> Any:
    """Run the hook against `root` and return parsed stdout, or None if silent."""
    payload = json.dumps(
        {
            "hook_event_name": "Stop",
            "session_id": session_id,
            "cwd": str(root),
            "transcript_path": str(root / "transcript.jsonl"),
            "permission_mode": "default",
            "stop_hook_active": stop_hook_active,
        }
    )
    result = subprocess.run(
        [sys.executable, SCRIPT],
        input=payload,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"hook exited {result.returncode}: {result.stderr}"
    if not result.stdout.strip():
        return None
    return json.loads(result.stdout)


def blocks(output: Any) -> bool:
    return isinstance(output, dict) and output.get("decision") == "block"


# ===== section 1: the hook stays out of the way unless a run is active =====


def test_no_run_file_is_silent(tmp_path: Path) -> None:
    """The overwhelmingly common case: no autonomous run, so behave as if absent."""
    assert run_hook(tmp_path) is None


def test_malformed_run_file_is_silent(tmp_path: Path) -> None:
    path = tmp_path / ".loam" / "run.json"
    path.parent.mkdir(parents=True)
    path.write_text("{not json")
    assert run_hook(tmp_path) is None


def test_other_session_is_silent(tmp_path: Path) -> None:
    """A claimed run belonging to another session must not hijack this one."""
    write_run(tmp_path)
    write_plan(tmp_path, "- [ ] ### Task 1: Thing\n")
    assert run_hook(tmp_path, session_id="a-different-session") is None


# ===== section 1b: claiming =====
#
# The model cannot read its own session id, so it arms runs unclaimed and the
# hook stamps its own id in on first sight.


@pytest.mark.parametrize("unclaimed", [None, ""], ids=["null", "empty"])
def test_first_session_claims_an_unclaimed_run(tmp_path: Path, unclaimed: str | None) -> None:
    write_run(tmp_path, session_id=unclaimed)
    write_plan(tmp_path, "- [ ] ### Task 1: Thing\n")
    assert blocks(run_hook(tmp_path))
    assert read_run(tmp_path)["session_id"] == SESSION


def test_absent_session_id_is_also_unclaimed(tmp_path: Path) -> None:
    """The skill tells the model to omit the field entirely."""
    path = write_run(tmp_path)
    run = json.loads(path.read_text())
    del run["session_id"]
    path.write_text(json.dumps(run))
    write_plan(tmp_path, "- [ ] ### Task 1: Thing\n")
    assert blocks(run_hook(tmp_path))
    assert read_run(tmp_path)["session_id"] == SESSION


def test_a_claimed_run_is_not_re_claimed(tmp_path: Path) -> None:
    write_run(tmp_path, session_id="the-original-session")
    write_plan(tmp_path, "- [ ] ### Task 1: Thing\n")
    assert run_hook(tmp_path) is None
    assert read_run(tmp_path)["session_id"] == "the-original-session"


def test_clearing_session_id_re_arms_after_a_resume(tmp_path: Path) -> None:
    """Recovery path when a resumed session gets a fresh id: drop the field."""
    write_run(tmp_path, session_id="a-stale-id-from-before-the-resume")
    write_plan(tmp_path, "- [ ] ### Task 1: Thing\n")
    assert run_hook(tmp_path) is None

    path = tmp_path / ".loam" / "run.json"
    run = json.loads(path.read_text())
    del run["session_id"]
    path.write_text(json.dumps(run))

    assert blocks(run_hook(tmp_path))
    assert read_run(tmp_path)["session_id"] == SESSION


@pytest.mark.parametrize("status", ["pending", "paused", "completed", "capped", "stalled", "error"])
def test_inactive_status_is_silent(tmp_path: Path, status: str) -> None:
    write_run(tmp_path, status=status)
    write_plan(tmp_path, "- [ ] ### Task 1: Thing\n")
    assert run_hook(tmp_path) is None


def test_stop_hook_active_is_silent(tmp_path: Path) -> None:
    """Guards against the hook re-entering its own continuation."""
    write_run(tmp_path)
    write_plan(tmp_path, "- [ ] ### Task 1: Thing\n")
    assert run_hook(tmp_path, stop_hook_active=True) is None


# ===== section 2: counting unchecked work =====


def test_blocks_while_tasks_remain(tmp_path: Path) -> None:
    write_run(tmp_path)
    write_plan(tmp_path, "- [x] ### Task 1: Done\n- [ ] ### Task 2: Pending\n",
    )
    output = run_hook(tmp_path)
    assert blocks(output)
    assert "Task 2: Pending" in output["reason"]


def test_silent_when_everything_checked(tmp_path: Path) -> None:
    write_run(tmp_path)
    write_plan(tmp_path, "- [x] ### Task 1: Done\n")
    write_plan(tmp_path, "- [X] ### Task 2: Done\n")
    assert run_hook(tmp_path) is None
    assert read_run(tmp_path)["status"] == "completed"


def test_indented_checkboxes_are_ignored(tmp_path: Path) -> None:
    """Requirements nest under a task; only column-0 boxes are work items."""
    write_plan(tmp_path, "- [x] ### Task 1: Done\n  - [ ] widgets.1.1 verified\n    - [ ] deeper still\n",
    )
    write_run(tmp_path)
    assert run_hook(tmp_path) is None


def test_next_item_follows_document_order(tmp_path: Path) -> None:
    """Document order in plan.md is execution order; no sorting is involved."""
    write_run(tmp_path)
    write_plan(tmp_path, "- [ ] Early issue\n- [ ] Late issue\n")
    output = run_hook(tmp_path)
    assert "Early issue" in output["reason"]
    assert "Late issue" not in output["reason"]


def test_ticked_items_are_skipped(tmp_path: Path) -> None:
    write_run(tmp_path)
    write_plan(tmp_path, "- [x] Done issue\n- [ ] Pending issue\n")
    assert "Pending issue" in run_hook(tmp_path)["reason"]


def test_reason_names_the_issue_file_and_skill(tmp_path: Path) -> None:
    """The continuation turn gets no UserPromptSubmit hooks, so it must self-orient."""
    write_run(tmp_path)
    write_plan(tmp_path, "- [ ] [02 - TokenService](issues/02-token-service.md)\n")
    reason = run_hook(tmp_path)["reason"]
    assert "issues/02-token-service.md" in reason
    assert "core:execute-implement-a-project" in reason


def test_unlinked_boxes_are_worked_from_the_plan(tmp_path: Path) -> None:
    """Milestone gates and wrap-up boxes have no issue file of their own."""
    write_run(tmp_path)
    write_plan(tmp_path, "- [ ] Milestone 1 verified\n")
    reason = run_hook(tmp_path)["reason"]
    assert "plan.md" in reason
    assert "issues/" not in reason


def test_missing_plan_errors_once_then_goes_quiet(tmp_path: Path) -> None:
    """A bad plan_dir must surface itself rather than silently disabling autonomy."""
    write_run(tmp_path, plan_dir=".loam/tasks/typo")
    output = run_hook(tmp_path)
    assert blocks(output)
    assert read_run(tmp_path)["status"] == "error"
    assert run_hook(tmp_path) is None


# ===== section 2b: the wrap-up checklist =====
#
# The wrap-up sequence belongs to no milestone. It sits at the end of plan.md and
# must keep the loop alive after every milestone box is ticked.

WRAP_UP = "- [ ] Final code review passed\n"


def test_wrap_up_keeps_the_run_alive(tmp_path: Path) -> None:
    write_run(tmp_path)
    write_plan(tmp_path, "- [x] [01 - Setup](issues/01-setup.md)\n" + WRAP_UP)
    output = run_hook(tmp_path)
    assert blocks(output)
    assert "Final code review" in output["reason"]


def test_wrap_up_is_ordered_after_every_milestone(tmp_path: Path) -> None:
    """Wrap-up sits last in the document, so pending issues outrank it."""
    write_run(tmp_path)
    write_plan(tmp_path, "- [ ] [01 - Setup](issues/01-setup.md)\n" + WRAP_UP)
    reason = run_hook(tmp_path)["reason"]
    assert "01 - Setup" in reason
    assert "Final code review" not in reason


def test_milestone_gate_outranks_wrap_up(tmp_path: Path) -> None:
    """A milestone is not done until its gate is ticked, wrap-up notwithstanding."""
    write_run(tmp_path)
    write_plan(
        tmp_path,
        "- [x] [01 - Setup](issues/01-setup.md)\n- [ ] Milestone 1 verified\n" + WRAP_UP,
    )
    reason = run_hook(tmp_path)["reason"]
    assert "Milestone 1 verified" in reason
    assert "Final code review" not in reason


def test_run_completes_only_once_wrap_up_is_ticked(tmp_path: Path) -> None:
    write_run(tmp_path)
    write_plan(
        tmp_path,
        "- [x] [01 - Setup](issues/01-setup.md)\n- [x] Final code review passed\n",
    )
    assert run_hook(tmp_path) is None
    assert read_run(tmp_path)["status"] == "completed"


# ===== section 2c: breadcrumbs =====
#
# A run that stops continuing is invisible from inside the session, so the hook
# leaves an after-the-fact record for whoever comes asking why.


def read_log(root: Path) -> str:
    path = root / ".loam" / "run.log"
    return path.read_text() if path.exists() else ""


def test_foreign_claim_leaves_a_breadcrumb(tmp_path: Path) -> None:
    """The orphaned-run signature — the whole reason the log exists."""
    write_run(tmp_path, session_id="the-original-session")
    write_plan(tmp_path, "- [ ] ### Task 1: Thing\n")
    assert run_hook(tmp_path) is None
    log = read_log(tmp_path)
    assert "the-original-session" in log
    assert SESSION in log


def test_halting_leaves_a_breadcrumb(tmp_path: Path) -> None:
    write_run(tmp_path, continuations=30)
    write_plan(tmp_path, "- [ ] ### Task 1: Thing\n")
    run_hook(tmp_path)
    assert "capped" in read_log(tmp_path)


def test_completion_leaves_a_breadcrumb(tmp_path: Path) -> None:
    write_run(tmp_path)
    write_plan(tmp_path, "- [x] ### Task 1: Done\n")
    run_hook(tmp_path)
    assert "completed" in read_log(tmp_path)


def test_quiet_cases_do_not_spam_the_log(tmp_path: Path) -> None:
    """No run at all is the normal case for every other loam session."""
    assert run_hook(tmp_path) is None
    assert read_log(tmp_path) == ""


# ===== section 3: runaway guards =====


def test_continuation_count_increments(tmp_path: Path) -> None:
    write_run(tmp_path)
    write_plan(tmp_path, "- [ ] ### Task 1: Thing\n")
    run_hook(tmp_path)
    assert read_run(tmp_path)["continuations"] == 1
    assert read_run(tmp_path)["last_remaining"] == 1


def test_continuation_cap_stops_the_run(tmp_path: Path) -> None:
    write_run(tmp_path, continuations=30)
    write_plan(tmp_path, "- [ ] ### Task 1: Thing\n")
    output = run_hook(tmp_path)
    assert blocks(output)
    assert "cap" in output["reason"].lower()
    assert read_run(tmp_path)["status"] == "capped"
    assert run_hook(tmp_path) is None


def test_progress_resets_the_stall_counter(tmp_path: Path) -> None:
    write_run(tmp_path, last_remaining=3, stalls=1)
    write_plan(tmp_path, "- [ ] ### Task 1: A\n- [ ] ### Task 2: B\n")
    assert blocks(run_hook(tmp_path))
    assert read_run(tmp_path)["stalls"] == 0


def test_one_stalled_turn_is_tolerated(tmp_path: Path) -> None:
    """A turn spent investigating without ticking a box is normal."""
    write_run(tmp_path, last_remaining=1, stalls=0)
    write_plan(tmp_path, "- [ ] ### Task 1: Thing\n")
    assert blocks(run_hook(tmp_path))
    assert read_run(tmp_path)["status"] == "active"
    assert read_run(tmp_path)["stalls"] == 1


def test_two_stalled_turns_stop_the_run(tmp_path: Path) -> None:
    write_run(tmp_path, last_remaining=1, stalls=1)
    write_plan(tmp_path, "- [ ] ### Task 1: Thing\n")
    output = run_hook(tmp_path)
    assert blocks(output)
    assert "no progress" in output["reason"].lower()
    assert read_run(tmp_path)["status"] == "stalled"
    assert run_hook(tmp_path) is None
