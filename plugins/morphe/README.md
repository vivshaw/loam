# morphe

the agent menagerie: subagents and the skills that drive them. morphe is home to generic, self-contained agents (those with no dependencies on a specific plugin's workflow, vocabulary, or file formats).

## what's inside

**skills**

- `morphe:investigating-a-codebase`: how to build an understanding of a codebase and its patterns
- `morphe:researching-on-the-internet`: how to research a topic on the web
- `morphe:using-generic-agents`: when to dispatch the generic agents, and which to choose

**agents**

- `morphe:haiku-general-purpose` / `morphe:sonnet-general-purpose` / `morphe:opus-general-purpose`: generic agents at three model tiers
- `morphe:code-reviewer`: adversarial code review against plan + standards
- `morphe:codebase-investigator`: investigate existing codebase state
- `morphe:internet-researcher`: find current external information
- `morphe:combined-researcher`: codebase + internet in one pass
- `morphe:remote-code-researcher`: clone and analyze external repositories

**hooks**

- `session-start.sh`: reminds the model to invoke `morphe:using-generic-agents` whenever it dispatches a generic agent

## credits

morphe is derived from [ed3dai/ed3d-plugins](https://github.com/ed3dai/ed3d-plugins) (CC BY-SA 4.0, © Ed Ropple). Some agents trace through ed3d back to [obra/superpowers](https://github.com/obra/superpowers) (MIT, © Jesse Vincent). See `LICENSE.ed3d-plugins` and `LICENSE.superpowers`.
