# 46. Build a Multiplication Table

**What you learn:** Range and append.

## Problem

Return the first ten multiples of an integer.

## Example

```text
Input: number = 3
Output: [3, 6, 9, 12, 15, 18, 21, 24, 27, 30]
```

## Simple idea

Multiply the number by every integer from 1 through 10.

## Python solution

```python
def multiplication_table(number: int) -> list[int]:
    table: list[int] = []

    for multiplier in range(1, 11):
        table.append(number * multiplier)

    return table
```

## Complexity

- Time: `O(1)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

