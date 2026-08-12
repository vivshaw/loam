# AGENTS.md

Working guide for `loam`, viv shaw's Claude Code plugin marketplace.

## What this repo is

A curated marketplace of 4 plugins, mostly forked-and-evolved from [obra/superpowers](https://github.com/obra/superpowers) (MIT) and [ed3dai/ed3d-plugins](https://github.com/ed3dai/ed3d-plugins) (CC BY-SA 4.0).

Plugins included:

| plugin | contents |
|---|---|
| `core` | brainstorm → plan → implement → review, **all** subagent definitions, research + prose skills |
| `meta`  | skills for authoring plugins, skills, agents, marketplaces |
| `style` | coding standards + language-specific patterns |
| `extra` | hooks that enforce automatic good habits |

## Structure

- **`core` is home to all agents.** Every subagent definition lives in `plugins/core/agents/`, generic or workflow-bound. The one exception is `meta:project-context-librarian`, which is driven by `meta:maintaining-project-context` and lives with it.
- **`core` is also home to the workflow itself** (brainstorm → plan → implement → review), the skills that dispatch agents, and the prose skills.
- **`meta` is home to all skills about working with skills/agents/plugins** (the self-referential layer).
- **`style` is home to all skills about coding guidelines**, including for specific languages or frameworks.
- **`extra` is home to hooks** that enforce good habits automatically. Hooks belonging to a specific workflow live with that workflow instead — `core`'s `reminder-use-generic-agents.sh`, `reminder-use-skills.sh`, and `continue-yoloproject.py` are in `plugins/core/hooks/`.

## Reference conventions

**Always use `<plugin>:<identifier>` form** when referring to a skill or agent, even within the same plugin. Examples:

- `` `core:researcher-codebase` `` ✓
- `` `researcher-codebase` `` ✗ (bare, even from inside core)
- `Dispatch core:researcher-internet with...` ✓
- `Dispatch researcher-internet with...` ✗

Applies to:
- Backticked references
- Bare prose mentions
- `subagent_type` dispatch parameters
- READMEs, comments, hook script output, everything

**Explicit exceptions** (do NOT prefix):
- Frontmatter `name:` declarations (a skill or agent declaring itself)
- File paths like `agents/critic-code-reviewer.md` or `<skill>/SKILL.md`
- URLs

## Licensing

The whole marketplace is **CC BY-SA 4.0**. Whenever skills or plugins are forked in, ensure that you are following their licenses appropriately, and preserve those licenses. Current licenses to be aware of:

- **CC BY-SA 4.0 content from ed3dai/ed3d-plugins** → `LICENSE.ed3d-plugins` in the plugin root
- **MIT content from obra/superpowers** → `LICENSE.superpowers` in the plugin root
- **vivshaw-original content** → top-level `LICENSE`

Every plugin's `README.md` must include a `## credits` section that names upstream sources and points at the per-plugin `LICENSE.*` files.

## Required tooling

Use loam to develop loam! The `meta` plugin contains the skills you need to work effectively in this repo.

### Python toolchain

The Python hook scripts in `plugins/extra/hooks/` have a Nix + uv toolchain wired up at the repo root. See [docs/DEVELOPING.md](docs/DEVELOPING.md) for the full setup and command reference. After modifying a hook, run `uv run pytest` before committing.

## Adding things

### A new skill

1. Use the `meta:writing-skills` skill.
2. Set `user-invocable: false` unless you explicitly want `/<plugin>:<skill-name>` as a slash command
3. Cross-reference other skills/agents using the `<plugin>:<name>` form
4. Update the plugin's `README.md` "what's inside" section

### A new agent

Use the `meta:creating-an-agent` skill to create the agent. Agents go in `plugins/core/agents/<agent-name>.md`.

### A new plugin

Only create one if it's thematically distinct from the existing 4. then:

1. Choose a short, conceptually apt name (the older plugins use Greek philosophy terms; newer ones favor plain English)
2. Use the `meta:creating-a-plugin` skill
3. Add a bullet to the top-level `README.md` "currently in stock" list
4. Set up `LICENSE.*` files for any forked content

### Porting a plugin from another marketplace

The established pattern: **wholesale copy first, targeted edits after**. Don't try to hand-merge.

1. Fetch the upstream file with `curl` to `/tmp/`
2. `cp` it into the destination
3. Then run targeted `sed`/`Edit` passes to:
   - Rewire identifier prefixes to local plugins (`ed3d-plan-and-execute:<x>` → `core:<x>` etc.)
   - Update paths (`docs/implementation-plans/...` → `.loam/tasks/...`)
   - Rename in-line if the local name differs
4. Preserve attribution chain via the LICENSE.* files
5. Surface any remaining loose ends (broken refs, dependent skills/agents to port next)
