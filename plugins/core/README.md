# core

the core toolkit. an opinionated `research -> plan -> implement -> review` workflow, the agents that carry it out, and other basic tools.

## what's inside

**orientation skills:**

- `core:using-loam`: how to find and dispatch the rest of loam's skills
- `core:using-generic-agents`: when to dispatch the generic agents, and which to choose

**workflow skills:**

- `core:design-spec-getting-started`: orchestrates the full design phase
- `core:design-spec-asking-clarifying-questions`: resolves contradictions and scope before brainstorming
- `core:design-spec-brainstorming`: Socratic refinement of rough ideas into validated designs
- `core:design-spec-writing`: writes the validated design spec
- `core:project-getting-started`: orchestrates branch creation and project planning from a design spec
- `core:project-writing-plan`: writes the engineering task breakdown for each phase of a project
- `core:execute-implement-a-project`: executes a project plan phase by phase, dispatching a subagent per task
- `core:execute-test-driven-development`: applies red-green-refactor TDD discipline for any feature or bugfix
- `core:execute-finishing-a-development-branch`: structured options for merge, PR, or cleanup when work is done
- `core:critique-verifying-completion`: evidence-before-assertions gate before claiming work is done
- `core:critique-reviewing-code`: dispatches `core:critic-code-reviewer` and manages a loop of reviews and fixes until no more issues are flagged

**explore skills:**

- `core:explore-investigating-a-codebase`: how to build an understanding of a codebase and its patterns
- `core:explore-researching-on-the-internet`: how to research a topic on the web
- `core:explore-systematic-debugging`: applies structured root-cause analysis before proposing fixes

**prose skills:**

- `core:prose-writing-for-a-technical-audience`: prose craft for docs, commit messages, and explanations

**agents:**

- `core:general-purpose-haiku` / `core:general-purpose-sonnet` / `core:general-purpose-opus`: generic agents at three model tiers
- `core:researcher-codebase`: investigate existing codebase state
- `core:researcher-remote-code`: clone and analyze external repositories
- `core:researcher-internet`: find current external information
- `core:researcher-combined`: codebase + internet in one pass
- `core:executor-task`: implements individual tasks from a phase plan
- `core:executor-bug-fix`: applies code-review feedback systematically
- `core:critic-code-reviewer`: adversarial code review against plan + standards
- `core:critic-test-analyst`: validates test coverage against acceptance criteria

**hooks:**

| hook | event | what it does |
|---|---|---|---|
| `reminder-use-generic-agents.sh` | SessionStart | reminds the model to invoke `core:using-generic-agents` whenever it dispatches a generic agent |
| `reminder-use-skills.sh` | UserPromptSubmit | injects a reminder about invoking the right skill before responding |

## credits

core is derived from [obra/superpowers](https://github.com/obra/superpowers) (MIT, © Jesse Vincent) and [ed3dai/ed3d-plugins](https://github.com/ed3dai/ed3d-plugins) (CC BY-SA 4.0, © Ed Ropple). See `LICENSE.superpowers` & `LICENSE.ed3d-plugins`.
