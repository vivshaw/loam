---
name: execute-implement-a-project
description: Use when executing a project plan - dispatches a fresh subagent per issue, verifies each milestone against its spec requirements, tracks progress in plan.md
user-invocable: false
---

# Implementing a Project

Execute a plan milestone by milestone: run its issues, then verify the milestone against the spec requirements it claims.

**Core principle:** every executor gets `plan.md` plus one issue. That pair is deliberately everything it needs — don't hand it more, and don't make it go looking.

Use `core:critique-reviewing-code` for review loops (dispatch, fix, re-review until zero issues).

**When not to use:** no plan exists yet — use `core:project-writing-plan` first.

## Reporting on Subagents

Before dispatching, say in a sentence or two what you're asking for and which milestone it serves. After it returns, say what it did and whether it worked. Surface anything that changes what happens next — failing tests, unresolved review issues, work it couldn't do.

## Plan Path

If the user hasn't named a plan directory, ask. Executing the wrong plan is expensive to unwind.

```
Question: "Which project plan should I execute?"
Options:
  - [list directories you find in .gro/tasks/]
  - "Let me provide the path"
```

## 1. Read the plan

Read `plan.md` once, in full. It's short by design, and it's the context every dispatch depends on — you'll be quoting its path into subagent prompts all run.

Note what you'll need throughout:

- the milestones, their issues, and which boxes are already ticked
- the absolute path to `plan.md` and to `issues/`
- `.gro/project-plan-guidance.md` if it exists — pass its absolute path to reviewers, and omit the field entirely if it doesn't

Ticked boxes are work already done. Resume from the first unchecked one.

Create a session-isolated scratchpad so parallel runs don't collide:

```bash
SLUG=$(basename "[plan-directory]")
SCRATCHPAD_DIR="/tmp/exec-${SLUG}-$(printf '%04x%04x' $RANDOM $RANDOM)"
mkdir -p "${SCRATCHPAD_DIR}"
```

Then TaskCreate two entries per milestone — "Milestone N: issues" and "Milestone N: verify" — plus one for wrap-up. Put the absolute plan path in the first description; after compaction the task list is all that survives.

## 2. Run each milestone

### 2a. Issues

For each unchecked issue in the milestone, in order, dispatch `core:executor-task`:

```
<invoke name="Task">
<parameter name="subagent_type">core:executor-task</parameter>
<parameter name="description">Implementing issue NN: [title]</parameter>
<parameter name="prompt">
  Implement one issue from a project plan.

  Plan:  [absolute path to plan.md]
  Issue: [absolute path to issues/NN-slug.md]

  Read both. The plan holds the architecture, dependency choices, patterns, and
  test conventions for this project — follow them rather than inventing your own.
  The issue holds your specific task and its "Done when".

  1. Apply relevant skills, such as `style:coding-effectively`
  2. Implement what the issue specifies, and nothing beyond it
  3. Satisfy every "Done when" box — run the tests, run the build
  4. Commit
  5. Report back with evidence

  Work from: [directory]
</parameter>
</invoke>
```

Check the result, then **tick that issue's box in `plan.md`**. The checkbox is the durable record; your task list dies with the context.

Never tick a box you haven't verified. No code review between issues — that comes at the milestone.

If an issue implements behavior but its "Done when" names no tests, that's a hole in the plan, not a step to skip. Surface it.

### 2b. Verify the milestone

This is the gate. Two things have to hold.

**The requirements pass.** The milestone's `Verifies:` line names spec requirements by scoped ID. Run the tests covering them and confirm they pass. If a requirement has no test, it isn't verified — say so rather than ticking.

**The review is clean.** Use `core:critique-reviewing-code` with:

- WHAT_WAS_IMPLEMENTED — the issues in this milestone
- PLAN_OR_REQUIREMENTS — plan.md path, plus this milestone's issue files
- BASE_SHA — commit before the milestone started
- HEAD_SHA — current commit
- PROJECT_GUIDANCE — absolute path, only if the file exists
- SCRATCHPAD_DIR

When issues come back, TaskCreate one per issue with the reviewer's text **copied verbatim** — after compaction that description is all `core:executor-review-fixer` has to work from. Dispatch the fixer with the plan and issue paths, then re-review.

Fix every issue, Minor included. Ignore APPROVED/BLOCKED status and count issues. **Three-strike rule:** if the same issues survive three cycles, stop and ask your human partner.

Only when both hold, tick the milestone's gate box.

If the reviewer hits a context limit, the milestone changed too much for one pass — review the first half of its commits, fix, then the second half.

## 3. Wrap-up

After every milestone is verified, work the `## Wrap-up` boxes in `plan.md` in order.

**Project context updated.** Dispatch `meta:project-context-librarian` with the base commit, current HEAD, and working directory. It follows `meta:maintaining-project-context` to update any `AGENTS.md` whose contracts moved.

**Final code review passed.** `core:critique-reviewing-code` across the whole range, adding:

```
REQUIREMENTS_COVERAGE_CHECK: "Verify every requirement in the design spec is
covered by a milestone, or listed as deferred in plan.md. Flag any requirement
in neither, and flag any deferred P10."
```

**Test coverage analyzed** and **human test plan written.** Dispatch `core:critic-test-analyst` with the spec and plan paths, the working directory, and the commit range. It validates that automated tests exist for the spec's requirements, then generates the human test plan.

If coverage fails, dispatch `core:executor-review-fixer` to add the missing tests, then re-run the analyst. Three failed attempts means escalate. When it passes, write the plan to `.gro/tasks/{slug}/test-plan.md`.

**Run summary written for the human operator.** Per milestone: issues implemented, review cycles needed, and any compromise made. There should be none — but "I couldn't run the integration tests so I continued" is a partial failure, and your partner needs to know what to do about it. Say whether any review issue was left outstanding.

Then activate `core:execute-finishing-a-development-branch` — not before.

**Under `core:execute-implement-a-project-autonomously`, write the summary in the same turn that ticks its box.** The run ends the instant nothing is unchecked, so that turn is the last one your partner sees. A summary deferred to the next turn is a summary nobody reads.

## Common Rationalizations

| Excuse | Reality |
|---|---|
| "I'll pass the executor the whole plan directory" | Plan plus one issue. More context makes it likelier to build the neighbouring issue too. |
| "I'll review after each issue to catch problems early" | Review once per milestone. Per-issue review burns the context the run needs. |
| "The tests for this requirement are probably fine" | Run them. The gate is evidence, not inference. |
| "Minor issues can wait" | Fix them all. The reviewer flagged them for a reason. |
| "I'll tick the boxes at the end of the milestone" | Tick each as it's verified. Batched, a crash loses the whole milestone. |
| "My task list already tracks this" | Your task list dies with your context. `plan.md` doesn't. |
| "This issue is obviously done" | Tick only what you verified. |
| "Context error on review, I'll skip it" | Chunk it into halves instead. |
