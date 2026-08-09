# loam 🌱

vivshaw's Claude sundries

## setup

add loam as a marketplace in Claude Code:

```
/plugin marketplace add vivshaw/loam
```

then browse and install plugins:

```
/plugin install core@loam
```

to update all plugins from loam later:

```
/plugin marketplace update loam
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