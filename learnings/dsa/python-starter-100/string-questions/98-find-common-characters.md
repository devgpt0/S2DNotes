# 98. Find Common Characters

**What you learn:** Set membership with order.

## Problem

Return characters that appear in both strings, preserving first-string order and removing duplicates.

## Example

```text
Input: first = "banana", second = "band"
Output: "ban"
```

## Simple idea

Make a set from the second string, then scan the first string while remembering results already added.

## Python solution

```python
def common_characters(first: str, second: str) -> str:
    allowed = set(second)
    seen: set[str] = set()
    result: list[str] = []
    for character in first:
        if character in allowed and character not in seen:
            seen.add(character)
            result.append(character)
    return "".join(result)
```

## Complexity

- Time: `O(n + m)`
- Extra space: `O(n + m)`

Try to write the solution yourself before reading the code.
