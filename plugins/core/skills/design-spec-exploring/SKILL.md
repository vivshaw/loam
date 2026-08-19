---
name: design-spec-exploring
description: Use when beginning any design process - gathers context, resolves contradictions, and explores approaches until requirements are clear enough to write down.
user-invocable: false
---

# Exploring a Design

## Overview

Turn a rough idea into understood requirements. This skill governs the exploration. `core:design-spec-writing` governs the resulting document.

**Core principle:** Resolve contradictions, then disambiguate, then explore approaches. Specifying the wrong thing precisely is the failure this order prevents.

**Announce at start:** "I'm using the `core:design-spec-exploring` skill to work out what we're building."

**Output:** discussion the problem and why it matters now, who it's for and what they're trying to do, what the system must do, which approach, and what's still unknown.

You are gathering *requirements*, not architecture. A requirement says what must be true of the finished thing. Notice when you've drifted into how it gets built — a little of that is useful for sanity-checking feasibility, but it isn't the goal here.

## Task tracking

TaskCreate three tasks (TodoWrite in older Claude Code versions):

- Context: problem understood, materials gathered
- Clarification: contradictions resolved, terms disambiguated
- Approach: options explored, one selected

Going backward is normal. A constraint surfacing during Approach sends you back to Clarification. Follow the understanding rather than the numbering.

## Context

Ask freeform (not AskUserQuestion). Ask only for what the user hasn't already given you:

- What are you building, and what's wrong with the status quo?
- Who is this for, and what are they trying to accomplish?
- Constraints: regulatory, existing systems, deadlines, decisions already made?
- Materials: URLs, file paths, prior research?

Then check for `.gro/design-spec-guidance.md`. If it exists, read it and fold it in. It carries project-specific terminology, required or forbidden technologies, stakeholders, and conventions designs must follow. If it doesn't exist, say nothing and move on.

## Clarification

**Answer your own questions first.** Dispatch `core:researcher-codebase` for anything about this repo, and `core:researcher-combined` when a recognizable technology or proper noun means both the codebase and the internet are worth checking. Bring the user only what research can't settle. If skills or MCP connections reach product-management datastores, send `core:general-purpose-sonnet` to look.

### Contradictions come first

Scan for goals that can't both hold. Resolving these changes what "right" means, so technical clarification before them is wasted.

- **Stated both ways:** "real-time" plus "batch is fine"; "keep it simple" plus "handle every edge case"; "no new dependencies" plus "integrate with Stripe"
- **Physically impossible:** "offline-first" plus "always-current"; "zero latency" plus "synchronous validation"
- **Unacknowledged trade-offs:** simple/flexible, fast/thorough, cheap/custom, secure/convenient

Illuminate the tension rather than accusing: "X and Y pull in different directions here — which takes priority when they conflict?"

### Then disambiguate

| Vague input | What to pin down |
|---|---|
| A technical term ("OAuth2", "caching", "database") | Which variant, at which layer |
| A broad noun ("users", "reporting", "integrate with X") | What's in scope and what's explicitly out |
| A stated requirement ("must use X", "needs to be fast") | The *why* behind it, and whether it's hard or preference |
| An external service or library | Which version, which API — quick check, not deep research |

AskUserQuestion for choices between 2-4 distinct options with trade-offs. Open-ended questions for *why* — those uncover constraints the user didn't know they had.

Numbers matter here. "Fast" becomes "sub-200ms p99." "Handles load" becomes "500 concurrent requests." Vague adjectives at this stage become untestable requirements later.

### Ask only questions worth asking

Every option you present must be one a reasonable person could choose. A question where two of three options are obviously wrong is not a valuable question. If only one answer is coherent, state your assumption and move on. If you have no useful questions left, stop asking.

## Approach

Research before proposing. Dispatch `core:researcher-codebase` for existing patterns **in this project**; if this project has an established pattern and it isn't clearly unwise, that's the default and one proposed approach should follow it. When the project is new or has no such pattern, use `core:researcher-internet` for how the problem is usually solved. Research stays inside this project and the public internet. If the user wants an existing project of theirs treated as prior art, they'll tell you explicitly. If research comes up empty, refine the query and try again before handing the question to the user.

Propose 2-3 approaches. For each: the shape of it, the trade-offs, rough complexity. AskUserQuestion to select.

Then walk the user through the chosen design in a few paragraphs: what the pieces are, how they interact, where the boundaries sit. Ask "does this look right so far?" Incremental validation catches a wrong turn while it's still cheap.

Stay at the level of boundaries and responsibilities. Function bodies and algorithms belong to later planning and execution steps.

## Common Rationalizations

| Excuse | Reality |
|---|---|
| "User gave lots of detail, skip context" | Ask for what's missing. Detail isn't completeness. |
| "Requirements are clear, skip clarification" | Clarification is what makes them clear to *both* of you. |
| "Simple idea, one approach is enough" | Two or three surface problems that one hides. It can go quickly. |
| "I know this codebase" | You know a past state of it. Dispatch the researcher. |
| "Project is empty — their other repos show the conventions" | The project boundary is the research boundary. Ask which conventions apply, or read `.gro/design-spec-guidance.md`. |
| "I'll research this inline, it's quick" | Inline research eats the context you need for the design. Delegate it. |
| "Research found nothing on the first try" | Refine the query. Try different terms before escalating to the user. |
| "I'll present the whole design at once" | Section-by-section validation catches wrong turns early. |

## When to stop

Stop when contradictions are resolved, terms are unambiguous, scope boundaries are explicit, constraints are understood rather than merely stated, and an approach is chosen. Perfect information is not the bar. Enough information to write requirements is.

Then invoke `core:design-spec-writing`.
