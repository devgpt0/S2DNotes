# 06. Keep Positive Numbers

**What you learn:** Building a new list.

## Problem

Given a list of integers, return a new list containing only positive numbers.

## Example

```text
Input: numbers = [-2, 0, 5, -1, 3]
Output: [5, 3]
```

## Simple idea

Visit every number and append it only when it is greater than zero.

## Python solution

```python
def keep_positive_numbers(numbers: list[int]) -> list[int]:
    positive_numbers: list[int] = []

    for number in numbers:
        if number > 0:
            positive_numbers.append(number)

    return positive_numbers
```

## Complexity

- Time: `O(n)`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.

