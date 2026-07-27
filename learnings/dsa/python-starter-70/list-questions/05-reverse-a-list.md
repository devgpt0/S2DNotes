# 05. Reverse a List

**What you learn:** List indexes and append.

## Problem

Given a list, return a new list with the elements in reverse order.

## Example

```text
Input: numbers = [1, 2, 3, 4]
Output: [4, 3, 2, 1]
```

## Simple idea

Start at the last index and append each value to a new list.

## Python solution

```python
def reverse_list(numbers: list[int]) -> list[int]:
    reversed_numbers: list[int] = []

    index = len(numbers) - 1
    while index >= 0:
        reversed_numbers.append(numbers[index])
        index = index - 1

    return reversed_numbers
```

## Complexity

- Time: `O(n)`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.

