# Focus300 157: LeetCode 11 - Container With Most Water

**Source:** [LeetCode 11](https://leetcode.com/problems/container-with-most-water/)  
**Difficulty:** Medium  
**Pattern:** proof-driven two pointers

## Exact contract

At index `i`, a vertical line has nonnegative height `height[i]`. Choose two
different indices; together with the x-axis they hold
`(right-left) * min(height[left], height[right])` water. Return the maximum
possible area. Tilting is not allowed.

## First principles

With endpoints fixed, the shorter line limits the height. Moving the taller
line inward decreases width while the same shorter line still caps height, so
it cannot improve the area. Only moving a shortest endpoint can possibly find
a taller limiting wall; this eliminates one endpoint safely each step.


## Classroom board: see the repeated work once

```text
brute force tries every choice.
the optimized solution keeps only the state that must survive to the
next step.
```



## Step-by-step transformation

1. Load the current candidates into a stack, queue, heap, or window.
2. Push or pop the structure while the current element keeps the invariant true.
3. Drop stale candidates and keep only the ones that can still affect the answer.
4. Read the final top, window score, or popped order as the output.

These problems transform the input by keeping just the active frontier of candidates instead of rescanning the whole array every time.


## Diagram: active frontier only

```text

            scan left to right
                |
                v
            keep active candidates
                |
                v
            pop stale work
                |
                v
            current best answer
```

These notes keep only the active frontier of useful candidates instead of rescanning the whole input.

## Cases that decide correctness

- Exactly two lines have only one possible container.
- Zero-height lines are valid.
- Equal endpoint heights allow either endpoint to move.
- Width uses index distance, not the number of elements between lines.
- Input order and the input list must remain unchanged.

## Brute force: evaluate every pair

```python
def maximum_container_area_brute(heights: list[int]) -> int:
    if type(heights) is not list or not 2 <= len(heights) <= 100_000:
        raise ValueError("heights length must be between 2 and 100,000")
    if any(type(height) is not int or not 0 <= height <= 10_000 for height in heights):
        raise ValueError("heights must be integers in the source range")

    best = 0
    for left in range(len(heights)):
        for right in range(left + 1, len(heights)):
            area = (right - left) * min(heights[left], heights[right])
            best = max(best, area)
    return best
```

This takes `O(n^2)` time and `O(1)` space.

## Better insight: discard the endpoint that proves its own upper bound

For the current width, every container retaining the shorter endpoint has no
greater height and a smaller width. That endpoint can never belong to a better
unseen pair.

## Expert solution: converge from both ends

```python
def maximum_container_area(heights: list[int]) -> int:
    if type(heights) is not list or not 2 <= len(heights) <= 100_000:
        raise ValueError("heights length must be between 2 and 100,000")
    if any(type(height) is not int or not 0 <= height <= 10_000 for height in heights):
        raise ValueError("heights must be integers in the source range")

    left = 0
    right = len(heights) - 1
    best = 0
    while left < right:
        best = max(best, (right - left) * min(heights[left], heights[right]))
        if heights[left] <= heights[right]:
            left += 1
        else:
            right -= 1
    return best
```

Every discarded endpoint has been paired at its maximum remaining width, so no
optimal pair is skipped.

**Complexity:** `O(n)` time and `O(1)` space.
