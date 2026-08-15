# Focus300 248: LeetCode 167 - Two Sum II - Input Array Is Sorted

**Source:** [LeetCode 167](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/)  
**Difficulty:** Medium  
**Pattern:** two-pointer search on a sorted array

## Exact contract

Return the one-based indices of two numbers in the sorted array whose sum equals the target.

## First principles

The array is sorted, so the sum moves predictably when either pointer changes. That makes a two-pointer sweep enough to pin down the unique pair.

## Cases that decide correctness

- Exactly one pair is guaranteed by the usual problem contract.
- The answer is one-based, not zero-based.
- Moving the left pointer increases the sum; moving the right pointer decreases it.
- Duplicates are fine as long as the index pair is correct.

## Brute force

```python
def two_sum_brute(numbers, target):
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if numbers[i] + numbers[j] == target:
                return [i + 1, j + 1]
```

Try every pair of indices.

## Better insight

Start at both ends and move inward according to the current sum.

## Expert solution

```python
def two_sum(numbers, target):
    left, right = 0, len(numbers) - 1
    while left < right:
        total = numbers[left] + numbers[right]
        if total == target:
            return [left + 1, right + 1]
        if total < target:
            left += 1
        else:
            right -= 1
```

Use one pointer at the left and one at the right, and adjust the side that makes the sum move toward the target.

**Complexity:** O(n) time and O(1) space.
