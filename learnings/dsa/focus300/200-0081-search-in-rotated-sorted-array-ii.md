# Focus300 200: LeetCode 81 - Search in Rotated Sorted Array II

**Source:** [LeetCode 81](https://leetcode.com/problems/search-in-rotated-sorted-array-ii/)  
**Difficulty:** Medium  
**Pattern:** modified binary search with duplicate trimming

## Exact contract

Determine whether the target exists in a rotated sorted array that may contain duplicates.

## First principles

Rotation preserves sorted halves except for the pivot, so binary search still works once the ambiguous duplicate edges are trimmed away. The challenge is deciding which half is definitely ordered when equal values blur the comparison.

## Cases that decide correctness

- All-equal arrays need duplicate trimming before the half decision is meaningful.
- The target may sit exactly at the pivot.
- A one-element array is still searchable.
- Duplicate values can force a temporary linear step, but the search logic stays binary in spirit.

## Brute force

```python
def search_brute(nums, target):
    for i, num in enumerate(nums):
        if num == target:
            return True
    return False
```

Scan the array linearly until the target is found or the list ends.

## Better insight

Use binary search, but shrink equal endpoints whenever they hide the sorted half.

## Expert solution

```python
def search(nums, target):
    left = 0
    right = len(nums) - 1
    while left <= right:
        while left < right and nums[left] == nums[left + 1]:
            left += 1
        while left < right and nums[right] == nums[right - 1]:
            right -= 1
        mid = (left + right) // 2
        if nums[mid] == target:
            return True
        if nums[left] <= nums[mid]:
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
    return False
```

Compare the midpoint against the endpoints, discard the impossible half, and trim duplicate boundaries whenever the ordering test is inconclusive.

**Complexity:** O(log n) average behavior with duplicate-driven worst-case O(n) time and O(1) space.
