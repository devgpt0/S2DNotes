# 30. Keep Scores Above a Limit

**What you learn:** Filtering dictionary entries.

## Problem

Return a dictionary containing only students whose scores are at least the limit.

## Example

```text
Input: scores = {"A": 40, "B": 70, "C": 60}, limit = 60
Output: {"B": 70, "C": 60}
```

## Simple idea

Build a new dictionary and copy an entry only when its score reaches the limit.

## Python solution

```python
def keep_passing_scores(
    scores: dict[str, int], limit: int
) -> dict[str, int]:
    passing_scores: dict[str, int] = {}

    for name, score in scores.items():
        if score >= limit:
            passing_scores[name] = score

    return passing_scores
```

## Complexity

- Time: `O(n)`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.

