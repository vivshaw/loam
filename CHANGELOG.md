# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **core:** `design-spec-exploring` skill, holding the whole pre-writing conversation — context gathering, contradiction resolution, disambiguation, and approach selection
- **core:** `design-spec-writing/spec-template.md`, a fill-in-the-blank PRD skeleton with per-section guidance in strippable HTML comments
- **repo:** this changelog, plus versioning and release guidance in `AGENTS.md`

### Changed

- **core:** `design-spec-writing` now produces a product requirements document — Context, Objectives, Use Cases, numbered Requirements each carrying a P1-P10 priority, Approach, Open Questions, Glossary. Verification folds into the requirement that needs it, so one line serves as requirement, acceptance criterion, and test plan.
- **core:** `project-writing-plan` derives its own phase breakdown from the spec's requirements and presents it for approval. The eight-phase limit survives, but priorities do the scoping: over budget it cuts P1-P3 first, then P4-P6, reports what it cut, and stops rather than dropping a P10 silently.
- **core:** requirement identifiers are scoped `{slug}.1.1` rather than `{slug}.AC1.1`, with priority carried through to the executor
- **core:** `project-getting-started` and `execute-implement-a-project` read requirements coverage instead of acceptance criteria coverage
- **meta:** `maintaining-a-marketplace` now treats its changelog format as a default a project can override

### Removed

- **core:** `design-spec-getting-started`, `design-spec-asking-clarifying-questions`, and `design-spec-brainstorming`, folded into `design-spec-exploring`
- **core:** design specs no longer carry Summary, Definition of Done, Acceptance Criteria, Existing Patterns, Implementation Phases, `<!-- START_PHASE_N -->` markers, or Additional Considerations

## [1.0.0] - 2026-02-16

### Added

- Initial marketplace: the `core`, `meta`, `style`, and `extra` plugins
