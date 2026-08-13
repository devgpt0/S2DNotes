# 71. Convert Decimal to Binary

**What you learn:** Division and remainders.

## Problem

Return the binary text for a non-negative decimal number.

## Example

```text
Input: number = 13
Output: "1101"
```

## Simple idea

Keep taking the remainder after division by 2. Read the remainders backwards.

## Python solution

```python
def decimal_to_binary(number: int) -> str:
    if number < 0:
        raise ValueError("number must be non-negative")
    if number == 0:
        return "0"

    digits: list[str] = []
    while number > 0:
        digits.append(str(number % 2))
        number //= 2

    return "".join(reversed(digits))
```

## Complexity

- Time: `O(log n)`
- Extra space: `O(log n)`

Try to write the solution yourself before reading the code.
