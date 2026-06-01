# Study Agent

## Run

From the project root:

```powershell
uv sync
uv run study-agent
```

Alternative module-based run:

```powershell
uv run --with . python -m study_agent.main
```

Direct file execution like `python src/study_agent/main.py` is not recommended for this src-layout package.
