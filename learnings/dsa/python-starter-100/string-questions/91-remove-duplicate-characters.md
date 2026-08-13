# 91. Remove Duplicate Characters

**What you learn:** Keeping first occurrences.

## Problem

Return text with each character kept only at its first position.

## Example

```text
Input: text = "programming"
Output: "progamin"
```

## Simple idea

Use a set to remember characters already kept while preserving the original order in a list.

## Python solution

```python
def remove_duplicate_characters(text: str) -> str:
    seen: set[str] = set()
    result: list[str] = []
    for character in text:
        if character not in seen:
            seen.add(character)
            result.append(character)
    return "".join(result)
```

## Complexity

- Time: `O(n)`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.
