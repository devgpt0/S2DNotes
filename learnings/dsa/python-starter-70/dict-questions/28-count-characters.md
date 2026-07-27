# 28. Count Characters

**What you learn:** Character keys in a dictionary.

## Problem

Return a dictionary containing the count of every character in a string.

## Example

```text
Input: text = "apple"
Output: {"a": 1, "p": 2, "l": 1, "e": 1}
```

## Simple idea

Use each character as a dictionary key and increase its count.

## Python solution

```python
def count_characters(text: str) -> dict[str, int]:
    counts: dict[str, int] = {}

    for character in text:
        if character in counts:
            counts[character] = counts[character] + 1
        else:
            counts[character] = 1

    return counts
```

## Complexity

- Time: `O(n)`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.

