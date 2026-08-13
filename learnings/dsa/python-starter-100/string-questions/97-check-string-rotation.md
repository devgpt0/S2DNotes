# 97. Check String Rotation

**What you learn:** Using doubled text.

## Problem

Return `True` when the second string is a rotation of the first string.

## Example

```text
Input: first = "waterbottle", second = "erbottlewat"
Output: True
```

## Simple idea

A rotation of a string always appears inside two copies of the original string joined together.

## Python solution

```python
def is_string_rotation(first: str, second: str) -> bool:
    if len(first) != len(second):
        return False
    return second in first + first
```

## Complexity

- Time: `O(n²)`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.
