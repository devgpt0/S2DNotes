# ICPC300 257: Codeforces 1102F - Elongated Matrix

**Source:** [Codeforces 1102F - Elongated Matrix](https://codeforces.com/problemset/problem/1102/F)  
**Rating:** 2200  
**Pattern:** Hamiltonian bottleneck bitmask DP with a shifted closing edge  
**Goal:** Permute all matrix rows to maximize the minimum absolute difference
between equal columns of consecutive rows and between column `j` of the last
row and column `j+1` of the first row.

## 1. First principles

Precompute two bottleneck values:

```text
normal[u][v] = min_j |matrix[u][j] - matrix[v][j]|
closing[u][v] = min_j |matrix[u][j] - matrix[v][j+1]|
```

For each fixed first row, a subset DP finds the best minimum `normal` edge along
a Hamiltonian path. Closing the full path uses the different shifted value.

## 2. Cases that decide correctness

- Every row appears exactly once.
- Path transitions compare equal column indices.
- Only the final-to-first comparison shifts the first row by one column.
- A one-row matrix still uses the shifted self-comparison.
- At least two columns are required by the source's closing comparison.

## 3. Brute force: enumerate every row order

```python
from itertools import permutations


def elongated_matrix_score_brute(matrix: list[list[int]]) -> int:
    if (
        not matrix
        or len(matrix[0]) < 2
        or any(len(row) != len(matrix[0]) for row in matrix)
    ):
        raise ValueError("matrix must be rectangular with at least two columns")

    row_count = len(matrix)
    column_count = len(matrix[0])
    answer = 0
    for order in permutations(range(row_count)):
        score = min(
            abs(matrix[order[-1]][column] - matrix[order[0]][column + 1])
            for column in range(column_count - 1)
        )
        for index in range(row_count - 1):
            score = min(
                score,
                min(
                    abs(matrix[order[index]][column] - matrix[order[index + 1]][column])
                    for column in range(column_count)
                ),
            )
        answer = max(answer, score)
    return answer
```

**Complexity:** `O(rows! * rows * columns)` time and `O(rows)` space.

## 4. Better transition: maximize a path bottleneck

For a fixed start, the best partial ordering depends only on its used row mask,
last row, and current minimum edge. Extending takes the minimum with one
precomputed row-pair value, exactly the standard bottleneck Hamiltonian DP.

## 5. Expert solution: start-anchored subset DP

```python
def elongated_matrix_score(matrix: list[list[int]]) -> int:
    if (
        not matrix
        or len(matrix[0]) < 2
        or any(len(row) != len(matrix[0]) for row in matrix)
    ):
        raise ValueError("matrix must be rectangular with at least two columns")

    row_count = len(matrix)
    column_count = len(matrix[0])
    normal = [[0] * row_count for _ in range(row_count)]
    closing = [[0] * row_count for _ in range(row_count)]
    for first in range(row_count):
        for second in range(row_count):
            normal[first][second] = min(
                abs(matrix[first][column] - matrix[second][column])
                for column in range(column_count)
            )
            closing[first][second] = min(
                abs(matrix[first][column] - matrix[second][column + 1])
                for column in range(column_count - 1)
            )

    full_mask = (1 << row_count) - 1
    infinity = 10**30
    answer = 0
    for start in range(row_count):
        dp = [[-1] * row_count for _ in range(1 << row_count)]
        dp[1 << start][start] = infinity
        for mask in range(1 << row_count):
            for last in range(row_count):
                if dp[mask][last] < 0:
                    continue
                for next_row in range(row_count):
                    if mask >> next_row & 1 == 0:
                        next_mask = mask | (1 << next_row)
                        dp[next_mask][next_row] = max(
                            dp[next_mask][next_row],
                            min(dp[mask][last], normal[last][next_row]),
                        )
        for last in range(row_count):
            answer = max(
                answer,
                min(dp[full_mask][last], closing[last][start]),
            )
    return answer
```

### Why the expert code is correct

For a fixed first row, every row permutation corresponds to one sequence of DP
extensions. The state value is the largest possible minimum normal edge for its
mask and endpoint, preserved by the max-min transition. Every complete path is
then evaluated with its exact shifted closing edge, so maximizing over endpoints
and starts checks every legal permutation.

**Complexity:** `O(rows^3 2^rows + rows^2 * columns)` time and
`O(rows 2^rows)` space.

## 6. What to remember

```text
row ordering -> Hamiltonian path over rows
maximize minimum edge -> bottleneck subset DP
special last-first rule -> apply only when closing the path
```
