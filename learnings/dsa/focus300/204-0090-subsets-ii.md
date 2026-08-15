# Focus300 204: LeetCode 90 - Subsets II

**Source:** [LeetCode 90](https://leetcode.com/problems/subsets-ii/)  
**Difficulty:** Medium  
**Pattern:** power-set construction with duplicate pruning

## Exact contract

Return every subset of the input values, including the empty subset, without repeating the same subset.

## First principles

Each value either joins the current subset or skips it, so the answer is the power set. Duplicates require a stable ordering rule so identical values do not generate the same subset twice.

## Cases that decide correctness

- An empty input returns only the empty subset.
- Duplicate values need start-position pruning in the recursive case.
- The empty subset must appear exactly once.
- Every emitted subset should represent a unique membership pattern.

## Brute force

```python
def subsets_with_dup_brute(nums):
    nums.sort()
    result = [[]]
    for num in nums:
        result += [subset + [num] for subset in result]
    unique = []
    seen = set()
    for subset in result:
        key = tuple(subset)
        if key not in seen:
            seen.add(key)
            unique.append(subset)
    return unique
```

Try every include/skip mask and deduplicate the finished subsets.

## Better insight

Grow the answer one value at a time and only extend the subsets produced in the previous layer when duplicates appear.

## Expert solution

```python
def subsets_with_dup(nums):
    nums.sort()
    result = []
    path = []

    def backtrack(start):
        result.append(path.copy())
        for i in range(start, len(nums)):
            if i > start and nums[i] == nums[i - 1]:
                continue
            path.append(nums[i])
            backtrack(i + 1)
            path.pop()

    backtrack(0)
    return result
```

Track the current index, skip repeated siblings where needed, and append copies of the current path whenever a complete subset is reached.

**Complexity:** O(n * 2^n) time and O(n * 2^n) space for the output.
