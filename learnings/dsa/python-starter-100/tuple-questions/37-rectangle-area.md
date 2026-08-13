# 37. Calculate Rectangle Area

**What you learn:** Tuple unpacking.

## Problem

A tuple contains `(length, width)`. Return the rectangle's area.

## Example

```text
Input: dimensions = (5, 3)
Output: 15
```

## Simple idea

Unpack the two values and multiply them.

## Python solution

```python
def rectangle_area(dimensions: tuple[int, int]) -> int:
    length, width = dimensions
    return length * width
```

## Complexity

- Time: `O(1)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

