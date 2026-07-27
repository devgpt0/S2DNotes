# 31. Get the First and Last Tuple Values

**What you learn:** Tuple indexing.

## Problem

Given a non-empty tuple, return a tuple containing its first and last values.

## Example

```text
Input: values = (4, 7, 9, 2)
Output: (4, 2)
```

## Simple idea

Index `0` is the first value and index `-1` is the last value.

## Python solution

```python
def first_and_last(values: tuple[int, ...]) -> tuple[int, int]:
    if len(values) == 0:
        raise ValueError("values must not be empty")

    return values[0], values[-1]
```

## Complexity

- Time: `O(1)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

