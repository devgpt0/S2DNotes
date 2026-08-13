# 44. Find the Largest of Three Numbers

**What you learn:** Simple comparisons.

## Problem

Return the largest of three integers without using `max()`.

## Example

```text
Input: first = 4, second = 9, third = 6
Output: 9
```

## Simple idea

Start with the first number and replace it when another number is larger.

## Python solution

```python
def largest_of_three(first: int, second: int, third: int) -> int:
    largest = first

    if second > largest:
        largest = second
    if third > largest:
        largest = third

    return largest
```

## Complexity

- Time: `O(1)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

