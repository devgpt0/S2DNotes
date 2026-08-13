# 43. Find a Number's Sign

**What you learn:** If, elif, and else.

## Problem

Return `"positive"`, `"negative"`, or `"zero"` for an integer.

## Example

```text
Input: number = -5
Output: "negative"
```

## Simple idea

Compare the number with zero.

## Python solution

```python
def number_sign(number: int) -> str:
    if number > 0:
        return "positive"
    if number < 0:
        return "negative"

    return "zero"
```

## Complexity

- Time: `O(1)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

