# 50. Check a Prime Number

**What you learn:** Divisibility.

## Problem

Return `True` when an integer is prime.

## Example

```text
Input: number = 29
Output: True
```

## Simple idea

Try divisors starting at 2. Stop when the divisor squared becomes larger than the number.

## Python solution

```python
def is_prime(number: int) -> bool:
    if number < 2:
        return False

    divisor = 2

    while divisor * divisor <= number:
        if number % divisor == 0:
            return False

        divisor = divisor + 1

    return True
```

## Complexity

- Time: `O(√n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

