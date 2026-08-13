# 76. Convert Seconds to Hours, Minutes, and Seconds

**What you learn:** Integer division and remainder.

## Problem

Return `(hours, minutes, seconds)` for a non-negative total number of seconds.

## Example

```text
Input: total_seconds = 3671
Output: (1, 1, 11)
```

## Simple idea

Take full hours first. Then take full minutes from what remains.

## Python solution

```python
def seconds_to_hms(total_seconds: int) -> tuple[int, int, int]:
    if total_seconds < 0:
        raise ValueError("total_seconds must be non-negative")

    hours = total_seconds // 3600
    remaining_seconds = total_seconds % 3600
    minutes = remaining_seconds // 60
    seconds = remaining_seconds % 60
    return hours, minutes, seconds
```

## Complexity

- Time: `O(1)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.
