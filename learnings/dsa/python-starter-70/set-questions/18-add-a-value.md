# 18. Add a Value to a Set

**What you learn:** The add method.

## Problem

Given a set and one integer, return a new set that also contains the integer.

## Example

```text
Input: numbers = {1, 2}, value = 3
Output: {1, 2, 3}
```

## Simple idea

Copy the input so it stays unchanged, then use `add()` on the copy.

## Python solution

```python
def add_value(numbers: set[int], value: int) -> set[int]:
    result = numbers.copy()
    result.add(value)
    return result
```

## Complexity

- Time: `O(n)`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.

