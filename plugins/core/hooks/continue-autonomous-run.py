#!/usr/bin/env python3
"""
Stop hook that drives `core:execute-implement-a-project-autonomously`.

When `.gro/run.json` marks an autonomous run as active for this session, the
hook counts unchecked work items in the plan's `plan.md`. Work left means the
turn is blocked and the model is handed the next item; no work left means the
hook stays silent and the session ends on its own.

`plan.md` is the single source of truth for progress: milestone issue boxes,
milestone verification gates, and the wrap-up checklist all live there, in the
order they must be worked. Document order is execution order.

The continuation condition is a pure function of files on disk. The model
cannot talk its way past it -- it can only tick a checkbox, which
`core:execute-implement-a-project` permits only after the work is verified.
"""

import json
import os
import re
import sys
from datetime import datetime
from typing import Any

# Column 0 only, so that any nested list in plan.md stays detail rather than
# becoming trackable work. Issue files are never scanned at all -- their "Done
# when" is plain bullets precisely so no second progress record can exist.
CHECKBOX = re.compile(r"^- \[([ xX])\] (.*)$")

# Issue boxes link to their file: `- [ ] [02 -- TokenService](issues/02-token.md)`.
# Gate and wrap-up boxes carry no link and are worked from plan.md itself.
ISSUE_LINK = re.compile(r"\[[^\]]*\]\(([^)]+\.md)\)")

CONTINUATION_CAP = 30
STALL_LIMIT = 2

CONTINUE = """<autonomous-run>
You are mid-flight on an autonomous run. The turn ended with work
remaining, so this is an automatic continuation. The contract is to keep
going until every checkbox is `- [x]`, so don't ask whether to continue.

- Plan directory: `{plan_dir}`
- Next unchecked item: `{next_item}`
- Work it from: `{work_file}`
- Remaining: {remaining} of {total}

Re-invoke the `core:execute-implement-a-project` skill and resume from that
item. `plan.md` is the source of truth for what is done, not your memory of
earlier turns. Tick an issue's checkbox only after you have verified the
executor's report; tick a milestone gate only after its requirement tests pass
and the review loop returns zero issues.

Surface state changes only. Do not restate the plan or recap prior turns.
</autonomous-run>"""

HALTED = """<autonomous-run-halted>
The autonomous run has been halted: {why}

Its status in `.gro/run.json` is now `{status}`, so it will not resume. Stop
work, tell your human partner what happened and what remains unchecked in
`{plan_dir}/plan.md`, and let them decide how to proceed.
</autonomous-run-halted>"""


def load_run(run_path: str) -> dict[str, Any] | None:
    try:
        with open(run_path) as handle:
            run = json.load(handle)
    except (OSError, json.JSONDecodeError):
        return None
    return run if isinstance(run, dict) else None


def save_run(run_path: str, run: dict[str, Any]) -> None:
    try:
        with open(run_path, "w") as handle:
            json.dump(run, handle, indent=2)
            handle.write("\n")
    except OSError:
        pass


def breadcrumb(cwd: str, message: str) -> None:
    """Record why the loop stopped.

    A run that stops continuing is invisible from inside the session -- there is
    no turn in which to notice a wake-up that never came. Only an after-the-fact
    record can answer "why did it go quiet", so every terminal decision leaves
    one. Routine silence (no run armed) writes nothing.
    """
    stamp = datetime.now().isoformat(timespec="seconds")
    try:
        with open(os.path.join(cwd, ".gro", "run.log"), "a") as handle:
            handle.write(f"{stamp} {message}\n")
    except OSError:
        pass


def scan_plan(plan_dir: str) -> tuple[int, int, str | None, str | None]:
    """Return (remaining, total, next item text, file to work it from).

    Only `plan.md` is read. Issue files carry no status of their own, so there is
    nothing to reconcile between two records -- and document order in plan.md is
    already execution order, which is why no sorting is needed.
    """
    remaining = 0
    total = 0
    next_item: str | None = None
    next_file: str | None = None

    path = os.path.join(plan_dir, "plan.md")
    try:
        with open(path) as handle:
            lines = handle.read().splitlines()
    except OSError:
        return 0, 0, None, None

    for line in lines:
        match = CHECKBOX.match(line)
        if match is None:
            continue
        total += 1
        if match.group(1) != " ":
            continue
        remaining += 1
        if next_item is None:
            next_item = match.group(2).strip()
            link = ISSUE_LINK.search(next_item)
            # An issue box points at its file; a gate or wrap-up box is worked
            # from plan.md itself.
            next_file = os.path.join(plan_dir, link.group(1)) if link else path

    return remaining, total, next_item, next_file


def halt(cwd: str, run_path: str, run: dict[str, Any], status: str, why: str) -> None:
    """Mark the run terminal and tell the model once, so it can report out."""
    run["status"] = status
    save_run(run_path, run)
    breadcrumb(cwd, f"halted ({status}): {why}")
    reason = HALTED.format(why=why, status=status, plan_dir=run.get("plan_dir", ""))
    print(json.dumps({"decision": "block", "reason": reason}))
    sys.exit(0)


def main() -> None:
    try:
        event = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    # The harness sets this once it is already replaying a Stop-hook
    # continuation. Re-blocking there would loop forever.
    if event.get("stop_hook_active"):
        sys.exit(0)

    cwd = event.get("cwd", "")
    run_path = os.path.join(cwd, ".gro", "run.json")
    run = load_run(run_path)
    if run is None:
        sys.exit(0)

    if run.get("status") != "active":
        sys.exit(0)

    # A run is armed unclaimed and the first Stop hook to see it stamps its own
    # id in. The model cannot do this itself: Claude Code hands the session id
    # to hooks and exposes it nowhere the model can read. Once claimed, other
    # sessions in the same checkout see a foreign id and leave the run alone.
    session_id = event.get("session_id")
    claimed = run.get("session_id")
    if not claimed:
        run["session_id"] = session_id
        save_run(run_path, run)
    elif claimed != session_id:
        breadcrumb(
            cwd,
            f"session {session_id} found an active run claimed by {claimed} and left it "
            "alone. If that claim is stale (the claiming session was resumed or "
            "restarted), delete `session_id` from run.json to re-arm.",
        )
        sys.exit(0)

    plan_dir = os.path.join(cwd, str(run.get("plan_dir", "")))
    remaining, total, next_item, next_file = scan_plan(plan_dir)

    if total == 0:
        halt(
            cwd,
            run_path,
            run,
            "error",
            f"no `plan.md` with checkboxes was found under `{plan_dir}`. "
            "Either `plan_dir` in `.gro/run.json` is wrong, or the plan predates "
            "the plan.md/issues layout and needs re-planning.",
        )

    if remaining == 0:
        run["status"] = "completed"
        run["last_remaining"] = 0
        save_run(run_path, run)
        breadcrumb(cwd, f"completed: all {total} item(s) ticked, including the final checklist")
        sys.exit(0)

    continuations = int(run.get("continuations", 0)) + 1
    if continuations > CONTINUATION_CAP:
        halt(
            cwd,
            run_path,
            run,
            "capped",
            f"it hit the {CONTINUATION_CAP}-continuation cap with {remaining} "
            "item(s) still unchecked.",
        )

    last_remaining = run.get("last_remaining")
    stalls = int(run.get("stalls", 0)) + 1 if last_remaining == remaining else 0
    if stalls >= STALL_LIMIT:
        halt(
            cwd,
            run_path,
            run,
            "stalled",
            f"it made no progress for {STALL_LIMIT} consecutive turns, stuck at "
            f"{remaining} unchecked item(s). Something is blocking `{next_item}`.",
        )

    run["continuations"] = continuations
    run["last_remaining"] = remaining
    run["stalls"] = stalls
    save_run(run_path, run)

    reason = CONTINUE.format(
        plan_dir=run.get("plan_dir", ""),
        next_item=next_item,
        work_file=next_file,
        remaining=remaining,
        total=total,
    )
    print(json.dumps({"decision": "block", "reason": reason}))
    sys.exit(0)


if __name__ == "__main__":
    main()
