# 07. Count a Target Value

**What you learn:** Counting matches in a list.

## Problem

Given a list and a target integer, return how many times the target occurs.

## Example

```text
Input: numbers = [3, 1, 3, 3, 5], target = 3
Output: 3
```

## Simple idea

Increase a counter every time the current number equals the target.

## Python solution

```python
def count_target(numbers: list[int], target: int) -> int:
    count = 0

    for number in numbers:
        if number == target:
            count = count + 1

    return count
```

## Complexity

- Time: `O(n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

