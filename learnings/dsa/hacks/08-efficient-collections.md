# Choose the Right Built-In Collection

## First principles

Choose a collection from the operation that must be fast. A list, set, dict,
deque, and heap store different invariants; replacing one with another can
change both semantics and complexity.

## Why it matters

Python's built-ins are fast when their guarantees match the operation. The
wrong collection can turn linear work into quadratic work.

## Decision table

| Need | Use |
| --- | --- |
| stack | `list` with `append` / `pop` |
| queue or deque | `collections.deque` |
| membership / uniqueness | `set` |
| key to value/count | `dict` / `collections.Counter` |
| repeated smallest item | `heapq` |
| sorted boundary in static list | `bisect` |
| compact numeric storage | `array`, `bytearray`, or carefully chosen lists |

## Python patterns

```python
from collections import Counter, defaultdict, deque

frequency = Counter(values)
graph: list[list[int]] = [[] for _ in range(vertex_count)]
queue = deque([start])
seen = {start}
```

Use `defaultdict` only when automatic insertion is wanted:

```python
groups: dict[int, list[int]] = defaultdict(list)
for key, value in pairs:
    groups[key].append(value)
```

## Pattern recognition

Write down the dominant operation: front removal, membership, minimum
extraction, sorted search, or indexed access. Choose from that operation.

## Visual worked example: choose by operation

```text
need                         structure       key cost
index by position            list            O(1)
membership by value          set             O(1) expected
value -> information         dict            O(1) expected
remove oldest item           deque           O(1)
remove smallest priority     heapq list       O(log n)

list.pop(0): shifts all remaining items -> O(n)
deque.popleft(): moves a boundary       -> O(1)
```

Start from required behavior; do not choose a structure merely because its
syntax is familiar.

## Traps

- Accessing a missing `defaultdict` key mutates the dictionary.
- `Counter` retains zero/negative counts until removed.
- A heap is not a sorted list; only index `0` is guaranteed minimum.
- A set destroys duplicates and should not replace a frequency map.
