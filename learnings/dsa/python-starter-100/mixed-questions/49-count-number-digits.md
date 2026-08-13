# 49. Count the Digits of a Number

**What you learn:** A while loop.

## Problem

Return the number of digits in a non-negative integer.

## Example

```text
Input: number = 5072
Output: 4
```

## Simple idea

Repeatedly remove the last digit. Zero is a special case with one digit.

## Python solution

```python
def count_digits(number: int) -> int:
    if number < 0:
        raise ValueError("number must not be negative")
    if number == 0:
        return 1

    count = 0

    while number > 0:
        count = count + 1
        number = number // 10

    return count
```

## Complexity

- Time: `O(d)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

