# loam 🌱

vivshaw's Claude sundries

## setup

add loam as a marketplace in Claude Code:

```
/plugin marketplace add vivshaw/loam
```

then browse and install plugins:

```
/plugin install techne@loam
```

to update all plugins from loam later:

```
/plugin marketplace update loam
```

## what's inside

- [techne](plugins/techne/README.md), an opinionated `research -> plan -> implement -> review` workflow that is the core of this repo
- [meta](plugins/meta/README.md), agent skills for working with agents and skills
- [morphe](plugins/morphe/README.md), the agent menagerie: subagents and the skills that drive them
- [sophia](plugins/sophia/README.md), viv shaw's house style: coding standards, language-specific patterns, writing craft
- [ethos](plugins/ethos/README.md), automated good habits: secret checks, sensitive-file guards, doc reminders, skill nudges
- [graphe](plugins/graphe/README.md), writing tools

## recommended complements

- [Modern Web Guidance](https://developer.chrome.com/docs/modern-web-guidance)
- [Chrome DevTools for Agents](https://developer.chrome.com/docs/devtools/agents)

## development

see [docs/DEVELOPING.md](docs/DEVELOPING.md).