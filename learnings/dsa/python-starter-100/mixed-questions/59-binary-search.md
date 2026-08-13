# 59. Binary Search

**What you learn:** Searching a sorted list.

## Problem

Given a list sorted in ascending order, return the target's index or `-1`.

## Example

```text
Input: numbers = [1, 3, 5, 7, 9], target = 7
Output: 3
```

## Simple idea

Check the middle value and discard the half that cannot contain the target.

## Python solution

```python
def binary_search(numbers: list[int], target: int) -> int:
    left = 0
    right = len(numbers) - 1

    while left <= right:
        middle = (left + right) // 2

        if numbers[middle] == target:
            return middle
        if numbers[middle] < target:
            left = middle + 1
        else:
            right = middle - 1

    return -1
```

## Complexity

- Time: `O(log n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

