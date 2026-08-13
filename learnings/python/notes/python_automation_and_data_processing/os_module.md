# `os` Module

## 1. Core truth

The `os` module provides operating-system related utilities.
It is a lower-level tool than `pathlib` and is often used for compatibility or system access.

```python
import os

print(os.path.basename("data/report.csv"))
```

Output:

```text
report.csv
```

`basename()` returns the last path component.

## 2. Operating-system foundations

### Path helpers

```python
import os

print(os.path.join("data", "report.csv").replace(os.sep, "/"))
print(os.path.basename("data/report.csv"))
```

Output:

```text
data/report.csv
report.csv
```

### Environment variables

```python
import os

value = os.getenv("DEMO_MODE", "off")
print(value)
```

Output:

```text
off
```

### Directory listing

```python
import os
import tempfile

with tempfile.TemporaryDirectory() as tmp:
    open(os.path.join(tmp, "a.txt"), "w", encoding="utf-8").close()
    open(os.path.join(tmp, "b.txt"), "w", encoding="utf-8").close()
    print(sorted(os.listdir(tmp)))
```

Output:

```text
['a.txt', 'b.txt']
```

## 3. OS APIs

- `os.getenv()`
- `os.path.join()`
- `os.path.basename()`
- `os.listdir()`

## 4. Practical OS operations

### Example 1: Join a path

```python
import os

print(os.path.join("logs", "app.log").replace(os.sep, "/"))
```

Output:

```text
logs/app.log
```

### Example 2: Read a default setting

```python
import os

print(os.getenv("APP_MODE", "development"))
```

Output:

```text
development
```

### Example 3: List files in a temp folder

```python
import os
import tempfile

with tempfile.TemporaryDirectory() as tmp:
    open(os.path.join(tmp, "one.txt"), "w", encoding="utf-8").close()
    open(os.path.join(tmp, "two.txt"), "w", encoding="utf-8").close()
    print(sorted(os.listdir(tmp)))
```

Output:

```text
['one.txt', 'two.txt']
```

- read configuration from environment variables;
- inspect directory contents;
- create compatibility code for older codebases;
- work with process and filesystem utilities.

## 5. OS mistakes

### Mistake 1: Using string concatenation for paths

Use path helpers instead of manual slashes.

### Mistake 2: Assuming environment variables are always set

Always provide a default or handle absence explicitly.

### Mistake 3: Using `os` where `pathlib` would be clearer

For new code, `pathlib` is often easier to read.

## 6. API decision guide

| Need | Best choice | Why |
| --- | --- | --- |
| Lower-level system utilities | `os` | broad compatibility |
| Readable path manipulation | `pathlib` | clearer object-oriented API |

## 7. Security and portability

- prefer `pathlib` for most new path code;
- use `os` when you need system-level helpers or compatibility;
- keep environment lookups explicit and predictable.

## 8. Advanced OS behavior

- `os.walk`;
- process environment;
- platform differences.

## 9. Mental model

| Function | Use |
| --- | --- |
| `os.getenv` | read environment value |
| `os.path.join` | combine path pieces |
| `os.path.basename` | get file name |
| `os.listdir` | list directory contents |

## 10. Environment variables are untyped input

Environment values are strings. Validate presence and syntax explicitly instead
of silently coercing unexpected values.

```python
import os

os.environ["WORKER_COUNT"] = "4"
raw_count = os.environ["WORKER_COUNT"]

if not raw_count.isdecimal() or int(raw_count) < 1:
    raise ValueError("WORKER_COUNT must be a positive integer")

print(int(raw_count))
```

Output:

```text
4
```

Do not log the environment: it commonly contains tokens and credentials.

## 11. Directory iteration and race safety

`os.scandir()` exposes file-type metadata with each entry and often avoids extra
system calls compared with `listdir()` plus `stat()`.

Filesystem checks are snapshots. Another process can replace a path after
`exists()` or `isfile()` succeeds. For security-sensitive operations, use APIs
that operate relative to an already-open directory descriptor where supported,
avoid following symlinks, and handle the operation's actual exception.

## 12. Processes and file descriptors

- Use `subprocess.run()` with an argument list, `check=True`, a timeout, and
  `shell=False` for external programs.
- Close file descriptors deterministically with context managers.
- Pass only required descriptors and environment values to child processes.
- Use `os.replace()` for atomic destination replacement on the same filesystem.
- Treat `os.walk()` errors explicitly; permission failures must not silently
  produce incomplete processing.
