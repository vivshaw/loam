<!--
  Design spec template. Copy to .loam/tasks/YYYY-MM-DD-{slug}/spec.md and fill in.
  Delete every HTML comment in this file, including this one, as you go.
  Guidance on writing each section lives in core:design-spec-writing.
-->

# [Feature Name]

## Context

<!--
  The problem and why it's live now. One or two paragraphs.
  Concrete beats abstract: name the incident, the complaint, the number.
-->

[What's wrong with the status quo, and what makes it worth fixing now.]

## Objectives

<!-- What changes if this succeeds. Attach numbers wherever numbers exist. -->

[Outcome, measurable where possible.]

[Outcome.]

## Use Cases

<!--
  Two or three narratives, a paragraph each. Named people, concrete situations.
  These routinely surface requirements nobody had written down.
-->

**[Name], [role].** [What they're trying to do, what goes wrong today, and what
this feature changes for them.]

**[Name], [role].** [Second narrative.]

## Requirements

<!--
  The document. Everything else supports it.

  - "shall" — binding, not descriptive
  - Fold verification into the requirement where checking isn't obvious
  - Cover failure and edge cases, not just the happy path
  - Group by aspect; number within the group; don't sub-sub-number
  - Contracts belong here as normative shapes, not in Approach
  - Cited elsewhere as {slug}.1.1 — plain 1.1 is enough inside this document

  Priorities:
    P10     ship-blocking — without it the feature doesn't exist
    P7-P9   important — shipping without it is a deliberate compromise
    P4-P6   valuable — worth building, survivable to defer
    P1-P3   nice to have — first to go

  If nearly everything is P10, the scope hasn't been examined yet.
-->

### 1. [Aspect]

1.1 The system shall [observable behavior]. (P10)

1.2 The system shall [behavior], [how it gets verified]. (P6)

1.3 [Invalid input / failure case] shall [what the system does about it]. (P10)

### 2. [Aspect]

2.1 The system shall [behavior]. (P10)

## Approach

<!--
  The shape of the solution, in a few paragraphs. Enough that a reader believes
  the requirements are achievable and knows which decisions are already settled.
  No phases, no file paths, no task breakdown — core:project-writing-plan derives
  those against the codebase as it actually is.
-->

[How this gets built, in broad strokes.]

[What was deliberately ruled out, and why. This is the part people re-litigate.]

## Open Questions

<!-- Ship these unanswered. A spec that resolves everything is hiding its risk. -->

- [Question nobody has settled yet.]
- [Question.]

## Glossary

<!-- Domain terms and third-party concepts a reader needs. Skip the obvious. -->

**[Term]** — [what it means here.]
