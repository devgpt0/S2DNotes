# 81. Check a Perfect Number

**What you learn:** Using divisor sums.

## Problem

Return `True` when a positive number equals the sum of its proper divisors.

## Example

```text
Input: number = 28
Output: True
```

## Simple idea

Find the proper-divisor sum and compare it with the number.

## Python solution

```python
def is_perfect_number(number: int) -> bool:
    if number < 1:
        return False
    if number == 1:
        return False

    total = 1
    factor = 2
    while factor * factor <= number:
        if number % factor == 0:
            total += factor
            partner = number // factor
            if partner != factor:
                total += partner
        factor += 1

    return total == number
```

## Complexity

- Time: `O(sqrt(n))`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.
