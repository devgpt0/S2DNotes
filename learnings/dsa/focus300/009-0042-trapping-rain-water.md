# Focus300 009: LeetCode 42 - Trapping Rain Water

**Source:** [LeetCode 42](https://leetcode.com/problems/trapping-rain-water/)  
**Difficulty:** Hard  
**Pattern:** two-sided boundary maxima

## Exact contract

Given nonnegative bar heights of unit width, return the total water trapped
after rain.

## First principles

Water above index `i` is

`min(max_height_left, max_height_right) - height[i]`.

With two pointers, the smaller current boundary is decisive: if the left bar is
no higher than the right bar, some right boundary at least that high exists, so
the left-side maximum alone fixes water at the left pointer. The symmetric rule
handles the right pointer.

## Cases that decide correctness

- Fewer than three bars trap no water.
- Equal boundary heights may advance either side.
- Monotone height arrays trap zero.
- Repeated valleys contribute independently.
- Heights are nonnegative by contract.

## Brute force: scan both boundaries for every index

```python
def trap_brute(heights: list[int]) -> int:
    water = 0
    for index, height in enumerate(heights):
        left_maximum = max(heights[: index + 1])
        right_maximum = max(heights[index:])
        water += min(left_maximum, right_maximum) - height
    return water
```

This takes `O(n^2)` time and `O(n)` temporary slice space.

## Better approach: precompute both boundary arrays

```python
def trap_prefix_suffix(heights: list[int]) -> int:
    if not heights:
        return 0
    left_maximum = [0] * len(heights)
    right_maximum = [0] * len(heights)
    current = 0
    for index, height in enumerate(heights):
        current = max(current, height)
        left_maximum[index] = current
    current = 0
    for index in range(len(heights) - 1, -1, -1):
        current = max(current, heights[index])
        right_maximum[index] = current
    return sum(
        min(left_maximum[index], right_maximum[index]) - height
        for index, height in enumerate(heights)
    )
```

This is `O(n)` time and `O(n)` space.

## Expert solution: resolve the lower boundary online

```python
def trap(heights: list[int]) -> int:
    left = 0
    right = len(heights) - 1
    left_maximum = 0
    right_maximum = 0
    water = 0
    while left <= right:
        if heights[left] <= heights[right]:
            left_maximum = max(left_maximum, heights[left])
            water += left_maximum - heights[left]
            left += 1
        else:
            right_maximum = max(right_maximum, heights[right])
            water += right_maximum - heights[right]
            right -= 1
    return water
```

The lower visible boundary always has a guaranteed opposite wall, so its water
amount cannot change after that pointer advances.

**Complexity:** `O(n)` time and `O(1)` space.
