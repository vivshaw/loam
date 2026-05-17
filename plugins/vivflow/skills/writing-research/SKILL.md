---
name: writing-research
description: "Use when writing or editing a research.md file inside .vivflow/tasks/<slug>/ — produced by /vivflow:research. Shapes the document as findings and observations (not solutions or recommendations), with file:line refs for codebase claims, citations for web claims, options framed as trade-offs, and any unresolved questions explicitly tagged for the user or for the next phase."
---

# Writing research

Research captures **findings, not solutions**. The next phase (`/vivflow:plan`) decides the approach. Your job here is to make that decision well-informed.

## Verify, don't assume

Every claim in the doc must trace to one of:

- direct user input
- something actually observed: file:line, command output, URL contents, git history

If you can't find the source, ask the user — but only when the question is about their intent or genuinely can't be verified from available sources. First, try to verify it yourself: read the file, run the command, search the web, check the git log.

Inferred requirements don't belong in research. They look identical to real ones to the next phase, and that's expensive.

## Shape

A `research.md` has these sections (omit any that don't apply):

- **Topic** — restate the topic in one sentence.
- **Current state** — what's in the relevant part of the codebase right now, with file:line refs.
- **Prior art** — related projects, libraries, conventions, similar problems solved elsewhere.
- **Options** — distinct approaches with brief trade-offs. Two to four is plenty; if you've found ten, you haven't compared yet.
- **Constraints** — frameworks, conventions, perf budgets, deps, deadlines.
- **References** — useful URLs, each with one line on why it's worth the click.
- **Open questions** — things you couldn't resolve. Each one tagged `for user` or `for next phase`.

## Voice

Plain English. Lowercase headings are fine. No marketing prose. No "we should" — that's the plan's job.

## Example: an option entry

> **Recharts** — declarative React components, decent default theming, but limited customization for non-standard chart types. Maintained, weekly downloads ~3M. (`https://recharts.org`)

Concrete, sourced, takes a position on the trade-off in one sentence. That's the shape.
