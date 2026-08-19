# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.0] - 2026-08-18

### Added

- **style:** A new `howto-code-in-go` skill.

## [Unreleased]

### Added

- **core:** `plan-template.md` and `issue-template.md` in `core:project-writing-plan`

### Changed

- **core:** a project plan is now one `plan.md` plus one file per issue under `issues/`, replacing the `phase_*.md` files
- **core:** `project-writing-plan` investigates once upfront and settles architecture, dependencies, and conventions in the plan, so each issue stays short enough to read
- **core:** work is grouped into 2-5 milestones, each gated on passing tests for the spec requirements it claims
- **core:** progress lives in `plan.md` checkboxes alone, and the autonomous hook reads that one file instead of globbing phase files
- **core:** `critic-test-analyst` reads the spec and plan directly
- **core:** `executor-task` receives the plan plus one issue, and nothing else

### Removed

- **core:** `test-requirements.md`, `final.md`, and the `<!-- START_TASK_N -->` / `<!-- START_SUBCOMPONENT_A -->` marker machinery

## [2.0.0] - 2026-08-16

### Added

- **core:** A new `design-spec-exploring` skill, covering the ideation and research process for a PRD.
- **repo:** Added this changelog and adopted semver.

### Changed

- **core:** `design-spec-getting-started`, `design-spec-asking-clarifying-questions`, and `design-spec-brainstorming`, are all folded into `design-spec-exploring`
- **core:** `design-spec-writing` now produces a more concise PRD-style spec.
- **core:** `project-writing-plan` now derives its own phase breakdown from the spec's requirements, using the priority levels for scoping.
- **meta:** `maintaining-a-marketplace` now treats its changelog format as a default a project can override

## [1.0.0] - 2026-02-16

### Added

- Initial marketplace: the `core`, `meta`, `style`, and `extra` plugins
