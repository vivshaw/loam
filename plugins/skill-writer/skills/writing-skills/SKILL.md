---
name: writing-skills
description: "Use when authoring, editing, drafting, or reviewing a SKILL.md file, or when designing how a Claude Code skill should be triggered. Covers description-vs-body division of labor, length budgets, and a TDD-style verification loop using fresh subagents to confirm the skill actually fires on its target scenarios and produces the behavior it claims."
---

# Writing skills

A `SKILL.md` has two distinct surfaces, and they tune separately:

- **Description** (frontmatter): the only part Claude reads when deciding whether to load the skill. Trigger accuracy lives here.
- **Body**: what the agent does once the skill is loaded. Behavior lives here.

A failure to fire is a description problem. A failure to do the right thing once loaded is a body problem. Distinguishing the two is what makes iteration efficient.

## The loop

1. **Define pressure scenarios.** Write 3-5 concrete prompts where the skill *should* fire, each paired with what good behavior looks like. Also include 1-2 *anti-scenarios* — prompts where it should *not* fire — so you catch over-triggering.

2. **Watch them fail.** Dispatch a fresh subagent (no skill loaded) against each scenario. If the model already does the right thing on its own, the skill isn't earning its keep.

3. **Write the skill.** Draft the description and body. Keep both short.

4. **Watch them pass.** Re-run the scenarios with the skill loaded. Iterate description until trigger accuracy is right; iterate body until behavior is right.

## Description shape

Lead with "Use when…" and name the concrete trigger condition (file type, phase of work, situation). Then say what the skill does, in one sentence. Specific beats general — "Use when editing a SKILL.md" fires more reliably than "Use for skill authoring."

If the skill applies to multiple related situations, list them rather than abstracting. Concrete trigger words are what Claude pattern-matches on.

## Body shape

Target 30-80 lines. One rule per rule, one short reason, one tiny example. If a skill wants to grow past that, it's probably two skills.

Describe what good output looks like, rather than what the agent must not do. "Do X because Y" beats "you MUST X" plus footnote.

Avoid: all-caps emphasis, "Iron Law" framing, moralizing, anti-rationalization tables, termination-threat language. They turn the prompt into theatre without changing behavior.

## Escape hatches

Discipline skills get an explicit escape hatch for trivial cases. Trust the user to know when a change is small — don't ceremony every config tweak.

## Dispatching subagents for verification

Use the Agent tool with a fresh subagent for each scenario. The subagent should receive only the scenario prompt — no preamble, no "you are testing a skill." You want to see what the model actually does when faced with the prompt cold, not what it does when primed.

Read the subagent's output as if you were the user. Did it do the thing? If yes, the skill is earning its trigger. If no, iterate the description.
