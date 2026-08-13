# 26. Invert a Dictionary

**What you learn:** Building a dictionary.

## Problem

Swap every key and value in a dictionary. All original values must be unique.

## Example

```text
Input: letters = {"a": 1, "b": 2}
Output: {1: "a", 2: "b"}
```

## Simple idea

Visit each key-value pair and store the old value as the new key.

## Python solution

```python
def invert_dictionary(values: dict[str, int]) -> dict[int, str]:
    inverted: dict[int, str] = {}

    for key, value in values.items():
        if value in inverted:
            raise ValueError("dictionary values must be unique")

        inverted[value] = key

    return inverted
```

## Complexity

- Time: `O(n)`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.

