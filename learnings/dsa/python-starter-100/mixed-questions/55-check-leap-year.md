# 55. Check a Leap Year

**What you learn:** Combining conditions.

## Problem

Return `True` when a year is a leap year in the Gregorian calendar.

## Example

```text
Input: year = 2024
Output: True
```

## Simple idea

A leap year is divisible by 400, or divisible by 4 but not by 100.

## Python solution

```python
def is_leap_year(year: int) -> bool:
    if year % 400 == 0:
        return True
    if year % 100 == 0:
        return False

    return year % 4 == 0
```

## Complexity

- Time: `O(1)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

