# 42. Check Even or Odd

**What you learn:** The remainder operator.

## Problem

Return `"even"` when an integer is even and `"odd"` otherwise.

## Example

```text
Input: number = 14
Output: "even"
```

## Simple idea

An even number has a remainder of zero when divided by 2.

## Python solution

```python
def even_or_odd(number: int) -> str:
    if number % 2 == 0:
        return "even"

    return "odd"
```

## Complexity

- Time: `O(1)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

