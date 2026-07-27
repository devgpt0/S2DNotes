# 58. Linear Search

**What you learn:** Searching from left to right.

## Problem

Return the first index of a target in a list, or `-1` when it is absent.

## Example

```text
Input: numbers = [7, 2, 9, 4], target = 9
Output: 2
```

## Simple idea

Check every list index in order and stop at the first match.

## Python solution

```python
def linear_search(numbers: list[int], target: int) -> int:
    for index in range(len(numbers)):
        if numbers[index] == target:
            return index

    return -1
```

## Complexity

- Time: `O(n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

