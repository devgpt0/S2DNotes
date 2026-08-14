# Focus300 012: LeetCode 52 - N-Queens II

**Source:** [LeetCode 52](https://leetcode.com/problems/n-queens-ii/)  
**Difficulty:** Hard  
**Pattern:** counting constraint backtracking

## Exact contract

Given `n` from 1 through 9, return the number of distinct ways to place `n`
queens on an `n x n` board so no two attack each other. Unlike LeetCode 51,
only the count is returned.

## First principles

Choosing one column per row already prevents row conflicts. A partial placement
can be extended only with columns absent from the occupied-column and two
diagonal sets. Counting complete legal prefixes avoids constructing boards.

## Cases that decide correctness

- `n = 1` returns one.
- `n = 2` and `n = 3` return zero.
- Mirror-image boards are distinct solutions.
- A diagonal attack shifts one column between adjacent rows.
- Only complete placements contribute to the answer.

## Brute force: filter every permutation

```python
from itertools import permutations


def total_n_queens_brute(size: int) -> int:
    if not 1 <= size <= 9:
        raise ValueError("size must be between 1 and 9")
    return sum(
        len({row - column for row, column in enumerate(columns)}) == size
        and len({row + column for row, column in enumerate(columns)}) == size
        for columns in permutations(range(size))
    )
```

This takes `O(n! * n)` time and `O(n)` space.

## Better approach: backtrack with occupied sets

```python
def total_n_queens_sets(size: int) -> int:
    if not 1 <= size <= 9:
        raise ValueError("size must be between 1 and 9")

    columns: set[int] = set()
    descending: set[int] = set()
    ascending: set[int] = set()

    def count(row: int) -> int:
        if row == size:
            return 1
        answer = 0
        for column in range(size):
            if (
                column in columns
                or row - column in descending
                or row + column in ascending
            ):
                continue
            columns.add(column)
            descending.add(row - column)
            ascending.add(row + column)
            answer += count(row + 1)
            ascending.remove(row + column)
            descending.remove(row - column)
            columns.remove(column)
        return answer

    return count(0)
```

Set membership rejects an invalid prefix before exploring its descendants.

## Expert solution: count available bits

```python
def total_n_queens(size: int) -> int:
    if not 1 <= size <= 9:
        raise ValueError("size must be between 1 and 9")

    full_mask = (1 << size) - 1

    def count(columns: int, descending: int, ascending: int) -> int:
        if columns == full_mask:
            return 1
        available = full_mask & ~(columns | descending | ascending)
        answer = 0
        while available:
            queen = available & -available
            available ^= queen
            answer += count(
                columns | queen,
                ((descending | queen) << 1) & full_mask,
                (ascending | queen) >> 1,
            )
        return answer

    return count(0, 0, 0)
```

The masks contain exactly the columns forbidden in the current row. Every
complete root-to-leaf choice sequence represents one board, so summing leaf
counts returns the exact number without materializing solutions.

**Complexity:** `O(n!)` worst-case time and `O(n)` recursion space.
