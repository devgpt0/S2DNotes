# 40. Reverse a Tuple

**What you learn:** Tuple slicing.

## Problem

Return a tuple containing the same values in reverse order.

## Example

```text
Input: values = (1, 2, 3, 4)
Output: (4, 3, 2, 1)
```

## Simple idea

A slice with a step of `-1` reads the tuple from end to start.

## Python solution

```python
def reverse_tuple(values: tuple[int, ...]) -> tuple[int, ...]:
    return values[::-1]
```

## Complexity

- Time: `O(n)`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.

