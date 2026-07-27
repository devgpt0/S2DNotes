# 61. Bubble Sort

**What you learn:** Nested loops and swapping.

## Problem

Return an ascending copy of a list using bubble sort.

## Example

```text
Input: numbers = [4, 2, 3, 1]
Output: [1, 2, 3, 4]
```

## Simple idea

Repeatedly swap neighbouring values that are in the wrong order.

## Python solution

```python
def bubble_sort(numbers: list[int]) -> list[int]:
    result = numbers.copy()

    for end in range(len(result) - 1, 0, -1):
        for index in range(end):
            if result[index] > result[index + 1]:
                temporary = result[index]
                result[index] = result[index + 1]
                result[index + 1] = temporary

    return result
```

## Complexity

- Time: `O(n²)`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.
