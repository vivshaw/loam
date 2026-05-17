---
name: implementing-a-plan
description: "Use when /vivflow:implement is invoked, to execute a plan.md from .vivflow/tasks/<slug>/ end-to-end. Orchestrates slug resolution, feature-branch discipline, TDD-driven execution of the task breakdown via the tdd and verifying-claims skills, and a final spec-check gate against every acceptance criterion. --quick skips per-task TDD but not spec-check."
user-invocable: false
---

# Implementing a plan

Reads `.vivflow/tasks/<slug>/plan.md` and works through its task breakdown.

## 1. Pick the task folder

In priority order:

- If a slug is given as an argument, use `.vivflow/tasks/<slug>/`.
- If a current task is in conversation context (set by a recent `/vivflow:plan`), use that slug.
- Otherwise, list the most recently modified folders under `.vivflow/tasks/` (top 5) and ask the user which one.

## 2. Read the plan

Read `plan.md` in full. If it doesn't exist, stop and ask the user to run `/vivflow:plan` first.

Note the **goal**, the **acceptance criteria** list, and the **task breakdown**. The first two drive spec-check; the third drives execution.

## 3. Branch discipline

Confirm you're on a feature branch:

- Run `git rev-parse --abbrev-ref HEAD`.
- If it returns `main` (or `master`), create a branch named `vivflow/<slug>` and check it out: `git checkout -b vivflow/<slug>`. Tell the user one line ("switched to branch `vivflow/<slug>`"). If the user is in a non-git directory, stop and tell them to `git init` first.
- If already on a branch, do nothing.

Why this matters: `/vivflow:review` diffs the current branch against `main`, so anything done directly on `main` is invisible to review. Branch-first keeps that flow clean.

Commit work as tasks complete (or at minimum before invoking `/vivflow:review`) so the diff actually contains the work to be reviewed.

## 4. Execute the task breakdown

Work through the tasks in order, honoring parallel/sequential markers from the plan.

For each task:

- The **tdd** skill will fire and discipline you through red → green → refactor.
- The **verifying-claims** skill will fire before you call the task done.

### Quick mode

If the invocation includes `--quick` (or the user explicitly says "skip TDD" / "quick mode" / equivalent), skip the per-task TDD cycle. Spec-check **still runs** at the end. You can shortcut the discipline; you cannot shortcut the confirmation.

## 5. Spec-check (gate)

After the last task, walk **every acceptance criterion** and **every task** in the plan and confirm each is satisfied.

For each item, produce one of:

- `satisfied by: <file:line or test name>` — you can point to the concrete evidence.
- `deferred: <one-line reason>` — explicitly out, append it to a `## Deferred` section in `plan.md`.

If any criterion is not satisfied and not deferred, **stop**. Print what's missing. Do not claim success.

The verifying-claims skill applies here too — "the test passed" requires that you ran it in this session, not earlier.

## 6. Report

One short summary:

- Tasks completed (count)
- Acceptance criteria satisfied (count) / deferred (count)
- Any items the user should know about
