#!/usr/bin/env bash

set -euo pipefail

# cetermine plugin root directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
PLUGIN_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "<skill-check>\nBefore responding, check whether any of your available skills apply to this prompt — they are listed in your system context. Activate each applicable skill with the Skill tool if it has not already been activated this session.\n</skill-check>"
  }
}
EOF

exit 0
