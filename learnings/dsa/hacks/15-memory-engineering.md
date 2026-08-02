# Memory Engineering

## First principles

Memory complexity counts elements, but Python representation determines bytes.
A list stores references and its integer elements are objects; packed arrays
and byte buffers store values more densely. Avoid creating duplicate full-size
collections without a reason.

## Why it matters

A Python `int` and list entry use far more than the raw numeric bytes. An
`O(n)` idea can still exceed memory when it creates several million objects.

## Technique

Estimate what is stored and remove redundant copies.

```text
number of states * fields per state * Python-object overhead
```

Use compact containers where appropriate:

```python
visited = bytearray(vertex_count)  # one byte per flag

from array import array
parent = array('i', [-1]) * vertex_count
```

Avoid shared-row bugs:

```python
# Wrong: all rows are the same list.
matrix = [[0] * columns] * rows

# Correct: each row is separate.
matrix = [[0] * columns for _ in range(rows)]
```

Stream or generate when random access is unnecessary:

```python
total = sum(int(token) for token in sys.stdin.buffer.readline().split())
```

## Pattern recognition

Check memory before allocating `n*m`, `2^n * n`, a graph with tuple edges, or a
whole-file token list.

## Expert habits

- Reuse rolling DP rows.
- Store parents/choices instead of complete paths.
- Coordinate-compress sparse large IDs.
- Use parallel integer lists instead of millions of tiny class instances in
  hot data structures.

## Visual worked example: one million flags

```text
logical data: 1,000,000 true/false flags

list[bool]:
[reference][reference][reference]...
one pointer-sized slot per flag

bytearray:
[byte][byte][byte]...
one byte per flag

same O(n) complexity, very different memory constant
```

Measure on the contest interpreter when memory is close to the limit; object
sizes are implementation-dependent.

## Traps

- A generator is one-use and may be slower if values are needed repeatedly.
- `read().split()` holds the input bytes plus a list and one bytes object per
  token.
- Copying a list with `[:]` is linear memory and time.
- Compact arrays have fixed numeric ranges; choose a type that cannot overflow.
