# 84. Convert Decimal to Any Base from 2 to 16

**What you learn:** General base conversion.

## Problem

Return uppercase text for a non-negative number in a base from 2 through 16.

## Example

```text
Input: number = 31, base = 16
Output: "1F"
```

## Simple idea

The repeated-division method works for every base. The base chooses the remainder digits.

## Python solution

```python
def decimal_to_base(number: int, base: int) -> str:
    if number < 0:
        raise ValueError("number must be non-negative")
    if base < 2 or base > 16:
        raise ValueError("base must be from 2 to 16")
    if number == 0:
        return "0"

    digits = "0123456789ABCDEF"
    result: list[str] = []
    while number > 0:
        result.append(digits[number % base])
        number //= base

    return "".join(reversed(result))
```

## Complexity

- Time: `O(log_base n)`
- Extra space: `O(log_base n)`

Try to write the solution yourself before reading the code.
