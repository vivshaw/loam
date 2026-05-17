---
name: researching-a-topic
description: "Use when /vivflow:research is invoked, to gather findings into .vivflow/tasks/<slug>/research.md. Orchestrates slug derivation, whatever-it-takes information gathering across codebase/git/web/similar repos, and handoff to the writing-research shape-guide. Findings, not solutions — the next phase decides the approach."
user-invocable: false
---

# Researching a topic

Information-gathering phase of vivflow. The output is **findings** that will inform the next phase (`/vivflow:plan`), not a solution.

## 1. Escape hatch

If the topic is small enough that the user could already answer it in one sentence, or you already have all the relevant context loaded in this conversation, say so and offer to skip straight to `/vivflow:plan`. Don't ceremony trivia.

If the user wants to proceed, continue.

## 2. Slug + folder

Derive a task slug: `YYYY-MM-DD-<kebab-name>` where the date is today (`date +%Y-%m-%d`) and `<kebab-name>` is a 3-6 word kebab-case summary of the topic.

Create `.vivflow/tasks/<slug>/` if it doesn't exist. If the folder already exists for today, append `-v2`, `-v3`, etc. to disambiguate (avoids ambiguity with kebab-names that already end in a digit).

Remember this slug in conversation context — `/vivflow:plan` and `/vivflow:implement` may need it later.

## 3. Research

Whatever-it-takes information-gathering. Pick whichever sources actually answer the question:

- the local codebase (`grep`, file reads)
- git history (`git log`, `git blame`) for *why* something is the way it is
- web searches for current best practices, library docs, known issues
- similar repos on github — read how others solved the same problem
- package docs, RFCs, changelogs, blog posts, conference talks
- running code (REPL, `curl`, browser devtools) to confirm actual behavior

Don't restrict to "what's in this codebase" by default.

**Verify, don't assume.** Every claim, requirement, or constraint must trace to direct user input or something actually observed (file:line, command output, URL contents, git history). When you cannot find the answer yourself, ask the user — but only when the question is about their intent/taste, or genuinely can't be verified from available sources. Inferred constraints look identical to real ones in the resulting code.

## 4. Write

The **writing-research** skill will fire and shape the output. Write to `.vivflow/tasks/<slug>/research.md`.

## 5. Report

Print the slug and the path. One line. Done.
