# Focus300 271: LeetCode 213 - House Robber II

**Source:** [LeetCode 213](https://leetcode.com/problems/house-robber-ii/)  
**Difficulty:** Medium  
**Pattern:** circular dynamic programming

## Exact contract

Return the maximum amount that can be robbed from a circular street without robbing adjacent houses.

## First principles

The circle breaks the ordinary line DP because the first and last houses are adjacent. Solve two linear subproblems instead: one excluding the first house and one excluding the last.

## Cases that decide correctness

- A one-house street returns that house's value.
- A two-house street can rob only the larger of the two.
- The first and last houses cannot both be taken.
- Each linear subproblem uses the standard house-robber recurrence.

## Brute force

```python
from functools import lru_cache

def rob_brute(nums):
    if len(nums) <= 1:
        return nums[0] if nums else 0

    def rob_line(arr):
        @lru_cache(None)
        def solve(i):
            if i >= len(arr):
                return 0
            return max(solve(i + 1), arr[i] + solve(i + 2))

        return solve(0)

    return max(rob_line(nums[:-1]), rob_line(nums[1:]))
```

Try every subset of houses that avoids adjacency.

## Better insight

Split the circle into two linear cases and reuse the ordinary DP twice.

## Expert solution

```python
def rob(nums):
    def rob_line(arr):
        prev2 = prev1 = 0
        for num in arr:
            prev2, prev1 = prev1, max(prev1, prev2 + num)
        return prev1

    if len(nums) <= 1:
        return nums[0] if nums else 0
    return max(rob_line(nums[:-1]), rob_line(nums[1:]))
```

Run the classic rob/not-rob recurrence on both `[0..n-2]` and `[1..n-1]`, then take the larger result.

**Complexity:** O(n) time and O(1) space.
