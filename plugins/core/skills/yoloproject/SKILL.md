---
name: yoloproject
description: Use when the human partner wants a whole project built with minimal supervision - "build me X, don't babysit me", "run this overnight", or any request to take a feature from idea to green branch without checking in at every phase
user-invocable: true
---

# yoloproject

## Overview

The front door to loam's whole workflow, for when your human partner wants to state their intent once and come back to finished work.

Design and planning run exactly as they normally do — they are full of questions because that is where your partner's judgment is irreplaceable. What changes is everything after: once a plan exists, a `Stop` hook checks its checkboxes and hands you the next unchecked item until none remain, so implementation runs to completion without pausing between phases.

The name is a warning label. Nobody should end up in this mode without noticing.

**Invoke this at the start of the work, not partway through.** The trigger belongs where the intent is formed. Asking your partner to remember, an hour into planning, that they meant to run unattended is a bad seam.

**Autonomy covers implementation only.** Merging is not covered; the run ends on a green branch and your partner decides what happens to it.

## When to Use

- "Build me X and don't babysit me" / "run this overnight" / "take this all the way"
- Any project-sized request where your partner has signalled they do not want per-phase check-ins
- You are resuming a run that a cap, stall, or crash interrupted

**Do NOT use when:**
- The request is a single change rather than a project — just do it
- The work touches production systems, credentials, or anything irreversible
- Your human partner has not asked for autonomy. **Never arm this on your own initiative.**

## The Process

### 1. Announce, and record the intent

Say this as the first line of your reply:

> **YOLOPROJECT** — I'll design and plan this with you, then implement the whole plan without checking in. I'll stop on: all work done, a 30-continuation cap, two turns without progress, or you setting `"status": "paused"` in `.loam/yoloproject.json`. I won't merge.

Then write `.loam/yoloproject.json` immediately, before any other work:

```json
{
  "plan_dir": null,
  "status": "pending",
  "continuations": 0,
  "last_remaining": null,
  "stalls": 0
}
```

`pending` is inert — the hook ignores any run that is not `active`, so nothing changes yet. The file exists at this point only so the intent survives. Design and planning can run long enough to compact your context, and a yoloproject your partner asked for and you then forgot is worse than one you never armed.

Invoking this skill IS the consent. Do not also ask "shall I run autonomously?" — your partner already said so.

### 2. Design, interactively

Use `core:design-spec-getting-started` and follow it exactly. Ask every question it tells you to ask.

**Do not economise on questions here.** This is the phase your partner is present for, and the one where getting it wrong is most expensive: an autonomous run will build whatever the spec says, thoroughly, all night. Wrong spec means a branch full of confidently wrong work.

### 3. Plan, interactively

Use `core:project-getting-started`, which cuts the branch and drives `core:project-writing-plan`.

One deviation: when `core:project-writing-plan` asks how to review phases, choose **"Write all phases to disk, I'll review afterwards"** without asking. Per-phase review prompts are exactly the check-ins your partner opted out of. Say that you did this.

If planning surfaces a `[DECISION NEEDED]` marker, ask. An unresolved decision is not something autonomy can absorb — it is a hole the implementation will fall into.

### 4. Arm the run

The plan now exists. Update `.loam/yoloproject.json`:

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
- The remaining fields are the hook's bookkeeping. Leave them as they are.

**Write exactly these five fields.** In particular, do not add a `session_id` — you cannot read your own, and a guessed one silently disables the run. The hook stamps its own in on the first turn, which scopes the run to this session and keeps a second Claude session in the same checkout from being dragged into it.

Confirm the plan carries checkboxes before arming: `grep -c "^- \[" .loam/tasks/<slug>/phase_*.md`. A phase file with zero matches predates checkbox tracking, and the hook has nothing to count — re-plan it rather than hand-patching it.

Say that the run is now armed, and from which plan directory.

### 5. Implement, autonomously

Invoke `core:execute-implement-a-project` for that plan directory and follow it exactly. Nothing about phase execution changes. The only difference is that when your turn ends with boxes unchecked, you are handed the next item instead of stopping.

### 6. Stop when the run stops

The run ends when `status` is no longer `active`.

| status | what happened | what to do |
|---|---|---|
| `completed` | every box ticked, final review included | Done. |
| `capped` | hit the continuation cap | Report what is done and what remains. Do not re-arm without your partner. |
| `stalled` | two turns with no box ticked | Report what is blocking the next item. Something is genuinely stuck. |
| `error` | no phase files found at `plan_dir` | Fix `plan_dir`, or re-plan if the phase files lack checkboxes |

**A halted run is a report, not a retry.** When the hook halts the run it is telling you that unattended progress stopped being safe. Say what happened and what remains. Re-arming a stalled run without diagnosing the stall just burns another 30 turns against the same wall.

## Completion

Autonomy ends at a green branch. `core:execute-finishing-a-development-branch` still asks before merging, opening a PR, or deleting anything.

Do not tick a checkbox for merge steps. Do not push to the default branch. Do not interpret "don't ask me" as authorization to land code — it is authorization to build it without interruption, which is a different thing.

## Starting From An Existing Plan

If your partner already has a validated plan and wants it run unattended, skip steps 2 and 3. Announce, write `.loam/yoloproject.json` straight to `active` with the plan directory filled in, and go to step 5.

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
| Arming (`active`) before the plan exists | The hook halts with `error` on the first turn. Step 1 writes `pending`, which is inert; only step 4 arms |
| Using an absolute path for `plan_dir` | It is resolved against the repo root; use a relative path |
| Writing a `session_id` yourself | You cannot read your own; a wrong one makes the run silently do nothing |
| Ticking boxes ahead of the work to "prime" the loop | The run reports success for work that was never done |
| Expecting the hook to fix a broken plan | It counts checkboxes. It has no opinion about whether the plan is good. |
