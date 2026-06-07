---
description: "Bootstrap .techne/ at the repo root and add it to .gitignore"
user-invocable: true
---

# /techne:setup

One-shot bootstrap for techne. Idempotent, safe to re-run.

## Steps

1. Determine the repo root (`git rev-parse --show-toplevel`). If that fails, the user isn't in a git repo; tell them to `git init` first and stop.

2. Create `.techne/` and `.techne/tasks/` at the repo root if they don't exist.

3. Check whether `.techne/` is already ignored. Run `git check-ignore -v .techne/` from the repo root:
   - Exit 0 with source = the repo's `.gitignore`: do nothing.
   - Exit 0 with source = any other file (global excludes, e.g. `~/.config/git/ignore` or `core.excludesFile`): do nothing.
   - Exit 1 (not ignored): Inform the user that `.techne/` is not gitignored, and suggest that they do so. Use AskUserQuestion to ask whether they'd like to ignore that directory globally, to ignore it in a local `.gitignore`, or to allow the files in that directory to be committed (not recommended). Then follow through on their answer.

4. Print **one line** confirming what was done. Examples:
   - `techne set up at .techne/ (added to .gitignore)`
   - `techne set up at .techne/ (.gitignore already had it)`
   - `techne set up at .techne/ (already globally ignored)`

No further output. The user just wants to know it's ready.
