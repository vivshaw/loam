# meta

the home for agent skills that work with agents and skills.

meta exists in part so that [techne](../techne/README.md) can be used to develop techne.

## installation

assuming you've already added nous as a marketplace:

```
/plugin install meta@nous
```

## what's inside

one auto-invoked skill:

- **writing-skills** — scaffolding a `SKILL.md` is trivial: title, description, body, save. the non-trivial work is verifying that the skill fires when it should, and produces the behavior it claims. that's what this plugin focuses on.
fires when you're authoring or editing a `SKILL.md`. encapsulates the description-vs-body division of labor (trigger accuracy vs behavior), a TDD-style verification loop using fresh subagents, and length budgets. 

## credits

meta's `writing-skills` skill is derived from [obra/superpowers](https://github.com/obra/superpowers) (MIT, © Jesse Vincent). See `LICENSE.superpowers`.
