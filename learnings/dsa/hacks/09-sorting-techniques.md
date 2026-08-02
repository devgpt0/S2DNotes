# Sorting Like a Competitor

## First principles

Python's sort is stable: records with equal keys keep their previous relative
order. A key function should compute the exact ordering tuple once per record,
avoiding a complicated and error-prone comparator.

## Why it matters

Sorting is often the bridge to greedy, two pointers, sweep lines, and canonical
states. Python's sort is stable and highly optimized.

## Technique

Use a key that directly describes the desired order.

```python
# score descending, name ascending
players.sort(key=lambda player: (-player.score, player.name))
```

Preserve original indices when needed:

```python
ordered = sorted((value, index) for index, value in enumerate(values))
```

Use stability for mixed directions without awkward transformed keys:

```python
# Secondary key first, then stable primary sort.
records.sort(key=lambda record: record.name)
records.sort(key=lambda record: record.score, reverse=True)
```

## Pattern recognition

Sort when relative order enables one scan, duplicate grouping, interval
processing, binary search, or a greedy proof.

## Performance rules

- `list.sort()` mutates and returns `None`.
- `sorted(iterable)` returns a new list.
- Key functions run once per element; comparison wrappers may run many times.
- Tuple comparison is lexicographic and implemented efficiently.

## Visual worked example: mixed sort directions

Sort score descending, then name ascending.

```text
records: (Ana,90), (Zoe,95), (Bob,90)

key = (-score, name)

Ana -> (-90, "Ana")
Zoe -> (-95, "Zoe")
Bob -> (-90, "Bob")

sorted keys:
(-95,"Zoe"), (-90,"Ana"), (-90,"Bob")

result: Zoe 95, Ana 90, Bob 90
```

Negate only numeric fields that must be descending; keep ascending fields
unchanged.

## Traps

- `reverse=True` reverses every key direction, not only the first.
- Subtraction-style comparators are unnecessary and can be inconsistent.
- Sorting destroys original order; save indices if the answer needs them.
- Do not sort if a linear frequency/counting approach is required by constraints.
