# 69. Calculate a Power

**What you learn:** Repeated multiplication.

## Problem

Return `base` raised to a non-negative integer exponent without using `**`.

## Example

```text
Input: base = 3, exponent = 4
Output: 81
```

## Simple idea

Start with 1 and multiply by the base once for each exponent step.

## Python solution

```python
def calculate_power(base: int, exponent: int) -> int:
    if exponent < 0:
        raise ValueError("exponent must not be negative")

    result = 1

    for _ in range(exponent):
        result = result * base

    return result
```

## Complexity

- Time: `O(exponent)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

