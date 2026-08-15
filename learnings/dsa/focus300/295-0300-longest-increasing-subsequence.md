# Focus300 295: LeetCode 300 - Longest Increasing Subsequence

**Source:** [LeetCode 300](https://leetcode.com/problems/longest-increasing-subsequence/)  
**Difficulty:** Medium  
**Pattern:** patience sorting / subsequence DP

## Exact contract

Return the length of the longest strictly increasing subsequence.

## First principles

The subsequence only needs to stay increasing, not contiguous. That lets the algorithm track the smallest possible tail for each length or run a classic quadratic DP.

## Cases that decide correctness

- A non-increasing array still has LIS length one.
- Duplicate values do not extend a strictly increasing subsequence.
- The subsequence need not be unique.
- A shorter tail is always better for future extension.

## Brute force

```python
from functools import lru_cache

def length_of_lis_brute(nums):
    @lru_cache(None)
    def solve(i, prev):
        if i == len(nums):
            return 0
        best = solve(i + 1, prev)
        if prev == -1 or nums[i] > nums[prev]:
            best = max(best, 1 + solve(i + 1, i))
        return best

    return solve(0, -1)
```

Check every subsequence directly.

## Better insight

Maintain the best tail values for subsequence lengths using binary search.

## Expert solution

```python
def length_of_lis(nums):
    tails = []
    for num in nums:
        left, right = 0, len(tails)
        while left < right:
            mid = (left + right) // 2
            if tails[mid] < num:
                left = mid + 1
            else:
                right = mid
        if left == len(tails):
            tails.append(num)
        else:
            tails[left] = num
    return len(tails)
```

Use patience sorting tails or the equivalent `O(n^2)` DP recurrence depending on the required tradeoff.

**Complexity:** O(n log n) with tails, or O(n^2) with straightforward DP.
