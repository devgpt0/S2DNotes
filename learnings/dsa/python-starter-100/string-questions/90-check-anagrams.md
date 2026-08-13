# 90. Check Anagrams

**What you learn:** Normalizing and counting.

## Problem

Return `True` when two strings contain the same letters, ignoring case and spaces.

## Example

```text
Input: first = "listen", second = "silent"
Output: True
```

## Simple idea

Normalize both strings, then compare their letter counts.

## Python solution

```python
def are_anagrams(first: str, second: str) -> bool:
    first_counts: dict[str, int] = {}
    second_counts: dict[str, int] = {}

    for character in first.lower():
        if not character.isspace():
            first_counts[character] = first_counts.get(character, 0) + 1
    for character in second.lower():
        if not character.isspace():
            second_counts[character] = second_counts.get(character, 0) + 1

    return first_counts == second_counts
```

## Complexity

- Time: `O(n + m)`
- Extra space: `O(n + m)`

Try to write the solution yourself before reading the code.
