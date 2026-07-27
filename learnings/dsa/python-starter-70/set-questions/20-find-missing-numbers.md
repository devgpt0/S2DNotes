# 20. Find Missing Numbers in a Range

**What you learn:** Set creation and difference.

## Problem

Given a set of numbers and an inclusive range, return the numbers missing from the set.

## Example

```text
Input: numbers = {1, 3, 5}, start = 1, end = 5
Output: {2, 4}
```

## Simple idea

Create the complete expected set, then subtract the given numbers.

## Python solution

```python
def find_missing_numbers(
    numbers: set[int], start: int, end: int
) -> set[int]:
    expected = set(range(start, end + 1))
    return expected - numbers
```

## Complexity

- Time: `O(end - start + 1)`
- Extra space: `O(end - start + 1)`

Try to write the solution yourself before reading the code.

