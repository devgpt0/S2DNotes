# 38. Sum Tuple Values

**What you learn:** Looping over a tuple.

## Problem

Return the sum of all integers in a tuple.

## Example

```text
Input: values = (2, 3, 5)
Output: 10
```

## Simple idea

Start at zero and add every tuple value to the total.

## Python solution

```python
def sum_tuple(values: tuple[int, ...]) -> int:
    total = 0

    for value in values:
        total = total + value

    return total
```

## Complexity

- Time: `O(n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

