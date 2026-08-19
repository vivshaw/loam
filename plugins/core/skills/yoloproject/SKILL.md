---
name: yoloproject
description: Use when the human partner wants a whole project built with minimal supervision - "build me X, don't babysit me", "run this overnight", or any request to take a feature from idea to green branch without checking in at every phase
user-invocable: true
---

# yoloproject

## Overview

The front door to loam's automated workflow, for when your human partner wants to state their intent once and come back to finished work.

The name is a warning label. Nobody should end up in this mode without noticing.

## When to Use

- "Build me X and don't babysit me" / "run this overnight" / "take this all the way"
- Any project-sized request where your partner has signalled they do not want per-milestone check-ins

**Don't use when:**
- The request is a single change rather than a project — just do it
- A validated plan already exists — go straight to `core:execute-implement-a-project-autonomously`
- The work touches production systems, credentials, or anything irreversible
- Your human partner has not asked for autonomy. **Never start this on your own initiative.**

## The Process

### 1. Announce, and record the intent

Say this as the first line of your reply:

> **YOLOPROJECT** — I'll design and plan this with you, then implement the whole plan without checking in. I won't merge.

Then write `.loam/run.json` immediately, before any other work:

```json
{
  "plan_dir": null,
  "status": "pending",
  "continuations": 0,
  "last_remaining": null,
  "stalls": 0
}
```

Invoking this skill IS the consent. Do not also ask "shall I run autonomously?" — your partner already said so.

### 2. Design, interactively

Use `core:design-spec-exploring` and follow it exactly. Ask every question it tells you to ask.

**Do not economise on questions here.** This is the phase your partner is present for, and the one where getting it wrong is most expensive: an autonomous run will build whatever the spec says, thoroughly, all night. A wrong spec means a branch full of confidently wrong work.

### 3. Plan, interactively

Use `core:project-getting-started`, which cuts the branch and drives `core:project-writing-plan`.

`core:project-writing-plan` asks you to approve its milestone breakdown. Answer that one — it is cheap and it is the last look at build order before the work multiplies. It writes the issues itself afterwards, so there is nothing further to sit through.

If planning surfaces a `[DECISION NEEDED]` marker, ask. An unresolved decision is not something autonomy can absorb — it is a hole the implementation will fall into.

### 4. Hand off to the autonomous runner

Invoke `core:execute-implement-a-project-autonomously` with the plan directory. It arms the run — updating the `pending` file you wrote in step 1 — and drives implementation to completion. Everything from here belongs to that skill.

## Red Flags

- Starting a yoloproject your human partner did not ask for
- Starting one to escape a conversation that felt like too many questions
- Skimping on design questions because autonomy is coming
- Proceeding past a `[DECISION NEEDED]` marker by picking an answer yourself
- Interpreting "don't ask me" as authorization to merge

**All of these mean: stop and talk to your human partner.**
