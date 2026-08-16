# Focus300 273: LeetCode 216 - Combination Sum III

**Source:** [LeetCode 216](https://leetcode.com/problems/combination-sum-iii/)  
**Difficulty:** Medium  
**Pattern:** bounded combination backtracking

## Exact contract

Choose exactly `k` distinct numbers from `1` through `9` whose sum equals `n`.

## First principles

The value set is tiny and strictly ordered, so the search space is small enough for backtracking with aggressive pruning. Each number can appear at most once.


## Classroom board: see the repeated work once

```text
brute force tries every choice.
the optimized solution keeps only the state that must survive to the
next step.
```



## Step-by-step transformation

1. Choose a start state such as a cell, node, or partial path.
2. Mark the state as visited or temporarily commit the choice.
3. Expand to valid neighbors or next choices while the invariant still holds.
4. Undo the temporary choice when the branch finishes, then return the collected answer.

These problems transform the input into output by exploring one branch at a time and backtracking whenever a branch can no longer produce a valid solution.


## Diagram: search and undo

```text

            start state
                |
                v
            choose one path
                |
                v
            explore neighbors
                |
                v
            undo and try next path
                |
                v
            answer
```

These notes use search, visit markers, and backtracking to turn one starting state into the final valid path or count.

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
