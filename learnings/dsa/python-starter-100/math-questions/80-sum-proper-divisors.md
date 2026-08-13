# 80. Sum Proper Divisors

**What you learn:** Divisor pairs.

## Problem

Return the sum of positive divisors smaller than a positive number.

## Example

```text
Input: number = 12
Output: 16
```

## Simple idea

Start with 1, then add each matching divisor pair below the number.

## Python solution

```python
def sum_proper_divisors(number: int) -> int:
    if number < 1:
        raise ValueError("number must be positive")
    if number == 1:
        return 0

    total = 1
    factor = 2
    while factor * factor <= number:
        if number % factor == 0:
            total += factor
            partner = number // factor
            if partner != factor:
                total += partner
        factor += 1

    return total
```

## Complexity

- Time: `O(sqrt(n))`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.
