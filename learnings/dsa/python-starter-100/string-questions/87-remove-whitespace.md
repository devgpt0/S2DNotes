# 87. Remove Whitespace

**What you learn:** Building a new string.

## Problem

Return a string with every whitespace character removed.

## Example

```text
Input: text = "a b\tc\n"
Output: "abc"
```

## Simple idea

Keep only characters for which `isspace()` is false.

## Python solution

```python
def remove_whitespace(text: str) -> str:
    result: list[str] = []
    for character in text:
        if not character.isspace():
            result.append(character)
    return "".join(result)
```

## Complexity

- Time: `O(n)`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.
