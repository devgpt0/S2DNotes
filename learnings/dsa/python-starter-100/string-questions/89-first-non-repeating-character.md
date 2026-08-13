# 89. Find the First Non-Repeating Character

**What you learn:** Frequency counting.

## Problem

Return the first character that appears exactly once, or an empty string when none exists.

## Example

```text
Input: text = "swiss"
Output: "w"
```

## Simple idea

Count every character first. Then scan the original order to find the first count of 1.

## Python solution

```python
def first_non_repeating_character(text: str) -> str:
    counts: dict[str, int] = {}
    for character in text:
        counts[character] = counts.get(character, 0) + 1

    for character in text:
        if counts[character] == 1:
            return character
    return ""
```

## Complexity

- Time: `O(n)`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.
