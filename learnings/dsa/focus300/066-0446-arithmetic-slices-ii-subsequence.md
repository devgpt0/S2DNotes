# Focus300 066: LeetCode 446 - Arithmetic Slices II - Subsequence

**Source:** [LeetCode 446](https://leetcode.com/problems/arithmetic-slices-ii-subsequence/)  
**Difficulty:** Hard  
**Pattern:** subsequence DP keyed by ending difference

## Exact contract

Return the number of index subsequences of length at least three whose adjacent
value differences are equal. Indices retain their original order; values and
differences may repeat.

## First principles

Let `dp[i][d]` count arithmetic subsequences of length at least two ending at
index `i` with difference `d`. For each earlier index `j`, the pair `(j,i)`
starts one length-two state. Every existing state in `dp[j][d]` extends to a
valid length-at-least-three answer and another state ending at `i`.

Pairs are stored for future extension but are not yet included in the answer.

## Cases that decide correctness

- Subsequences use indices, so equal values at different indices are distinct.
- Length-two pairs are DP states but not answers.
- Difference zero is valid.
- Differences may exceed 32-bit range even when inputs do not.
- The empty and short arrays return zero.

## Brute force: enumerate every index subset

```python
def arithmetic_slices_brute(values: list[int]) -> int:
    answer = 0
    for mask in range(1 << len(values)):
        if mask.bit_count() < 3:
            continue
        sequence = [value for index, value in enumerate(values) if mask >> index & 1]
        difference = sequence[1] - sequence[0]
        if all(
            sequence[index] - sequence[index - 1] == difference
            for index in range(2, len(sequence))
        ):
            answer += 1
    return answer
```

This takes `O(2^n n)` time.

## Better insight: an arithmetic subsequence is identified by its last index and difference

Those two fields contain everything needed to decide whether a new value can
extend it, so exponentially many subsequences aggregate into hash-map counts.

## Expert solution: difference maps at every endpoint

```python
from collections import defaultdict


def number_of_arithmetic_slices(values: list[int]) -> int:
    dynamic: list[dict[int, int]] = [defaultdict(int) for _ in values]
    answer = 0
    for right in range(len(values)):
        for left in range(right):
            difference = values[right] - values[left]
            extensions = dynamic[left][difference]
            answer += extensions
            dynamic[right][difference] += extensions + 1
    return answer
```

Every valid answer is counted exactly when its final index is appended; the
additional one records the new pair for later extensions.

**Complexity:** `O(n^2)` time and `O(n^2)` worst-case space.
