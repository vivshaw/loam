# extra

automated good habits. home to hooks with nudges that catch the mistakes Claude might otherwise make.

## what's inside

**hooks**

| hook | event | trigger | what it does |
|---|---|---|---|
| `check-bash-secrets.py` | PreToolUse | Bash | blocks bash commands that look like they're about to leak credentials, tokens, or env-var secrets |
| `check-sensitive-file.py` | PostToolUse | Write / Edit | warns when Claude's about to touch files that commonly contain secrets (`.env`, keys, etc.) |
| `git-command-reminder.py` | PostToolUse | Bash | after `git status` / `git log`, suggests invoking the `meta:project-context-librarian` agent if changes affect contracts, APIs, or domain structure |

## usage

this plugin's hooks use Python 3.11+. make sure it's installed on your system and available as `python3` to avoid hook failures.

## credits

extra consolidates content from three hook plugins (`ed3d-hook-claudemd-reminder`, `ed3d-hook-security-hardening`, `ed3d-hook-skill-reinforcement`), all from [ed3dai/ed3d-plugins](https://github.com/ed3dai/ed3d-plugins) (CC BY-SA 4.0, © Ed Ropple). See `LICENSE.ed3d-plugins`.
