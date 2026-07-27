# 17. Check Whether Sets Are Disjoint

**What you learn:** Set membership.

## Problem

Return `True` when two sets have no values in common.

## Example

```text
Input: left = {1, 2}, right = {3, 4}
Output: True
```

## Simple idea

The `isdisjoint()` method checks whether the intersection is empty.

## Python solution

```python
def are_disjoint(left: set[int], right: set[int]) -> bool:
    return left.isdisjoint(right)
```

## Complexity

- Time: `O(min(n, m))`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

