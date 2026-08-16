# Focus300 210: LeetCode 97 - Interleaving String

**Source:** [LeetCode 97](https://leetcode.com/problems/interleaving-string/)  
**Difficulty:** Medium  
**Pattern:** two-string dynamic programming

## Exact contract

Decide whether the third string can be formed by interleaving the first two strings without reordering characters inside either source string.

## First principles

The state is the pair of consumed prefix lengths from the two source strings. Every valid next step must match the next character of the target string.


## Classroom board: store the repeated state once

```text
brute force recomputes the same subproblem many times.
dp keeps the smallest useful state and extends it one step at a time.
```



## Step-by-step transformation

1. Turn the input into subproblems, prefixes, or states that can be reused.
2. Fill the base cases first so later states have something correct to build on.
3. Update each new state from earlier states while keeping the recurrence valid.
4. Read the answer from the final table entry or the best state collected at the end.

Dynamic-programming style notes transform the input by compressing many repeated choices into a small set of reusable states.


## Diagram: state table to answer

```text

            input
                |
                v
            base states
                |
                v
            reuse smaller states
                |
                v
            final dp answer
```

These notes compress repeated choices into reusable states, then read the answer from the last state that matters.

## Cases that decide correctness

- The target length must equal the sum of the source lengths.
- Either source may be empty.
- Repeated letters can create many equivalent-looking paths, so memoization matters.
- The same target prefix may be reachable from multiple source-prefix pairs.

## Brute force

```python
from functools import lru_cache

def is_interleave_brute(s1, s2, s3):
    if len(s1) + len(s2) != len(s3):
        return False

    @lru_cache(None)
    def solve(i, j):
        if i == len(s1) and j == len(s2):
            return True
        k = i + j
        return (
            i < len(s1) and s1[i] == s3[k] and solve(i + 1, j)
        ) or (
            j < len(s2) and s2[j] == s3[k] and solve(i, j + 1)
        )

    return solve(0, 0)
```

Recursively try both possible source strings at every step.

## Better insight

Memoize the prefix-pair states or fill a boolean grid bottom-up.

## Expert solution

```python
def is_interleave(s1, s2, s3):
    if len(s1) + len(s2) != len(s3):
        return False
    dp = [False] * (len(s2) + 1)
    dp[0] = True
    for j in range(1, len(s2) + 1):
        dp[j] = dp[j - 1] and s2[j - 1] == s3[j - 1]
    for i in range(1, len(s1) + 1):
        dp[0] = dp[0] and s1[i - 1] == s3[i - 1]
        for j in range(1, len(s2) + 1):
            k = i + j - 1
            dp[j] = (dp[j] and s1[i - 1] == s3[k]) or (dp[j - 1] and s2[j - 1] == s3[k])
    return dp[-1]
```

Use a 2D DP table where each cell records whether the target prefix can be formed from the corresponding source prefixes.

**Complexity:** O(m*n) time and O(m*n) space, or O(min(m, n)) with a rolling row.
