# Study Agent

## Run

From the project root:

```powershell
uv sync
uv run core-agent
```

Alternative module-based run:

```powershell
uv run --with . python -m core.main
```

Direct file execution like `python src/core/main.py` is not recommended for this src-layout package.

