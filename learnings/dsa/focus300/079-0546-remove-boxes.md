# Focus300 079: LeetCode 546 - Remove Boxes

**Source:** [LeetCode 546](https://leetcode.com/problems/remove-boxes/)  
**Difficulty:** Hard  
**Pattern:** interval DP carrying equal boxes across a boundary

## Exact contract

Given a nonempty color array, repeatedly remove a contiguous group of `k`
equal-colored boxes and score `k^2`. Return the maximum total after removing all
boxes.

## First principles

Removing a group immediately may lose the chance to merge it with the same
color beyond intervening boxes. For interval `[left, right]`, carry how many
boxes equal to `boxes[right]` are already attached just outside the right
boundary. Either remove that enlarged group now or first clear an intervening
suffix so it can merge with an earlier equal color.

## Cases that decide correctness

- Scores are quadratic, so delaying a removal can be profitable.
- Adjacent equal boxes should be compressed into the carried count.
- A single box scores one.
- Different removal orders can reach the same remaining sequence.
- Every box must eventually be removed.

## Brute force: remove every current run

```python
def remove_boxes_brute(boxes: list[int]) -> int:
    if not boxes:
        raise ValueError("boxes must be nonempty")

    def search(state: tuple[int, ...]) -> int:
        if not state:
            return 0
        answer = 0
        start = 0
        while start < len(state):
            end = start + 1
            while end < len(state) and state[end] == state[start]:
                end += 1
            answer = max(
                answer,
                (end - start) ** 2 + search(state[:start] + state[end:]),
            )
            start = end
        return answer

    return search(tuple(boxes))
```

This branches on every run and repeats remaining states exponentially.

## Better approach: memoize each remaining sequence

```python
from functools import cache


def remove_boxes_state_memoized(boxes: list[int]) -> int:
    if not boxes:
        raise ValueError("boxes must be nonempty")

    @cache
    def search(state: tuple[int, ...]) -> int:
        if not state:
            return 0
        answer = 0
        start = 0
        while start < len(state):
            end = start + 1
            while end < len(state) and state[end] == state[start]:
                end += 1
            answer = max(
                answer,
                (end - start) ** 2 + search(state[:start] + state[end:]),
            )
            start = end
        return answer

    return search(tuple(boxes))
```

This removes duplicate state work but can still have exponentially many tuple
states.

## Expert solution: interval DP with a carried color count

```python
from functools import cache


def remove_boxes(boxes: list[int]) -> int:
    if not boxes:
        raise ValueError("boxes must be nonempty")

    @cache
    def solve(left: int, right: int, carried: int) -> int:
        if left > right:
            return 0
        while right > left and boxes[right] == boxes[right - 1]:
            right -= 1
            carried += 1

        answer = solve(left, right - 1, 0) + (carried + 1) ** 2
        for matching in range(left, right):
            if boxes[matching] == boxes[right]:
                answer = max(
                    answer,
                    solve(left, matching, carried + 1)
                    + solve(matching + 1, right - 1, 0),
                )
        return answer

    return solve(0, len(boxes) - 1, 0)
```

The immediate-removal case covers solutions that never merge the right color
leftward. Otherwise, the first earlier equal box it joins determines an
intervening interval that must be removed independently. Trying every such box
therefore exhausts optimal strategies, and memoization stores the sufficient
boundary state.

**Complexity:** `O(n^4)` worst-case time and `O(n^3)` states.
