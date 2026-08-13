# 45. Calculate a Factorial

**What you learn:** A counting loop.

## Problem

Return `n!`, the product of all integers from 1 through a non-negative integer `n`.

## Example

```text
Input: number = 5
Output: 120
```

## Simple idea

Start with 1 and multiply it by every number from 2 through `n`.

## Python solution

```python
def factorial(number: int) -> int:
    if number < 0:
        raise ValueError("number must not be negative")

    result = 1

    for value in range(2, number + 1):
        result = result * value

    return result
```

## Complexity

- Time: `O(n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

