# 14. Find Values Only in the First Set

**What you learn:** Set difference.

## Problem

Return values that occur in the first set but not in the second.

## Example

```text
Input: left = {1, 2, 3}, right = {2, 4}
Output: {1, 3}
```

## Simple idea

Use the difference operator `-` to remove values found in the second set.

## Python solution

```python
def values_only_in_first(left: set[int], right: set[int]) -> set[int]:
    return left - right
```

## Complexity

- Time: `O(n)`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.

