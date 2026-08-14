# ICPC300 254: Codeforces 1209E2 - Rotate Columns (hard version)

**Source:** [Codeforces 1209E2 - Rotate Columns (hard version)](https://codeforces.com/problemset/problem/1209/E2)  
**Rating:** 2200  
**Pattern:** top-column reduction plus rotation subset DP  
**Goal:** Cyclically rotate each matrix column independently, then maximize the
sum of the maximum value in every row.

## 1. First principles

In an optimal result, assign each row to one column attaining its maximum. At
most `row_count` columns are responsible. Keeping the columns with the largest
individual maxima is sufficient: a discarded responsible column can be
replaced by a kept column and rotated so its at-least-as-large maximum serves
that responsible row.

For each kept column and row subset, try all rotations and record the best sum
on that subset. A mask DP assigns disjoint row subsets to successive columns.

## 2. Cases that decide correctness

- Every column may use a different cyclic rotation.
- One column may provide maxima for several rows.
- Only `min(rows, columns)` highest-maximum columns are needed.
- A column may receive the empty row subset.
- All rows must be assigned by the final mask.

## 3. Brute force: enumerate every column rotation

```python
from itertools import product


def maximum_rotated_columns_brute(matrix: list[list[int]]) -> int:
    if not matrix or not matrix[0] or any(len(row) != len(matrix[0]) for row in matrix):
        raise ValueError("matrix must be nonempty and rectangular")
    if any(value < 0 for row in matrix for value in row):
        raise ValueError("matrix values must be nonnegative")

    row_count = len(matrix)
    column_count = len(matrix[0])
    answer = 0
    for rotations in product(range(row_count), repeat=column_count):
        score = 0
        for row in range(row_count):
            score += max(
                matrix[(row + rotations[column]) % row_count][column]
                for column in range(column_count)
            )
        answer = max(answer, score)
    return answer
```

**Complexity:** `O(rows^columns * rows * columns)` time and `O(1)` space.

## 4. Better transition: assign rows to responsible columns

Once rotations are fixed, each row needs only one column that realizes its
maximum. Reversing that view lets a column own a subset of rows. Because the
row count is small, all subsets and rotations can be precomputed.

## 5. Expert solution: selected-column subset DP

```python
def maximum_rotated_columns(matrix: list[list[int]]) -> int:
    if not matrix or not matrix[0] or any(len(row) != len(matrix[0]) for row in matrix):
        raise ValueError("matrix must be nonempty and rectangular")
    if any(value < 0 for row in matrix for value in row):
        raise ValueError("matrix values must be nonnegative")

    row_count = len(matrix)
    column_count = len(matrix[0])
    selected = sorted(
        range(column_count),
        key=lambda column: max(matrix[row][column] for row in range(row_count)),
        reverse=True,
    )[: min(row_count, column_count)]

    mask_count = 1 << row_count
    best_by_column: list[list[int]] = []
    for column in selected:
        best = [0] * mask_count
        for rotation in range(row_count):
            subset_sum = [0] * mask_count
            for mask in range(1, mask_count):
                bit = mask & -mask
                row = bit.bit_length() - 1
                subset_sum[mask] = (
                    subset_sum[mask ^ bit]
                    + matrix[(row + rotation) % row_count][column]
                )
                best[mask] = max(best[mask], subset_sum[mask])
        best_by_column.append(best)

    negative_infinity = -(10**30)
    dp = [negative_infinity] * mask_count
    dp[0] = 0
    full_mask = mask_count - 1
    for best in best_by_column:
        next_dp = dp.copy()
        for used, current in enumerate(dp):
            if current == negative_infinity:
                continue
            remaining = full_mask ^ used
            subset = remaining
            while subset:
                next_dp[used | subset] = max(
                    next_dp[used | subset], current + best[subset]
                )
                subset = (subset - 1) & remaining
        dp = next_dp
    return dp[full_mask]
```

### Why the expert code is correct

The top-column argument preserves an optimum using at most one responsible
column per row. For a kept column, `best[mask]` tries every legal rotation and
is exactly its best contribution to those assigned rows. The DP partitions all
rows among columns with disjoint masks, so every feasible assignment appears
and its sum equals the corresponding row maxima.

**Complexity:** `O(k * (rows * 2^rows + 3^rows))` time and `O(k 2^rows)` space,
where `k = min(rows, columns)`.

## 6. What to remember

```text
row maxima -> assign each row to one responsible column
at most rows responsible columns -> keep top column maxima
column rotation plus chosen rows -> subset precomputation
```
