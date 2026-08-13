# 83. Convert Binary to Octal

**What you learn:** Combining base conversions.

## Problem

Return octal text for a non-empty binary string.

## Example

```text
Input: binary_text = "110101"
Output: "65"
```

## Simple idea

Validate the binary text, convert it to a number, then format that number in base 8.

## Python solution

```python
def binary_to_octal(binary_text: str) -> str:
    if len(binary_text) == 0:
        raise ValueError("binary_text must not be empty")
    for character in binary_text:
        if character not in "01":
            raise ValueError("binary_text must contain only 0 and 1")

    return format(int(binary_text, 2), "o")
```

## Complexity

- Time: `O(n)`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.
