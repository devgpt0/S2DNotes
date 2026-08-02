# Bisect and Boundary Searches

## First principles

Binary search should locate a boundary, not merely “some matching value.”
`bisect_left` finds the first position where the target may be inserted;
`bisect_right` finds the position after all equal targets.

## Why it matters

Most binary-search mistakes are boundary-definition mistakes. Python's
`bisect` gives tested lower and upper bounds for sorted lists.

## Technique

```python
from bisect import bisect_left, bisect_right

left = bisect_left(values, target)   # first index with value >= target
right = bisect_right(values, target) # first index with value > target
count = right - left
```

Count values inside inclusive numeric range `[low, high]`:

```python
count = bisect_right(values, high) - bisect_left(values, low)
```

Find a predecessor/successor:

```python
position = bisect_left(values, target)
predecessor = values[position - 1] if position > 0 else None
successor = values[position] if position < len(values) else None
```

## Pattern recognition

Use bisect on a sorted list for first/last occurrence, insertion boundary,
rank/count queries, LIS tails, and meet-in-the-middle combination.

## Visual clue

```text
bisect_left:  [ < target | >= target ]
bisect_right: [ <= target | > target ]
```

## Visual worked example: one duplicate block

```text
values = [1, 2, 2, 2, 5]
target = 2

index:         0  1  2  3  4
               1 [2  2  2] 5
bisect_left  = 1  first 2
bisect_right = 4  after last 2
count        = 4 - 1 = 3
```

For a custom monotone predicate, write down whether the desired boundary is
first true or last true before coding.

## Traps

- The list must already be sorted by the same key.
- `insort` finds the position in `O(log n)` but list insertion still costs
  `O(n)` due to shifting.
- A returned position may equal `len(values)`.
- With tuples, all tuple fields participate unless a separate key list is used.
