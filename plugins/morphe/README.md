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
| `code-reviewer` | adversarial code review against plan + standards |
| `task-bug-fixer` | apply code-review feedback systematically |
| `codebase-investigator` | investigate existing codebase state |
| `internet-researcher` | find current external information |
| `combined-researcher` | codebase + internet in one pass |
| `remote-code-researcher` | clone and analyze external repositories |
| `test-analyst` | validate test coverage against acceptance criteria |
| `task-implementor-fast` | implement individual tasks from a phase plan |
| `haiku-general-purpose` / `sonnet-general-purpose` / `opus-general-purpose` | generic agents at three model tiers |

**skills (agent-execution patterns)**

- `investigating-a-codebase` — used by the codebase/investigator agents
- `researching-on-the-internet` — used by the research agents
- `using-generic-agents` — how to dispatch the generic agents correctly
- `doing-a-simple-two-stage-fanout` — pattern for parallel agent dispatch

**hooks**

- `session-start.sh` — reminds the model to invoke `using-generic-agents` when it's about to dispatch a generic agent

## credits

morphe is derived from [ed3dai/ed3d-plugins](https://github.com/ed3dai/ed3d-plugins) (CC BY-SA 4.0, © Ed Ropple). See `LICENSE.ed3d-plugins`.
