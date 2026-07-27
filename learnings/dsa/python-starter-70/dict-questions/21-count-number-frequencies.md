# 21. Count Number Frequencies

**What you learn:** Dictionary keys and values.

## Problem

Given a list of integers, return a dictionary containing the count of each number.

## Example

```text
Input: numbers = [2, 1, 2, 3, 2]
Output: {2: 3, 1: 1, 3: 1}
```

## Simple idea

Use each number as a key. Increase its stored count whenever the number appears.

## Python solution

```python
def count_frequencies(numbers: list[int]) -> dict[int, int]:
    counts: dict[int, int] = {}

    for number in numbers:
        if number in counts:
            counts[number] = counts[number] + 1
        else:
            counts[number] = 1

    return counts
```

## Complexity

- Time: `O(n)`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.

