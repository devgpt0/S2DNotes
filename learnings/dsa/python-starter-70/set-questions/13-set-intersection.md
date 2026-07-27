# 13. Find Common Set Values

**What you learn:** Set intersection.

## Problem

Return the values that appear in both sets.

## Example

```text
Input: left = {1, 2, 3}, right = {2, 3, 4}
Output: {2, 3}
```

## Simple idea

Use the intersection operator `&` to keep shared values.

## Python solution

```python
def common_values(left: set[int], right: set[int]) -> set[int]:
    return left & right
```

## Complexity

- Time: `O(min(n, m))`
- Extra space: `O(min(n, m))`

Try to write the solution yourself before reading the code.

