# 48. Reverse a Number

**What you learn:** Building a number digit by digit.

## Problem

Reverse the digits of a non-negative integer.

## Example

```text
Input: number = 1204
Output: 4021
```

## Simple idea

Take the last digit and append it to the end of the reversed number.

## Python solution

```python
def reverse_number(number: int) -> int:
    if number < 0:
        raise ValueError("number must not be negative")

    reversed_number = 0

    while number > 0:
        digit = number % 10
        reversed_number = reversed_number * 10 + digit
        number = number // 10

    return reversed_number
```

## Complexity

- Time: `O(d)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

