---
name: using-loam
description: Use when starting any conversation - establishes how to find and use skills, invoking the Skill tool before responding, clarifying questions included
user-invocable: false
---

<subagent-note>
If you were dispatched as a subagent to execute a specific task, skip this skill.
</subagent-note>

# Getting Started with Skills

Skills carry the parts of this workflow you can't infer from the code in front of you. Checking for one costs seconds. Skipping one can cost a rewrite.

## The Rule

Check for relevant skills before any response or action — clarifying questions included.

1. List the available skills to yourself (shown in your system context)
2. Ask which of them could match this request
3. Invoke each plausible match with the Skill tool and follow it exactly

Even a 1% chance a skill applies is worth checking. If an invoked skill turns out not to fit, you don't have to use it — looking costs far less than missing.

```dot
digraph skill_flow {
    "User message received" [shape=doublecircle];
    "About to EnterPlanMode?" [shape=doublecircle];
    "Already explored the design?" [shape=diamond];
    "Invoke `core:design-spec-exploring` skill" [shape=box];
    "Might any skill apply?" [shape=diamond];
    "Invoke Skill tool" [shape=box];
    "Announce: 'Using [skill] to [purpose]'" [shape=box];
    "Has checklist?" [shape=diamond];
    "Create TodoWrite todo per item" [shape=box];
    "Follow skill exactly" [shape=box];
    "Respond (including clarifications)" [shape=doublecircle];

    "About to EnterPlanMode?" -> "Already explored the design?";
    "Already explored the design?" -> "Invoke `core:design-spec-exploring` skill" [label="no"];
    "Already explored the design?" -> "Might any skill apply?" [label="yes"];
    "Invoke `core:design-spec-exploring` skill" -> "Might any skill apply?";

    "User message received" -> "Might any skill apply?";
    "Might any skill apply?" -> "Invoke Skill tool" [label="yes, even 1%"];
    "Might any skill apply?" -> "Respond (including clarifications)" [label="definitely not"];
    "Invoke Skill tool" -> "Announce: 'Using [skill] to [purpose]'";
    "Announce: 'Using [skill] to [purpose]'" -> "Has checklist?";
    "Has checklist?" -> "Create TodoWrite todo per item" [label="yes"];
    "Has checklist?" -> "Follow skill exactly" [label="no"];
    "Create TodoWrite todo per item" -> "Follow skill exactly";
}
```

## Platform Adaptation

Skills use Claude Code tool names. Non-CC platforms: `references/codex-tools.md` (Codex) for tool equivalents.

## Red Flags

Each of these is a rationalization for skipping the check:

| Thought | Reality |
|---------|---------|
| "This is just a simple question" | Questions are tasks. Check for skills. |
| "I need more context first" | The skill check comes before clarifying questions. |
| "Let me explore the codebase first" | Skills tell you how to explore. Check first. |
| "I can check git/files quickly" | Files lack the conversation's context. Check for skills. |
| "This doesn't need a formal skill" | If a skill exists, use it. |
| "I remember this skill" | Skills evolve. Read the current version. |
| "The skill is overkill" | Simple things become complex. Use it. |
| "I'll just do this one thing first" | Check before doing anything. |
| "I know what that means" | Knowing the concept isn't the same as using the skill. |

## Announcing Skill Usage

Before using a skill, announce that you are using it. "I'm using [Skill Name] to [what you're doing]."

**Examples:**

- "I'm using the `core:design-spec-exploring` skill to work out what we're building."
- "I'm using the `core:execute-test-driven-development` skill to implement this feature."

**Why:** Transparency helps your human partner understand your process and catch errors early. It also confirms you actually read the skill.

## Skill Priority

When multiple skills could apply, use this order:

1. **Process skills first** (`core:design-spec-exploring`, `core:project-getting-started`) — these determine how to approach the task
2. **Implementation skills second** (`core:execute-implement-a-project`, `core:execute-test-driven-development`) — these guide execution

"Let's build X" → `core:design-spec-exploring` first, then implementation skills.
"Fix this bug" → debugging first, then domain-specific skills.

## Skill Types

**Many skills contain rigid rules** (`core:execute-test-driven-development`, `core:explore-systematic-debugging`, `core:critique-verifying-completion`): Follow them exactly. Don't adapt away discipline.

**Some skills contain flexible guidance** (architecture, patterns, naming): Adapt the principles to context.

The skill itself tells you which.

## User Instructions

User instructions say what, not how. "Add X" or "Fix Y" isn't an instruction to skip the workflow.
