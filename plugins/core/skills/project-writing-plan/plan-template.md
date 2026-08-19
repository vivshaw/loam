<!--
  Project plan template. Copy to .gro/tasks/YYYY-MM-DD-{slug}/plan.md and fill in.
  Delete every HTML comment as you go, including this one.
  Guidance on writing each section lives in core:project-writing-plan.
-->

# [Project Name] Project Plan

**Spec:** [spec.md](spec.md) · **Codebase verified:** [date]

## Problem Context

<!-- What the problem is, the current solution, and where it falls short. Condense
     from the spec rather than restating it — a reader can open the spec. -->

[What hurts today.]

## Proposed Solution

<!-- What this will do, how it will be built, what's different. -->

[High-level summary and why this approach.]

## Goals and Non-Goals

- [requirement / impact]
- [requirement / impact]

### Non-Goals

<!-- Optional, but worth writing when scope could plausibly creep. -->

- [what this deliberately does not do]

## Design

<!-- The major pieces and how they fit. Components, request paths, data model.
     Enough that an executor knows where their work sits. No file-by-file plans. -->

[Overall shape.]

[Component and interaction detail. Interface shapes other issues code against go
here, since more than one issue depends on them.]

## Technical Decisions

<!--
  The section that lets issues stay short. Everything an executor would otherwise
  have to guess or rediscover:
    - dependencies WITH versions, and why each was chosen
    - existing patterns to follow, with a path to an example
    - test framework, layout, and command
    - non-obvious findings from research — the gotchas that cost a research trip
-->

- **[dep@version]** for [purpose]. [Why this one. Any surprise in using it.]
- **[Pattern]** as in `[path/to/example]`. [What to copy about it.]
- **Tests** with [framework], [layout]. Run `[command]`.

## Alternatives Considered

<!-- What else was on the table and why it lost. Documents the decision so it
     isn't relitigated in three months. -->

- **[Alternative]** — [why not].

## Open Questions

<!-- Optional. Ship them unanswered; a plan that resolves everything is hiding risk. -->

- [question]

## Verification Strategy

<!--
  Which requirements can't be checked by a test, and why. Everything else is
  assumed automatable, so this list is usually short — often empty.

  core:critic-test-analyst reads this. A requirement that is neither tested nor
  listed here fails coverage; one listed here goes into the human test plan
  instead. Without the list, an unautomatable requirement can never pass.
-->

Every requirement is verified by automated test except:

- **[requirement ID]** — [what a human has to judge, and why a test can't]

## Milestones

<!--
  2-5 coherent, independently testable slices. Each names the spec requirements it
  verifies, lists its issues in execution order, and ends with a gate box.

  These checkboxes are the single source of truth for project progress. The
  autonomous runner reads them. Tick an issue only after verifying the executor's
  report; tick a gate only after the requirement tests pass and review is clean.
-->

### Milestone 1 — [Name]

Verifies: [requirement IDs, or "infrastructure — no requirements"]

- [ ] [01 — Issue title](issues/01-issue-slug.md)
- [ ] [02 — Issue title](issues/02-issue-slug.md)
- [ ] Milestone 1 verified — [tests pass for the IDs above; review clean]

### Milestone 2 — [Name]

Verifies: [requirement IDs]

- [ ] [03 — Issue title](issues/03-issue-slug.md)
- [ ] Milestone 2 verified — [tests pass for the IDs above; review clean]

### Deferred

<!-- Requirements not built in this project, with priority. Omit if none. -->

- [requirement ID] (P[N]) — [why]

## Wrap-up

<!-- Runs once, after every milestone is verified. The run summary box is last on
     purpose: an autonomous run ends the moment nothing is unchecked, so the turn
     that ticks it is the last one anybody sees. -->

- [ ] Project context updated
- [ ] Final code review passed
- [ ] Test coverage analyzed
- [ ] Human test plan written
- [ ] Run summary written for the human operator

## Appendix

<!-- Links and detailed figures you didn't want inline. Omit if empty. -->
