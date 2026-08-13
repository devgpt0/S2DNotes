# 02. Find the Largest Number

**What you learn:** Tracking a value while looping.

## Problem

Given a non-empty list of integers, return its largest number.

## Example

```text
Input: numbers = [5, 2, 9, 1]
Output: 9
```

## Simple idea

Treat the first number as the largest. Replace it whenever a bigger number is found.

## Python solution

```python
def find_largest(numbers: list[int]) -> int:
    if len(numbers) == 0:
        raise ValueError("numbers must not be empty")

    largest = numbers[0]

    for number in numbers:
        if number > largest:
            largest = number

    return largest
```

## Complexity

- Time: `O(n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

