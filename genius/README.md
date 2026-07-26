# Genius learning chatbot

Genius is a Streamlit retrieval-augmented chatbot for every supported document under the
repository's `learnings` directory. It uses the local open-source `BAAI/bge-m3` model for retrieval
embeddings and Gemini Flash chat models for answer generation. Search can run in the current
Streamlit process or in Upstash Vector.

Supported documents are Markdown, plain text, reStructuredText, PDF, and DOCX files. Virtual
environments, dependency folders, caches, hidden directories, and zero-byte files are excluded.

## Setup

Python 3.12 or newer is required.

```powershell
cd C:\pocs\notes\genius
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e .
streamlit run app.py
```

The existing `.env` file must contain:

```dotenv
GEMINI_API_KEY=your-gemini-api-key
UPSTASH_VECTOR_REST_URL=https://your-index-url.upstash.io
UPSTASH_VECTOR_REST_TOKEN=your-upstash-token
```

The Upstash Vector index must use 1,024 dimensions and cosine distance. The in-memory backend only
requires `GEMINI_API_KEY`. The sidebar can reindex the in-memory store, Upstash Vector, or both in a
single embedding pass. Upstash indexing uses deterministic vector IDs, so reindexing updates
existing chunks instead of duplicating them.

From the repository root, use the synchronized project environment to embed the corpus into both
stores and start the UI:

```powershell
uv run --project genius streamlit run genius/app.py -- --index-both
```

On later starts, this command rebuilds only the process-local in-memory index and reuses Upstash
when it already contains vectors. Upstash is changed again only when it is empty or when you choose
an Upstash reindex target in the UI and click **Reindex learnings**.

BGE-M3 embedding batches and model files are cached under `genius/.cache`, so they are downloaded
and generated only once. Upstash vectors are isolated in the `local-bge-m3` namespace.

Responses support Markdown, highlighted fenced code blocks, tables, inline code, Graphviz/DOT
diagrams, and LaTeX blocks. Before each answer, the activity panel shows query embedding, vector
search, chunk reading, context preparation, and response-generation progress. Retrieved files and
similarity scores are shown below each answer.

## Quality checks

```powershell
python -m pip install -e ".[dev]"
ruff format --check .
ruff check .
pyright app.py genius_app/rag.py
bandit -c pyproject.toml -r app.py genius_app/rag.py
python -m pytest
```
