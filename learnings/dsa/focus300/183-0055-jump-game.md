# Focus300 183: LeetCode 55 - Jump Game

**Source:** [LeetCode 55](https://leetcode.com/problems/jump-game/)  
**Difficulty:** Medium  
**Pattern:** greedy farthest reachable prefix

## Exact contract

Starting at index zero of a nonempty array of nonnegative integers, value
`numbers[i]` is the maximum forward jump length from `i`. Return whether the
last index is reachable. The source length is at most 10,000.

## First principles

All indices through the farthest reachable index form a reachable prefix. When
scanning that prefix, each position can extend its right boundary. The first
index beyond the boundary proves failure because no later index can be reached
to extend it.

## Cases that decide correctness

- A one-element array is already at the destination.
- Zero is harmless when an earlier jump crosses it.
- Stop immediately when the current index exceeds the reachable boundary.
- Overshooting the final index is allowed.
- Negative jump lengths violate the source contract.

## Brute force: try every legal jump sequence

```python
def can_reach_end_brute(numbers: list[int]) -> bool:
    if type(numbers) is not list or any(type(value) is not int for value in numbers):
        raise TypeError("numbers must be a list of integers")
    if not 1 <= len(numbers) <= 10_000 or any(value < 0 for value in numbers):
        raise ValueError("numbers must contain 1..10000 non-negative values")

    def search(index: int) -> bool:
        if index >= len(numbers) - 1:
            return True
        return any(
            search(index + jump)
            for jump in range(1, min(numbers[index], len(numbers) - index - 1) + 1)
        )

    return search(0)
```

Repeated suffix exploration makes this exponential in the worst case.

## Better approach: memoize reachability from each index

Caching the recursive result at every index reduces the search to `O(n^2)`
worst-case jump checks and `O(n)` storage. The greedy prefix invariant removes
the branching entirely.

## Expert solution: extend one reachable frontier

```python
def can_reach_end(numbers: list[int]) -> bool:
    if type(numbers) is not list or any(type(value) is not int for value in numbers):
        raise TypeError("numbers must be a list of integers")
    if not 1 <= len(numbers) <= 10_000 or any(value < 0 for value in numbers):
        raise ValueError("numbers must contain 1..10000 non-negative values")

    farthest = 0
    for index, jump in enumerate(numbers):
        if index > farthest:
            return False
        farthest = max(farthest, index + jump)
        if farthest >= len(numbers) - 1:
            return True
    return True
```

Before each iteration, every index through `farthest` is reachable. Processing
one such index preserves and possibly extends that invariant.

**Complexity:** `O(n)` time and `O(1)` space.
