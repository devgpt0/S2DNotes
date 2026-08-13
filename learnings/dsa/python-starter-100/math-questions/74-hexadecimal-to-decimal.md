# 74. Convert Hexadecimal to Decimal

**What you learn:** Place value in base 16.

## Problem

Return the decimal value of a non-empty hexadecimal string without a `0x` prefix.

## Example

```text
Input: hex_text = "FE"
Output: 254
```

## Simple idea

Multiply the current value by 16, then add the next digit value.

## Python solution

```python
def hexadecimal_to_decimal(hex_text: str) -> int:
    if len(hex_text) == 0:
        raise ValueError("hex_text must not be empty")

    digits = "0123456789ABCDEF"
    value = 0
    for character in hex_text.upper():
        index = digits.find(character)
        if index == -1:
            raise ValueError("hex_text must contain hexadecimal digits")
        value = value * 16 + index

    return value
```

## Complexity

- Time: `O(n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.
