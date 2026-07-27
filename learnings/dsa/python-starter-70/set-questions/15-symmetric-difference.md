# 15. Find Values in Exactly One Set

**What you learn:** Symmetric difference.

## Problem

Return values that occur in one set, but not in both sets.

## Example

```text
Input: left = {1, 2}, right = {2, 3}
Output: {1, 3}
```

## Simple idea

Use `^` to calculate the symmetric difference.

## Python solution

```python
def values_in_one_set(left: set[int], right: set[int]) -> set[int]:
    return left ^ right
```

## Complexity

- Time: `O(n + m)`
- Extra space: `O(n + m)`

Try to write the solution yourself before reading the code.

