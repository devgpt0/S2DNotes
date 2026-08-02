# Dynamic-Programming Performance in Python

## First principles

A DP table is justified only by dependencies. If row `i` reads only row
`i-1`, older rows carry no information for the future and should be removed.
Reducing Python objects often matters as much as reducing asymptotic space.

## Why it matters

DP may have the right asymptotic complexity but still time out because every
state uses dictionaries, recursion, slicing, or large Python objects.

## Technique

1. Use a list when states are dense integer indices.
2. Compress dimensions only after the transition is correct.
3. Choose loop direction deliberately.
4. Keep the hot loop simple.

## Rolling-row pattern

```python
previous = [0] * (columns + 1)
for row in range(1, rows + 1):
    current = [0] * (columns + 1)
    for column in range(1, columns + 1):
        current[column] = transition(previous, current, column)
    previous = current
```

## Dense versus sparse states

```python
# Dense: capacity 0..limit; list is faster.
dp = [-1] * (limit + 1)

# Sparse: only a small fraction of huge state space is reachable.
dp: dict[tuple[int, int], int] = {}
```

## Pattern recognition

Profile the number of states times work per transition. A `2D` table with
`n*m` states is not truly `O(nm)` if each transition copies an `O(n)` list.

## Expert habits

- Use an impossible sentinel consistent with min/max logic.
- For 0/1 knapsack loop capacity downward; for unbounded loop upward.
- `functools.cache` is excellent for sparse/reachable recursion, but bottom-up
  lists are often faster for dense states.
- Delete old layers that cannot be used again.

## Visual worked example: keep two grid rows

```text
full table:
row 0  [1, 1, 1, 1]
row 1  [1, 2, 3, 4]
row 2  [1, 3, 6,10]

to compute row 2, only row 1 is read

rolling state:
previous = [1,2,3,4]
current  = [1,3,6,10]
swap; reuse the old list for the next row
```

Before compressing further, check whether updates would overwrite a value still
needed later in the same iteration.

## Traps

- `[[0] * columns] * rows` creates shared rows.
- In-place compression can read states from the current iteration accidentally.
- Recursive memoization may exceed stack depth.
- Storing full paths in every state causes huge copying; store parent choices.
