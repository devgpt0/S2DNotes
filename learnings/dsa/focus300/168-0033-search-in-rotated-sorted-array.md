# Focus300 168: LeetCode 33 - Search in Rotated Sorted Array

**Source:** [LeetCode 33](https://leetcode.com/problems/search-in-rotated-sorted-array/)  
**Difficulty:** Medium  
**Pattern:** binary search using the sorted half invariant

## Exact contract

A strictly increasing array of distinct integers was possibly rotated at one
pivot. Return the index of `target`, or `-1` when absent, in `O(log n)` search
time.

## First principles

For any binary-search interval in a rotated sorted array, at least one half is
normally ordered. Determine which half by comparing its endpoints, then test
whether the target lies inside that half's value range. Keep that half when it
can contain the target; otherwise discard it.


## Classroom board: decide which half is sorted

```text
    rotated = [4, 5, 6, 7, 0, 1, 2]

    one half is always sorted, so the target must live in the half that
    still contains its value range.
```



## Step-by-step transformation

1. Compare the middle position with the target rule or boundary condition.
2. Discard the half that cannot still contain a valid answer.
3. Repeat until the remaining interval is exactly the split or value the problem asks for.
4. Convert the final boundary positions into the required output.

Binary-search style notes transform the input by shrinking the search space until only one valid boundary or value remains.


## Diagram: discard half the search space

```text

            sorted input
                |
                v
            check middle
                |
                v
            keep the half that can still work
                |
                v
            final boundary / value
```

Binary search keeps shrinking the input until only the valid boundary or value is left.

## Cases that decide correctness

- An unrotated array follows ordinary binary search.
- A one-element array may contain or miss the target.
- The pivot may lie immediately beside the midpoint.
- Distinct values make sorted-half detection unambiguous.
- Bounds are inclusive, so range comparisons must match pointer updates.

## Brute force: linear scan

```python
def rotated_search_brute(numbers: list[int], target: int) -> int:
    if type(numbers) is not list or not 1 <= len(numbers) <= 5_000:
        raise ValueError("numbers length must be between 1 and 5,000")
    if any(
        type(value) is not int or not -10_000 <= value <= 10_000 for value in numbers
    ):
        raise ValueError("numbers must be integers in the source range")
    if len(set(numbers)) != len(numbers):
        raise ValueError("numbers must be distinct")
    if type(target) is not int or not -10_000 <= target <= 10_000:
        raise ValueError("target must be an integer in the source range")

    for index, value in enumerate(numbers):
        if value == target:
            return index
    return -1
```

This ignores the rotated ordering and takes `O(n)` search time.

## Better insight: rotation breaks global order but preserves one midpoint half

The midpoint belongs to either the left sorted run or the right sorted run. One
endpoint comparison identifies a normally ordered half on every iteration.

## Expert solution: sorted-half binary search

```python
def rotated_search(numbers: list[int], target: int) -> int:
    if type(numbers) is not list or not 1 <= len(numbers) <= 5_000:
        raise ValueError("numbers length must be between 1 and 5,000")
    if any(
        type(value) is not int or not -10_000 <= value <= 10_000 for value in numbers
    ):
        raise ValueError("numbers must be integers in the source range")
    if len(set(numbers)) != len(numbers):
        raise ValueError("numbers must be distinct")
    if type(target) is not int or not -10_000 <= target <= 10_000:
        raise ValueError("target must be an integer in the source range")

    left = 0
    right = len(numbers) - 1
    while left <= right:
        middle = (left + right) // 2
        if numbers[middle] == target:
            return middle
        if numbers[left] <= numbers[middle]:
            if numbers[left] <= target < numbers[middle]:
                right = middle - 1
            else:
                left = middle + 1
        elif numbers[middle] < target <= numbers[right]:
            left = middle + 1
        else:
            right = middle - 1
    return -1
```

Each branch retains the only half whose ordered value interval can contain the
target, preserving binary search correctness despite the pivot.

**Complexity:** `O(log n)` search time and `O(1)` auxiliary space after input
validation.
