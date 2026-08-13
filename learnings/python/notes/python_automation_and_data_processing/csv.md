# CSV

## 1. Core truth

CSV is a simple text format for table-like data.
It is useful when your data is naturally arranged in rows and columns.

```python
import csv
from io import StringIO

text = "name,age\nAna,30\n"
reader = csv.reader(StringIO(text))

print(next(reader))
print(next(reader))
```

Output:

```text
['name', 'age']
['Ana', '30']
```

CSV reads each line as a row and splits it into columns.

## 2. CSV foundations

### `reader` returns rows as lists

```python
import csv
from io import StringIO

reader = csv.reader(StringIO("name,age\nAna,30\n"))
print(next(reader))
```

Output:

```text
['name', 'age']
```

### `DictReader` returns rows as dictionaries

```python
import csv
from io import StringIO

reader = csv.DictReader(StringIO("name,age\nAna,30\n"))
print(next(reader))
```

Output:

```text
{'name': 'Ana', 'age': '30'}
```

### `writer` writes rows

```python
import csv
from io import StringIO

buffer = StringIO()
writer = csv.writer(buffer, lineterminator="\n")
writer.writerow(["name", "age"])
writer.writerow(["Ana", 30])

print(buffer.getvalue(), end="")
```

Output:

```text
name,age
Ana,30
```

## 3. Reader and writer APIs

- `csv.reader(...)`
- `csv.DictReader(...)`
- `csv.writer(...)`
- `writerow()`
- `writerows()`

## 4. Practical CSV processing

### Example 1: Read rows as lists

```python
import csv
from io import StringIO

reader = csv.reader(StringIO("a,b\n1,2\n"))
print(next(reader))
print(next(reader))
```

Output:

```text
['a', 'b']
['1', '2']
```

### Example 2: Read rows as dictionaries

```python
import csv
from io import StringIO

reader = csv.DictReader(StringIO("name,age\nAna,30\n"))
print(next(reader)["name"])
```

Output:

```text
Ana
```

### Example 3: Write a small CSV

```python
import csv
from io import StringIO

buffer = StringIO()
writer = csv.writer(buffer, lineterminator="\n")
writer.writerow(["city", "country"])
writer.writerow(["Pune", "India"])

print(buffer.getvalue(), end="")
```

Output:

```text
city,country
Pune,India
```

- exporting rows from a report;
- importing spreadsheet-like data;
- simple data interchange when a table is enough;
- batch processing from flat files.

## 5. CSV mistakes

### Mistake 1: Forgetting that CSV values are strings

Convert numeric values explicitly.

### Mistake 2: Not handling headers

If your CSV has a header row, use `DictReader` or skip the header intentionally.

### Mistake 3: Ignoring newline handling in real files

When working with real files, open them correctly to avoid blank-line issues.

## 6. Format decision guide

| Need | Best choice | Why |
| --- | --- | --- |
| Table-like flat data | CSV | simple and widely supported |
| Nested structured data | JSON | supports dictionaries inside dictionaries |

## 7. Performance and safety

- CSV is simple but limited;
- values are text, so type conversion is your job;
- be careful with delimiters, quoting, and headers.

## 8. Advanced CSV behavior

- custom delimiters;
- quoting rules;
- streaming larger files row by row.

## 9. Mental model

| Tool | Use |
| --- | --- |
| `reader` | rows as lists |
| `DictReader` | rows as dictionaries |
| `writer` | write rows |

## 10. Validate the table contract

CSV has no schema; every field starts as text. Validate headers before rows and
convert each value explicitly.

```python
import csv
from io import StringIO


def read_ages(text: str) -> list[int]:
    reader = csv.DictReader(StringIO(text))
    if reader.fieldnames != ["name", "age"]:
        raise ValueError("expected columns: name, age")

    ages: list[int] = []
    for row_number, row in enumerate(reader, start=2):
        try:
            ages.append(int(row["age"]))
        except ValueError as error:
            raise ValueError(f"row {row_number}: age must be an integer") from error
    return ages


print(read_ages("name,age\nAna,30\nRaj,41\n"))
```

Output:

```text
[30, 41]
```

Reject duplicate or unexpected headers before using `DictReader`; duplicate
names otherwise overwrite earlier columns in each dictionary.

## 11. File and dialect correctness

Open real CSV files with `newline=""` so the `csv` module owns newline handling,
and specify an encoding.

```python
with open("records.csv", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
```

This is a contextual file fragment. For external feeds, configure the delimiter,
quote character, escape behavior, and header policy from a trusted contract.
`csv.Sniffer` is a heuristic, not validation.

## 12. Streaming and spreadsheet safety

- Process rows from the reader instead of calling `list(reader)` for large files.
- Set `csv.field_size_limit()` when untrusted fields must have an upper bound.
- Bound the file size and row count before expensive processing.
- Reject or deliberately escape cells beginning with `=`, `+`, `-`, or `@`
  when output will be opened in spreadsheet software.
- Write to a temporary file and replace the destination only after every row is
  valid.
