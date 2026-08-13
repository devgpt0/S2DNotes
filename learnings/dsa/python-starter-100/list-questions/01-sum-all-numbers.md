# 01. Sum All Numbers

**What you learn:** List traversal and an accumulator.

## Problem

Given a list of integers, return the sum of all numbers.

## Example

```text
Input: numbers = [2, 4, 6]
Output: 12
```

## Simple idea

Start with `total = 0`. Visit each number and add it to `total`.

## Python solution

```python
def sum_numbers(numbers: list[int]) -> int:
    total = 0

    for number in numbers:
        total = total + number

    return total
```

## Complexity

- Time: `O(n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

