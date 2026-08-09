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

- [core](plugins/core/README.md),  the `research -> plan -> implement -> review` workflow, the agent menagerie, and other basic tools
- [meta](plugins/meta/README.md), agent skills for working with agents and skills
- [sophia](plugins/sophia/README.md), viv shaw's house style: coding standards & language-specific patterns
- [ethos](plugins/ethos/README.md), automated good habits: secret checks & sensitive-file guards

## recommended complements

- [Chrome DevTools for Agents](https://developer.chrome.com/docs/devtools/agents)

## development

see [docs/DEVELOPING.md](docs/DEVELOPING.md).