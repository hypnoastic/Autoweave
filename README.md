# AutoWeave

AutoWeave is a terminal-first orchestration library for multi-agent workflow runs. The package owns canonical workflow state, scheduling, approvals, artifacts, routing, context services, observability, and the lightweight local operator console.

## Package surface

- `autoweave/`: library implementation
- `apps/cli/`: shipped CLI entrypoints
- `autoweave.templates`: packaged sample-project templates used by `bootstrap`
- `autoweave.monitoring`: lightweight local UI served by `autoweave ui`

The editable sample project does not live as committed root library state. Generate it explicitly with:

```bash
python -m apps.cli.main bootstrap --root .
```

## Common commands

```bash
python -m pip install -e .[dev]
python -m apps.cli.main validate --root .
python -m apps.cli.main doctor --root .
python -m apps.cli.main ui --root .
```

## Monitoring UI

The UI is part of the monitoring module, not `apps/ui`. The server entrypoint lives in `autoweave.monitoring.web`, and the page shell lives in `autoweave.monitoring.dashboard_page`.

## Packaging

Build a wheel locally with:

```bash
python -m pip wheel --no-build-isolation --wheel-dir dist .
```

Build a source distribution with:

```bash
python -m build --sdist
```
