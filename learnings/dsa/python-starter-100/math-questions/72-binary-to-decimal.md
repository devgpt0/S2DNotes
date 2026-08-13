# 72. Convert Binary to Decimal

**What you learn:** Place value in base 2.

## Problem

Return the decimal value of a non-empty binary string.

## Example

```text
Input: binary_text = "1101"
Output: 13
```

## Simple idea

Move left to right: multiply the current value by 2, then add the next bit.

## Python solution

```python
def binary_to_decimal(binary_text: str) -> int:
    if len(binary_text) == 0:
        raise ValueError("binary_text must not be empty")

    value = 0
    for character in binary_text:
        if character not in "01":
            raise ValueError("binary_text must contain only 0 and 1")
        value = value * 2 + int(character)

    return value
```

## Complexity

- Time: `O(n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.
