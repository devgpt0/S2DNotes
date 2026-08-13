# 16. Check Whether One Set Is a Subset

**What you learn:** Subset checking.

## Problem

Return `True` when every value in the smaller set is present in the larger set.

## Example

```text
Input: small = {1, 2}, large = {1, 2, 3}
Output: True
```

## Simple idea

Use `<=` to ask whether all values on the left exist on the right.

## Python solution

```python
def is_subset(small: set[int], large: set[int]) -> bool:
    return small <= large
```

## Complexity

- Time: `O(n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

