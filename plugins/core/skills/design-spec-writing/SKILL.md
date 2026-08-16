---
name: design-spec-writing
description: Use after core:design-spec-exploring has settled the requirements, to write the design spec as a concise prioritized PRD.
user-invocable: false
---

# Writing Design Specs

## Overview

Write the design spec as a **product requirements document**: what must be true of the finished thing, numbered and prioritized, with just enough approach to make it feasible.

**Core principle:** A requirement states what must be true and how you'd know. Everything else is context that makes the requirements legible.

**Announce at start:** "I'm using the `core:design-spec-writing` skill to write the spec."

The entire Apple AirPods Pro PRD is about eight pages. It contains no architecture diagram, no component list, and no implementation schedule — just numbered requirements like *"7.3 The product shall pass vibration testing. It will be tested in 3 directions for one hour each, subjected to frequencies from 20 to 2,000 Hz. (P8)"*. One line that is simultaneously a requirement, its acceptance criterion, and its test plan. That is the target.

Length is a signal. A spec running past a few pages usually means implementation detail crept into the requirements. `core:project-writing-plan` handles the how, with fresh codebase context to do it well.

## Creating the file

Ask the user for a slug. Offer 2-3 generated from the conversation. Choose slugs that are lowercase, hyphenated, terse but unambiguous (`authn` over `authentication`, but not `auth`, which collides with `authz`). If the user has a ticketing system, the ticket ID works.

Copy the template at `design-spec-writing/spec-template.md` to `.loam/tasks/YYYY-MM-DD-{slug}/spec.md` and fill it in. The template carries per-section guidance in HTML comments — delete every one of them as you go, including the header comment. A spec that ships with its scaffolding still attached reads as unfinished.

## Structure

| Section | Holds |
|---|---|
| Context | Why this, why now. What's wrong with the status quo. |
| Objectives | What success looks like. Measurable wherever a number exists. |
| Use Cases | Two or three narratives. Named people, concrete situations. |
| Requirements | Numbered, prioritized, binding. The document. |
| Approach | The shape of the solution and the decisions already settled. |
| Open Questions | Unanswered, on purpose. |
| Glossary | Domain terms and third-party concepts a reader needs. |

The rest of this skill is how to write each of them well.

## Requirements

This is the document. Everything else supports it.

**Use "shall."** It reads stiffly and that's the point: it marks the sentence as binding rather than descriptive. "The system shall reject expired tokens" commits. "Tokens are validated" describes.

**Fold verification into the requirement.** Where checking is not obvious, say how it gets checked in the same sentence.

```markdown
2.2 Validation shall tolerate 5 minutes of clock skew between issuer and validator. (P8)
2.3 Token issuance shall complete within 200ms at p99, measured at 500 req/s sustained for 10 minutes. (P6)
```

**Cover failure, not just success.** For each capability, ask what the system must reject or degrade gracefully under. Those are requirements too, and they're the ones implementations forget.

```markdown
2.1 An expired token shall be rejected with 401 and a message that reveals nothing about why it failed. (P10)
```

**Group by aspect, number within the group.** `### 1. Token issuance` has sub-requirements `1.1`, `1.2`. Groups are for navigation, not hierarchy. Stick to one level of nesting; resist sub-sub-numbering.

**Cite requirements externally as `{slug}.1.1`.** Inside the document, plain `1.1` is enough. Project plans and test names use the scoped form, because a repo accumulates specs and `authn.2.1` versus `billing.2.1` needs to be unambiguous.

**Contracts belong here, not in Approach.** When other systems depend on an interface, its shape is a requirement, not a sketch:

```markdown
### 3. Token endpoint
3.1 POST /token shall accept `{client_id, client_secret}` and return `{access_token, expires_in}`, or 401 with `{error}`. (P10)
```

### Priorities

Every requirement carries a priority from P1 to P10. It answers one question: when the implementation hits a wall, what gets dropped?

| Range | Meaning |
|---|---|
| P10 | Ship-blocking. Without it the feature doesn't exist. |
| P7-P9 | Important. Shipping without it is a known, deliberate compromise. |
| P4-P6 | Valuable. Worth building, survivable to defer. |
| P1-P3 | Nice to have. First to go. |

If nearly everything is P10, the spec has scope that hasn't been examined yet. Push on it.

### Requirements versus implementation

| A requirement | Not a requirement |
|---|---|
| "Tokens shall expire within 1 hour of issue" | "TokenService.generate() sets exp to now + 3600" |
| "An expired token shall be rejected with 401" | "Middleware in src/api/middleware/auth.ts checks exp" |
| "Issuance shall complete within 200ms at p99" | "Cache the signing key in Redis" |

The left column stays true regardless of how it's built. The right column is an implementation detail. Later workflow steps will choose the implementation against the codebase as it actually exists, which is more current information than you have now.

## The other sections

**Context:** the problem and why it's live now. Concrete beats abstract: "two incidents last quarter traced to secrets leaked in CI logs" tells a reader more than "improve security posture."

**Objectives:** what changes if this succeeds. Attach numbers where numbers exist.

**Use Cases:** two or three narratives, a paragraph each, with names and specifics. They're what makes a reader feel the requirements rather than parse them, and they routinely surface requirements nobody had written down.

**Approach:** the shape of the solution in a few paragraphs. Enough that a reader believes the requirements are achievable and knows which architectural decisions are already settled. Also record what was deliberately ruled out and why; that's the part people re-litigate later. No phases, no file paths, no task breakdown.

**Open Questions:** Optional, but high value. If there are any, write them unanswered. A spec that pretends to have resolved everything is hiding its risk rather than flagging it.

**Glossary:** domain terms and third-party concepts a reader needs. Skip what's obvious to any engineer.

Write it all in `core:prose-writing-for-a-technical-audience` style: direct, specific, no throat-clearing, honest about unknowns.

## Validate the requirements

The requirements are the contract with implementation, so the user confirms them before the spec is done.

Present the Requirements section. AskUserQuestion: "Review the requirements. Approve, or tell me what's missing or mis-prioritized." Loop until approved.

Push on two things while reviewing: requirements that can't be checked ("the system shall be secure" — how would you know?), and priorities that are all P10.

## Handoff

Announce the spec is written, then hand off:

```
Design spec written to `.loam/tasks/{slug}/spec.md`.

Ready for the project plan? That needs fresh context to investigate the codebase properly.

**Copy the line below before running /clear — it erases this conversation.**

(1) Copy this:

    Use the core:project-getting-started skill for @.loam/tasks/{slug}/spec.md

(2) Run /clear

(3) Paste and run it.
```

## Common Rationalizations

| Excuse | Reality |
|---|---|
| "More detail makes implementation easier" | It makes the spec stale faster. Detail belongs where it can be checked against the codebase. |
| "I should break this into phases" | That's `core:project-writing-plan`, with better information than you have. |
| "Everything here is genuinely P10" | Then the scope hasn't been examined. Ask what ships if the deadline halves. |
| "This requirement is obviously testable" | Write how it's checked. If you can't, it isn't a requirement yet. |
| "I'll note the open questions once they're answered" | Unanswered questions are the highest-value content in the document. |
| "The approach section should show the code" | Contracts go in Requirements as normative shapes. Behavior goes in the plan. |
| "The template's comments explain things, I'll leave them in" | They're scaffolding addressed to you, not the reader. Strip them. |
| "The user approved the objectives, requirements are implied" | Objectives are direction. Requirements are the contract. Confirm them explicitly. |
