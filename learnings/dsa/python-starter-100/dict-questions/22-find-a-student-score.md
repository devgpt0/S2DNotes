# 22. Find a Student's Score

**What you learn:** Dictionary lookup.

## Problem

Given a dictionary of student scores and a name, return that student's score.

## Example

```text
Input: scores = {"Asha": 80, "Ravi": 75}, name = "Asha"
Output: 80
```

## Simple idea

Check that the name exists, then read its value using square brackets.

## Python solution

```python
def find_score(scores: dict[str, int], name: str) -> int:
    if name not in scores:
        raise KeyError("student was not found")

    return scores[name]
```

## Complexity

- Time: `O(1) average`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

