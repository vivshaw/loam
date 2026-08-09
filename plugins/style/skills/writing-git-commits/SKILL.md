---
name: writing-git-commits
description: Use when committing changes, splitting work into commits, or writing commit messages - covers atomic commits, bisect-able history, separating concerns, and message style
user-invocable: false
---

# Writing Git Commits

Applies to all languages. Commits are the unit of review and bisect; treat them with the same care as the code they contain.

## What Makes a Commit

- Each commit is a logical, atomic unit of change.
- Every commit must build and pass all checks (bisect-able history).
- Separate concerns: formatting fixes and refactoring go in separate commits from feature changes.

## Message Style

- Use the Conventional Commits format (https://www.conventionalcommits.org/en/v1.0.0/)
- Use simple past and present tense in bodies: "Previously X happened. With this commit, Y now happens."
- Commit message bodies use markdown. Do not use backticks in commit titles, but do use them in bodies.
