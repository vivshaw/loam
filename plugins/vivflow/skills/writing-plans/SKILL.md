---
name: writing-plans
description: "Use when writing or editing a plan.md file inside .vivflow/tasks/<slug>/ — produced by /vivflow:plan. Shapes the document with goal / acceptance criteria / approach / file map / TDD-sized task breakdown / out-of-scope, and gives concrete heuristics for what good content in each section looks like: testable criteria, properly-sized tasks, trade-off-aware approach, deferrals with reasons. No question marks remain in the final plan."
---

# Writing plans

A plan.md is a spec to be implemented. It can describe a one-line fix or a multi-week initiative — the shape is the same; the depth scales.

## Ground the plan in codebase reality

Before designing the approach, read the files where the work will land, run the existing tests, and check `git log` for recent activity in that area. Plans built on stale or assumed codebase state turn into implementations that don't compile or quietly duplicate things that already exist.

Cheap verification before designing:

- `grep -r "<function-name>"` — find existing call sites and conventions
- `git log --oneline -- <path>` — see what's been changing and why
- read the test file alongside the production file — tests document intent better than comments

If research already covered this, just confirm it's still current.

## Verify, don't assume

Every element traces to direct user input, research findings, or something you actually observed. If you can't trace it, don't add it — invented constraints look identical to real ones in the resulting code, and the reader will faithfully build them.

If something needs to be decided and you can't verify the answer yourself, ask the user **before** writing the plan. Plans don't carry question marks.

## Shape

A plan uses these top-level sections, in order, as `##` headings. The literal heading text matters — tooling and tooling-like readers extract sections by heading, so consistency is what makes the plan machine-readable as well as human-readable.

### `## Goal`

The user-provided goal, in plain English. One short paragraph. This is what the review judge receives.

### `## Acceptance criteria`

Bulleted, objectively verifiable. Each criterion is something an LLM with no context could test pass/fail in under a minute.

| not testable | testable |
|---|---|
| auth works | `POST /login` with valid creds returns 200 + a `Set-Cookie: session=...` header |
| dashboard loads fast | dashboard p95 load time under 2s on the staging dataset |
| handles errors gracefully | a malformed JSON body returns 400 with `{"error": ...}`, never 5xx |

If a criterion can't be made testable, the underlying goal is still fuzzy — go back to the user.

### `## Approach`

Chosen design, with brief rationale. For each significant design choice: name the options you considered (2-4 is plenty), pick one, note the trade-off accepted. Approach is design, not code — "use Postgres advisory locks for serialization, accepting that contention scales with shard count" is enough; don't pre-write SQL.

### `## File map`

Files to add/edit, one line per file with a few words on what changes. Cross-check against the task breakdown: every file change should trace to a task; every task should touch files listed here. Mismatches mean one of the two is wrong.

Before adding a file in a new directory, `grep` for similar files to confirm the convention. Inventing a directory layout is a planning smell — the codebase has opinions.

### `## Task breakdown`

Ordered list. Each task is sized for one red → green → refactor cycle — roughly 5-30 minutes of work depending on language and surface area.

- Too big: "Implement the auth service."
- Right size: "Add `verifyPassword(plaintext, hash): boolean` to `auth/password.ts`. Tests: happy path, wrong password, malformed hash. *Sequential after #2; blocks #4-#6.*"

Each task should leave the codebase in a working state — tests green, build clean. "This won't compile until task 5 lands" means the task is the wrong size; split it. Mark dependencies explicitly; default is sequential, parallel groups need to be called out.

### `## Out of scope`

Explicit deferrals. For each item, name the temptation *and* the reason it's being deferred.

- Weak: "perf out of scope."
- Useful: "perf optimization deferred until baseline metrics show it's actually a bottleneck"

A good "out of scope" entry lets a future reader see why something was *not* done, so they can revisit when conditions change.

## Voice

Plain English, lowercase headings. No "we will" preamble — just say what gets built. Concrete signatures, concrete test cases, explicit dependencies. Vague plans produce vague code.

## Escape hatch reminder

If you find yourself writing a plan for a one-line change, stop and ask whether the user wants a plan at all. Some changes don't need one — and an unnecessary plan invites unnecessary scope.
