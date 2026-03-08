# vivipr

a Claude plugin for working with GitHub pull requests.

## requirements

- [`gh` CLI](https://cli.github.com/), authenticated
- agent harness must have a `TaskCreate` tool

## installation

assuming you've already added vivimart as a marketplace:

```
/plugin install vivipr@vivimart
```

## usage

one command is available:

- `/vivipr:address-pr-feedback` — walk through PR review comments in priority order, propose fixes, and draft replies. the user approves each fix and reply.
