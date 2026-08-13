# 11. Create a Set of Unique Values

**What you learn:** Creating a set.

## Problem

Given a list of integers, return a set containing each value once.

## Example

```text
Input: numbers = [1, 1, 2, 3, 3]
Output: {1, 2, 3}
```

## Simple idea

Passing the list to `set()` automatically removes repeated values.

## Python solution

```python
def unique_values(numbers: list[int]) -> set[int]:
    return set(numbers)
```

## Complexity

- Time: `O(n)`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.

