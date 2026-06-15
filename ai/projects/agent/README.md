# Study Agent (Agent V4)

A CLI study assistant that retrieves answers from an internal project knowledge base using multiple search modes.

This README is the main operational document for this project. It is intentionally practical and debug-first.

## 1) Project Snapshot

- Package name: `agent`
- Python: `>=3.12`
- Packaging style: `src` layout
- Entrypoint script: `core-agent`
- Main runtime: `src/core/agent_v4.py`
- Verified against repository state on: June 11, 2026

## 2) What The Project Does

The app runs an interactive CLI and supports these retrieval modes:

- `chat`: LLM-backed response via OpenRouter (when `OPENROUTER_API_KEY` is configured)
- `keyword`: TF-IDF retrieval with LLM answer synthesis from retrieved context
- `semantic`: embedding retrieval with LLM answer synthesis from retrieved context
- `hybrid`: keyword + semantic pipeline path (currently keyword-weighted in ranking)

Data source for retrieval starts with built-in docs from `src/data/knowledge_base.py` and can be extended at runtime using `load <path>` for TXT/MD/PDF/DOCX files.

## 3) Architecture Overview

Request flow:

1. User runs `uv run core-agent`
2. `src/core/main.py` creates `AgentV4`
3. `AgentV4.run(query)`
4. Mode command handling (`/mode ...`) or retrieval dispatch
5. Mode-specific engine returns ranked docs
6. Agent extracts best section context and returns LLM-synthesized answer (fallback: section text)

Core components:

- `src/core/main.py`: CLI loop and banner
- `src/core/agent_v4.py`: mode parsing, retrieval orchestration, section extraction
- `src/core/query_router.py`: active mode state
- `src/core/search_mode.py`: mode enum
- `src/core/hybrid_search.py`: hybrid combiner
- `src/core/openrouter_llm.py`: OpenRouter chat completion client

NLP components:

- `src/nlp/keyword_search.py`: keyword engine API
- `src/nlp/tfidf.py`: TF-IDF scoring logic
- `src/nlp/document_corpus.py`: in-memory documents
- `src/nlp/embedding_model.py`: `SentenceTransformer` wrapper
- `src/nlp/embedding_search.py`: semantic index and cosine similarity
- `src/nlp/pipeline.py`, `text_processor.py`, `tokenzier.py`: normalization/token pipeline

Knowledge/docs:

- `src/data/knowledge_base.py`: internal documents indexed by the agent

Tests:

- `src/tests/`

## 4) Setup

From `ai/projects/agent`:

```bash
uv sync
```

If `uv` is missing, install it first and rerun.

Optional chat-mode LLM configuration:

```bash
export OPENROUTER_API_KEY="your_api_key_here"
export OPENROUTER_MODEL="openrouter/free"
export OPENROUTER_MAX_TOKENS=512
```

You can also store these in either:
- `ai/projects/agent/.env`
- `ai/projects/agent/src/.env`

## 5) Run

Recommended:

```bash
uv run core-agent
```

Alternative:

```bash
uv run --with . python -m core.main
```

Not recommended with src-layout:

```bash
python src/core/main.py
```

That direct file execution can fail import resolution for `core`/`nlp` modules.

## 6) CLI Commands And Modes

Supported commands:

- `/mode` -> show mode selection menu
- `/mode <number>` -> set mode by index
- `/mode <name>` -> set mode by name
- `mode <name>` -> backward-compatible old syntax
- `load <path>` -> load one file or a directory of TXT/MD/PDF/DOCX files
- `exit` -> quit CLI

### Mode Index Mapping (Source Of Truth)

`AgentV4.MODE_BY_INDEX` currently maps:

- `1` -> `chat`
- `2` -> `keyword`
- `3` -> `semantic`
- `4` -> `hybrid`

The startup banner and runtime mode map are aligned with this order.

## 7) Retrieval Behavior

Keyword mode:

- Scores docs with TF-IDF based on query tokens
- Extracts best matching section, then asks LLM to answer from that context
- If LLM is unavailable/credits fail, returns the extracted section directly

Semantic mode:

- Lazily initializes embedding model on first semantic/hybrid usage
- Can fail when model download/init fails; agent falls back with message
- When semantic retrieval succeeds, agent uses LLM synthesis with retrieved context

Hybrid mode:

- Calls both keyword and semantic search paths
- Current combine logic only aggregates keyword scores in ranking (known limitation)
- Uses LLM synthesis over the selected retrieval context, with local fallback on LLM failure

Section extraction:

- Agent does not dump full docs by default
- It extracts one best section using heuristic token overlap and intent boosts

## 8) Project File Map

- `src/core/main.py`: CLI entrypoint
- `src/core/agent_v4.py`: primary runtime logic
- `src/core/agent.py`: legacy `StudyAgent`
- `src/core/hybrid_search.py`: hybrid ranking combiner
- `src/data/knowledge_base.py`: built-in seed docs
- `src/document_loader/*.py`: dynamic file loaders + document manager
- `src/nlp/*.py`: NLP/retrieval building blocks
- `src/tests/*.py`: pytest coverage

## 9) Testing And Validation

Run full suite:

```bash
uv run pytest -q src/tests
```

Compile/syntax check:

```bash
uv run python -m compileall -q src
```

Targeted mode tests:

```bash
uv run pytest -q src/tests/test_agent_v4_mode.py
```

Observed status (June 11, 2026):

- `14 passed, 0 failed`
- Previously unstable retrieval case for start-intent query is currently passing.

## 10) Error And Debug Catalog

### A) Setup / Environment Errors

1. `uv: command not found`
- Meaning: `uv` is not installed or not in `PATH`
- Debug:
  - `uv --version`
- Fix:
  - Install `uv`
  - Reopen terminal and rerun `uv sync`

2. Python version mismatch (`requires-python = ">=3.12"`)
- Meaning: interpreter is too old
- Debug:
  - `python --version`
- Fix:
  - Switch to Python 3.12+
  - Recreate environment and run `uv sync`

3. Environment mismatch warning from `uv`
- Signature:
  - `VIRTUAL_ENV=... does not match the project environment path .venv`
- Meaning: shell has a different active venv than project venv
- Impact: warning only, but can confuse dependency expectations
- Debug:
  - `echo $VIRTUAL_ENV`
  - `uv run python -V`
- Fix:
  - deactivate old venv, then run via `uv run ...`

### B) Import / Entry Errors

4. `ModuleNotFoundError: No module named 'core'` (or `nlp`)
- Typical cause: direct file run in src-layout (`python src/core/main.py`)
- Fix:
  - use `uv run core-agent` or `uv run --with . python -m core.main`

5. Import break after renaming `tokenzier.py`
- Meaning: `nlp.pipeline` imports `from nlp.tokenzier import Tokenizer`
- Debug:
  - `rg -n "tokenzier|Tokenizer" src`
- Fix:
  - update all imports atomically with any rename
  - rerun tests

### C) Runtime Mode / Routing Errors

6. Invalid mode input response
- Signature:
  - `Invalid mode selection.` or `Please choose 1, 2, 3, 4...`
- Cause: unsupported mode name/index
- Debug:
  - run `/mode`
- Fix:
  - use valid values (`1..4`, `chat|keyword|semantic|hybrid`)

7. Document load failures
- Signature:
  - `Load error(s): ...`
- Cause:
  - unsupported extension, missing file, or missing PDF dependency (`pypdf`)
- Debug:
  - validate path and extension
  - run `load <absolute-or-relative-path>`
  - for PDFs install dependency: `uv add pypdf`

### D) Retrieval Errors / Low Relevance

8. `No keyword results found.`
- Cause: empty corpus or token mismatch
- Debug:
  - verify knowledge docs are loaded in `AgentV4.__init__`
  - run keyword mode query with strong exact terms from docs
- Fix:
  - ensure docs are present in `knowledge_base.py`
  - adjust query wording

9. `No semantic results found.`
- Cause: semantic index empty or embedding issue
- Debug:
  - ensure semantic mode initialized
  - verify documents added to semantic engine in `_ensure_semantic_engine`
- Fix:
  - rerun semantic mode after successful model init

10. `Semantic mode is currently unavailable (...) Staying in keyword mode.`
- Cause: exception during semantic engine/model initialization
- Common reasons:
  - model download/network restrictions
  - dependency/runtime issues in `sentence-transformers`
- Debug:
  - run `uv run pytest -q src/tests/test_embedding_model.py`
  - run a minimal semantic query after `/mode 3`
- Fix:
  - ensure network/dependencies for model availability
  - inspect exception text in response for root cause

11. Start/run query returns wrong section (regression scenario)
- Regression signature:
  - query: `How to start this application ?`
  - expected: section containing `## Run`
  - observed (if regressed): another section such as `## Repository identity`
- Debug:
  - run `uv run pytest -q src/tests/test_agent_v4_mode.py::test_keyword_mode_returns_focused_run_section_for_start_query`
  - inspect `_select_best_document` + `_extract_relevant_section`
- Fix options:
  - boost run/setup intent scoring
  - tune token normalization and section scoring

12. Hybrid not truly combining semantic rank
- Cause:
  - `HybridSearch.search` calculates semantic results but does not include them in combined score
- Debug:
  - inspect `src/core/hybrid_search.py`
- Fix:
  - merge both keyword and semantic scores with normalized weighting

### E) Test / Quality Issues

13. Retrieval expectation regression
- File:
  - `src/tests/test_agent_v4_mode.py`
- Regression signature:
  - focused run-section assertion fails
- Debug path:
  - reproduce single test
  - print top-k docs and section scores for query
  - adjust ranking heuristics

14. Semantic tests slow on first run
- Cause: model initialization and artifact fetch
- Debug:
  - run only embedding tests to isolate
- Workaround:
  - warm up model once before full suite

### F) Platform-Specific Warnings

15. Hugging Face cache/symlink warnings (especially Windows)
- Meaning: non-fatal caching behavior differences
- Impact: usually warning-level; may increase disk usage
- Action: continue unless it escalates to hard failure

## 11) Recommended Debug Workflow

1. Verify environment:
```bash
python --version
uv --version
```

2. Sync dependencies:
```bash
uv sync
```

3. Run tests:
```bash
uv run pytest -q src/tests
```

4. Reproduce CLI behavior:
```bash
uv run core-agent
```

5. Reproduce targeted mode issue:
- `/mode`
- `/mode 2`
- `How to start this application ?`

6. Narrow by layer:
- Mode parsing: `handle_mode_change`
- Retrieval ranking: `_select_best_document`
- Section extraction: `_extract_relevant_section`
- Semantic init: `_ensure_semantic_engine`

7. Run focused tests after fix:
```bash
uv run pytest -q src/tests/test_agent_v4_mode.py
```

## 12) Known Limitations (Current)

- LLM-backed answers (all modes) need `OPENROUTER_API_KEY`; without it, retrieval modes return local context
- Hybrid ranking does not yet fuse semantic score into final rank
- `tokenzier.py` naming typo is legacy coupling risk

## 13) Maintenance Checklist

Before merging any core change:

1. Update `src/data/knowledge_base.py` docs to reflect behavior changes.
2. Re-run full tests and compile check.
3. Verify `/mode` UX manually.
4. Ensure README commands and behavior are still accurate.
5. If changing module/file names, run:

```bash
rg -n "keyword_engine|keyword_search|tokenzier|search_mode|core-agent" src README.md pyproject.toml
```
