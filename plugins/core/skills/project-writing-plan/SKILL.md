---
name: project-writing-plan
description: Use when a design spec is complete and the project needs a plan and issue breakdown for engineers with zero codebase context.
user-invocable: false
---

# Writing a Project Plan

## Overview

Turn a design spec into one plan document and a set of issue files.

**Core principle:** the plan carries the context a teammate would already have in their head. The issue carries only what's specific to one task. Together they're everything an executor needs; separately, neither is.

**Announce at start:** "I'm using the `core:project-writing-plan` skill to plan this project."

Executors are fresh subagents with no memory of this codebase. That's why the plan settles architecture, dependencies, and patterns **once, upfront** — so every issue after it can be short. Writing the same context into forty issues is how the old plans got to a thousand lines.

## What you produce

```
.gro/tasks/YYYY-MM-DD-{slug}/
  spec.md              # the design spec, already written
  plan.md              # shared context + milestones + progress
  issues/
    01-project-setup.md
    02-token-service.md
```

Copy `project-writing-plan/plan-template.md` to `plan.md` and `project-writing-plan/issue-template.md` for each issue. Delete the guidance comments as you fill them in.

## Step 1: Investigate, once

Everything the issues rely on gets verified here, so it never has to be re-verified per issue.

Dispatch these in parallel:

- `core:researcher-codebase` — "The spec assumes [X]. Verify what exists, report differences, and describe the patterns this project should follow." Give it the spec's assumptions explicitly.
- `core:researcher-codebase` — "How does this project test? Find AGENTS.md files covering testing behavior and report the commands, layout, and conventions." Follow what the codebase does rather than prescribing.
- `core:researcher-internet` — for any external library, API, or standard the spec names. Escalate to `core:researcher-remote-code` when the docs don't cover what you need.

The findings become the plan's Design and Technical Decisions sections. Write down exact paths, exact versions, and anything non-obvious you learned — a gotcha discovered here costs one research trip; discovered during execution it costs a failed issue and a review cycle.

**If the codebase contradicts the spec**, say so in the plan and adjust. Don't quietly plan against a codebase that doesn't exist.

## Step 2: Write the plan

`plan.md` explains the why, the what, and the how. Keep it short — a plan nobody reads is worse than no plan, and short specs are the ones that get read.

**Technical Decisions is the section that earns everything else.** It's where an executor looks instead of guessing:

```markdown
## Technical Decisions

- **jose@5.9.6** for JWT signing. Already a transitive dep; `jsonwebtoken` is
  unmaintained. Verify needs `createLocalJWKSet` called before `jwtVerify` —
  undocumented, found in source.
- **Service layer pattern** as in `src/services/session/`. Class per service,
  constructor injection, no module-level state.
- **Tests** with vitest, colocated as `*.test.ts`. Run `npm test`.
```

Name versions. Name paths. Name the surprise you found. Anything an executor would otherwise have to rediscover belongs here.

## Step 3: Break into milestones

A milestone is a coherent, independently testable slice — it ends with a working build and a set of spec requirements you can actually verify.

- **Target 2-5 milestones.** Needing more means the project is too big; say so and offer to split it rather than planning eighteen.
- Each milestone lists the spec requirements it verifies, by scoped ID.
- Every requirement in the spec lands in exactly one milestone, or in the Deferred list with its priority. One in neither is one nobody builds.
- Dependencies run forward only.

### Deferring by priority

When the work won't fit, cut from the bottom and say what you cut:

| Priority | Policy |
|---|---|
| P1-P3 | Cut these first. Note them in Deferred and move on. |
| P4-P9 | Cut deliberately, one at a time, and say what each costs. Stop cutting as soon as it fits. |
| P10 | Never defer one on your own. Stop and ask. |

A P10 is the spec saying the feature doesn't exist without it. If the P10s alone don't fit, that's a scoping conversation, not an arithmetic problem — put the options to the user and let them choose.

Deferring is a decision, not an omission. `core:critic-code-reviewer` flags a deferred P10 at the end, but by then the plan is written; the point of the rule is that you never get there.

**Present the milestone breakdown before writing any issues.** It's the cheapest moment to catch a wrong build order, and the last one before the work multiplies.

```
Question: "Here's the milestone breakdown. Approve, or tell me what to regroup?"
Options:
  - "Approved - proceed"
  - "Needs revision - [describe changes]"
```

Milestones carry the progress record:

```markdown
### Milestone 2 — Token issuance

Verifies: authn.1.1, authn.1.2, authn.3.1

- [ ] [02 — TokenService](issues/02-token-service.md)
- [ ] [03 — POST /token](issues/03-token-endpoint.md)
- [ ] Milestone 2 verified — tests pass for authn.1.1, authn.1.2, authn.3.1; review clean
```

The checkboxes in `plan.md` are the single source of truth for what's done. Issue files hold no status and no checkboxes at all — an issue's "Done when" is acceptance criteria, written as plain bullets, because a box invites someone to tick it and two records mean two records to reconcile.

The last box in each milestone is its gate. It gets ticked only after the milestone's requirement tests pass and the review loop returns zero issues.

### Requirements a test can't check

Most requirements are automatable. The few that aren't — a judgment call about copy, a layout you have to look at — go in the plan's Verification Strategy section with a line on what a human has to judge.

Write that list even when it's empty, and say so explicitly. `core:critic-test-analyst` treats anything neither tested nor listed as a coverage failure, so an unautomatable requirement left off the list can never pass.

## Step 4: Write the issues

One file per issue, numbered in execution order across the whole project (`01`, `02`, … — not restarting per milestone).

An issue names a concrete task with a defined outcome, in plain language. Keep it to what someone needs to do this specific piece of work:

```markdown
# 02 — TokenService

**Milestone:** 2 · **Verifies:** authn.1.1, authn.1.2

## Task

Issue signed JWTs from client credentials. Claims shape is in plan.md §Design.
Validation is issue 03 — don't build it here.

## Done when

- Tests pass for authn.1.1 (valid credentials return a token) and
  authn.1.2 (tokens expire within 1 hour)
- `npm run build` is clean

## Notes

`createLocalJWKSet` must be called before `jwtVerify` — see plan.md §Technical Decisions.
```

**Sizing:** an issue is one sitting's work with a visible outcome — a diff you could review. Big issues hide progress and are where executors go wrong quietly. When one feels large, split it.

**Say what's out of scope** when a neighbouring issue covers it. That one line prevents two executors building the same thing twice.

### What issues don't contain

| Not in an issue | Where it lives |
|---|---|
| Complete implementation code | The executor writes it, against the codebase as it is |
| Step-by-step "write the test, run it, commit" | `core:executor-task` already works that way |
| Architecture, dependency choices, conventions | `plan.md`, once |
| Status or completion state | `plan.md` milestone checkboxes |

**Interfaces and hard-won findings are the exception.** A type signature other issues code against, or a non-obvious library behavior you had to read source to learn — include those. They're cheaper to state than to rediscover. Everything else the executor derives from the codebase, which it can see and you're only remembering.

## Step 5: Validate

Dispatch `core:critic-code-reviewer` over `plan.md` and every issue file, passing `.gro/project-plan-guidance.md` if it exists. Ask it to check:

1. **Coverage** — every spec requirement in exactly one milestone or explicitly deferred; flag deferred P10s
2. **Sufficiency** — could a fresh engineer execute each issue with only `plan.md` and that issue?
3. **Ordering** — no issue depends on something a later issue builds
4. **Scope** — no implementation code in issues, no context duplicated across them

Create one task per issue found, copying the text verbatim, fix them all including Minor, and re-review until zero.

Then hand off to execution:

```
Plan complete: [N] milestones, [M] issues in `.gro/tasks/{slug}/`.

**Copy the line below before running /clear — it erases this conversation.**

    Use the core:execute-implement-a-project skill for /abs/path/.gro/tasks/{slug}/

Then /clear, paste, and run.
```

## Common Rationalizations

| Excuse | Reality |
|---|---|
| "I'll include the code so the executor can't get it wrong" | The executor sees the codebase as it is now. You're working from a memory of it. |
| "This context is important, I'll repeat it in each issue" | Put it in plan.md and reference it. Repetition is how these documents got unreadable. |
| "Eight milestones, but they're small" | Two to five. More means split the project — that's the user's call, so offer it. |
| "The issue is obvious from its title" | Write the Done when. An outcome you can't state is one nobody can verify. |
| "I'll investigate per issue, just-in-time" | Investigate once. Per-issue research repeats the same lookups and burns the context you need. |
| "The spec is weeks old but probably still accurate" | Verify it. Planning against a codebase that moved is how executors get sent to files that don't exist. |
| "I'll track status in the issue files too" | One source of truth. plan.md holds the checkboxes. |
| "This requirement doesn't fit a milestone cleanly" | Then the breakdown is wrong. Regroup rather than dropping it. |
