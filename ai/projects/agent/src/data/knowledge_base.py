"""
Central project knowledge base for the `agent` repository.

These strings are indexed by AgentV4 and returned through retrieval modes.
Keep this file aligned with README.md and runtime behavior whenever code changes.
"""

PROJECT_OVERVIEW_DOCS = """
# Project Overview Docs

## Repository Identity
- Relative root: `ai/projects/agent`
- Package name: `agent`
- Version: `0.1.0`
- Python requirement: `>=3.12`
- Packaging style: src-layout (`src/`)
- Build backend: `setuptools.build_meta`
- CLI entrypoint: `core-agent -> core.main:main`

## Primary Purpose
- Runs a CLI study assistant over an internal documentation corpus.
- Supports multiple retrieval strategies over that corpus.
- Returns focused section answers (not full document dumps) for user queries.

## Search Modes
- `chat`
  - placeholder conversational mode, no LLM backend connected.
- `keyword`
  - TF-IDF style lexical scoring using local in-memory documents.
- `semantic`
  - embedding-based similarity using `sentence-transformers`.
- `hybrid`
  - keyword + semantic pipeline path (currently ranking is keyword-dominant).

## Runtime Entry Points
- Shell script entry:
  - `uv run core-agent`
- Python module entry:
  - `uv run --with . python -m core.main`
- Direct file execution (`python src/core/main.py`) is not recommended for src-layout imports.

## Project State Snapshot (June 11, 2026)
- Main runtime class: `core.agent_v4.AgentV4`
- Internal documentation source: `src/data/knowledge_base.py`
- Test suite status observed in this repository: 14 passed, 0 failed
- Known technical debt:
  - mode order mismatch between startup banner text and runtime mode map
  - typo-coupled filename `tokenzier.py`
  - hybrid ranking path does not blend semantic scores into final score yet
"""

ARCHITECTURE_DOCS = """
# Architecture Docs

## High-Level Architecture
- Interface layer
  - `core/main.py`: CLI loop and user IO
- Orchestration layer
  - `core/agent_v4.py`: mode handling, retrieval dispatch, section extraction
- Routing/state layer
  - `core/query_router.py`, `core/search_mode.py`
- Retrieval engines
  - Keyword: `nlp/keyword_search.py` + `nlp/tfidf.py`
  - Semantic: `nlp/embedding_search.py` + `nlp/embedding_model.py`
  - Hybrid: `core/hybrid_search.py`
- Data source layer
  - `data/knowledge_base.py` static markdown docs

## Request Lifecycle
1. User runs `uv run core-agent`.
2. `core.main.main()` creates `AgentV4`.
3. `AgentV4.__init__` loads docs from `knowledge_base.py`.
4. Docs are split into section nodes and indexed into keyword engine.
5. For each user query, `AgentV4.run()` performs:
   - mode command handling (`/mode`, `mode <name>`) or
   - retrieval in active mode.
6. Top document candidate is selected.
7. Best section inside that document is extracted and returned.

## Internal Data Flow
- Knowledge docs (`str`) -> split into section nodes (`list[str]`) -> added to keyword corpus.
- Query (`str`) -> normalized retrieval query -> engine result list (`list[(doc, score)]`).
- Top-k results -> heuristic rerank in `_select_best_document`.
- Final doc -> `_extract_relevant_section` -> response section text.

## Mode and State Model
- Mode enum values: `chat`, `keyword`, `semantic`, `hybrid`
- Default mode: `chat`
- Router owner: `QueryRouter`
- Mode selection supports:
  - numeric (`/mode 1..4`)
  - name (`/mode keyword`, etc.)
  - follow-up single token after menu prompt

## Semantic Initialization Strategy
- Semantic engine is lazily initialized.
- Triggered when mode changes to `semantic` or `hybrid` (or when running those paths).
- On initialization failure, the agent returns a safe error message and stays/falls back to keyword mode.

## Section-Level Response Strategy
- Docs are split by markdown `##` headers.
- Agent tries to return only the most relevant section.
- Heuristic boosts prioritize run/setup/mode/test/debug intent tokens.
- This keeps responses focused and reduces irrelevant long outputs.
"""

SETUP_AND_RUN_DOCS = """
# Setup And Run Docs

## Prerequisites
- Python 3.12+
- `uv` installed and available in PATH

## Setup
1. `cd ai/projects/agent`
2. `uv sync`

## Run Commands
- Recommended:
  - `uv run core-agent`
- Alternative:
  - `uv run --with . python -m core.main`
- Not recommended:
  - `python src/core/main.py`

## CLI Commands
- `/mode`
  - show mode menu and current mode
- `/mode 1|2|3|4`
  - select mode by index
- `/mode <name>`
  - select by name (`chat|keyword|semantic|hybrid`)
- `mode <name>`
  - backward-compatible syntax
- `exit`
  - quit app

## Mode Index Source Of Truth
`AgentV4.MODE_BY_INDEX` currently maps:
- `1 -> chat`
- `2 -> keyword`
- `3 -> semantic`
- `4 -> hybrid`

Important note:
- Startup banner in `core/main.py` currently shows a different numbering order.
- Runtime behavior follows `AgentV4.MODE_BY_INDEX` and `/mode` menu output.

## First Semantic Run Notes
- `sentence-transformers` model initialization can take extra time on first usage.
- If model artifacts are unavailable or init fails, agent returns semantic-unavailable message.

## Quick Sanity Run
1. Launch: `uv run core-agent`
2. Ask menu: `/mode`
3. Switch keyword: `/mode 2`
4. Query: `How to start this application ?`
5. Exit: `exit`
"""

CODE_MAP_DOCS = """
# Code Map Docs

## Folder Structure (Detailed)

```text
ai/projects/agent/
  README.md
  pyproject.toml
  uv.lock
  src/
    __init__.py
    core/
      __init__.py
      main.py
      agent_v4.py
      agent.py
      hybrid_search.py
      models.py
      query_router.py
      search_mode.py
    data/
      __init__.py
      knowledge_base.py
    nlp/
      __init__.py
      bag_of_words.py
      document_corpus.py
      document_stats.py
      embedding_model.py
      embedding_search.py
      frequency_analyzer.py
      keyword_engine.py
      keyword_search.py
      pipeline.py
      stopword.py
      text_processor.py
      tfidf.py
      tokenizer_engine.py
      tokenzier.py
      vocabulary.py
    tests/
      test_agent.py
      test_agent_v4_mode.py
      test_bag_of_words.py
      test_embedding_model.py
      test_frequency_analyzer.py
      test_keyword_search.py
      test_term_frequency.py
      test_tokenizer.py
      test_tokenizer_engine.py
      test_vocabulary.py
      text_processor.py
```

## Root Files: What Each File Does
- `README.md`
  - human-facing main project documentation.
- `pyproject.toml`
  - package metadata, dependencies, script entrypoint, pytest pythonpath setup.
- `uv.lock`
  - dependency lock file for reproducible installs in this environment.

## `src/` Package Root
- `src/__init__.py`
  - package marker; currently empty.

## `src/core` Package: File-by-File
- `src/core/__init__.py`
  - package marker with short docstring.

- `src/core/main.py`
  - CLI executable entrypoint.
  - Responsibilities:
    - creates `AgentV4`
    - prints startup banner
    - runs REPL loop
    - handles blank input and `exit`
    - sends all other input to `agent.run()`
  - Important behavior:
    - banner mode numbering currently differs from runtime mapping.

- `src/core/agent_v4.py`
  - primary runtime orchestrator.
  - Responsibilities:
    - mode parsing and state transitions
    - mode menu and awaiting-followup logic
    - lazy semantic engine initialization
    - knowledge docs loading and node splitting
    - query normalization for retrieval
    - document reranking heuristics
    - section-level extraction for focused answers
  - Key attributes:
    - `MODE_BY_INDEX`, `MODE_BY_NAME`
    - `RETRIEVAL_FILLER_TOKENS`
    - `documents`, `nodes`, `keyword_engine`, `semantic_engine`
  - Key methods:
    - `_split_document_into_nodes`: splits by `##` headers
    - `_ensure_semantic_engine`: guarded semantic bootstrapping
    - `_select_best_document`: intent-aware rerank over top-k
    - `_extract_relevant_section`: section-level narrowing

- `src/core/agent.py`
  - legacy `StudyAgent` implementation.
  - Uses tokenizer/bag-of-words and canned responses for simple queries.
  - Includes old `search` behavior with hardcoded sample documents.
  - Still tested by `test_agent.py`, but not the default CLI path.

- `src/core/hybrid_search.py`
  - hybrid retrieval combiner.
  - Current behavior:
    - computes both keyword and semantic result sets
    - only keyword scores are merged into `combined` ranking
    - semantic scores are currently unused in final ranking
  - Technical debt:
    - parameter typo name: `sematic_engine`

- `src/core/models.py`
  - simple dataclass models.
  - `Task` dataclass wraps `query: str` for legacy agent path.

- `src/core/query_router.py`
  - runtime mode state container.
  - `set_mode` converts input string to `SearchMode` enum.

- `src/core/search_mode.py`
  - enum definitions for supported modes.
  - Source of canonical mode string values.

## `src/data` Package
- `src/data/__init__.py`
  - package marker; currently empty.

- `src/data/knowledge_base.py`
  - internal retrievable docs used by `AgentV4`.
  - Exposes constants for documentation sections.
  - Exposes `KNOWLEDGE_BASE` dict and `get_knowledge_base()` accessor.

## `src/nlp` Package: File-by-File
- `src/nlp/__init__.py`
  - package marker; currently empty.

- `src/nlp/pipeline.py`
  - `NLPPipeline` composition object.
  - Flow: normalize -> tokenize -> stopword removal.
  - Imports tokenizer from `tokenzier.py` (typo-coupled module name).

- `src/nlp/tokenzier.py`
  - minimal whitespace tokenizer.
  - `Tokenizer.tokenize(text) -> list[str]`.

- `src/nlp/text_processor.py`
  - normalization and stopword filtering.
  - `normalize`: lowercase, punctuation strip, trim.
  - `remove_stopwords`: filters against `STOP_WORDS`.

- `src/nlp/stopword.py`
  - small static stopword set used by pipeline.

- `src/nlp/document_corpus.py`
  - in-memory document list abstraction.
  - add/get/count methods.

- `src/nlp/tfidf.py`
  - lexical scoring core.
  - Implements:
    - term frequency
    - inverse document frequency
    - per-document vector construction
    - query vs document score aggregation
  - Depends on `NLPPipeline` for tokenization/normalization.

- `src/nlp/keyword_search.py`
  - keyword retrieval engine.
  - `KeywordEngine` stores corpus + TFIDF object.
  - Methods:
    - `add_document`
    - `search`
    - `keyword_search` (alias wrapper)
  - Backward aliases:
    - `SearchEngine = KeywordEngine`
    - `KeywordSearch = KeywordEngine`

- `src/nlp/keyword_engine.py`
  - compatibility shim.
  - Re-exports `KeywordEngine`, `KeywordSearch`, `SearchEngine` from `keyword_search`.

- `src/nlp/embedding_model.py`
  - wraps `SentenceTransformer("all-MiniLM-L6-v2")`.
  - `embed(text)` returns numpy vector.

- `src/nlp/embedding_search.py`
  - semantic retrieval implementation.
  - Maintains parallel arrays for documents and embeddings.
  - Computes cosine similarity and sorted ranking.
  - `semantic_search` is alias to `search`.

- `src/nlp/frequency_analyzer.py`
  - token frequency helper using `Counter`.
  - supports `count_tokens` and `most_common`.

- `src/nlp/bag_of_words.py`
  - bag-of-words feature extractor.
  - Uses `NLPPipeline` + `FrequencyAnalyzer`.

- `src/nlp/tokenizer_engine.py`
  - token-ID encoding/decoding helper.
  - Cleans text and maps tokens through `Vocabulary`.

- `src/nlp/vocabulary.py`
  - dynamic token<->id mapping.
  - Supports incremental vocab growth and decode fallback.
  - Contains default decode fallback for ids 0 and 1.

- `src/nlp/document_stats.py`
  - simple token metrics helper (`word_count`, `unique_words`).
  - currently standalone and not wired into main runtime path.

## `src/tests` Package: File-by-File
- `src/tests/test_agent_v4_mode.py`
  - mode menu text expectations
  - numeric mode switching assertions
  - retrieval focus assertion for start/run query

- `src/tests/test_agent.py`
  - legacy `StudyAgent` response tests for python/ai prompts.

- `src/tests/test_keyword_search.py`
  - keyword search ranking sanity check.

- `src/tests/test_embedding_model.py`
  - embedding vector generation basic check.

- `src/tests/test_bag_of_words.py`
  - bag-of-words token count output check.

- `src/tests/test_frequency_analyzer.py`
  - token frequency counting check.

- `src/tests/test_term_frequency.py`
  - TF term frequency math checks.

- `src/tests/test_tokenizer.py`
  - whitespace tokenizer output check.

- `src/tests/test_tokenizer_engine.py`
  - token id encode/decode deterministic flow check.

- `src/tests/test_vocabulary.py`
  - encode/decode mapping checks.

- `src/tests/text_processor.py`
  - contains a test-like function but filename does not start with `test_`.
  - not auto-collected by default pytest discovery patterns.
"""

TESTING_DOCS = """
# Testing Docs

## Core Commands
- Full suite:
  - `uv run pytest -q src/tests`
- Targeted mode logic:
  - `uv run pytest -q src/tests/test_agent_v4_mode.py`
- Targeted embedding smoke:
  - `uv run pytest -q src/tests/test_embedding_model.py`
- Compile check:
  - `uv run python -m compileall -q src`

## Current Observed Status (June 11, 2026)
- Test files under `src/tests`: 11 files
- Auto-collected test files: 10 (`text_processor.py` not auto-collected)
- Total executed tests observed: 14
- Status observed: 14 passed, 0 failed

## Coverage Characteristics
- Strongest coverage:
  - mode switching and menu formatting
  - basic keyword/embedding/tokenization paths
- Gaps:
  - no explicit assertions for hybrid semantic score blending
  - no tests validating banner numbering consistency with runtime mapping
  - no integration tests across very large doc corpora
  - no tests for semantic init failure simulation path

## Practical Regression Watchlist
- Start/run query should return section containing `## Run` and `uv run core-agent`.
- `/mode 2` should map to keyword mode based on `AgentV4.MODE_BY_INDEX`.
- Renaming `tokenzier.py` without import updates breaks tests/runtime.
"""

DEBUGGING_DOCS = """
# Debugging Docs

## Fast Debug Workflow
1. `cd ai/projects/agent`
2. `python --version`
3. `uv --version`
4. `uv sync`
5. `uv run pytest -q src/tests`
6. `uv run core-agent`
7. Reproduce with minimal input and mode-specific steps.

## Troubleshooting Matrix (Detailed)

### Environment and Tooling
1) `uv: command not found`
- Cause: uv missing or not in PATH.
- Fix: install uv, reopen shell, rerun `uv sync`.

2) Python version mismatch (`>=3.12` required)
- Cause: old interpreter.
- Fix: switch to Python 3.12+, recreate env, rerun sync.

3) `VIRTUAL_ENV ... does not match ... .venv`
- Cause: another venv already active.
- Impact: warning, but can cause confusion over installed packages.
- Fix: deactivate foreign venv and prefer `uv run ...` commands.

### Import and Entry Errors
4) `ModuleNotFoundError` for `core`/`nlp`
- Cause: direct script execution in src-layout.
- Fix: use `uv run core-agent` or `python -m core.main` through uv.

5) Import errors after tokenizer rename
- Cause: code imports `nlp.tokenzier`; rename not fully propagated.
- Debug command: `rg -n "tokenzier|tokenizer" src`
- Fix: update imports atomically before/with rename.

### CLI and Mode Routing
6) Invalid mode selection responses
- Signatures:
  - `Invalid mode selection.`
  - `Please choose 1, 2, 3, 4 ...`
- Cause: unsupported index/name or malformed input.
- Fix: run `/mode`, then choose valid index/name.

7) Banner mode order confusion
- Cause: banner text order differs from runtime mapping.
- Fix now: trust `/mode` menu and `MODE_BY_INDEX` map.
- Long-term fix: align `main.py` banner labels with runtime map.

### Retrieval Relevance and Result Shape
8) `No keyword results found.`
- Cause: empty corpus, token mismatch, or query normalization side effects.
- Checkpoints:
  - verify `AgentV4.__init__` loaded docs
  - verify nodes were added to keyword engine
  - test exact phrase from docs

9) `No semantic results found.`
- Cause: semantic index empty or no valid embeddings loaded.
- Checkpoints:
  - ensure `_ensure_semantic_engine` succeeded
  - ensure `add_document` ran for nodes

10) `Semantic mode is currently unavailable (...) Staying in keyword mode.`
- Cause: exception while constructing semantic engine/model.
- Typical reasons:
  - model initialization/download issue
  - dependency/runtime incompatibility
- Fix path:
  - run `uv run pytest -q src/tests/test_embedding_model.py`
  - inspect exception string in agent response

11) Start intent returns wrong section (regression pattern)
- Repro flow:
  - `/mode 2`
  - `How to start this application ?`
- Expected pattern:
  - contains `## Run`
  - contains `uv run core-agent`
- Debug focus:
  - `_normalize_query_for_retrieval`
  - `_select_best_document`
  - `_extract_relevant_section`
  - run mode-specific test file

12) Hybrid seems keyword-only
- Cause:
  - `hybrid_search.py` computes semantic results but does not merge semantic scores.
- Debug:
  - inspect `combined` dict building logic in hybrid search.
- Fix direction:
  - normalize keyword and semantic score scales
  - weighted fusion and rerank

### Data and NLP Component Issues
13) Unexpected stopword filtering
- Cause: small stopword list may remove intended tokens.
- File: `nlp/stopword.py`
- Fix: adjust stopword list and rerun token/pipeline tests.

14) Vocabulary decode surprises (`<UNK>` or defaults)
- Cause: decode for unseen ids uses defaults (`hello`/`world`) then `<UNK>` fallback.
- File: `nlp/vocabulary.py`
- Fix: align decode policy with expected behavior before expanding usage.

15) Performance slow with larger corpora
- Cause:
  - TF-IDF is computed per query per document without persistent vector cache
  - semantic embeddings are generated eagerly when docs added
- Mitigations:
  - precompute/cached vectors
  - chunk pruning/top-k narrowing before expensive phases

## Layered Debug Isolation
- Layer 1: CLI and IO
  - file: `core/main.py`
- Layer 2: mode routing and behavior
  - files: `core/agent_v4.py`, `core/query_router.py`, `core/search_mode.py`
- Layer 3: keyword retrieval
  - files: `nlp/keyword_search.py`, `nlp/tfidf.py`, `nlp/document_corpus.py`
- Layer 4: semantic retrieval
  - files: `nlp/embedding_model.py`, `nlp/embedding_search.py`
- Layer 5: data corpus content
  - file: `data/knowledge_base.py`
"""

KNOWN_ISSUES_DOCS = """
# Known Issues Docs

## Active Issues and Risks

1) Mode numbering inconsistency
- `core/main.py` banner shows a mode order that differs from `AgentV4.MODE_BY_INDEX`.
- User confusion risk when selecting by numbers from banner instead of `/mode` menu.

2) Hybrid score fusion incomplete
- Semantic results are computed in hybrid path but not included in final combined score.
- Current hybrid ranking behaves close to keyword-only.

3) Typo-coupled module name
- `nlp/tokenzier.py` misspelling is part of current import graph.
- Any rename must include synchronized import updates.

4) Thin stopword list design risk
- `STOP_WORDS` is minimal and static.
- Retrieval quality can vary for broader natural-language prompts.

5) Legacy path still present
- `core/agent.py` and `core/models.py` remain for legacy tests/use.
- Not default runtime path but still part of maintenance surface.

6) `tests/text_processor.py` is not auto-collected
- File name does not match pytest default `test_*.py` pattern.
- Can cause false assumption that all test-like functions are executed.

7) Semantic initialization dependency sensitivity
- `sentence-transformers` runtime and model availability can fail in constrained environments.
"""

RETRIEVAL_NOTES_DOCS = """
# Retrieval Notes Docs

## Node Construction Strategy
- Agent ingests docs as large markdown blocks.
- `_split_document_into_nodes` splits each doc by `##` section headers.
- Each node is prefixed with parent `#` doc title.

## Query Normalization
- `_normalize_query_for_retrieval` removes filler tokens:
  - examples: `how`, `what`, `the`, `please`, `should`
- If all tokens are removed, original query is retained.

## Document Selection Heuristics
- Base score comes from engine result score.
- Additional boosts in `_select_best_document` for intent tokens:
  - run/setup intent boosts
  - test intent boosts
  - mode/command boosts
  - debug/issue boosts
- Top-k considered currently: first 5 engine results.

## Section Selection Heuristics
- `_extract_relevant_section` scores each `##` section with token overlap.
- Title matches are weighted stronger than content matches.
- Additional boosts for run/setup/mode/test intent mapping.

## Keyword Retrieval Characteristics
- Per-query scoring over full corpus.
- Uses TF-IDF computed from current in-memory corpus.
- Deterministic for same corpus and query.

## Semantic Retrieval Characteristics
- Embeddings generated using `all-MiniLM-L6-v2`.
- Cosine similarity ranking over stored embeddings.
- First semantic use includes model boot cost.

## Hybrid Retrieval Characteristics
- Currently computes both keyword and semantic results.
- Final ranking only reflects keyword score accumulation.
- Semantic list is currently unused in final `combined` dict.

## Quality and Precision Considerations
- Very large sections can dilute relevance.
- Section-level nodes improve precision vs full-document indexing.
- Heuristic tuning impacts run/setup style queries significantly.
"""

MAINTENANCE_DOCS = """
# Maintenance Docs

## Change Checklist (Code + Docs)
1. Implement the code change.
2. Update `README.md` for user-facing behavior changes.
3. Update `data/knowledge_base.py` for retrievable in-app docs.
4. Run test suite and compile checks.
5. Verify mode flow manually (`/mode`, numeric and named switching).
6. Confirm no stale imports/aliases after refactors.

## Validation Commands
- `uv run pytest -q src/tests`
- `uv run python -m compileall -q src`
- `uv run pytest -q src/tests/test_agent_v4_mode.py`

## Refactor-Safe Grep Commands
- `rg -n "tokenzier|tokenizer" src`
- `rg -n "KeywordEngine|KeywordSearch|SearchEngine" src`
- `rg -n "MODE_BY_INDEX|SearchMode|/mode" src/core`
- `rg -n "EmbeddingSearch|EmbeddingModel|semantic" src`

## Documentation Synchronization Rule
- If runtime behavior changes, update docs in same change set.
- Keep section headings stable when possible so retrieval heuristics continue to work.
- Preserve critical headings used by intent/ranking logic:
  - `## Run Commands`
  - `## Setup`
  - `## CLI Commands`
  - `## Testing Docs`

## Safe Modernization Backlog
1. Align banner mode numbering with runtime mode map.
2. Implement true hybrid score fusion.
3. Decide and execute `tokenzier.py` rename migration plan.
4. Strengthen tests for semantic failure paths.
5. Add collection-safe name for `tests/text_processor.py` if intended for execution.
"""

KNOWLEDGE_BASE_INDEX_DOCS = """
# Knowledge Base Index

Available sections in `KNOWLEDGE_BASE`:
- `project_overview_docs`
- `architecture_docs`
- `setup_and_run_docs`
- `code_map_docs`
- `testing_docs`
- `debugging_docs`
- `known_issues_docs`
- `retrieval_notes_docs`
- `maintenance_docs`
- `knowledge_base_index_docs`

Primary lookup function:
- `get_knowledge_base() -> dict[str, str]`
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
