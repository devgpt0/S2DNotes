# 51. Find the Greatest Common Divisor

**What you learn:** Euclid's algorithm.

## Problem

Return the greatest common divisor of two positive integers.

## Example

```text
Input: first = 12, second = 18
Output: 6
```

## Simple idea

Replace the pair with the second number and the remainder until the remainder is zero.

## Python solution

```python
def greatest_common_divisor(first: int, second: int) -> int:
    if first <= 0 or second <= 0:
        raise ValueError("numbers must be positive")

    while second != 0:
        remainder = first % second
        first = second
        second = remainder

    return first
```

## Complexity

- Time: `O(log(min(a, b)))`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

