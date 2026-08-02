# Fast Input and Output

## First principles

The algorithm cannot start until input is parsed, and output is not free.
Reading or writing one tiny piece at a time repeats interpreter and system-call
overhead. Buffer large chunks, then parse or emit them in memory.

## Why it matters

Python's algorithm can be fast enough while line-by-line parsing or many
`print` calls cause a time-limit failure.

## Technique

- Use `sys.stdin.buffer` for bytes-based input.
- Parse a whole token stream only when memory allows it.
- Collect output strings and write once.

## When to use it

- `input()` is fine for small input.
- Use buffered line reads for large graphs/matrices.
- Use a whole-file token iterator when input is token-based and comfortably
  fits memory.

## Python patterns

### Whole-file token parser

```python
import sys


def solve() -> None:
    tokens = iter(sys.stdin.buffer.read().split())
    size = int(next(tokens))
    values = [int(next(tokens)) for _ in range(size)]
    answer = sum(values)
    sys.stdout.write(str(answer))


if __name__ == '__main__':
    solve()
```

### Buffered line parser

```python
import sys


def solve() -> None:
    read = sys.stdin.buffer.readline
    vertex_count, edge_count = map(int, read().split())
    graph = [[] for _ in range(vertex_count)]
    for _ in range(edge_count):
        first, second = map(int, read().split())
        first -= 1
        second -= 1
        graph[first].append(second)
        graph[second].append(first)
    sys.stdout.write(f'{sum(map(bool, graph))}\n')
```

### Batch output

```python
answers = [3, 5, 8]
sys.stdout.write('\n'.join(map(str, answers)))
```

## Visual rule

```text
many small Python calls = overhead
one buffered read/write = work done in optimized C code
```

## Visual worked example: buffer once

For input `5\n10 20 30 40 50\n`:

```text
slow shape:
read "10" -> Python call
read "20" -> Python call
read "30" -> Python call
... many boundary crossings

buffered shape:
read all bytes once
b"5\n10 20 30 40 50\n"
        |
        +-> split in memory -> [5,10,20,30,40,50]
```

Likewise, collect output strings and write one joined block instead of printing
inside a very large loop.

## Traps

- `read().split()` can use several times the input file size in memory.
- Byte tokens compare with `b'word'`, not `'word'`, until decoded.
- Never call `next(tokens)` beyond valid contest input; let malformed input fail.
- Do not shadow `input` globally unless the shorter name genuinely improves the
  solution.
