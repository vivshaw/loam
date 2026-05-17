---
name: reviewing-a-branch
description: "Use when /vivflow:review is invoked, to run iterative adversarial GAN-style review against the current branch's diff. Orchestrates branch + committed-state preconditions, locating the goal paragraph, dispatching a fresh judge subagent each round (anchored only to goal + diff, not planning context), revising or ignoring feedback with cross-round memory, and terminating on convergence, graceful exit, or 8-round cap."
user-invocable: false
---

# Reviewing a branch

GAN-style review. Two roles in tension push toward higher code quality than either reaches alone.

## Roles

- **Implementer** (you): carries memory across rounds. Remembers what feedback was addressed, what was ignored and why, and any patterns in the judge's behavior.
- **Judge** (subagent): dispatched **fresh each round**. No memory between rounds. Anchored to two inputs:
  - The **goal paragraph** from `plan.md` (so it knows what the code is supposed to accomplish).
  - The **diff** (see below).

The judge is not given the rest of the plan, the research doc, the seed spec, or any other implementation-context document. Those would bias the critique toward "does this match what was planned" instead of "is this good code for the stated goal."

The judge is free to read source files, grep the repo, look at git history, run code, and consult external docs — whatever a good reviewer would do to evaluate the diff. Effective review requires that latitude; the spec only restricts the planning/design context, not the codebase itself.

## Escape hatch

If the branch's diff against `main` is obviously trivial — a typo fix, a single-line config tweak, a formatter run, a dependency bump — say so and offer to skip review entirely. Don't ceremony a one-liner through eight rounds of GAN critique.

## 1. Preconditions

- **Branch.** `git rev-parse --abbrev-ref HEAD` must return something other than `main`. `/vivflow:implement` puts you on a branch automatically; if you're on `main`, stop and tell the user to move their work to a branch first (e.g., `git checkout -b vivflow/<slug>` + commit).
- **Committed.** The branch's work should be committed. Anything uncommitted (working tree changes, untracked files) won't be in `git diff main..HEAD` and the judge won't see it. Warn the user if `git status` is dirty and offer to stop or proceed.
- **Goal.** Locate the goal paragraph:
  - If a current task slug is in conversation context, read the paragraph under `## Goal` from `.vivflow/tasks/<slug>/plan.md`.
  - If the user names a slug in the invocation, use that plan's `## Goal`.
  - If neither is available, stop and ask the user to paste a goal paragraph inline. The judge cannot evaluate "relative to the goal" without one.

## 2. Each round

### a. Dispatch judge

Spin up a fresh subagent using the Agent tool with this exact prompt (substituting `<goal paragraph>`):

```
<vivflow_judge>
You are an adversarial code reviewer. You receive a goal and a branch to review. Your job is to find real problems in the branch's code.

Anchored inputs (these define your task):
- Goal: <goal paragraph>
- Branch diff: run `git diff $(git merge-base HEAD main)..HEAD` to see only the work added on this branch (i.e., excluding anything already on `main`).

You are free to do whatever a good reviewer would do to evaluate that work against that goal: read source files, grep, check git history, run code, consult external docs. The only context off-limits is the planning/design layer for *this* work — do not read the plan, research notes, or seed spec inside `.vivflow/`. Those would bias you toward "does this match what was planned" instead of "is this good code for the stated goal."

Produce feedback grouped by severity:
- **blocker**: the work fails to accomplish the goal, introduces a bug, or violates a stated constraint
- **consider**: a real improvement, but the work is acceptable without it
- **nit**: tiny taste or style call

For each item: file:line and a short concrete suggestion. If you find nothing, say so plainly. Do not invent issues.
</vivflow_judge>
```

### b. Read the feedback

For each item:

- Revise the code, or
- Mark it ignored with a one-line reason (e.g., "judge misread the type; foo.ts:42 confirms it's already `Maybe<T>`"). Keep this in your cross-round memory.

### c. Loop or terminate

If anything changed in the code this round, loop back to (a). Otherwise check termination.

## 3. Termination

Stop when one of:

- **Convergence.** Judge returns no `blocker` items and no `consider` items you're acting on.
- **Graceful exit.** Using your cross-round memory, you conclude the judge is hallucinating, contradicting prior rounds, or no longer surfacing useful input. Log a one-line reason.

Cap at **8 rounds**. If you hit the cap without convergence, stop and report the remaining open items rather than churn further.

## 4. Report

Print:

- Round count, and how the loop ended (convergence / graceful exit / cap).
- A short log: per round, what changed and what was ignored (with reasons).
- Final state: any items left open that the user should decide on.

Refined code is in the working tree.
