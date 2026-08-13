# 93. Check for a Substring

**What you learn:** Comparing slices.

## Problem

Return `True` when `target` occurs inside `text`.

## Example

```text
Input: text = "datastructures", target = "struct"
Output: True
```

## Simple idea

Try every possible starting position and compare a slice of the target length.

## Python solution

```python
def contains_substring(text: str, target: str) -> bool:
    if len(target) == 0:
        return True

    for start in range(len(text) - len(target) + 1):
        if text[start : start + len(target)] == target:
            return True
    return False
```

## Complexity

- Time: `O(n × m)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.
