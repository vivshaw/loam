# multiharnessifying gro

research notes and a plan for running gro on Claude Code, Codex, and OpenCode as equals.

## the premise

there should be no primary platform. all three harnesses should be first-class citizens.

gro today is four Claude Code plugins carrying 41 skills, 12 agents, and 6 hooks. the question then is what it costs to adapt these things across platforms.

## portability

| asset | Claude Code | Codex | OpenCode |
|---|---|---|---|
| skills (41) | native | native | native |
| hooks (6) | native | 5 of 6 | 6 of 6, via a generated TS plugin |
| agents (12) | native, bundled | separate install, TOML | separate install, markdown |
| distribution | marketplace | marketplace | manual or npm |

skills are genuinely portable. everything else needs rendering per platform, and one capability cannot be ported (see [impossible](#impossible)).

## what each platform supports

| | Claude Code | Codex | OpenCode |
|---|---|---|---|
| **skills** | plugin `skills/`, `.claude/skills/` | `.agents/skills/`, plugin `skills/` | `.opencode/skills/`, and **also reads `.claude/skills/` and `.agents/skills/`** |
| **agents** | `agents/*.md` — `name`/`description`/`model`/`color` | `.codex/agents/*.toml` — `name`/`description`/`developer_instructions`; needs `[features] multi_agent = true` | `.opencode/agents/*.md` — `description`/`mode: subagent`/`model`/`permission`. **does not read `.claude/agents/`** |
| **hooks** | `hooks.json`, 6 events | same event names, same `hooks.json` schema, same stdin-JSON / exit-2 contract; behind `[features] codex_hooks = true` | **no shell hooks.** JS/TS plugin only |
| **marketplace** | `.claude-plugin/marketplace.json` | `.agents/plugins/marketplace.json` + `.codex-plugin/plugin.json` | none — npm package or manual install |
| **context file** | `CLAUDE.md` (imports `AGENTS.md`) | `AGENTS.md` | `AGENTS.md` |

the Agent Skills spec covers **only** `SKILL.md`. subagents, hooks, and plugin packaging are explicitly out of scope.

## fixable

### the `<plugin>:<name>` convention

329 uses across the repo. skills file are `agents/critic-code-reviewer.md` with the bare `name: critic-code-reviewer`, but other skills reference it as `core:critic-code-reviewer`, composing the plugin name.

measured, the 329 split three ways:

| refs | verdict |
|---|---|
| 12 `subagent_type` dispatch sites | **required** — tested: a bare name errors `Agent type not found`, with no fuzzy fallback |
| 290 same-plugin prose refs | noise; `core:` written inside `core/` |
| 39 cross-plugin prose refs | judgment call; carries an install-dependency signal (`core`→`style` 20x) |

instead, the references should drop the prefixes. the prefix will survive only at the 12 subagent dispatch sites. all 41 skill names and all 12 agent names are globally unique. this newly flat namespace needs zero renames.

### agents

three incompatible formats, and `model: opus|sonnet|haiku` is a Claude Code alias that means nothing elsewhere. worse, Codex's official plugin manifest declares only `skills`, `mcpServers`, `apps`, and `hooks`. agents install separately from the plugin.

the 12 split into two kinds:

- **3 tier-selectors** (`general-purpose-{opus,sonnet,haiku}`) — these encode nothing but a model pick. Codex ships `default`/`worker`/`explorer`/`monitor` and OpenCode ships `general`.
- **9 role agents** (`researcher-*`, `critic-*`, `executor-*`) — a system prompt, a model pick, and usually "use skill X".

note what superpowers does here: it ships **zero agent definitions**, only prompt markdown files (`code-reviewer.md`, `implementer-prompt.md`) that skills hand to whatever generic subagent the platform has. that sidesteps the format problem entirely, at the cost of losing description-based auto-dispatch and per-agent model routing.

### hooks

hooks are currently written to work with Claude Code specifically:

| hook | Claude Code | Codex | OpenCode |
|---|---|---|---|
| `check-bash-secrets.py` (pre_tool_use:Bash) | works | works | works |
| `git-command-reminder.py` (post_tool_use:Bash) | works | works | works |
| `check-sensitive-file.py` (post_tool_use:Write\|Edit) | works | **dead** — Codex matchers currently only ever see `tool_name: "Bash"` | works |
| `reminder-use-skills.sh` (user_prompt_submit) | works | works | `chat.message` |
| `reminder-use-generic-agents.sh` (session_start) | works | works | system-prompt transform |
| `continue-autonomous-run.py` (stop) | works | needs exit-2 port | `session.idle` + re-prompt |

other specifics:

- `continue-autonomous-run.py` emits `{"decision": "block", "reason": ...}`, which is Claude-specific. Codex documents exit-2 + stderr for blocking.
- both `hooks.json` files use `${CLAUDE_PLUGIN_ROOT}`. superpowers avoids the env var entirely by resolving from `$(dirname $0)`. our shell scripts already do this, the manifests do not.
- output JSON shape differs per host. Claude wants `hookSpecificOutput.additionalContext`, Cursor wants `additional_context`, the SDK standard wants top-level `additionalContext`. superpowers sniffs `CURSOR_PLUGIN_ROOT` / `CLAUDE_PLUGIN_ROOT` / `COPILOT_CLI` and emits three different shapes from one script.

### tool references in skill bodies

| tool | uses | elsewhere |
|---|---|---|
| `AskUserQuestion` | 31 | **no equivalent anywhere.** see [impossible](#impossible) |
| `Glob` | 22 | native equivalents exist |
| `TodoWrite` | 14 | Codex `update_plan`, OpenCode `todowrite` |
| `subagent_type` | 12 | Codex `spawn_agent`, OpenCode `task` |
| `WebSearch`/`WebFetch` | 16 | native equivalents exist |

skill bodies currently name Claude Code tools directly. instead, these should name the *capability* and let the registry supply the tool name per target.

`plugins/core/skills/using-gro/references/codex-tools.md` already covers some of this for Codex only.

## impossible


1. **`AskUserQuestion`.** 31 uses. structured multiple-choice has no equivalent on Codex or OpenCode. the skills must stop depending on a structured question tool.

## prior art

| project | strategy | verdict for us |
|---|---|---|
| [obra/superpowers](https://github.com/obra/superpowers) | commit N wrapper dirs (`.codex-plugin/`, `.opencode/`, `.cursor-plugin/`, `.pi/`, `.kimi-plugin/`, `.devin-plugin/`, `.hermes-plugin/`) + sync scripts over one shared `skills/` | the right *distribution* model: committed artifacts, no user-facing install step. the wrapper dirs rot at gro's surface area |
| [github/spec-kit](https://github.com/github/spec-kit) | nothing per-platform in the repo. a CLI with 36 declarative integration modules renders artifacts at install time | the right *authoring* model: each platform is ~60 lines of declarative config. generate-at-install costs the one-line marketplace UX |
| [BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) | `npx bmad-method install` writes into each IDE's dirs from a unified config; 40+ tools | same generate-at-install shape as spec-kit |
| [ed3dai/ed3d-plugins](https://github.com/ed3dai/ed3d-plugins) | **none — Claude Code only** | our other upstream offers no precedent. third-party directory sites claim multi-platform support; the repo and README do not |

### mapping hook events

spec-kit's integrations carry a canonical hook-event vocabulary mapped per platform:

```
canonical:  session_start  user_prompt_submit  pre_tool_use  post_tool_use  session_end  stop

claude   →  same names, no translation          .claude/settings.json   format: json-nested
codex    →  same names, no translation          .codex/config.toml      format: toml
opencode →  session_start       → a transform hook; which one is ours to pick
            user_prompt_submit  → chat.message
            pre_tool_use        → tool.execute.before
            post_tool_use       → tool.execute.after
            session_end         → session.deleted
                                                opencode.json           format: ts-plugin
```

1. **Codex uses Claude Code's exact event names, so no translation is needed** — corroborated by spec-kit's shipped Codex integration, whose event map is character-for-character identical to its Claude one.
2. **`session_start` has no direct equivalent on OpenCode.** our hook works by printing text the host injects into context. OpenCode's `session.created` is notification-only — a handler can observe that a session started but has no way to return text into the conversation, so nothing it prints goes anywhere. the bootstrap therefore has to happen in some other way. spec-kit does this by modifying he system prompt. superpowers, by prepending to the first user message (which requires a content check).

## recommended architecture

**spec-kit's authoring model, superpowers' distribution model.**

- a **neutral source tree** that names no platform: flat skill and agent names, canonical hook events, capabilities rather than tool names.
- a **platform registry** — one declarative table per target supplying skills dir, agent format and directory, hook event map, hook output shape, model tier aliases, tool name map, and name prefix.
- a **generator** rendering all three targets, Claude Code included.
- **generated artifacts committed to the repo**, so `/plugin marketplace add vivshaw/gro` keeps working with no user-facing build. contributors pay the build; users do not. a pre-commit hook regenerates and fails on drift.

### the layout question

today `plugins/` is both source and shipped artifact. to go cross-platform, it should become generated output for one target among three.

proposed: `skills/`, `agents/`, `hooks/` at the repo root as source; `plugins/`, `.agents/`, `.opencode/` as committed build output. that follows superpowers' layout and keeps every install path working.

the cost is the develop-gro-with-gro loop: edit a skill, regenerate before any harness sees it. mitigate with a `just`/`make` target in the existing Nix shell plus the pre-commit drift check. superpowers lives with exactly this via `sync-to-codex-plugin.sh`.

### documentation

going cross-platform changes what gro *is*, not only how it is built. `README.md` and `AGENTS.md` both describe a Claude Code plugin marketplace, and `AGENTS.md` mandates the `<plugin>:<name>` reference convention that a neutral source drops. both need updating, and `meta:`'s authoring skills (`writing-skills`, `creating-an-agent`, `creating-a-plugin`) teach the Claude-shaped form.

## phased plan

sequence is build-neutral, then render. earlier phases do not assume any target.

### phase 1 — neutralize the source

- flat skill and agent names in prose; prefix retained only at the 12 `subagent_type` dispatch sites
- hooks named by canonical event, not Claude's event names
- skill bodies name capabilities, not Claude tool names
- audit `using-gro` for hard Claude-isms (`EnterPlanMode` and `TodoWrite` appear in its decision graph)
- move the model tier off the agent and into the registry
- axe `AskUserQuestion`, per [impossible](#impossible)

### phase 2 — build the platform registry

the declarative table described above, plus the layout move to root-level `skills/` `agents/` `hooks/`.

### phase 3 — render Claude Code and Codex

the two cheap targets. Claude Code needs prefix injection and the existing plugin manifests; Codex needs `.codex-plugin/plugin.json`, `.agents/plugins/marketplace.json`, `.agents/skills/`, and `.codex/agents/*.toml`. hook events are an identity mapping for both.

verify parity on Claude Code before anything else merges — the generated output must be indistinguishable from what ships today.

### phase 4 — render OpenCode

generate, do not hand-write, `.opencode/plugins/gro.js`: registers skill paths via the `config` hook, injects bootstrap, and shells out to the phase-0 CLI. plus `.opencode/agents/*.md`.

### phase 5 — CI

- lint that every skill and agent reference resolves
- drift check: generated artifacts match their sources
- smoke test each target's output against its host's loader

## still to verify

- does Codex accept `hookSpecificOutput.permissionDecision`, or only exit-2 + stderr?
- what does Codex use in place of `${CLAUDE_PLUGIN_ROOT}`?
- can a Codex plugin bundle agents? official docs say no; one third-party writeup shows a `components.agents` manifest key. resolve before phase 3.
- do Codex and OpenCode reject unknown `SKILL.md` frontmatter keys, or ignore them?
- when do Codex `pre_tool_use`/`post_tool_use` matchers see tool names other than `Bash`?
- can the 4-plugin split survive off-platform at all? Codex reads a flat `.agents/skills/` and OpenCode has no plugin concept for skills, so `core`/`meta`/`style`/`extra` collapse into one pool on both. if per-plugin installability matters off-platform, that needs its own answer.

## sources

- [Agent Skills specification](https://github.com/agentskills/agentskills)
- [OpenCode: skills](https://opencode.ai/docs/skills/) · [agents](https://opencode.ai/docs/agents/) · [plugins](https://opencode.ai/docs/plugins/)
- [Codex: packaging plugins](https://developers.openai.com/codex/plugins/build)
- [Codex hooks guide](https://codex.danielvaughan.com/2026/04/15/codex-cli-hooks-complete-guide-events-policy-patterns/)
- [Codex customisation stack](https://codex.danielvaughan.com/2026/04/12/codex-cli-customisation-stack-unified-system/)
- [superpowers OpenCode support design](https://github.com/obra/superpowers/blob/main/docs/plans/2025-11-22-opencode-support-design.md)
- [spec-kit integration registry](https://github.com/github/spec-kit/tree/main/src/specify_cli/integrations)
- [opencode-agent-skills](https://github.com/joshuadavidthomas/opencode-agent-skills) — a compatibility shim, now in maintenance mode since OpenCode shipped native skills
