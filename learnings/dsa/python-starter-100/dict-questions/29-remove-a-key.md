# 29. Remove a Dictionary Key

**What you learn:** Deleting a key.

## Problem

Return a new dictionary without the given key. Fail if the key does not exist.

## Example

```text
Input: scores = {"A": 10, "B": 20}, name = "A"
Output: {"B": 20}
```

## Simple idea

Check the key, copy the dictionary, and delete the key from the copy.

## Python solution

```python
def remove_score(
    scores: dict[str, int], name: str
) -> dict[str, int]:
    if name not in scores:
        raise KeyError("student was not found")

    updated_scores = scores.copy()
    del updated_scores[name]
    return updated_scores
```

## Complexity

- Time: `O(n)`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.

