# PYTHON - FILE HANDLING

File handling moves data between a Python program and persistent storage.

## 1. File Path and File Content

A path identifies a file. Opening the path gives a file object used to read or write content.

```python
from pathlib import Path

path = Path("notes.txt")

print(path.name)
print(path.suffix)
```

Output:

```text
notes.txt
.txt
```

`Path` represents the path; it does not open the file.

## 2. File Modes

| Mode | Meaning | Missing file | Existing content |
| --- | --- | --- | --- |
| `r` | read | error | preserved |
| `w` | write | created | erased |
| `a` | append | created | preserved |
| `x` | create only | created | error |
| `b` | binary modifier | depends on base mode | bytes |
| `t` | text modifier | depends on base mode | text; default |
| `+` | read and write modifier | depends on base mode | depends on base mode |

Examples: `rb`, `w+`, and `a+b` combine a base mode with modifiers.

## 3. Write and Read a Text File

Use `with` so the file closes even when an error occurs.

```python
from pathlib import Path
from tempfile import TemporaryDirectory

with TemporaryDirectory() as directory:
    path = Path(directory) / "message.txt"

    with path.open("w", encoding="utf-8") as file:
        file.write("Hello, Python!")

    with path.open("r", encoding="utf-8") as file:
        print(file.read())
```

Output:

```text
Hello, Python!
```

The first block writes and closes the file. The second block reads it.

## 4. `with` Closes the File

A file object is open inside its context and closed afterward.

```python
from pathlib import Path
from tempfile import TemporaryDirectory

with TemporaryDirectory() as directory:
    path = Path(directory) / "status.txt"

    with path.open("w", encoding="utf-8") as file:
        print(file.closed)
        file.write("ready")

    print(file.closed)
```

Output:

```text
False
True
```

## 5. `write()`

`write()` writes a string and returns the number of characters written.

```python
from io import StringIO

file = StringIO()
count = file.write("Python")

print(count)
print(file.getvalue())
```

Output:

```text
6
Python
```

`write()` does not add a newline automatically.

## 6. Write Multiple Lines

Use explicit `\n` characters or `writelines()`.

```python
from io import StringIO

file = StringIO()
file.writelines(["first\n", "second\n"])

print(file.getvalue(), end="")
```

Output:

```text
first
second
```

`writelines()` does not insert separators; each string must contain its own newline.

## 7. `read()`

`read()` returns all remaining content, or at most the requested number of characters.

```python
from io import StringIO

file = StringIO("Python")

print(file.read(2))
print(file.read())
```

Output:

```text
Py
thon
```

Reading advances the file position.

## 8. `readline()`

`readline()` returns one line at a time, including its newline when present.

```python
from io import StringIO

file = StringIO("first\nsecond\n")

print(file.readline(), end="")
print(file.readline(), end="")
```

Output:

```text
first
second
```

## 9. `readlines()`

`readlines()` returns the remaining lines as a list.

```python
from io import StringIO

file = StringIO("first\nsecond\n")

print(file.readlines())
```

Output:

```text
['first\n', 'second\n']
```

For large files, iterate instead of loading every line into a list.

## 10. Iterate Over a File

File objects are iterable and yield one line at a time.

```python
from io import StringIO

file = StringIO("10\n20\n30\n")

for line in file:
    print(int(line))
```

Output:

```text
10
20
30
```

This keeps memory usage low for large text files.

## 11. File Position: `tell()` and `seek()`

`tell()` reports the current position. `seek()` moves it.

```python
from io import StringIO

file = StringIO("Python")

print(file.read(2))
print(file.tell())
file.seek(0)
print(file.read())
```

Output:

```text
Py
2
Python
```

## 12. Write Mode Overwrites

Opening an existing file with `w` erases its previous content.

```python
from pathlib import Path
from tempfile import TemporaryDirectory

with TemporaryDirectory() as directory:
    path = Path(directory) / "value.txt"
    path.write_text("old", encoding="utf-8")

    with path.open("w", encoding="utf-8") as file:
        file.write("new")

    print(path.read_text(encoding="utf-8"))
```

Output:

```text
new
```

Use `w` only when replacing content is intentional.

## 13. Append Mode

Opening with `a` writes at the end without erasing existing content.

```python
from pathlib import Path
from tempfile import TemporaryDirectory

with TemporaryDirectory() as directory:
    path = Path(directory) / "log.txt"
    path.write_text("first\n", encoding="utf-8")

    with path.open("a", encoding="utf-8") as file:
        file.write("second\n")

    print(path.read_text(encoding="utf-8"), end="")
```

Output:

```text
first
second
```

## 14. Exclusive Creation Mode

`x` creates a new file and fails if the path already exists.

```python
from pathlib import Path
from tempfile import TemporaryDirectory

with TemporaryDirectory() as directory:
    path = Path(directory) / "unique.txt"
    path.write_text("existing", encoding="utf-8")

    try:
        with path.open("x", encoding="utf-8"):
            pass
    except FileExistsError as error:
        print(type(error).__name__)
```

Output:

```text
FileExistsError
```

Use `x` when overwriting would be unsafe.

## 15. `pathlib` Convenience Methods

`Path.read_text()` and `Path.write_text()` are concise for small files.

```python
from pathlib import Path
from tempfile import TemporaryDirectory

with TemporaryDirectory() as directory:
    path = Path(directory) / "note.txt"
    characters_written = path.write_text("learn", encoding="utf-8")

    print(characters_written)
    print(path.read_text(encoding="utf-8"))
```

Output:

```text
5
learn
```

Use streaming with `open()` for large files.

## 16. Build Paths Safely

Use `/` with `Path` instead of manually joining path strings.

```python
from pathlib import Path

path = Path("data") / "reports" / "sales.csv"

print(path.parts)
print(path.name)
```

Output:

```text
('data', 'reports', 'sales.csv')
sales.csv
```

`Path` uses the correct separator for the operating system.

## 17. Check Path Type

`exists()`, `is_file()`, and `is_dir()` answer different questions.

```python
from pathlib import Path
from tempfile import TemporaryDirectory

with TemporaryDirectory() as directory:
    folder = Path(directory)
    file_path = folder / "note.txt"
    file_path.write_text("hello", encoding="utf-8")

    print(file_path.exists())
    print(file_path.is_file())
    print(folder.is_dir())
```

Output:

```text
True
True
True
```

The result can change after the check, so still handle file-operation failures.

## 18. Text Encoding

An encoding maps text characters to bytes. Use UTF-8 unless the file contract requires another encoding.

```python
text = "cafe"
encoded = text.encode("utf-8")
decoded = encoded.decode("utf-8")

print(encoded)
print(decoded)
```

Output:

```text
b'cafe'
cafe
```

Always specify `encoding="utf-8"` for text files to avoid platform-dependent defaults.

## 19. Binary Files

Binary modes read and write `bytes`, not `str`.

```python
from pathlib import Path
from tempfile import TemporaryDirectory

with TemporaryDirectory() as directory:
    path = Path(directory) / "data.bin"
    path.write_bytes(bytes([65, 66, 67]))

    data = path.read_bytes()
    print(data)
    print(type(data).__name__)
```

Output:

```text
b'ABC'
bytes
```

Use binary mode for images, audio, archives, and other non-text formats.

## 20. Handle a Missing File

Reading a missing path raises `FileNotFoundError`.

```python
from pathlib import Path

path = Path("file_that_does_not_exist_12345.txt")

try:
    path.read_text(encoding="utf-8")
except FileNotFoundError as error:
    print(type(error).__name__)
```

Output:

```text
FileNotFoundError
```

Catch it only when the program has a defined response, such as reporting a missing optional configuration.

## 21. JSON Files

JSON stores objects, arrays, strings, numbers, Booleans, and null in portable text.

```python
import json
from io import StringIO

profile = {"name": "Ana", "active": True}
file = StringIO()

json.dump(profile, file)
file.seek(0)
restored = json.load(file)

print(restored)
```

Output:

```text
{'name': 'Ana', 'active': True}
```

Use `dump` and `load` for files; use `dumps` and `loads` for strings.

## 22. CSV Files

The `csv` module handles separators and quoting correctly.

```python
import csv
from io import StringIO

file = StringIO()
writer = csv.writer(file, lineterminator="\n")
writer.writerow(["name", "score"])
writer.writerow(["Ana", 95])

print(file.getvalue(), end="")
```

Output:

```text
name,score
Ana,95
```

Do not build CSV rows with manual string joining because values may contain commas or quotes.

## 23. Untrusted Paths

Never allow user input to escape the intended base directory.

```python
from pathlib import Path

base = Path("uploads").resolve()
requested = (base / "reports" / "result.txt").resolve()

print(requested.is_relative_to(base))
```

Output:

```text
True
```

Reject the path if `is_relative_to(base)` is false. Also validate file type, size, and permissions when handling uploads.

## 24. Common Mistakes

| Mistake | Result | Better rule |
| --- | --- | --- |
| forgetting `with` | leaked resource | use a context manager |
| opening with `w` accidentally | content erased | choose mode deliberately |
| omitting encoding | platform-dependent text behavior | use UTF-8 explicitly |
| reading a huge file at once | high memory use | iterate line by line |
| joining paths as strings | fragile paths | use `Path` |
| trusting external paths | path traversal risk | resolve and verify base path |
| loading untrusted `pickle` | arbitrary code execution risk | use a safe validated format |

## 25. Final Mental Model

When handling a file, ask:

1. Is the data text or bytes?
2. Which mode preserves the intended content?
3. Is UTF-8 specified for text?
4. Is cleanup guaranteed by `with`?
5. Can the file be streamed instead of loaded fully?
6. Is the path trusted and inside the allowed directory?
7. Which expected file errors can this layer handle?

| Need | Tool |
| --- | --- |
| small text file | `Path.read_text()` / `write_text()` |
| large text file | `open()` and line iteration |
| binary file | `rb`, `wb`, `read_bytes()`, `write_bytes()` |
| structured nested data | JSON |
| tabular data | CSV |
| path construction | `pathlib.Path` |
