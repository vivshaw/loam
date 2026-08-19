---
name: execute-implement-a-project-autonomously
description: Use when a validated project plan should be implemented without pausing between phases - the human partner has asked for an unattended or overnight run, or core:yoloproject has reached the implementation phase
user-invocable: true
---

# Implementing a Project Autonomously

## Overview

`core:execute-implement-a-project` stops at the end of every turn and waits. This skill removes that pause: a `Stop` hook counts the checkboxes in `plan.md` and hands you the next unchecked item until none remain.

**Announce at start:** "I'm using the `core:execute-implement-a-project-autonomously` skill to run this plan without stopping between phases."

**This skill does not replace `core:execute-implement-a-project`.** It arms the loop, hands off, and handles the ending. Every rule about dispatching issues, verifying milestones, and ticking boxes still comes from that skill.

**Autonomy covers implementation only.** The run ends on a green branch; your human partner decides what happens to it.

## When to Use

- Your human partner asked for an unattended run of a plan that already exists
- `core:yoloproject` has finished designing and planning and reached implementation
- You are resuming a run that a cap, stall, or crash interrupted

**Don't use when:**
- No validated plan exists — use `core:yoloproject` to design and plan first
- The plan still contains `[DECISION NEEDED]` markers. An unresolved decision is not something autonomy can absorb; it is a hole the implementation falls into
- The work touches production systems, credentials, or anything irreversible
- Your human partner has not asked for autonomy. **Never arm this on your own initiative.**

## Prerequisites

Check these; do not assume.

1. **A plan exists** at `.gro/tasks/<slug>/plan.md`, with issue files under `issues/`.
2. **Its milestones carry checkboxes.** Run `grep -c "^- \[" .gro/tasks/<slug>/plan.md`. Zero matches means the plan predates the plan.md layout and the hook has nothing to count — re-plan it with `core:project-writing-plan` rather than hand-patching it.
3. **A working branch is checked out**, not the default branch.

## The Process

### 1. Arm the run

Write `.gro/run.json`:

```json
{
  "plan_dir": ".gro/tasks/2026-08-09-widgets",
  "status": "active",
  "continuations": 0,
  "last_remaining": null,
  "stalls": 0
}
```

- `plan_dir` is relative to the repo root and must be the directory holding `plan.md`.
- The remaining fields are the hook's bookkeeping. Initialize them exactly as above, then leave them alone.

If `core:yoloproject` already wrote this file as `pending`, update it in place rather than starting a new one.

Say that the run is armed and from which plan directory. Never arm silently.

### 2. Implement

Invoke `core:execute-implement-a-project` for that plan directory and follow it exactly. Nothing about phase execution changes. The only difference is that when your turn ends with boxes unchecked, you are handed the next item instead of stopping.

### 3. Stop when the run stops

The run ends when `status` is no longer `active`.

| status | what happened | what to do |
|---|---|---|
| `completed` | every box ticked, final review included | Done. |
| `capped` | hit the continuation cap | Report what is done and what remains. Do not re-arm without your partner. |
| `stalled` | two turns with no box ticked | Report what is blocking the next item. Something is genuinely stuck. |
| `error` | no `plan.md` with checkboxes at `plan_dir` | Fix `plan_dir`, or re-plan if the plan predates this layout |

**A halted run is a report, not a retry.** When the hook halts a run it is saying unattended progress stopped being safe. Say what happened and what remains. Re-arming a stalled run without diagnosing the stall just burns another 30 turns against the same wall.

## 4. Completion

Autonomy ends at a green branch. `core:execute-finishing-a-development-branch` still asks before merging, opening a PR, or deleting anything. Do not tick a checkbox for merge steps. Do not push to the default branch. Do not interpret "don't ask me" as authorization to land code — it is authorization to build it without interruption, which is a different thing.

## Red Flags

- Arming a run your human partner did not ask for
- Arming a run to escape a conversation that felt like too many questions
- Ticking a box so the loop keeps going
- Re-arming a `stalled` run without finding out what stalled it
- Editing `continuations` or `stalls` to buy more turns
- Adding a merge or deploy step to the plan so autonomy covers it

**All of these mean: stop and talk to your human partner.**

## Common Mistakes

| Mistake | Why it breaks |
|---|---|
| Arming before the plan exists | The hook halts with `error` on the first turn |
| Using an absolute path for `plan_dir` | It is resolved against the repo root; use a relative path |
| Ticking boxes ahead of the work to "prime" the loop | The run reports success for work that was never done |
