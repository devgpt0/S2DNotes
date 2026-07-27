# 23. Add or Update a Score

**What you learn:** Dictionary assignment.

## Problem

Return a new score dictionary with the given student's score added or updated.

## Example

```text
Input: scores = {"Asha": 80}, name = "Ravi", score = 75
Output: {"Asha": 80, "Ravi": 75}
```

## Simple idea

Copy the dictionary, then assign the score using the student's name as the key.

## Python solution

```python
def save_score(
    scores: dict[str, int], name: str, score: int
) -> dict[str, int]:
    updated_scores = scores.copy()
    updated_scores[name] = score
    return updated_scores
```

## Complexity

- Time: `O(n)`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.

