# File I/O, Pathlib, and Serialization Mastery

## 1) File I/O Principles

- use context managers (`with`) for automatic cleanup
- specify encoding explicitly for text files
- stream large files instead of loading entire content by default

## 2) `pathlib` Preferred Over String Paths

```python
from pathlib import Path

root = Path("data")
for file in root.glob("*.csv"):
    print(file.name, file.stat().st_size)
```

Benefits:
- cleaner cross-platform path handling
- better composability

## 3) Text vs Binary Modes

- text: `"r"`, `"w"`, `"a"` with encoding
- binary: `"rb"`, `"wb"` for bytes payloads

## 4) Safe Write Patterns

- write to temp file then atomic rename for critical files
- avoid partial-write corruption in crash scenarios

## 5) CSV and JSON Essentials

Use stdlib for common formats:
- `csv` for tabular text
- `json` for structured payloads

Guideline:
- validate expected schema before trusting input.

## 6) Pickle Caution

`pickle` is Python-specific and unsafe for untrusted data.
Use only for trusted internal persistence/cache scenarios.

## 7) Error Handling at I/O Boundaries

Catch and classify:
- missing file
- permission denied
- parse errors

Surface meaningful domain messages upstream.

## 8) Performance Patterns

- iterate line-by-line for large files
- use buffering defaults unless profiling indicates otherwise
- avoid repeated open/close in tight loops when batching is possible

## 9) Interview Points

1. Why prefer `pathlib`?
2. Why explicit encoding?
3. Why `pickle` is risky for untrusted payloads?
4. How to process large files memory-efficiently?

## 10) Production Checklist

1. all file operations use `with`.
2. path handling is `pathlib`-based.
3. serialization format is selected by interoperability and safety needs.
4. I/O failures are logged with context and surfaced clearly.
