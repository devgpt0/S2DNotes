# 32. Swap Two Values

**What you learn:** Tuple packing and unpacking.

## Problem

Given two integers, return them in swapped order.

## Example

```text
Input: left = 3, right = 8
Output: (8, 3)
```

## Simple idea

Python can pack two values directly into a tuple in the return statement.

## Python solution

```python
def swap_values(left: int, right: int) -> tuple[int, int]:
    return right, left
```

## Complexity

- Time: `O(1)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

