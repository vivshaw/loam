# developing gro

contributor guide for Gro, viv shaw's Claude Code plugin marketplace.

## developing hooks

some Gro features are implemented as hooks. most of these hooks live in `plugins/extra`; workflow-specific ones live in `plugins/core/hooks`. at this time, the preferred language for hooks is Python. shell is also acceptable (for extremely simple scripts only).

### prerequisites

- [Nix](https://nixos.org/download) (with flakes enabled)
- [direnv](https://direnv.net/) (optional, for auto-activation)

everything else (Python, uv, ruff, mypy, pre-commit, git) is pinned in the flake.

### up and running

if you have direnv active, you will be prompted to `direnv allow` upon `cd`ing in. if you do not, use `nix develop` to enter a one-off Nix shell.

once you are in the shell, run `pre-commit install` to activate Git hooks.

### Python toolchain

dev deps are managed by [uv](https://docs.astral.sh/uv/).

| command | what it does |
|---|---|
| `uv sync` | install dev deps into `.venv/` |
| `uv run pytest` | run the hook tests |
| `uv run ruff check plugins/` | lint |
| `uv run ruff format plugins/` | format |
| `uv run mypy` | typecheck |

config lives in:

- `flake.nix`: pinned tool versions
- `pyproject.toml`: uv deps, ruff / mypy / pytest config
- `.pre-commit-config.yaml`: git hook config
