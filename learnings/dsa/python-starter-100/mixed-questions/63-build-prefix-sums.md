# 63. Build Prefix Sums

**What you learn:** Running totals.

## Problem

Return a list where each position contains the sum from the start through that position.

## Example

```text
Input: numbers = [2, 4, 1, 3]
Output: [2, 6, 7, 10]
```

## Simple idea

Keep a running total and append it after reading each number.

## Python solution

```python
def prefix_sums(numbers: list[int]) -> list[int]:
    result: list[int] = []
    running_total = 0

    for number in numbers:
        running_total = running_total + number
        result.append(running_total)

    return result
```

## Complexity

- Time: `O(n)`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.

