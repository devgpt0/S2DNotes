# 10. Merge Two Sorted Lists

**What you learn:** Two indexes.

## Problem

Given two lists sorted in ascending order, return one sorted list containing every value.

## Example

```text
Input: left = [1, 4, 7], right = [2, 3, 8]
Output: [1, 2, 3, 4, 7, 8]
```

## Simple idea

Compare the current value in each list. Append the smaller value and move that index.

## Python solution

```python
def merge_sorted_lists(left: list[int], right: list[int]) -> list[int]:
    merged: list[int] = []
    left_index = 0
    right_index = 0

    while left_index < len(left) and right_index < len(right):
        if left[left_index] <= right[right_index]:
            merged.append(left[left_index])
            left_index = left_index + 1
        else:
            merged.append(right[right_index])
            right_index = right_index + 1

    while left_index < len(left):
        merged.append(left[left_index])
        left_index = left_index + 1

    while right_index < len(right):
        merged.append(right[right_index])
        right_index = right_index + 1

    return merged
```

## Complexity

- Time: `O(n + m)`
- Extra space: `O(n + m)`

Try to write the solution yourself before reading the code.

