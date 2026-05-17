---
name: tdd
description: "Use when about to write production code during /vivflow:implement, or when starting a new red → green → refactor cycle for a behavior change. Runs the three steps in order so behavior is captured by a test that actually failed before the code existed."
---

# TDD

Write a failing test. Watch it fail. Make it pass. Refactor.

## Why

A test that never saw the code fail doesn't prove the code is being tested. Skipping red is the single most common way to ship a test that passes regardless of the behavior under it.

## The cycle

1. **Red.** Write the test. Run it. Confirm it fails *for the reason you expect* — the actual assertion you care about, not a syntax error or missing import.
2. **Green.** Write the minimum production code to make the test pass. Run it. Confirm it passes.
3. **Refactor.** Clean up. Run the test again. Still green.

Each cycle is one task in the plan's breakdown. Keep cycles small — if a cycle has grown to "write three files and four tests," it's actually three cycles.

## Example

Adding a `slugify` function:

1. Red: `expect(slugify("Hello World")).toBe("hello-world")` — run, see `slugify is not defined`.
2. Green: write `slugify` returning lowercase, spaces-to-hyphens. Run, see green.
3. Refactor: collapse repeated whitespace handling, extract a regex constant. Run, still green.

## Escape hatch

Skip the cycle and say so when:

- the change isn't testable by its nature — copy edits, dependency bumps, formatter runs, deleting dead code.
- `/vivflow:implement` was invoked with `--quick` (or the user explicitly asked to skip TDD for this run).

TDD applies to behavior; not every change is behavior, and the user gets to call when ceremony is overkill. Spec-check still runs at the end either way.
