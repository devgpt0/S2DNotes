# Python Complexity Traps

## First principles

Python syntax can hide linear work. Complexity belongs to the operation, not
to how short it looks. Ask whether an expression scans, copies, shifts, hashes,
or allocates data.

## Why it matters

Short Python syntax can hide copying or linear work inside a loop.

## Critical operations

| Operation | Cost |
| --- | --- |
| `items.append(x)` | amortized `O(1)` |
| `items.pop()` | `O(1)` |
| `items.pop(0)` / `items.insert(0, x)` | `O(n)` |
| `x in list` | `O(n)` |
| `x in set/dict` | expected `O(1)` |
| `items[a:b]` | `O(b-a)` copy |
| `text += piece` repeatedly | can become `O(total^2)` |
| `sorted(items)` | `O(n log n)` plus a new list |
| `sum(items[a:b])` | slice copy plus linear sum |

## Common accidental quadratic code

```python
# Slow: each front deletion shifts the list.
while values:
    process(values.pop(0))

# Correct queue.
from collections import deque
queue = deque(values)
while queue:
    process(queue.popleft())
```

```python
# Slow inside a loop: repeated slicing and summing.
for left in range(len(values)):
    total = sum(values[left:right])

# Precompute once.
prefix = [0]
for value in values:
    prefix.append(prefix[-1] + value)
total = prefix[right] - prefix[left]
```

## Pattern recognition

Before accepting a nested-looking or compact expression, ask:

```text
Does this operation copy, shift, scan, sort, hash, or allocate?
How many times does the outer code call it?
```

## Expert habit

Count total element touches, not source-code lines. A comprehension is faster
than a manual loop but has the same asymptotic work.

## Visual worked example: one innocent line becomes quadratic

```text
values is a list of n items

for x in values:          n iterations
    if x in values:       scans up to n items
                          -------------------
                          O(n^2)

seen = set(values)        O(n) expected build
for x in values:
    if x in seen:         O(1) expected each
                          -------------------
                          O(n) expected
```

Use a set only when membership is the required operation; preserving duplicate
counts or order may require a different structure.

## Traps

- `setdefault(key, expensive())` evaluates the default even when the key exists.
- `list.count` and `list.index` are linear.
- `min`, `max`, `all`, and `any` scan until done; repeated calls may dominate.
- Nested list multiplication can create shared inner lists; see memory notes.
