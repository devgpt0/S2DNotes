# 77. Sum Numbers from 1 to n

**What you learn:** A running total.

## Problem

Return the sum of every integer from 1 through a positive number `n`.

## Example

```text
Input: n = 5
Output: 15
```

## Simple idea

Visit each number and add it to the total.

## Python solution

```python
def sum_one_to_n(n: int) -> int:
    if n < 1:
        raise ValueError("n must be positive")

    total = 0
    for number in range(1, n + 1):
        total += number
    return total
```

## Complexity

- Time: `O(n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.
