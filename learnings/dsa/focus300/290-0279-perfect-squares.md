# Focus300 290: LeetCode 279 - Perfect Squares

**Source:** [LeetCode 279](https://leetcode.com/problems/perfect-squares/)  
**Difficulty:** Medium  
**Pattern:** minimum-count dynamic programming / number theory

## Exact contract

Return the minimum number of perfect squares that sum to `n`.

## First principles

Every target can be formed by appending one perfect square to a smaller target. The optimal count is therefore a shortest-path style recurrence over reachable remainders.

## Cases that decide correctness

- A perfect square needs one term.
- Small values should match the direct table base cases.
- The same remainder can be reached many times, so memoization helps.
- Number-theoretic shortcuts may prove the count without full DP.

## Brute force

```python
def num_squares_brute(n):
    squares = [i * i for i in range(1, int(n ** 0.5) + 1)]
    dp = [0] + [float("inf")] * n
    for i in range(1, n + 1):
        for square in squares:
            if square > i:
                break
            dp[i] = min(dp[i], dp[i - square] + 1)
    return dp[n]
```

Try all combinations of squares recursively.

## Better insight

Use DP or BFS over remainders to find the smallest term count.

## Expert solution

```python
def num_squares(n):
    squares = [i * i for i in range(1, int(n ** 0.5) + 1)]
    dp = [0] + [float("inf")] * n
    for i in range(1, n + 1):
        for square in squares:
            if square > i:
                break
            dp[i] = min(dp[i], dp[i - square] + 1)
    return dp[n]
```

Build the best count for every prefix sum from `1` through `n` using the squares as transitions.

**Complexity:** Typically `O(n*sqrt(n))` time and `O(n)` space for the DP approach.
