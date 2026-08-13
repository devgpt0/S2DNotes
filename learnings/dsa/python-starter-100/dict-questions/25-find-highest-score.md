# 25. Find the Highest Score

**What you learn:** Comparing dictionary values.

## Problem

Given a non-empty score dictionary, return the name with the highest score.

## Example

```text
Input: scores = {"Asha": 80, "Ravi": 92, "Mina": 85}
Output: "Ravi"
```

## Simple idea

Remember the best name seen so far and replace it when a higher score appears.

## Python solution

```python
def find_top_student(scores: dict[str, int]) -> str:
    if len(scores) == 0:
        raise ValueError("scores must not be empty")

    top_name = next(iter(scores))

    for name in scores:
        if scores[name] > scores[top_name]:
            top_name = name

    return top_name
```

## Complexity

- Time: `O(n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

