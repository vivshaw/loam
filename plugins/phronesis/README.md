# phronesis

practical-wisdom hooks. small nudges that catch the mistakes Claude might otherwise make. designed to live alongside [techne](../techne/README.md) and [morphe](../morphe/README.md).

## installation

assuming you've already added nous as a marketplace:

```
/plugin install phronesis@nous
```

## what's inside

| hook | event | trigger | what it does |
|---|---|---|---|
| `check-bash-secrets.py` | PreToolUse | Bash | blocks bash commands that look like they're about to leak credentials, tokens, or env-var secrets |
| `check-sensitive-file.py` | PostToolUse | Write / Edit | warns when you touch files that commonly contain secrets (`.env`, keys, etc.) |
| `git-command-reminder.py` | PostToolUse | Bash | after `git status` / `git log`, suggests invoking the `project-claude-librarian` agent if changes affect contracts, APIs, or domain structure |
| `hook-reminder.sh` | UserPromptSubmit | (any) | injects a reminder about invoking the right skill before responding |

## credits

phronesis consolidates content from three ed3d hook plugins (`ed3d-hook-claudemd-reminder`, `ed3d-hook-security-hardening`, `ed3d-hook-skill-reinforcement`), all from [ed3dai/ed3d-plugins](https://github.com/ed3dai/ed3d-plugins) (CC BY-SA 4.0, © Ed Ropple). See `LICENSE.ed3d-plugins`.
