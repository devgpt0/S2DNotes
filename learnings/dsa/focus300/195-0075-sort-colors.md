# Focus300 195: LeetCode 75 - Sort Colors

**Source:** [LeetCode 75](https://leetcode.com/problems/sort-colors/)  
**Difficulty:** Medium  
**Pattern:** Dutch national flag three-way partition

## Exact contract

Sort an array containing only `0`, `1`, and `2` in place so equal values are
contiguous in that order. Do not call a library sorting routine. The one-pass,
constant-space follow-up is the target solution.

## First principles

Maintain four regions: `[0, low)` contains zeros, `[low, current)` contains
ones, `[current, high]` is unknown, and `(high, end]` contains twos. A zero swaps
left and advances both pointers; a one advances; a two swaps right and keeps
`current` fixed because the incoming value is still unknown.


## Classroom board: discard half the search space

```text
binary search keeps the side that can still contain the answer and throws
away the side that cannot.
```



## Step-by-step transformation

1. Compare the middle position with the target rule or boundary condition.
2. Discard the half that cannot still contain a valid answer.
3. Repeat until the remaining interval is exactly the split or value the problem asks for.
4. Convert the final boundary positions into the required output.

Binary-search style notes transform the input by shrinking the search space until only one valid boundary or value remains.


## Diagram: discard half the search space

```text

            sorted input
                |
                v
            check middle
                |
                v
            keep the half that can still work
                |
                v
            final boundary / value
```

Binary search keeps shrinking the input until only the valid boundary or value is left.

## Cases that decide correctness

- An array containing one color is already sorted.
- After swapping with `high`, re-examine the new current value.
- Swapping a zero at `current` preserves the ones region.
- The input list itself must be mutated.
- Every value outside `0..2` fails immediately.

## Brute force: bubble adjacent inversions

```python
def sort_colors_brute(colors: list[int]) -> None:
    if type(colors) is not list or not 1 <= len(colors) <= 300:
        raise ValueError("colors length must be between 1 and 300")
    if any(type(color) is not int or color not in (0, 1, 2) for color in colors):
        raise ValueError("colors must contain only integer values 0, 1, and 2")

    for end in range(len(colors) - 1, 0, -1):
        swapped = False
        for index in range(end):
            if colors[index] > colors[index + 1]:
                colors[index], colors[index + 1] = colors[index + 1], colors[index]
                swapped = True
        if not swapped:
            break
```

This is in place but costs `O(n^2)` time.

## Better approach: count each color, then rewrite

```python
def sort_colors_counting(colors: list[int]) -> None:
    if type(colors) is not list or not 1 <= len(colors) <= 300:
        raise ValueError("colors length must be between 1 and 300")
    if any(type(color) is not int or color not in (0, 1, 2) for color in colors):
        raise ValueError("colors must contain only integer values 0, 1, and 2")

    counts = [0, 0, 0]
    for color in colors:
        counts[color] += 1
    write = 0
    for color, count in enumerate(counts):
        for _ in range(count):
            colors[write] = color
            write += 1
```

Counting is linear and constant-space, but it requires two full passes.

## Expert solution: one-pass Dutch national flag partition

```python
def sort_colors(colors: list[int]) -> None:
    if type(colors) is not list or not 1 <= len(colors) <= 300:
        raise ValueError("colors length must be between 1 and 300")
    if any(type(color) is not int or color not in (0, 1, 2) for color in colors):
        raise ValueError("colors must contain only integer values 0, 1, and 2")

    low = 0
    current = 0
    high = len(colors) - 1
    while current <= high:
        if colors[current] == 0:
            colors[low], colors[current] = colors[current], colors[low]
            low += 1
            current += 1
        elif colors[current] == 1:
            current += 1
        else:
            colors[current], colors[high] = colors[high], colors[current]
            high -= 1
```

Each action grows a finalized region, so the unknown interval eventually
vanishes with all three partition invariants intact.

**Complexity:** `O(n)` time, one pass, and `O(1)` auxiliary space.
