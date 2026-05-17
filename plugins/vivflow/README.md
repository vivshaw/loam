# vivflow

an opinionated `research → plan → implement → review` workflow for Claude Code.

four phases, four commands, a handful of auto-invoked skills that enforce discipline (TDD, completion verification, doc shape). plus an iterative adversarial review pass at the end.

artifacts live in `.vivflow/` at the repo root, which is gitignored. nothing the workflow produces gets committed unless you explicitly choose to.

## why

[superpowers](https://github.com/obra/superpowers) and [ed3d-plugins](https://github.com/EdoardoTosin/ed3d-plugins) have the right *shape* — a planned, test-driven, reviewed flow with a self-hosting meta layer — but both commit plan/spec docs into your repo by default, both moralize with all-caps Iron Laws and termination-threat language, and both insist every change flow through the full ceremony.

vivflow's pitch: same R → P → I bones, same TDD spine, but quieter prose, escape hatches for small changes, artifacts in `.vivflow/` instead of `docs/`, and the addition of an adversarial review pass.

## installation

assuming you've already added vivimart as a marketplace:

```
/plugin install vivflow@vivimart
```

## setup

one-time per repo:

```
/vivflow:setup
```

creates `.vivflow/` and adds it to `.gitignore`. idempotent — safe to re-run.

## commands

- `/vivflow:setup` — bootstrap `.vivflow/` and gitignore.
- `/vivflow:research <topic>` — gather information into `.vivflow/tasks/<slug>/research.md`.
- `/vivflow:plan <goal>` — write the spec-to-implement into `.vivflow/tasks/<slug>/plan.md`.
- `/vivflow:implement [<slug>] [--quick]` — execute the plan, TDD-style, with a spec-check gate at the end.
- `/vivflow:review` — iterative adversarial review against the branch diff.

each phase has an explicit escape hatch. trivial changes don't need the full ceremony.

## the skills (auto-invoked)

- **tdd** — red → green → refactor, fires when about to write production code during `/vivflow:implement`.
- **verifying-claims** — fires before any "done" claim; catches the common ways those claims go wrong.
- **writing-research** — shape-guide for `research.md`.
- **writing-plans** — shape-guide for `plan.md`.

## file layout

```
.vivflow/                                  # gitignored
  specs/                                    # design specs, optional, hand-authored
  tasks/
    2026-05-16-react-data-viz/              # one folder per workflow run
      research.md                           # /vivflow:research output
      plan.md                               # /vivflow:plan output
      notes.md                              # optional scratchpad
```

each workflow run gets its own task folder. files are never scanned across folders — the workflow is sequential per task, and past research has no implicit bearing on a present task.

task slugs are `YYYY-MM-DD-<kebab-name>`, where the name comes from whichever phase kicked off the task.

## the four phases, briefly

### research

information-gathering, not feature design. produces findings — file:line refs, prior art, options with trade-offs, web references, and any open questions for the user. whatever-it-takes sourcing: codebase, git history, web, similar repos, package docs, running code.

### plan

the spec to be implemented. has goal, acceptance criteria (testable), approach (with rationale), file map, TDD-sized task breakdown (with parallel/sequential markers), and out-of-scope.

open questions from research, and any new ones that surface during planning, get asked to the user before the plan is written. the finished plan has no question marks.

### implement

reads `plan.md`, ensures work happens on a feature branch (auto-creates `vivflow/<slug>` if you're on `main`), executes the task breakdown using the tdd and verifying-claims skills, then runs **spec-check** — a final pass that walks every acceptance criterion and confirms it's done (or explicitly deferred).

if any criterion fails spec-check, implementation pauses and reports rather than claiming success. `--quick` skips the per-task TDD cycle but **not** spec-check.

### review

GAN-style adversarial critique against the current branch. each round: a fresh judge subagent reads the goal and runs `git diff $(git merge-base HEAD main)..HEAD` itself, produces severity-grouped feedback; the implementer revises or ignores each item, carrying memory across rounds. loop until convergence, or until the implementer concludes the judge is no longer being useful (graceful exit). capped at 8 rounds.

the judge is anchored to goal + branch diff, but is free to read source files, grep, and check git history — whatever a good reviewer would do. the only context off-limits is the planning layer for *this* work (plan, research, spec inside `.vivflow/`), which would bias the critique toward "matches plan" instead of "is good code."
