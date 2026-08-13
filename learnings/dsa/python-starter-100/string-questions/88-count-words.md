# 88. Count Words

**What you learn:** Splitting whitespace.

## Problem

Return the number of words in a string, where one or more whitespace characters separate words.

## Example

```text
Input: text = "  learn   DSA with Python "
Output: 4
```

## Simple idea

`split()` with no argument ignores leading, trailing, and repeated whitespace.

## Python solution

```python
def count_words(text: str) -> int:
    return len(text.split())
```

## Complexity

- Time: `O(n)`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.
