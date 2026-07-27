# 68. Rotate a String Left

**What you learn:** String slicing.

## Problem

Move the first `positions` characters to the end of a string.

## Example

```text
Input: text = "abcdef", positions = 2
Output: "cdefab"
```

## Simple idea

Reduce large positions with remainder, then join the two string slices.

## Python solution

```python
def rotate_left(text: str, positions: int) -> str:
    if text == "":
        return ""

    positions = positions % len(text)
    return text[positions:] + text[:positions]
```

## Complexity

- Time: `O(n)`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.

