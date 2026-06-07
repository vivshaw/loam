# CLAUDE.md

Working guide for `nous`, viv shaw's Claude Code plugin marketplace.

## Required tooling

Use nous to develop nous! The `meta` plugin contains the skills you need to work effectively in this repo.

## What this repo is

A curated marketplace of 7 plugins, mostly forked-and-evolved from [obra/superpowers](https://github.com/obra/superpowers) (MIT) and [ed3dai/ed3d-plugins](https://github.com/ed3dai/ed3d-plugins) (CC BY-SA 4.0).

Plugins included:

| plugin | contents |
|---|---|---|
| `techne` | brainstorm → plan → implement → review |
| `morphe` | **all** subagent definitions + agent-execution skills |
| `meta`  | skills for authoring plugins, skills, agents, marketplaces |
| `sophia` | coding standards + language-specific patterns |
| `ethos` | hooks that enforce automatic good habits |
| `graphe` | prose tools |
| `ephemera` | one-off commands (currently just `/ephemera:headpat`) |

## Plugin boundaries (these are the easy ones to get wrong)

- **`morphe` is the ONLY home for agent definitions**, even agents authored to support techne's workflow. skills that orchestrate or guide agents live in their topical plugin.
   - **agent-dispatching skills** (like `techne:reviewing-code`) stay in the topical plugin; the agent they dispatch (`morphe:code-reviewer`) is in morphe.
- **`meta` is home to all skills about working with skills/agents/plugins** (the self-referential layer).
- **`sophia` is home to all skills about coding guidelines**, including for specific languages or frameworks.

## Reference conventions

**Always use `<plugin>:<identifier>` form** when referring to a skill or agent, even within the same plugin. Examples:

- `` `morphe:codebase-investigator` `` ✓
- `` `codebase-investigator` `` ✗ (bare, even from inside morphe)
- `Dispatch morphe:internet-researcher with...` ✓
- `Dispatch internet-researcher with...` ✗

Applies to:
- Backticked references
- Bare prose mentions
- `subagent_type` dispatch parameters
- READMEs, comments, hook script output, everything

**Explicit exceptions** (do NOT prefix):
- Frontmatter `name:` declarations (a skill or agent declaring itself)
- File paths like `agents/code-reviewer.md` or `<skill>/SKILL.md`
- URLs

## Licensing

The whole marketplace is **CC BY-SA 4.0**. Whenever skills or plugins are forked in, ensure that you are following their licenses appropriately, and preserve those licenses. Current licenses to be aware of:

- **CC BY-SA 4.0 content from ed3dai/ed3d-plugins** → `LICENSE.ed3d-plugins` in the plugin root
- **MIT content from obra/superpowers** → `LICENSE.superpowers` in the plugin root
- **vivshaw-original content** → top-level `LICENSE`

Every plugin's `README.md` must include a `## credits` section that names upstream sources and points at the per-plugin `LICENSE.*` files.

## Adding things

### A new skill

1. Use the `meta:writing-skills` skill.
2. Set `user-invocable: false` unless you explicitly want `/<plugin>:<skill-name>` as a slash command
3. Cross-reference other skills/agents using the `<plugin>:<name>` form
4. Update the plugin's `README.md` "what's inside" section

### A new agent

Use the `meta:creating-an-agent` skill to create the agent. Agents go in `morphe/agents/<agent-name>.md`.

### A new plugin

Only create one if it's thematically distinct from the existing 7. then:

1. Choose a Greek philosophy-flavored name with conceptual fit
2. Use the `morphe:creating-a-plugin` skill
3. Add a bullet to the top-level `README.md` "currently in stock" list
4. Set up `LICENSE.*` files for any forked content

### Porting a plugin from another marketplace

The established pattern: **wholesale copy first, targeted edits after**. Don't try to hand-merge.

1. Fetch the upstream file with `curl` to `/tmp/`
2. `cp` it into the destination
3. Then run targeted `sed`/`Edit` passes to:
   - Rewire identifier prefixes to local plugins (`ed3d-plan-and-execute:<x>` → `morphe:<x>` etc.)
   - Update paths (`docs/implementation-plans/...` → `.techne/tasks/...`)
   - Rename in-line if the local name differs
4. Preserve attribution chain via the LICENSE.* files
5. Surface any remaining loose ends (broken refs, dependent skills/agents to port next)
