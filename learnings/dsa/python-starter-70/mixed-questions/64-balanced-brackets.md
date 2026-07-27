# 64. Check Balanced Brackets

**What you learn:** Using a list as a stack.

## Problem

Return `True` when `()`, `[]`, and `{}` brackets are correctly opened and closed.

## Example

```text
Input: text = "([])"
Output: True
```

## Simple idea

Push opening brackets. Each closing bracket must match the most recent opening bracket.

## Python solution

```python
def has_balanced_brackets(text: str) -> bool:
    matching = {")": "(", "]": "[", "}": "{"}
    stack: list[str] = []

    for character in text:
        if character in "([{":
            stack.append(character)
        elif character in matching:
            if len(stack) == 0:
                return False
            if stack.pop() != matching[character]:
                return False

    return len(stack) == 0
```

## Complexity

- Time: `O(n)`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.

