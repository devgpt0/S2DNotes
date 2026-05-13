# Project 06: Log File Parser and Report Generator

## Estimated Time
4 to 6 hours

## Goal
Parse plain-text log files and generate useful summary reports.

## Functional Requirements
- Read log file line by line.
- Parse fields:
  - timestamp
  - level (`INFO`, `WARN`, `ERROR`)
  - message
- Generate report:
  - count by level
  - top repeated error messages
  - timeline by hour
- Write report as JSON/text file.

## Non-Functional Requirements
- Skip malformed lines with error counter.
- Must handle large files (line-by-line, not full load required).

## Input Format Example
```text
2026-05-13 10:00:01 | INFO | server started
2026-05-13 10:01:11 | ERROR | db timeout
```

## Concepts Practiced
- string split/cleanup
- `dict` counters
- `list` of parsed records
- `setdefault` patterns

## HLD
- `parser.py`: parse line and file
- `analyzer.py`: metrics computation
- `writer.py`: report output
- `main.py`: orchestrator

## LLD
- `parse_line(line) -> dict|None`
- `read_logs(path) -> (records, malformed_count)`
- `count_by_level(records) -> dict[str, int]`
- `top_errors(records, top_n=5) -> list[tuple[str, int]]`
- `count_by_hour(records) -> dict[str, int]`
- `build_report(records, malformed_count) -> dict`
- `write_report(path, report) -> None`

## Passing Criteria
- Correct count by level.
- Malformed lines counted, not crashing parser.
- Top errors sorted by frequency.
- Output report file created.

## Implementation Roadmap
1. Build line parser.
2. Build file reader.
3. Build metrics functions.
4. Build report writer.
5. Test on sample log file.

## Optional Extensions
- Filter report by date range.
- CLI args for input/output paths.
