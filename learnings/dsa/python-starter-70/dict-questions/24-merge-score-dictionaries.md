# 24. Merge Score Dictionaries

**What you learn:** Looping through dictionary items.

## Problem

Merge two score dictionaries. If a name occurs in both, add the two scores.

## Example

```text
Input: first = {"A": 2, "B": 3}, second = {"A": 4, "C": 5}
Output: {"A": 6, "B": 3, "C": 5}
```

## Simple idea

Copy the first dictionary, then visit every key-value pair in the second dictionary.

## Python solution

```python
def merge_scores(
    first: dict[str, int], second: dict[str, int]
) -> dict[str, int]:
    merged = first.copy()

    for name, score in second.items():
        if name in merged:
            merged[name] = merged[name] + score
        else:
            merged[name] = score

    return merged
```

## Complexity

- Time: `O(n + m)`
- Extra space: `O(n + m)`

Try to write the solution yourself before reading the code.

