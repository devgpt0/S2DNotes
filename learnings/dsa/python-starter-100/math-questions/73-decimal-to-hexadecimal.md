# 73. Convert Decimal to Hexadecimal

**What you learn:** Base conversion with digits above 9.

## Problem

Return uppercase hexadecimal text for a non-negative decimal number.

## Example

```text
Input: number = 254
Output: "FE"
```

## Simple idea

Divide by 16. A remainder from 10 to 15 uses A to F.

## Python solution

```python
def decimal_to_hexadecimal(number: int) -> str:
    if number < 0:
        raise ValueError("number must be non-negative")
    if number == 0:
        return "0"

    digits = "0123456789ABCDEF"
    result: list[str] = []
    while number > 0:
        result.append(digits[number % 16])
        number //= 16

    return "".join(reversed(result))
```

## Complexity

- Time: `O(log_16 n)`
- Extra space: `O(log_16 n)`

Try to write the solution yourself before reading the code.
