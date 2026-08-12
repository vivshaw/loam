#!/usr/bin/env bash

cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "<agent-guidance>\nWhen instructed to use a 'general-purpose' agent, invoke the 'core:using-generic-agents' skill first — it covers which generic agent fits the task.\n</agent-guidance>"
  }
}
EOF

exit 0
