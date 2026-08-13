# `pathlib`

## 1. Core truth

`pathlib` gives you a clean object-oriented way to work with filesystem paths.
It is usually easier to read than manual string-based path handling.

```python
from pathlib import Path

path = Path("data") / "report.csv"
print(path.as_posix())
```

Output:

```text
data/report.csv
```

The `/` operator joins path parts in a readable way.

## 2. Path foundations

### Join path parts

```python
from pathlib import Path

path = Path("data") / "report.csv"
print(path.as_posix())
```

Output:

```text
data/report.csv
```

### Inspect path parts

```python
from pathlib import Path

path = Path("data/report.csv")
print(path.name)
print(path.suffix)
```

Output:

```text
report.csv
.csv
```

### Read and write text

```python
from pathlib import Path
import tempfile

with tempfile.TemporaryDirectory() as tmp:
    file_path = Path(tmp) / "note.txt"
    file_path.write_text("hello", encoding="utf-8")
    print(file_path.read_text(encoding="utf-8"))
```

Output:

```text
hello
```

## 3. Path APIs

- `Path(...)`
- `/` path joining
- `name`, `suffix`, `parent`
- `exists()`
- `read_text()`
- `write_text()`

## 4. Practical path operations

### Example 1: Join paths

```python
from pathlib import Path

print((Path("logs") / "app.log").as_posix())
```

Output:

```text
logs/app.log
```

### Example 2: Inspect a file path

```python
from pathlib import Path

path = Path("logs/app.log")
print(path.name)
print(path.suffix)
```

Output:

```text
app.log
.log
```

### Example 3: Round-trip text content

```python
from pathlib import Path
import tempfile

with tempfile.TemporaryDirectory() as tmp:
    file_path = Path(tmp) / "data.txt"
    file_path.write_text("Python", encoding="utf-8")
    print(file_path.read_text(encoding="utf-8"))
```

Output:

```text
Python
```

- build file paths safely;
- read and write config or report files;
- inspect extensions before processing;
- avoid manual string concatenation for paths.

## 5. Path mistakes

### Mistake 1: Using raw string concatenation for paths

### Mistake 2: Forgetting encoding when reading text files

### Mistake 3: Treating paths like plain strings when methods exist

## 6. Path decision guide

| Need | Best choice | Why |
| --- | --- | --- |
| New path code | `pathlib` | readable and modern |
| Low-level compatibility | `os.path` | system-style helpers |

## 7. Security and portability

- use `pathlib` by default for path manipulation;
- be explicit about encoding for text files;
- validate paths before using them in scripts.

## 8. Advanced path behavior

- globbing;
- recursive search;
- path resolution.

## 9. Mental model

| Method | Use |
| --- | --- |
| `Path()` | create a path object |
| `/` | join path parts |
| `name` | final component |
| `suffix` | file extension |
| `read_text()` | read file text |
| `write_text()` | write file text |

## 10. Validate containment after resolution

Joining an untrusted absolute path discards the trusted base, and `..` can escape
it. Resolve the candidate and verify containment before access.

```python
from pathlib import Path

base = Path("/srv/uploads").resolve()
candidate = (base / "reports" / "summary.txt").resolve()
print(candidate.is_relative_to(base))
```

Output:

```text
True
```

The example demonstrates lexical resolution. A hostile process can still swap a
symlink between validation and use; security-critical code needs descriptor-based
filesystem APIs or an isolated storage boundary.

## 11. Atomic writes

Write the complete replacement beside the destination, then use `replace()`.

```python
from pathlib import Path
from tempfile import TemporaryDirectory

with TemporaryDirectory() as directory:
    target = Path(directory) / "state.txt"
    temporary = target.with_suffix(".tmp")
    temporary.write_text("ready", encoding="utf-8")
    temporary.replace(target)
    print(target.read_text(encoding="utf-8"))
```

Output:

```text
ready
```

Replacement is atomic only under the filesystem's guarantees and normally must
stay on the same filesystem. Flush and synchronize when crash durability matters.

## 12. Traversal details

- `Path.walk()` provides top-down or bottom-up traversal on current Python.
- Globbing order is unspecified; sort paths when output order matters.
- Decide whether symlinks are allowed before recursive traversal.
- Catch specific `OSError` subclasses at the boundary that can handle them.
- `Path.resolve(strict=True)` verifies that every component exists; the default
  is useful for normalization but is not proof that a later operation is safe.
