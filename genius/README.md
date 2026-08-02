# Genius Learning RAG

Genius is a local-first learning chat application built with Next.js, pnpm,
FastAPI, uv, self-hosted BGE-M3 retrieval, and optional Upstash Vector retrieval.

## Features

- Learning chat grounded in Markdown under the sibling learnings directory
- Selectable local hybrid RAG or Upstash Vector RAG
- Heading-aware chunks, BM25 plus dense retrieval, and local cross-encoder reranking
- Technical tutor with written-answer and interactive-MCQ practice
- Random DSA challenges and Monaco templates for C++, Java, Python, Go, and Rust
- Streaming learning chat with cited sources and local SQLite conversation history
- Server-side Gemini, Cerebras, and Groq provider selection
- Local SQLite chat and study-history persistence

## Credentials

Copy .env.example to .env and set only the provider credentials you intend to
use. Never commit .env or real keys.

| Variable | Purpose |
| --- | --- |
| GEMINI_API_KEY | Google Gemini chat provider |
| CEREBRAS_API_KEY | Cerebras chat provider |
| GROQ_API_KEY | Groq chat provider |
| UPSTASH_VECTOR_REST_URL | Optional Upstash Vector endpoint |
| UPSTASH_VECTOR_REST_TOKEN | Optional Upstash Vector token |
| UPSTASH_REDIS_REST_URL | Upstash Redis HTTPS endpoint for the coding-question CLI |
| UPSTASH_REDIS_REST_TOKEN | Upstash Redis token for the coding-question CLI |

BGE-M3 and the cross-encoder run locally in the RAG container and need no
external embedding API key. The first startup downloads model weights into the
rag-model-cache Docker volume. MODEL_CACHE_DIR is passed directly to both
model loaders and defaults to the persistent /models Docker volume.

Upstash is optional. When enabled, Genius records the chunk IDs it owns under
LOCAL_INDEX_DIR and deletes IDs that disappear on later reindexes. It never
blindly deletes unknown vectors from the configured namespace; unknown stale
results are discarded before citations are created. Use a dedicated Upstash
namespace for Genius so retained vectors from another application cannot crowd
out retrieval results.

## Run

1. Install Docker Desktop, pnpm, and uv for host development.
2. Copy .env.example to .env and add at least one chat-provider key.
3. Run docker compose up --build from this directory.
4. Open http://localhost:3000.

The RAG API rebuilds indexes at startup from indexable Markdown files in the
sibling learnings directory. It excludes dependency, VCS, and build folders.

For host-only development, run `uv sync --group dev` and
`uv run uvicorn app.main:app --port 8000` from `services/rag-api`, then create
a local uncommitted environment file with RAG_API_URL=http://localhost:8000 and
DATABASE_URL=file:./data/genius.sqlite before running pnpm dev.

## Use

- Learn: choose a provider/model and Local or Upstash RAG, optionally select
  folders and Markdown files from the full tree, then ask a question. Responses
  stream with file and heading citations.
- Tutor: choose a topic and files, then start a five-question written-answer
  or interactive-MCQ session. Each answer receives a critique and a 1-5 rating.
- Code review: start a random DSA prompt, choose one of the five supported
  languages, and submit code for an LLM-only review. Submitted code is not run.

## Coding question CLI

See [scripts/README.md](scripts/README.md) for the complete command reference
for every repository script.

The standalone CLI reads `UPSTASH_REDIS_REST_URL` and
`UPSTASH_REDIS_REST_TOKEN` from the process environment or the uncommitted
`genius/.env` file. Existing environment variables take precedence. Run these
commands from the Genius directory:

```text
uv run --project services/rag-api python scripts/coding_question.py migrate
uv run --project services/rag-api python scripts/coding_question.py migrate --apply

uv run --project services/rag-api python scripts/coding_question.py get --id <uuid>
uv run --project services/rag-api python scripts/coding_question.py list --offset 0 --limit 100
uv run --project services/rag-api python scripts/coding_question.py query --company Anduril --topic Array --difficulty Medium
uv run --project services/rag-api python scripts/coding_question.py query --title "Game of Life"
uv run --project services/rag-api python scripts/coding_question.py random --topic Graph --count 5
```

`migrate` only reads and validates the legacy source string and performs no
writes.
`migrate --apply` builds and verifies the hash and indexes, then atomically
moves the original string to `coding_questions:legacy` and promotes
`coding_questions` to a hash whose fields are question UUIDs. The original JSON
remains available at the rollback key.

```text
coding_questions                         HASH: UUID -> question JSON
coding_questions:legacy                  STRING: original JSON array
coding_questions:index:all               SET: every question UUID
coding_questions:index:title:<value>     SET: matching question UUIDs
coding_questions:index:<field>:<value>   SET: matching question UUIDs
```

Company, topic, subtopic, difficulty, status, and exact normalized title
filters use AND semantics. Substring and fuzzy title search are not supported.
See [docs/coding-questions-nestjs.md](docs/coding-questions-nestjs.md) for the
NestJS provider, DTO, service, controller, module, tests, and request examples.

### Copy coding questions between Upstash databases

Set `UPSTASH_REDIS_REST_URL_SRC`, `UPSTASH_REDIS_REST_TOKEN_SRC`,
`UPSTASH_REDIS_REST_URL_DST`, and `UPSTASH_REDIS_REST_TOKEN_DST` in the
uncommitted `.env` file. Validate the copy without writing, then apply it:

```text
uv run --project services/rag-api python scripts/copy_coding_questions.py
uv run --project services/rag-api python scripts/copy_coding_questions.py --apply
```

The script copies every `coding_questions*` key, preserving strings, hashes,
sets, and TTLs. It stages and verifies source data before replacing matching
destination keys. Unrelated and destination-only keys are not deleted.

## Validation

Run the web checks with pnpm lint, pnpm test, and pnpm build from apps/web.
The RAG API uses its committed `services/rag-api/uv.lock`; run its checks with
`uv run --group dev pytest`, `uv run --group dev ruff check .`,
`uv run --group dev pyright app tests`, and
`uv run --group dev bandit -q -r app` from `services/rag-api`. To validate
Compose configuration without real credentials, run
docker compose --env-file .env.example config from this directory.

The coding-question CLI tests are included in the RAG API test suite. Validate
the CLI itself with `uv run --project services/rag-api ruff check
scripts/coding_question.py`, `uv run --project services/rag-api pyright
scripts/coding_question.py`, and `uv run --project services/rag-api bandit -q
scripts/coding_question.py` from the Genius directory.

With Docker Desktop running, scripts/smoke-compose.ps1 performs the complete
credential-free local Compose smoke test and tears the stack down afterward.

## Security Notes

- API keys remain server-side; no provider key uses a NEXT_PUBLIC_ variable.
- Coding submissions are reviewed by an LLM only and are never executed.
- The local SQLite database is stored in the web-data Docker volume.
