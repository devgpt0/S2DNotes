# 92. Find the First Character Index

**What you learn:** Linear search.

## Problem

Return the first index of a target character, or `-1` when it is absent.

## Example

```text
Input: text = "python", target = "t"
Output: 2
```

## Simple idea

Visit characters from left to right and return as soon as the target matches.

## Python solution

```python
def find_first_character_index(text: str, target: str) -> int:
    if len(target) != 1:
        raise ValueError("target must contain exactly one character")

    for index, character in enumerate(text):
        if character == target:
            return index
    return -1
```

## Complexity

- Time: `O(n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.
