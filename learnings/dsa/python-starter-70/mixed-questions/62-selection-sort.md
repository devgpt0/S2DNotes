# 62. Selection Sort

**What you learn:** Finding the next smallest value.

## Problem

Return an ascending copy of a list using selection sort.

## Example

```text
Input: numbers = [3, 1, 4, 2]
Output: [1, 2, 3, 4]
```

## Simple idea

For each position, find the smallest remaining value and swap it into that position.

## Python solution

```python
def selection_sort(numbers: list[int]) -> list[int]:
    result = numbers.copy()

    for index in range(len(result)):
        smallest_index = index

        for candidate in range(index + 1, len(result)):
            if result[candidate] < result[smallest_index]:
                smallest_index = candidate

        temporary = result[index]
        result[index] = result[smallest_index]
        result[smallest_index] = temporary

    return result
```

## Complexity

- Time: `O(n²)`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.
