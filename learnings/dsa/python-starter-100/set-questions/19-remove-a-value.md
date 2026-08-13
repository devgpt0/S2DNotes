# 19. Remove a Value Safely

**What you learn:** The discard method.

## Problem

Return a new set without the given value. The value may be absent.

## Example

```text
Input: numbers = {1, 2, 3}, value = 2
Output: {1, 3}
```

## Simple idea

Use `discard()` because it does not fail when the value is absent.

## Python solution

```python
def remove_value(numbers: set[int], value: int) -> set[int]:
    result = numbers.copy()
    result.discard(value)
    return result
```

## Complexity

- Time: `O(n)`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.

