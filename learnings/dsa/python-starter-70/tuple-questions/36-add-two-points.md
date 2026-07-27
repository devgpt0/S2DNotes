# 36. Add Two Coordinate Points

**What you learn:** Fixed-size tuples.

## Problem

Add two `(x, y)` coordinate tuples and return the new point.

## Example

```text
Input: first = (2, 1), second = (3, 4)
Output: (5, 5)
```

## Simple idea

Add the x values together and the y values together.

## Python solution

```python
def add_points(
    first: tuple[int, int], second: tuple[int, int]
) -> tuple[int, int]:
    x = first[0] + second[0]
    y = first[1] + second[1]
    return x, y
```

## Complexity

- Time: `O(1)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

