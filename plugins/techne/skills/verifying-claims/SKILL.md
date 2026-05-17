---
name: verifying-claims
description: "Use before claiming a task, acceptance criterion, or implementation milestone is 'done' during /techne:implement, including the final spec-check pass. A short checklist that catches the common ways completion claims are wrong — test never failed first, tests not actually rerun in this session, UI not actually exercised."
---

# Verifying claims

Before you say "done," run this checklist:

- Did the test you wrote actually **fail first**? If you never saw red, you don't know what the test is testing.
- Do the relevant tests **pass now**? Run them.
- Did you run them **in this session**? "They passed earlier" is not evidence — the code has changed since.
- For UI or behavior changes the test suite doesn't cover: did you actually exercise the path? Open the browser, hit the endpoint, run the command, eyeball the output.

If any of those is "no" or "not sure," it's not done yet. Say so.

## Why

The most common false claim of completion is "the tests pass" when the speaker hasn't run them recently, has run only a subset, or has run a stale build. The checklist is short on purpose — longer checklists get skimmed.

## Example

> red seen: `slugify is not defined` (commit abc123 in WIP)
> green now: `npm test utils/slugify` → 4 passed (just ran)
> ran in this session: yes, output above
> UI exercise: n/a, pure utility

That's a clean done. The point isn't the format — it's that each line points to evidence you produced in this session.

## Escape hatch

For changes that genuinely have no test surface — docs, comments, ignored files, gitignore tweaks — say so explicitly when claiming done, instead of pretending a test ran.
