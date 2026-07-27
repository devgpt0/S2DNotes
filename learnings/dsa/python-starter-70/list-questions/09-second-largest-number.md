# 09. Find the Second-Largest Distinct Number

**What you learn:** Tracking two list values.

## Problem

Given a list with at least two distinct integers, return the second-largest distinct number.

## Example

```text
Input: numbers = [5, 1, 5, 3]
Output: 3
```

## Simple idea

Track the largest and second-largest distinct values while scanning once.

## Python solution

```python
def find_second_largest(numbers: list[int]) -> int:
    largest = None
    second_largest = None

    for number in numbers:
        if largest is None or number > largest:
            if number != largest:
                second_largest = largest
                largest = number
        elif number != largest:
            if second_largest is None or number > second_largest:
                second_largest = number

    if second_largest is None:
        raise ValueError("numbers must contain two distinct values")

    return second_largest
```

## Complexity

- Time: `O(n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

