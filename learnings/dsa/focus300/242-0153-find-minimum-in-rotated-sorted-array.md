# Focus300 242: LeetCode 153 - Find Minimum in Rotated Sorted Array

**Source:** [LeetCode 153](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/)  
**Difficulty:** Medium  
**Pattern:** binary search on a rotated order

## Exact contract

Return the minimum element in a rotated sorted array.

## First principles

The minimum is the pivot point between two sorted halves. Binary search can discard the sorted half that cannot contain the pivot.

## Cases that decide correctness

- A fully sorted array returns its first element.
- The pivot may be at index zero in the unrotated case.
- A one-element array returns that element.
- The comparison must distinguish the sorted side from the wrapped side.

## Brute force

```python
def find_min_brute(nums):
    return min(nums)
```

Scan the entire array for the smallest value.

## Better insight

Use binary search to keep only the half that can still contain the pivot.

## Expert solution

```python
def find_min(nums):
    left, right = 0, len(nums) - 1
    while left < right:
        mid = (left + right) // 2
        if nums[mid] > nums[right]:
            left = mid + 1
        else:
            right = mid
    return nums[left]
```

Compare midpoint and boundary values, then move the search window toward the unsorted side until only the minimum remains.

**Complexity:** O(log n) time and O(1) space.
