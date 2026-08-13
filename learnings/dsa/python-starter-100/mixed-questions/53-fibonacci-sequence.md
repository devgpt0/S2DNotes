# 53. Build a Fibonacci Sequence

**What you learn:** Updating two values.

## Problem

Return the first `count` Fibonacci numbers.

## Example

```text
Input: count = 6
Output: [0, 1, 1, 2, 3, 5]
```

## Simple idea

Store the current and next numbers. Update both after appending each value.

## Python solution

```python
def fibonacci(count: int) -> list[int]:
    if count < 0:
        raise ValueError("count must not be negative")

    numbers: list[int] = []
    current = 0
    next_number = 1

    for _ in range(count):
        numbers.append(current)
        current, next_number = next_number, current + next_number

    return numbers
```

## Complexity

- Time: `O(n)`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.

