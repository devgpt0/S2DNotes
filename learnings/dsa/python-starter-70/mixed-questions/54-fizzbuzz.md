# 54. FizzBuzz

**What you learn:** Ordered conditions.

## Problem

Return labels from 1 through `limit`: `Fizz` for multiples of 3, `Buzz` for 5, and `FizzBuzz` for both.

## Example

```text
Input: limit = 5
Output: ["1", "2", "Fizz", "4", "Buzz"]
```

## Simple idea

Check multiples of 15 first so numbers divisible by both 3 and 5 are handled correctly.

## Python solution

```python
def fizz_buzz(limit: int) -> list[str]:
    if limit < 0:
        raise ValueError("limit must not be negative")

    result: list[str] = []

    for number in range(1, limit + 1):
        if number % 15 == 0:
            result.append("FizzBuzz")
        elif number % 3 == 0:
            result.append("Fizz")
        elif number % 5 == 0:
            result.append("Buzz")
        else:
            result.append(str(number))

    return result
```

## Complexity

- Time: `O(n)`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.

