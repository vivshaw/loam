---
description: "Bootstrap .techne/ at the repo root and add it to .gitignore"
user-invocable: true
---

# /techne:setup

One-shot bootstrap for techne. Idempotent — safe to re-run.

## Steps

1. Determine the repo root (`git rev-parse --show-toplevel`). If that fails, the user isn't in a git repo; tell them to `git init` first and stop.

2. Create `.techne/` and `.techne/tasks/` at the repo root if they don't exist.

3. Check `.gitignore` at the repo root:
   - If it contains a line `.techne/` (with or without trailing whitespace, ignoring blank/comment lines), do nothing.
   - Otherwise, append `.techne/` on its own line. Create `.gitignore` if it doesn't exist.

4. Print **one line** confirming what was done. Examples:
   - `techne set up at .techne/ (added to .gitignore)`
   - `techne already configured`
   - `techne set up at .techne/ (.gitignore already had it)`

No further output. The user just wants to know it's ready.
