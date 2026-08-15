# Focus300 261: LeetCode 198 - House Robber

**Source:** [LeetCode 198](https://leetcode.com/problems/house-robber/)  
**Difficulty:** Medium  
**Pattern:** problem-specific recursion or scanning

## Exact contract

Solve the LeetCode problem 'House Robber' according to the statement and constraints.

## First principles

Most interview-style problems reduce to the right state definition. Once that state is explicit, the rest is choosing the simplest way to preserve it.

## Cases that decide correctness

- Check the empty and single-item boundary first.
- Look for duplicate handling and off-by-one errors.
- Confirm whether the answer is a boolean, count, value, or structure.
- Make sure the invariant survives every update step.

## Brute force

```python
from functools import lru_cache

def rob_brute(nums):
    @lru_cache(None)
    def solve(i):
        if i >= len(nums):
            return 0
        return max(solve(i + 1), nums[i] + solve(i + 2))

    return solve(0)
```

Try the most direct exhaustive solution.

## Better insight

Identify the state that can be reused and avoid recomputing it.

## Expert solution

```python
def rob(nums):
    prev2 = prev1 = 0
    for num in nums:
        prev2, prev1 = prev1, max(prev1, prev2 + num)
    return prev1
```

Use the smallest invariant that proves correctness and update it once per step.

**Complexity:** Usually linear or near-linear in the input size, with the exact bound determined by the pattern.
