# 82. Find a Number's Digital Root

**What you learn:** Repeated digit sums.

## Problem

Keep summing a non-negative number's digits until one digit remains.

## Example

```text
Input: number = 9875
Output: 2
```

## Simple idea

Turn the number into text, sum its digits, and repeat while it has two or more digits.

## Python solution

```python
def digital_root(number: int) -> int:
    if number < 0:
        raise ValueError("number must be non-negative")

    while number >= 10:
        total = 0
        for character in str(number):
            total += int(character)
        number = total

    return number
```

## Complexity

- Time: `O(d)`
- Extra space: `O(d)`

Try to write the solution yourself before reading the code.
