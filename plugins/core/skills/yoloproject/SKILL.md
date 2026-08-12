---
name: yoloproject
description: Use when a validated project plan should be executed without stopping between phases for human input - long unattended runs, overnight work, or when the human partner has explicitly asked not to be asked
user-invocable: true
---

# yoloproject

## Overview

Normally a project run pauses whenever your turn ends and waits for your human partner. This skill removes that pause: a `Stop` hook checks the plan's checkboxes and hands you the next unchecked item until none remain.

The name is a warning label. Nobody should arm this without noticing they did.

**Announce at start, as the first line of your reply:**

> **YOLOPROJECT ARMED** — running `<plan-dir>` to completion without checking in. Stopping only on: all boxes ticked, the 30-continuation cap, two turns without progress, or you setting `"status": "paused"` in `.loam/yoloproject.json`. I will not merge.

Fill in the real plan directory. Say it every time you arm a run — never silently.

**Autonomy covers execution only.** Design and planning stay interactive, because that is where the questions are. Merging is not covered either; the run ends on a green branch and your human partner decides what happens to it.

**This skill does not replace `core:execute-implement-a-project`.** It arms the loop and then hands off. Every rule about dispatching, reviewing, and ticking boxes still comes from that skill.

## When to Use

- Your human partner asked for a long unattended run ("run this overnight", "don't ask me, just build it")
- A validated plan has many phases and no open questions
- You are resuming a run that a cap, stall, or crash interrupted

**Do NOT use when:**
- The plan still contains `[DECISION NEEDED]` markers or unresolved questions — resolve them first
- The design spec was never validated with your human partner
- The work touches production systems, credentials, or anything irreversible
- Your human partner has not asked for autonomy. **Never arm this on your own initiative.**

## Prerequisites

All three must hold. Check them; do not assume.

1. **A validated plan exists** with phase files at `.loam/tasks/<slug>/phase_*.md`.
2. **Every task carries a checkbox.** Run `grep -c "^- \[" .loam/tasks/<slug>/phase_*.md`. A phase file with zero matches predates checkbox tracking — re-plan it with `core:project-writing-plan` rather than hand-patching it.
3. **A working branch is checked out**, not the default branch. `core:project-getting-started` creates one.

## The Process

### 1. Confirm autonomy with your human partner

State plainly what will happen and get an explicit yes:

> "This will run all N phases without stopping to check in. I'll stop on my own if I hit the continuation cap, make no progress for two turns, or finish. I won't merge — you'll get a green branch to review. Go ahead?"

If they have already said "run it overnight, don't ask me," that is the yes. Do not ask twice.

### 2. Arm the run

Write `.loam/yoloproject.json`:

```json
{
  "plan_dir": ".loam/tasks/2026-08-09-widgets",
  "status": "active",
  "continuations": 0,
  "last_remaining": null,
  "stalls": 0
}
```

- `plan_dir` is relative to the repo root and must be the directory holding the `phase_*.md` files.
- The remaining fields are the hook's bookkeeping. Initialize them exactly as above and then leave them alone.

**Write exactly these five fields.** In particular, do not add a `session_id` — you cannot read your own, and a guessed one silently disables the run. The hook stamps its own in on the first turn, which is what scopes the run to this session and keeps a second Claude session in the same checkout from being dragged into it.

**The file is the switch.** No file means no autonomy — that is why every other loam run is unaffected by this skill existing.

### 3. Hand off to the normal execution skill

Invoke `core:execute-implement-a-project` for the same plan directory and follow it exactly. Nothing about phase execution changes. The only difference is that when your turn ends with boxes unchecked, you will be handed the next item instead of stopping.

### 4. Stop when the run stops

The run ends when `status` is no longer `active`.

| status | what happened | what to do |
|---|---|---|
| `completed` | every box ticked, final review included | Done. |
| `capped` | hit the continuation cap | Report what is done and what remains. Do not re-arm without your partner. |
| `stalled` | two turns with no box ticked | Report what is blocking the next item. Something is genuinely stuck. |
| `error` | no phase files found at `plan_dir` | Fix `plan_dir`, or re-plan if the phase files lack checkboxes |

**A halted run is a report, not a retry.** When the hook halts the run it is telling you that unattended progress stopped being safe. Say what happened and what remains. Re-arming a stalled run without diagnosing the stall just burns another 30 turns against the same wall.

## 5. Completion

Autonomy ends at a green branch. `core:execute-finishing-a-development-branch` still asks before merging, opening a PR, or deleting anything.

Do not tick a checkbox for merge steps. Do not push to the default branch. Do not interpret "don't ask me" as authorization to land code — it is authorization to build it without interruption, which is a different thing.

## Red Flags - STOP

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
| Writing `.loam/yoloproject.json` before the plan exists | The hook halts with `error` on the first turn |
| Using an absolute path for `plan_dir` | It is resolved against the repo root; use a relative path |
| Writing a `session_id` yourself | You cannot read your own; a wrong one makes the run silently do nothing |
| Ticking boxes ahead of the work to "prime" the loop | The run reports success for work that was never done |
| Expecting the hook to fix a broken plan | It counts checkboxes. It has no opinion about whether the plan is good. |
