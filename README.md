# gro 🌱

vivshaw's Claude sundries

## setup

add gro as a marketplace in Claude Code:

```
/plugin marketplace add vivshaw/gro
```

then browse and install plugins:

```
/plugin install core@gro
```

to update all plugins from gro later:

```
/plugin marketplace update gro
```

## what's inside

- [core](plugins/core/README.md), the `research -> plan -> implement -> review` workflow, the agent menagerie, and other basic tools
- [meta](plugins/meta/README.md), skills for working with agents and skills
- [style](plugins/style/README.md), coding standards & language-specific patterns
- [extra](plugins/extra/README.md), extra agent hooks

## recommended complements

- [Chrome DevTools for Agents](https://developer.chrome.com/docs/devtools/agents)

## development

see [docs/DEVELOPING.md](docs/DEVELOPING.md).