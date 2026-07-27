# 60. Check Whether a List Is Sorted

**What you learn:** Comparing neighbours.

## Problem

Return `True` when a list is sorted in ascending order.

## Example

```text
Input: numbers = [1, 2, 2, 5]
Output: True
```

## Simple idea

Compare each number with the number immediately before it.

## Python solution

```python
def is_sorted(numbers: list[int]) -> bool:
    for index in range(1, len(numbers)):
        if numbers[index] < numbers[index - 1]:
            return False

    return True
```

## Complexity

- Time: `O(n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

