# Focus300 295: LeetCode 300 - Longest Increasing Subsequence

**Source:** [LeetCode 300](https://leetcode.com/problems/longest-increasing-subsequence/)  
**Difficulty:** Medium  
**Pattern:** patience sorting / subsequence DP

## Exact contract

Return the length of the longest strictly increasing subsequence.

## First principles

The subsequence only needs to stay increasing, not contiguous. That lets the algorithm track the smallest possible tail for each length or run a classic quadratic DP.


## Classroom board: keep the smallest tail for each length

```text
    nums = [10, 9, 2, 5, 3, 7]

    tails length 1 -> 2
    tails length 2 -> 3
    tails length 3 -> 7
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
