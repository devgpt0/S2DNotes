"""
Central project knowledge base for the `agent` repository.

This module is organized into focused doc variables so code can consume
specific sections (architecture, runbook, debugging, maintenance, etc.).
"""

PROJECT_OVERVIEW_DOCS = """
# Project Overview Docs

## Repository identity
- Root: `C:/pocs/notes/ai/projects/agent`
- Packaging: `src` layout
- Python: `>=3.12`
- Build backend: `setuptools`
- Runtime script entrypoint: `core-agent`

## What this project does
- Runs a CLI study assistant over an internal project knowledge base.
- Supports retrieval modes:
  - chat
  - keyword (TF-IDF)
  - semantic (embeddings)
  - hybrid (keyword + semantic pipeline scaffold)

## Main package areas
- `src/core`
  - app entrypoint, mode router, agent runtime
- `src/nlp`
  - NLP and retrieval engines
- `src/tests`
  - pytest tests for core behaviors
- `src/data`
  - knowledge base docs used by the agent

## Current maturity snapshot (June 10, 2026)
- `core/main.py` starts `AgentV4` with ASCII banner and command help.
- `/mode` supports numbered direct selection (`1..4`) and named selection.
- Keyword and semantic engines are runnable.
- Full test suite currently passes in this project environment.
"""

ARCHITECTURE_DOCS = """
# Architecture Docs

## Request lifecycle
1. User launches CLI via `uv run core-agent`.
2. `core.main` creates `AgentV4`.
3. `AgentV4.run(query)` handles either:
   - mode command (`/mode`, `/mode 2`, `/mode semantic`, etc.)
   - retrieval query in current mode

## Runtime components
- `core.main`
  - prints banner, command help, and runs REPL loop
- `core.agent_v4.AgentV4`
  - mode management
  - retrieval orchestration
  - lazy semantic engine initialization
- `core.query_router.QueryRouter`
  - stores current `SearchMode`
- `core.search_mode.SearchMode`
  - enum: `chat`, `keyword`, `semantic`, `hybrid`
- `core.hybrid_search.HybridSearch`
  - combines engine outputs (currently keyword-weighted behavior)

## Retrieval stack
- Keyword:
  - `nlp.keyword_search.KeywordEngine`
  - `DocumentCorpus` + `TFIDF`
- Semantic:
  - `nlp.embedding_search.EmbeddingSearch`
  - `nlp.embedding_model.EmbeddingModel`
  - `sentence_transformers` backend
- Hybrid:
  - `HybridSearch.search(query, keyword_engine, semantic_engine)`

## Knowledge base integration
- `AgentV4` loads sections from `data.knowledge_base`.
- Each section is indexed into keyword search at startup.
- Semantic embeddings are built lazily when semantic/hybrid mode is activated.
"""

SETUP_AND_RUN_DOCS = """
# Setup And Run Docs

## Prerequisites
- Python 3.12+
- `uv` installed

## Setup
1. `cd C:/pocs/notes/ai/projects/agent`
2. `uv sync`

## Run
- Script:
  - `uv run core-agent`
- Module:
  - `uv run --with . python -m core.main`

## CLI commands
- `/mode`
  - show numbered mode menu
- `/mode 1|2|3|4`
  - switch mode directly by number
- `/mode <name>`
  - switch by mode name (`chat|keyword|semantic|hybrid`)
- `exit`
  - quit app

## First-run note for semantic mode
- First semantic usage may download model artifacts (`all-MiniLM-L6-v2`).
- Initial semantic mode activation can be slower than keyword/chat mode.
"""

CODE_MAP_DOCS = """
# Code Map Docs

## `src/core`

### `core/main.py`
- Active CLI entrypoint.
- Prints banner and command help.
- Uses `AgentV4`.

### `core/agent_v4.py`
- Primary runtime agent.
- Features:
  - `/mode` menu and direct selection
  - mode-by-index and mode-by-name parsing
  - lazy semantic engine startup
  - retrieval dispatch by current mode

### `core/query_router.py`
- `QueryRouter` stores and updates active `SearchMode`.

### `core/search_mode.py`
- Enum values:
  - `chat`
  - `keyword`
  - `semantic`
  - `hybrid`

### `core/hybrid_search.py`
- Hybrid retrieval combiner.
- Calls keyword and semantic engines.
- Returns ranked `(document, score)` list.

### `core/agent.py`
- Legacy/simple study agent path.
- Uses keyword search and canned responses.
- Not the default CLI path anymore.

### `core/models.py`
- `Task` dataclass for legacy/simple agent flow.

## `src/nlp`

### `nlp/keyword_search.py`
- Primary keyword engine.
- Exposes:
  - `KeywordEngine` (primary)
  - `KeywordSearch` alias
  - `SearchEngine` legacy alias

### `nlp/keyword_engine.py`
- Compatibility shim re-exporting symbols from `keyword_search`.

### `nlp/tfidf.py`
- TF-IDF math and query/document scoring.

### `nlp/document_corpus.py`
- In-memory document store.

### `nlp/embedding_model.py`
- `SentenceTransformer` wrapper.
- Uses model: `all-MiniLM-L6-v2`.

### `nlp/embedding_search.py`
- Builds embedding index and cosine-similarity search.
- Provides `semantic_search(query)` alias.

### `nlp/pipeline.py`, `text_processor.py`, `tokenzier.py`, `tokenizer_engine.py`, `vocabulary.py`, `bag_of_words.py`, `frequency_analyzer.py`
- Token pipeline and lexical feature utilities.
"""

TESTING_DOCS = """
# Testing Docs

## Test files in `src/tests`
- `test_agent.py`
- `test_agent_v4_mode.py`
- `test_bag_of_words.py`
- `test_embedding_model.py`
- `test_frequency_analyzer.py`
- `test_keyword_search.py`
- `test_term_frequency.py`
- `test_tokenizer.py`
- `test_tokenizer_engine.py`
- `test_vocabulary.py`
- `text_processor.py` (not auto-collected; filename does not start with `test_`)

## Main test command
- `uv run pytest -q src/tests`

## Validation commands
- Compile check:
  - `uv run python -m py_compile src/core/agent_v4.py src/core/main.py src/nlp/embedding_model.py src/nlp/embedding_search.py`
- Whole source compile check:
  - `uv run python -m compileall -q src`

## Current expected status
- Full suite should pass in this project environment.
- Semantic tests may take longer on first run due model initialization/download.
"""

DEBUGGING_DOCS = """
# Debugging Docs

## Fast debugging workflow
1. `cd C:/pocs/notes/ai/projects/agent`
2. `uv sync`
3. `uv run pytest -q src/tests`
4. `uv run core-agent`
5. Reproduce with targeted inputs (`/mode`, `/mode 2`, query text)

## Mode debugging
- Check mode list:
  - `/mode`
- Set mode numerically:
  - `/mode 1`
  - `/mode 2`
  - `/mode 3`
  - `/mode 4`
- Set mode by name:
  - `/mode keyword`
- Backward compatibility:
  - `mode keyword` is still accepted

## Retrieval debugging
- Keyword issues:
  - inspect `KeywordEngine.search` results and scores
- Semantic issues:
  - validate embedding model can initialize
  - validate document embeddings are present
- Hybrid issues:
  - inspect both keyword and semantic outputs before combine

## Import/path debugging
- Confirm running from project root.
- Confirm `pythonpath = ["src"]` behavior under pytest.
- After renames, run:
  - `rg -n "keyword_engine|keyword_search|search_engine|study_agent|score" src README.md pyproject.toml`
"""

KNOWN_ISSUES_DOCS = """
# Known Issues Docs

## Active issues and risks

### 1) Hybrid scoring behavior is still simplistic
- `HybridSearch` currently computes semantic results but does not blend semantic
  scores into ranking logic.
- Effective behavior is close to keyword-only ranking.

### 2) Semantic mode startup can fail in constrained environments
- First semantic run may require model download/network.
- If model initialization fails, `AgentV4` falls back safely and returns a
  semantic-unavailable message.

### 3) Windows Hugging Face cache warnings
- On Windows, symlink limitations can trigger hub warnings.
- This is non-fatal but may use more disk space.

### 4) `tokenzier.py` filename typo coupling
- Renaming this file without synchronized import updates will break pipeline/tests.

### 5) Keyword compatibility shim debt
- `nlp/keyword_engine.py` is kept for backward compatibility.
- Remove only after all imports rely solely on `nlp.keyword_search`.
"""

RETRIEVAL_NOTES_DOCS = """
# Retrieval Notes Docs

## Current behavior and limitation
- Retrieval in this project is still largely pattern/keyword driven.
- When documents are too large, top matches can be broad and less precise.

## Why smaller nodes improve accuracy
- Smaller section-level nodes reduce topic mixing.
- Query-to-node matching becomes more focused (higher precision).
- Returned answers are shorter and more relevant to the intent.

## Current implementation choice
- `AgentV4` now indexes section-level nodes built from each knowledge-base doc.
- Node splitting is based on `##` section boundaries.
- Retrieved node output is further narrowed by section scoring in
  `_extract_relevant_section`.

## Next improvements (optional)
- Add overlap-aware chunking for long sections.
- Add metadata tags (`doc_name`, `section_name`) to each node.
- Re-rank top-k nodes with semantic+keyword fusion.
- Add confidence thresholds before returning a section directly.
"""

MAINTENANCE_DOCS = """
# Maintenance Docs

## Refactor checklist
1. Rename/move module.
2. Update imports with `rg`.
3. Run targeted tests.
4. Run full tests.
5. Run compile checks.
6. Update these docs immediately after behavior changes.

## Release readiness checklist
- `uv run pytest -q src/tests` passes.
- `uv run core-agent` starts and `/mode` flow works.
- Semantic mode can be activated (or failure path is clearly handled).
- No syntax errors from `uv run python -m compileall -q src`.
- README and `pyproject.toml` entrypoint match runtime reality.

## Useful grep commands
- `rg -n "keyword_engine|keyword_search|search_engine" src`
- `rg -n "study_agent|score" src README.md pyproject.toml`
- `rg -n "^from |^import " src`
"""

KNOWLEDGE_BASE_INDEX_DOCS = """
# Knowledge Base Index

- `project_overview_docs`
- `architecture_docs`
- `setup_and_run_docs`
- `code_map_docs`
- `testing_docs`
- `debugging_docs`
- `known_issues_docs`
- `retrieval_notes_docs`
- `maintenance_docs`

Use `get_knowledge_base()` to fetch all sections as a dictionary.
"""


KNOWLEDGE_BASE: dict[str, str] = {
    "project_overview_docs": PROJECT_OVERVIEW_DOCS,
    "architecture_docs": ARCHITECTURE_DOCS,
    "setup_and_run_docs": SETUP_AND_RUN_DOCS,
    "code_map_docs": CODE_MAP_DOCS,
    "testing_docs": TESTING_DOCS,
    "debugging_docs": DEBUGGING_DOCS,
    "known_issues_docs": KNOWN_ISSUES_DOCS,
    "retrieval_notes_docs": RETRIEVAL_NOTES_DOCS,
    "maintenance_docs": MAINTENANCE_DOCS,
    "knowledge_base_index_docs": KNOWLEDGE_BASE_INDEX_DOCS,
}


def get_knowledge_base() -> dict[str, str]:
    """Return all knowledge-base sections."""
    return dict(KNOWLEDGE_BASE)
