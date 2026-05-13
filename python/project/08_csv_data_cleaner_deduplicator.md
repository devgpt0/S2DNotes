# Project 08: CSV Data Cleaner and Deduplicator

## Estimated Time
5 to 7 hours

## Goal
Build a tool to clean CSV data and remove duplicate rows by chosen key columns.

## Functional Requirements
- Load CSV.
- Clean data:
  - trim spaces
  - normalize case for selected fields
  - replace empty fields with default value
- Deduplicate by one or more columns (e.g., `email`, `phone`).
- Save cleaned CSV.
- Save duplicates CSV.

## Non-Functional Requirements
- Preserve header order.
- Handle missing key columns gracefully.

## Concepts Practiced
- `list[dict]` record handling
- `set` for dedup signatures
- `dict` transformations
- CSV I/O

## HLD
- `reader.py`: load CSV rows
- `cleaner.py`: normalization functions
- `dedupe.py`: duplicate filtering
- `writer.py`: output files
- `main.py`: config and run flow

## LLD
- `read_csv(path) -> (rows, headers)`
- `clean_row(row, clean_config) -> dict`
- `make_signature(row, key_columns) -> tuple`
- `split_unique_duplicates(rows, key_columns) -> (unique, dupes)`
- `write_csv(path, headers, rows) -> None`
- `run_pipeline(input_path, output_path, dup_path, config) -> dict`

## Passing Criteria
- Whitespace cleanup works.
- Duplicates correctly split.
- Output file row count + duplicate row count = input rows.
- Report includes total/cleaned/duplicates counts.

## Implementation Roadmap
1. Build reader/writer.
2. Build cleaning transformations.
3. Build dedupe logic.
4. Wire pipeline and report.
5. Test with messy sample CSV.

## Optional Extensions
- Support column mapping/renaming.
- CLI flags for key columns.
