# techne

an opinionated `research -> plan -> implement -> review` workflow for Claude Code.

## what's inside

**skills:**

- `techne:using-techne`: how to find and dispatch the rest of techne's skills
- `techne:starting-a-design-plan`: orchestrates the full design phase (context -> clarify -> brainstorm -> write)
- `techne:asking-clarifying-questions`: resolves contradictions and scope before brainstorming
- `techne:brainstorming`: Socratic refinement of rough ideas into validated designs
- `techne:writing-design-plans`: writes validated design specs with discrete phases
- `techne:starting-an-implementation-plan`: orchestrates branch creation and detailed planning from a design
- `techne:writing-implementation-plans`: writes engineering task breakdowns for each phase of a project
- `techne:implementing-a-plan`: executes phase plans by dispatching subagents
- `techne:test-driven-development`: applies red-green-refactor TDD discipline for any feature or bugfix
- `techne:systematic-debugging`: applies structured root-cause analysis before proposing fixes
- `techne:verifying-completion`: evidence-before-assertions gate before claiming work is done
- `techne:reviewing-code`: dispatches `morphe:code-reviewer` and manages a loop of reviews and fixes until no more issues are flagged
- `techne:finishing-a-development-branch`: structured options for merge, PR, or cleanup when work is done

**agents**:

- `techne:task-implementor-fast`: implements individual tasks from a phase plan
- `techne:task-bug-fixer`: applies code-review feedback systematically
- `techne:test-analyst`: validates test coverage against acceptance criteria

## credits

techne is derived from [obra/superpowers](https://github.com/obra/superpowers) (MIT, © Jesse Vincent) and [ed3dai/ed3d-plugins](https://github.com/ed3dai/ed3d-plugins) (CC BY-SA 4.0, © Ed Ropple). See `LICENSE.superpowers` & `LICENSE.ed3d-plugins`.
