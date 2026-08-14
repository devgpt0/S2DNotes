# Focus300 017: LeetCode 84 - Largest Rectangle in Histogram

**Source:** [LeetCode 84](https://leetcode.com/problems/largest-rectangle-in-histogram/)  
**Difficulty:** Hard  
**Pattern:** monotonic increasing stack

## Exact contract

Given a nonempty list of nonnegative bar heights, each with width one, return
the largest rectangular area formed by one or more consecutive bars.

## First principles

For a bar of height `h`, its maximum rectangle extends until the first lower
bar on each side. An increasing stack delays a bar until the current height is
lower; at that moment the current index is its first lower position on the
right, and the new stack top identifies its first lower position on the left.

## Cases that decide correctness

- A single bar contributes its own height.
- Zero-height bars split independent regions.
- Equal heights must not lose the earliest possible left boundary.
- Increasing suffixes need a final sentinel to force evaluation.
- The best rectangle may use a height smaller than every interior bar.

## Brute force: extend every left boundary

```python
def largest_rectangle_area_brute(heights: list[int]) -> int:
    if not heights or any(height < 0 for height in heights):
        raise ValueError("heights must be nonempty and nonnegative")

    answer = 0
    for left in range(len(heights)):
        minimum = heights[left]
        for right in range(left, len(heights)):
            minimum = min(minimum, heights[right])
            answer = max(answer, minimum * (right - left + 1))
    return answer
```

This takes `O(n^2)` time and `O(1)` auxiliary space.

## Better transition: finalize a height at its first lower bar

Keep unresolved bars in increasing-height order. When a lower bar arrives,
every taller bar now knows its maximal right boundary and can be popped. The
bar below it in the stack exposes the maximal left boundary.

## Expert solution: monotonic stack with a sentinel

```python
def largest_rectangle_area(heights: list[int]) -> int:
    if not heights or any(height < 0 for height in heights):
        raise ValueError("heights must be nonempty and nonnegative")

    answer = 0
    stack = [-1]
    for index in range(len(heights) + 1):
        current = 0 if index == len(heights) else heights[index]
        while stack[-1] != -1 and heights[stack[-1]] >= current:
            height = heights[stack.pop()]
            width = index - stack[-1] - 1
            answer = max(answer, height * width)
        stack.append(index)
    return answer
```

When a bar is popped, every bar between the new stack top and the current index
has height at least the popped height. Both adjacent boundaries are lower, so
that width is maximal for the height. Every possible limiting height is popped
exactly once.

**Complexity:** `O(n)` time and `O(n)` space.
