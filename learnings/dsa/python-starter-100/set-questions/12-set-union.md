# 12. Find the Union of Two Sets

**What you learn:** Set union.

## Problem

Return all values that appear in either of two sets.

## Example

```text
Input: left = {1, 2}, right = {2, 3}
Output: {1, 2, 3}
```

## Simple idea

Use the union operator `|` to combine all unique values.

## Python solution

```python
def set_union(left: set[int], right: set[int]) -> set[int]:
    return left | right
```

## Complexity

- Time: `O(n + m)`
- Extra space: `O(n + m)`

Try to write the solution yourself before reading the code.

