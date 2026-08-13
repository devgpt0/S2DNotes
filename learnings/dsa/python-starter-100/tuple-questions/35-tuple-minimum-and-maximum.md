# 35. Find a Tuple's Minimum and Maximum

**What you learn:** Tuple traversal and comparison.

## Problem

Given a non-empty tuple, return its smallest and largest values.

## Example

```text
Input: values = (4, 1, 9, 3)
Output: (1, 9)
```

## Simple idea

Track both the smallest and largest values during one loop.

## Python solution

```python
def minimum_and_maximum(
    values: tuple[int, ...]
) -> tuple[int, int]:
    if len(values) == 0:
        raise ValueError("values must not be empty")

    smallest = values[0]
    largest = values[0]

    for value in values:
        if value < smallest:
            smallest = value
        if value > largest:
            largest = value

    return smallest, largest
```

## Complexity

- Time: `O(n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

