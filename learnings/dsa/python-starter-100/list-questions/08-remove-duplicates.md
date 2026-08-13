# 08. Remove Duplicate Values

**What you learn:** List membership.

## Problem

Given a list, return a new list that keeps only the first occurrence of each value.

## Example

```text
Input: numbers = [3, 1, 3, 2, 1]
Output: [3, 1, 2]
```

## Simple idea

Build a result list. Append a number only when it is not already in the result.

## Python solution

```python
def remove_duplicates(numbers: list[int]) -> list[int]:
    unique_numbers: list[int] = []

    for number in numbers:
        if number not in unique_numbers:
            unique_numbers.append(number)

    return unique_numbers
```

## Complexity

- Time: `O(n²)`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.

