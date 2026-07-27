# 47. Sum the Digits of a Number

**What you learn:** Division and remainder.

## Problem

Return the sum of the digits of a non-negative integer.

## Example

```text
Input: number = 482
Output: 14
```

## Simple idea

Use `% 10` to read the last digit and `// 10` to remove it.

## Python solution

```python
def sum_digits(number: int) -> int:
    if number < 0:
        raise ValueError("number must not be negative")

    total = 0

    while number > 0:
        total = total + number % 10
        number = number // 10

    return total
```

## Complexity

- Time: `O(d)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

