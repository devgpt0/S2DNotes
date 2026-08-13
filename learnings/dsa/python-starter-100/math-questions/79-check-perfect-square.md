# 79. Check a Perfect Square

**What you learn:** Integer square roots.

## Problem

Return `True` when a non-negative number is the square of an integer.

## Example

```text
Input: number = 144
Output: True
```

## Simple idea

Find the integer square root and multiply it by itself to check.

## Python solution

```python
from math import isqrt


def is_perfect_square(number: int) -> bool:
    if number < 0:
        return False

    root = isqrt(number)
    return root * root == number
```

## Complexity

- Time: `O(1)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.
