# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- **repo:** renamed from loam to gro. The marketplace is now `gro`, so installs are `/plugin install core@gro` and existing users need to re-add the marketplace.
- **core:** the state directory moved from `.loam/` to `.gro/`. In-flight work under `.loam/` is not migrated — move the directory by hand, or re-plan.
- **core:** `using-loam` is now `core:using-gro`.

## [3.0.0] - 2026-08-19

### Changed

- **core:** The project planning workflow is dramatically simplified. A project plan is now one `plan.md` plus one file per issue under `issues/`.

## [2.1.0] - 2026-08-18

### Added

- **style:** A new `howto-code-in-go` skill.

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
