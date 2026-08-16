# Focus300 223: LeetCode 120 - Triangle

**Source:** [LeetCode 120](https://leetcode.com/problems/triangle/)  
**Difficulty:** Medium  
**Pattern:** bottom-up dynamic programming on a triangle

## Exact contract

Return the minimum path sum from the top of the triangle to the bottom.

## First principles

Every cell depends only on the two cells directly beneath it. That makes the problem ideal for collapsing the triangle upward from the base row.


## Classroom board: choose the best child on each row

```text
       2
      3 4
     6 5 7

    dp on the bottom row rolls upward one row at a time.
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

- A single-row triangle returns that row's value.
- Edge cells have only one child on the next row.
- Negative numbers can change which branch is optimal.
- The path must move one step down-left or down-right each row.

## Brute force

```python
from functools import lru_cache

def minimum_total_brute(triangle):
    @lru_cache(None)
    def solve(r, c):
        if r == len(triangle) - 1:
            return triangle[r][c]
        return triangle[r][c] + min(solve(r + 1, c), solve(r + 1, c + 1))

    return solve(0, 0)
```

Enumerate every root-to-leaf path and sum it.

## Better insight

Store the best cost from each position to the bottom and reuse the row below.

## Expert solution

```python
def minimum_total(triangle):
    dp = triangle[-1][:]
    for r in range(len(triangle) - 2, -1, -1):
        for c in range(len(triangle[r])):
            dp[c] = triangle[r][c] + min(dp[c], dp[c + 1])
    return dp[0]
```

Walk upward from the last row, overwriting each cell with its value plus the smaller of its two children.

**Complexity:** O(n^2) time and O(n) space, or O(1) extra space if the triangle itself is reused.
