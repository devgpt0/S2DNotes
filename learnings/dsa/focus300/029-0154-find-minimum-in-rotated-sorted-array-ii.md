# Focus300 029: LeetCode 154 - Find Minimum in Rotated Sorted Array II

**Source:** [LeetCode 154](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array-ii/)  
**Difficulty:** Hard  
**Pattern:** duplicate-aware binary search

## Exact contract

Given a nonempty nondecreasing array rotated an unknown number of times, return
its minimum value. Duplicate values are allowed.

## First principles

Compare the middle value with the right boundary:

- smaller means the minimum is at middle or to its left;
- larger means the minimum is strictly right of middle;
- equal is ambiguous, but discarding one right-boundary duplicate cannot remove
  the only minimum value.

Duplicates destroy the strict ordering information that guarantees logarithmic
time, so worst-case linear behavior is unavoidable.

## Cases that decide correctness

- The array may be unrotated.
- All values may be equal.
- The minimum may equal the right boundary at several positions.
- Search retains `middle` when it may itself be the minimum.
- The source guarantees a nonempty array.

## Brute force: scan every value

```python
def find_min_brute(values: list[int]) -> int:
    if not values:
        raise ValueError("array must be nonempty")
    return min(values)
```

This is `O(n)` time.

## Better insight: preserve the half that must contain a drop

Strict middle/right comparisons discard half the search interval. Equality is
the only information-free case and safely shrinks it by one.

## Expert solution: duplicate-aware binary search

```python
def find_min(values: list[int]) -> int:
    if not values:
        raise ValueError("array must be nonempty")
    left = 0
    right = len(values) - 1
    while left < right:
        middle = (left + right) // 2
        if values[middle] < values[right]:
            right = middle
        elif values[middle] > values[right]:
            left = middle + 1
        else:
            right -= 1
    return values[left]
```

Every step preserves at least one occurrence of the global minimum in the
closed search interval.

**Complexity:** `O(log n)` average and `O(n)` worst-case time, `O(1)` space.
