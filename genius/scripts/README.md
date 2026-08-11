# Genius Scripts

Run every command in this guide from the Genius project directory:

```powershell
cd C:\pocs\notes\genius
```

Python commands use the existing `services/rag-api` uv environment. Secrets are
loaded from the uncommitted `genius/.env` file without overriding variables
already present in the process environment.

## `coding_question.py`

Migrates the legacy `coding_questions` JSON string into a queryable hash and
set indexes. It also retrieves complete questions by UUID or indexed fields.

Required environment variables:

```env
UPSTASH_REDIS_REST_URL=
UPSTASH_REDIS_REST_TOKEN=
```

Show help:

```powershell
uv run --project services/rag-api python scripts/coding_question.py --help
```

Validate the source without writing:

```powershell
uv run --project services/rag-api python scripts/coding_question.py migrate
```

Apply the string-to-hash migration:

```powershell
uv run --project services/rag-api python scripts/coding_question.py migrate --apply
```

The migration stores complete question objects in the `coding_questions` hash,
keeps the original JSON at `coding_questions:legacy`, and creates indexes under
`coding_questions:index:*`.

Fetch one complete question by UUID:

```powershell
uv run --project services/rag-api python scripts/coding_question.py get --id 634dd126-6074-4c1f-9c0e-1eac866d5d05
```

Fetch Easy questions:

```powershell
uv run --project services/rag-api python scripts/coding_question.py query --difficulty Easy --limit 20
```

Combine filters with AND semantics:

```powershell
uv run --project services/rag-api python scripts/coding_question.py query --company Anduril --topic Array --difficulty Medium --limit 20
```

Query an exact normalized title:

```powershell
uv run --project services/rag-api python scripts/coding_question.py query --title "Game of Life" --limit 20
```

List questions in deterministic UUID order:

```powershell
uv run --project services/rag-api python scripts/coding_question.py list --offset 0 --limit 100
```

Select random questions without replacement:

```powershell
uv run --project services/rag-api python scripts/coding_question.py random --topic Array --difficulty Easy --count 5
```

Supported exact filters are `company`, `topic`, `difficulty`, `status`, and
`title`. Query and list limits, and random counts, have a maximum of 1,000.
Topics are restricted to the canonical values in `coding_question_topics.txt`.
The migration writes that lowercase underscore value to both document topic
fields and indexes only the canonical top-level topic. Subtopics remain
document metadata.

## `audit_coding_question_indexes.py`

Audits every coding-question index key, key type, and set membership against
the validated source dataset. It also reports topic aliases consolidated by
the canonical naming rules.

Run a read-only audit:

```powershell
uv run --project services/rag-api python scripts/audit_coding_question_indexes.py
```

Rebuild the indexes and require a clean post-migration audit:

```powershell
uv run --project services/rag-api python scripts/audit_coding_question_indexes.py --apply
```

Write the verified canonical topic list while rebuilding:

```powershell
uv run --project services/rag-api python scripts/audit_coding_question_indexes.py --apply --topics-output coding_question_topics.txt
```

## `copy_coding_questions.py`

Copies every `coding_questions*` key from one Upstash Redis database to another
while preserving strings, hashes, sets, and TTLs. Matching destination keys are
replaced only after staged data passes verification. Destination-only and
unrelated keys are not deleted.

Required environment variables:

```env
UPSTASH_REDIS_REST_URL_SRC=
UPSTASH_REDIS_REST_TOKEN_SRC=
UPSTASH_REDIS_REST_URL_DST=
UPSTASH_REDIS_REST_TOKEN_DST=
```

Show help:

```powershell
uv run --project services/rag-api python scripts/copy_coding_questions.py --help
```

Inspect source and destination without writing:

```powershell
uv run --project services/rag-api python scripts/copy_coding_questions.py
```

Apply the staged and verified copy:

```powershell
uv run --project services/rag-api python scripts/copy_coding_questions.py --apply
```

The script rejects identical source and destination URLs and never prints Redis
tokens.

## `smoke-compose.ps1`

Builds and starts the Docker Compose application, waits for RAG indexing,
checks the file tree and local retrieval endpoint, and then stops the stack.

Requirements:

- Docker Desktop must be running.
- The repository must contain `.env.example`.
- The sibling learnings directory must contain indexable Markdown files.

Run the smoke test and stop Compose afterward:

```powershell
powershell -File scripts/smoke-compose.ps1
```

Run the smoke test and keep Compose running:

```powershell
powershell -File scripts/smoke-compose.ps1 -KeepRunning
```

## Validate the scripts

Run the script tests:

```powershell
uv run --project services/rag-api pytest -q services/rag-api/tests/test_coding_question_cli.py services/rag-api/tests/test_copy_coding_questions_cli.py
```

Run formatting, lint, type, and security checks:

```powershell
uv run --project services/rag-api ruff format --check scripts/coding_question.py scripts/audit_coding_question_indexes.py scripts/copy_coding_questions.py
uv run --project services/rag-api ruff check scripts/coding_question.py scripts/audit_coding_question_indexes.py scripts/copy_coding_questions.py
uv run --project services/rag-api pyright scripts/coding_question.py scripts/audit_coding_question_indexes.py scripts/copy_coding_questions.py
uv run --project services/rag-api bandit -q scripts/coding_question.py scripts/audit_coding_question_indexes.py scripts/copy_coding_questions.py
```
