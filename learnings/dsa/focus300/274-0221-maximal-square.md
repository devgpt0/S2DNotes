# Focus300 274: LeetCode 221 - Maximal Square

**Source:** [LeetCode 221](https://leetcode.com/problems/maximal-square/)  
**Difficulty:** Medium  
**Pattern:** grid dynamic programming

## Exact contract

Return the area of the largest square consisting only of `1`s.

## First principles

A square ending at a cell exists only if the cell itself is `1` and its top, left, and top-left neighbors can support a smaller square. The minimum of those three side lengths determines the current cell.


## Classroom board: reuse the three neighboring squares

```text
    1 1 1
    1 1 1

    a cell can extend a square only if its top, left, and top-left cells
    already support it.
```



## Step-by-step transformation

1. Turn the input into subproblems, prefixes, or states that can be reused.
2. Fill the base cases first so later states have something correct to build on.
3. Update each new state from earlier states while keeping the recurrence valid.
4. Read the answer from the final table entry or the best state collected at the end.

Dynamic-programming style notes transform the input by compressing many repeated choices into a small set of reusable states.


## Diagram: state table to answer

```text

            input
                |
                v
            base states
                |
                v
            reuse smaller states
                |
                v
            final dp answer
```

These notes compress repeated choices into reusable states, then read the answer from the last state that matters.

## Cases that decide correctness

- A board of all zeroes returns zero area.
- A one-cell square has area one.
- Squares are determined by side length, not by count of ones.
- The DP can be stored in place or in a rolling row.

## Brute force

```python
def maximal_square_brute(matrix):
    rows = len(matrix)
    cols = len(matrix[0]) if rows else 0
    best = 0
    for r in range(rows):
        for c in range(cols):
            side = 1
            while r + side <= rows and c + side <= cols and all(
                matrix[i][j] == "1" for i in range(r, r + side) for j in range(c, c + side)
            ):
                best = max(best, side)
                side += 1
    return best * best
```

Check every possible square and test all of its cells.

## Better insight

Use the three-neighbor recurrence to build the best square size ending at each cell.

## Expert solution

```python
def maximal_square(matrix):
    if not matrix:
        return 0
    rows = len(matrix)
    cols = len(matrix[0])
    dp = [0] * (cols + 1)
    best = 0
    for r in range(1, rows + 1):
        prev = 0
        for c in range(1, cols + 1):
            temp = dp[c]
            if matrix[r - 1][c - 1] == "1":
                dp[c] = 1 + min(dp[c], dp[c - 1], prev)
                best = max(best, dp[c])
            else:
                dp[c] = 0
            prev = temp
    return best * best
```

Fill a DP table where each `1` cell becomes one plus the minimum of its top, left, and top-left neighbors, then square the maximum side length.

**Complexity:** O(m*n) time and O(m*n) space, or O(n) with a rolling row.
