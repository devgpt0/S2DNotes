# Focus300 273: LeetCode 216 - Combination Sum III

**Source:** [LeetCode 216](https://leetcode.com/problems/combination-sum-iii/)  
**Difficulty:** Medium  
**Pattern:** bounded combination backtracking

## Exact contract

Choose exactly `k` distinct numbers from `1` through `9` whose sum equals `n`.

## First principles

The value set is tiny and strictly ordered, so the search space is small enough for backtracking with aggressive pruning. Each number can appear at most once.

## Cases that decide correctness

- No solution exists if the target sum is outside the achievable range.
- Each chosen number must be distinct.
- Exactly `k` numbers must be selected.
- The search can stop once the partial sum exceeds the target.

## Brute force

```python
def combination_sum3_brute(k, n):
    result = []
    nums = range(1, 10)
    for mask in range(1 << 9):
        subset = [nums[i] for i in range(9) if mask & (1 << i)]
        if len(subset) == k and sum(subset) == n:
            result.append(subset)
    return result
```

Try every subset of `1..9` and filter by size and sum.

## Better insight

Backtrack in increasing order and prune branches that cannot still reach the target.

## Expert solution

```python
def combination_sum3(k, n):
    result = []
    path = []

    def backtrack(start, remaining):
        if len(path) == k:
            if remaining == 0:
                result.append(path.copy())
            return
        for num in range(start, 10):
            if num > remaining:
                break
            path.append(num)
            backtrack(num + 1, remaining - num)
            path.pop()

    backtrack(1, n)
    return result
```

Pick each next digit at most once, track the remaining sum, and stop when either the count or sum constraint is violated.

**Complexity:** Small exponential search with pruning over a fixed nine-element domain.
