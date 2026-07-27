# 03. Find the Smallest Number

**What you learn:** List traversal and comparison.

## Problem

Given a non-empty list of integers, return its smallest number.

## Example

```text
Input: numbers = [5, 2, 9, 1]
Output: 1
```

## Simple idea

Keep the smallest number seen so far. Update it when a smaller number appears.

## Python solution

```python
def find_smallest(numbers: list[int]) -> int:
    if len(numbers) == 0:
        raise ValueError("numbers must not be empty")

    smallest = numbers[0]

    for number in numbers:
        if number < smallest:
            smallest = number

    return smallest
```

## Complexity

- Time: `O(n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

