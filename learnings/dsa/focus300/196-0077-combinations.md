# Focus300 196: LeetCode 77 - Combinations

**Source:** [LeetCode 77](https://leetcode.com/problems/combinations/)  
**Difficulty:** Medium  
**Pattern:** increasing-choice backtracking with capacity pruning

## Exact contract

Return every size-`k` combination of distinct integers from `1` through `n`.
Order within a combination is conventionally increasing, and result order is
unrestricted.

## First principles

Choosing values in strictly increasing order gives every subset exactly one
construction path. If `remaining` positions are still needed, the next value
cannot exceed `n - remaining + 1`; larger starts leave too few values to finish.

## Cases that decide correctness

- `k = 1` returns every singleton.
- `k = n` returns one full combination.
- Selection order must not create permutations of one combination.
- A path is emitted only at exactly length `k`.
- Capacity pruning changes work, not output.

## Brute force: use the complete Cartesian-free library enumeration

```python
from itertools import combinations


def combinations_brute(upper_bound: int, size: int) -> list[list[int]]:
    if type(upper_bound) is not int or not 1 <= upper_bound <= 20:
        raise ValueError("upper_bound must be an integer from 1 through 20")
    if type(size) is not int or not 1 <= size <= upper_bound:
        raise ValueError("size must be an integer from 1 through upper_bound")
    return [list(values) for values in combinations(range(1, upper_bound + 1), size)]
```

This delegates the generation mechanics and is useful as a compact baseline.

## Better insight: monotone choices eliminate duplicates by construction

Carry only the next allowable value and stop the loop where completing `k`
choices would become impossible.

## Expert solution: pruned increasing backtracking

```python
def combinations_of(upper_bound: int, size: int) -> list[list[int]]:
    if type(upper_bound) is not int or not 1 <= upper_bound <= 20:
        raise ValueError("upper_bound must be an integer from 1 through 20")
    if type(size) is not int or not 1 <= size <= upper_bound:
        raise ValueError("size must be an integer from 1 through upper_bound")

    answer: list[list[int]] = []
    path: list[int] = []

    def build(next_value: int) -> None:
        if len(path) == size:
            answer.append(path.copy())
            return
        remaining = size - len(path)
        last_start = upper_bound - remaining + 1
        for value in range(next_value, last_start + 1):
            path.append(value)
            build(value + 1)
            path.pop()

    build(1)
    return answer
```

Every path is increasing and therefore unique, while the upper loop bound
removes exactly the prefixes that cannot reach the required size.

**Complexity:** `O(k * C(n, k))` output time and `O(k)` auxiliary recursion
space, excluding output.
