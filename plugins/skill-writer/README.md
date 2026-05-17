# skill-writer

a TDD-style plugin for authoring and verifying Claude Code skills.

scaffolding a `SKILL.md` is trivial — title, description, body, save. the non-trivial work is verifying that the skill actually fires when it should, and produces the behavior it claims once loaded. that's what this plugin focuses on.

skill-writer exists in part so that [vivflow](../vivflow/README.md) can be used to develop vivflow.

## installation

assuming you've already added vivimart as a marketplace:

```
/plugin install skill-writer@vivimart
```

## what's inside

one auto-invoked skill:

- **writing-skills** — fires when you're authoring or editing a `SKILL.md`. encapsulates the description-vs-body division of labor (trigger accuracy vs behavior), a TDD-style verification loop using fresh subagents, and length budgets.

there is no slash command. the skill loads when the work calls for it.

## the loop, briefly

1. **define pressure scenarios** — concrete prompts where the skill should fire, paired with what good behavior looks like. these are the tests.
2. **watch them fail** — run the scenarios in a fresh subagent without the skill loaded. confirm the model doesn't already do the right thing on its own.
3. **write the skill** — author the `SKILL.md`.
4. **watch them pass** — re-run with the skill loaded. iterate.

trigger accuracy lives in the `description` frontmatter; behavior lives in the body. they tune separately — distinguishing the two is what makes iteration efficient.
