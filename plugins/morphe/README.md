# morphe

the agent menagerie: subagents and the skills that drive them. designed for interoperation with [techne](../techne/README.md).

## installation

assuming you've already added nous as a marketplace:

```
/plugin install morphe@nous
```

## what's inside

**agents**

| agent | role |
|---|---|
| `morphe:code-reviewer` | adversarial code review against plan + standards |
| `morphe:task-bug-fixer` | apply code-review feedback systematically |
| `morphe:codebase-investigator` | investigate existing codebase state |
| `morphe:internet-researcher` | find current external information |
| `morphe:combined-researcher` | codebase + internet in one pass |
| `morphe:remote-code-researcher` | clone and analyze external repositories |
| `morphe:test-analyst` | validate test coverage against acceptance criteria |
| `morphe:task-implementor-fast` | implement individual tasks from a phase plan |
| `morphe:project-claude-librarian` | keep `CLAUDE.md` current as the codebase evolves |
| `morphe:haiku-general-purpose` / `morphe:sonnet-general-purpose` / `morphe:opus-general-purpose` | generic agents at three model tiers |

**skills (agent-execution patterns)**

- `morphe:investigating-a-codebase` — used by the codebase/investigator agents
- `morphe:researching-on-the-internet` — used by the research agents
- `morphe:using-generic-agents` — how to dispatch the generic agents correctly
- `morphe:doing-a-simple-two-stage-fanout` — pattern for parallel agent dispatch

**hooks**

- `session-start.sh` — reminds the model to invoke `morphe:using-generic-agents` when it's about to dispatch a generic agent

## credits

morphe is derived from [ed3dai/ed3d-plugins](https://github.com/ed3dai/ed3d-plugins) (CC BY-SA 4.0, © Ed Ropple). Some agents trace through ed3d back to [obra/superpowers](https://github.com/obra/superpowers) (MIT, © Jesse Vincent). See `LICENSE.ed3d-plugins` and `LICENSE.superpowers`.
