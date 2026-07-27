# 34. Find a Value's Tuple Index

**What you learn:** Tuple indexes.

## Problem

Return the first index of a target in a tuple, or `-1` if it is absent.

## Example

```text
Input: values = (5, 8, 5), target = 8
Output: 1
```

## Simple idea

Loop through valid indexes and return as soon as the target is found.

## Python solution

```python
def find_index(values: tuple[int, ...], target: int) -> int:
    for index in range(len(values)):
        if values[index] == target:
            return index

    return -1
```

## Complexity

- Time: `O(n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

