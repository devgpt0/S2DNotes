# 04. Count Even Numbers

**What you learn:** Conditions inside a list loop.

## Problem

Given a list of integers, count how many numbers are even.

## Example

```text
Input: numbers = [1, 2, 4, 7, 8]
Output: 3
```

## Simple idea

A number is even when its remainder after division by 2 is zero.

## Python solution

```python
def count_even_numbers(numbers: list[int]) -> int:
    count = 0

    for number in numbers:
        if number % 2 == 0:
            count = count + 1

    return count
```

## Complexity

- Time: `O(n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

