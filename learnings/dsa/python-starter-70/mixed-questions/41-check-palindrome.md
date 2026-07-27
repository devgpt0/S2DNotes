# 41. Check a Palindrome

**What you learn:** String indexes.

## Problem

Return `True` when a string reads the same from left to right and right to left.

## Example

```text
Input: text = "level"
Output: True
```

## Simple idea

Compare characters from both ends and move toward the middle.

## Python solution

```python
def is_palindrome(text: str) -> bool:
    left = 0
    right = len(text) - 1

    while left < right:
        if text[left] != text[right]:
            return False

        left = left + 1
        right = right - 1

    return True
```

## Complexity

- Time: `O(n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

