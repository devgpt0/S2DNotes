# Focus300 298: LeetCode 307 - Range Sum Query - Mutable

**Source:** [LeetCode 307](https://leetcode.com/problems/range-sum-query-mutable/)  
**Difficulty:** Medium  
**Pattern:** prefix sums and indexed updates

## Exact contract

Support rectangle sum queries, and for the mutable variant also support point updates efficiently.

## First principles

A prefix table turns a rectangle sum into four cached lookups. If the matrix is mutable, a Fenwick tree or segment tree preserves those sums under updates.


## Classroom board: turn a range into two prefixes

```text
a subarray sum becomes prefix[right] - prefix[left], so one prefix table
replaces many repeated range scans.
```



## Step-by-step transformation

1. Compress the input into counts, prefixes, bit masks, or another compact state.
2. Update that state once per element instead of recomputing earlier work.
3. Combine the stored pieces to recover the value the problem asks for.
4. Return the final count, sum, or constructed answer.

These notes transform input into output by reducing the data to a compact invariant first, then rebuilding the answer from that invariant.


## Diagram: compress the input first

```text

            raw values
                |
                v
            counts / prefix / bit state
                |
                v
            combine stored facts
                |
                v
            final answer
```

The algorithm first compresses the input into a small invariant, then rebuilds the answer from that compact state.

## Cases that decide correctness

- Single-cell queries should still work.
- Rectangle boundaries are inclusive under the usual problem contract.
- Updates must affect future queries only.
- Mutable structures must trade a little more setup for faster repeated queries.

## Brute force

```python
class NumMatrixBrute:
    def __init__(self, matrix):
        self.matrix = matrix

    def sumRegion(self, row1, col1, row2, col2):
        return sum(
            self.matrix[r][c]
            for r in range(row1, row2 + 1)
            for c in range(col1, col2 + 1)
        )
```

Recompute every query by scanning the whole rectangle.

## Better insight

Use a 2D prefix sum for immutable data or a tree structure for point updates.

## Expert solution

```python
class NumMatrix:
    def __init__(self, matrix):
        rows = len(matrix)
        cols = len(matrix[0]) if rows else 0
        self.prefix = [[0] * (cols + 1) for _ in range(rows + 1)]
        for r in range(rows):
            for c in range(cols):
                self.prefix[r + 1][c + 1] = (
                    matrix[r][c]
                    + self.prefix[r][c + 1]
                    + self.prefix[r + 1][c]
                    - self.prefix[r][c]
                )

    def sumRegion(self, row1, col1, row2, col2):
        p = self.prefix
        return p[row2 + 1][col2 + 1] - p[row1][col2 + 1] - p[row2 + 1][col1] + p[row1][col1]
```

Answer immutable queries by inclusion-exclusion on prefix sums, and answer mutable queries by maintaining indexed partial sums.

**Complexity:** Immutable: O(1) query after O(m*n) build. Mutable: typically O(log n) per update/query with a Fenwick or segment tree variant.
