# Project 10: Text Search Indexer

## Estimated Time
5 to 7 hours

## Goal
Build a mini search engine for local text files using an inverted index.

## Functional Requirements
- Read all `.txt` files from a folder.
- Tokenize words (lowercase, remove punctuation basic).
- Build inverted index:
  - `word -> set(file_ids)`
- Search query words and return matching files.
- Support:
  - single-word query
  - multi-word AND query
- Save/load index as JSON.

## Non-Functional Requirements
- Case-insensitive search.
- Ignore stop words (optional list).

## Concepts Practiced
- `dict` for inverted index
- `set` for fast intersection
- `list` for file metadata
- string cleaning and parsing

## HLD
- `scanner.py`: file discovery and read
- `tokenizer.py`: normalize text to tokens
- `indexer.py`: build/load/save index
- `search.py`: query and ranking
- `main.py`: CLI

## LLD
- `read_documents(folder) -> list[dict]`
- `tokenize(text) -> list[str]`
- `build_index(docs) -> dict[str, set[int]]`
- `search_one(index, word) -> set[int]`
- `search_and(index, words) -> set[int]`
- `save_index(path, index, docs_meta) -> None`
- `load_index(path) -> (index, docs_meta)`
- `format_results(doc_ids, docs_meta) -> list[dict]`

Document metadata shape:
```python
{"doc_id": 4, "filename": "notes.txt", "path": "..."}
```

## Passing Criteria
- Index created for all text files.
- Search `python` returns expected files.
- AND query (`python dict`) returns intersection only.
- Index reload works without rebuilding.

## Implementation Roadmap
1. Build document scanner.
2. Build tokenizer.
3. Build inverted index creator.
4. Build search functions.
5. Add save/load index.
6. Add CLI query loop.

## Optional Extensions
- Simple ranking by matched word count.
- Highlight matched words in preview lines.
