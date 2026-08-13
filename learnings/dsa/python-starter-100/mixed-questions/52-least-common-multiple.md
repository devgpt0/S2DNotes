# 52. Find the Least Common Multiple

**What you learn:** GCD and arithmetic.

## Problem

Return the least common multiple of two positive integers.

## Example

```text
Input: first = 6, second = 8
Output: 24
```

## Simple idea

First find the GCD, then use `LCM = first × second ÷ GCD`.

## Python solution

```python
def least_common_multiple(first: int, second: int) -> int:
    if first <= 0 or second <= 0:
        raise ValueError("numbers must be positive")

    left = first
    right = second

    while right != 0:
        left, right = right, left % right

    gcd = left
    return first * second // gcd
```

## Complexity

- Time: `O(log(min(a, b)))`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

