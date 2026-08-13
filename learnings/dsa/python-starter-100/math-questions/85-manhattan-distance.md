# 85. Calculate Manhattan Distance

**What you learn:** Coordinate differences.

## Problem

Return the Manhattan distance between two integer grid points.

## Example

```text
Input: first = (1, 2), second = (4, 6)
Output: 7
```

## Simple idea

Add the absolute horizontal difference and the absolute vertical difference.

## Python solution

```python
def manhattan_distance(
    first: tuple[int, int], second: tuple[int, int]
) -> int:
    return abs(first[0] - second[0]) + abs(first[1] - second[1])
```

## Complexity

- Time: `O(1)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.
