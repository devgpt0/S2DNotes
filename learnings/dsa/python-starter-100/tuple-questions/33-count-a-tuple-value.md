# 33. Count a Value in a Tuple

**What you learn:** Tuple traversal.

## Problem

Return the number of times a target integer occurs in a tuple.

## Example

```text
Input: values = (1, 2, 1, 3, 1), target = 1
Output: 3
```

## Simple idea

Visit each tuple value and increase a counter when it matches the target.

## Python solution

```python
def count_target(values: tuple[int, ...], target: int) -> int:
    count = 0

    for value in values:
        if value == target:
            count = count + 1

    return count
```

## Complexity

- Time: `O(n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

