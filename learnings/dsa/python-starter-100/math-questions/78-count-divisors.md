# 78. Count a Number's Divisors

**What you learn:** Factor pairs.

## Problem

Return how many positive divisors a positive number has.

## Example

```text
Input: number = 12
Output: 6
```

## Simple idea

A divisor below the square root has a matching divisor above it.

## Python solution

```python
def count_divisors(number: int) -> int:
    if number < 1:
        raise ValueError("number must be positive")

    count = 0
    factor = 1
    while factor * factor <= number:
        if number % factor == 0:
            count += 1
            if factor != number // factor:
                count += 1
        factor += 1

    return count
```

## Complexity

- Time: `O(sqrt(n))`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.
