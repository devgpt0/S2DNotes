# ICPC300 107: CSES - Permutation Inversions

**Source:** [CSES - Permutation Inversions](https://cses.fi/problemset/task/2229/)  
**Pattern:** prefix-sum optimized inversion DP  
**Goal:** Count, modulo `1_000_000_007`, permutations of `1..n` containing
exactly `k` inversions.

## 1. Problem in plain words

An inversion is a pair of positions `i < j` with `permutation[i] >
permutation[j]`. For `n = 3`, the inversion counts of the six permutations are
`0, 1, 1, 2, 2, 3`, so two permutations have exactly one inversion.

## 2. First principles

Take a permutation of `1..size-1` and insert the new largest value `size`.
Placing it at the far right adds zero inversions; moving it left one position
at a time adds `1, 2, ..., size-1` inversions.

Thus:

`dp[size][x] = sum(dp[size-1][x-added], added=0..size-1)`.

This is a sliding window over the previous DP row. Maintain its sum while `x`
increases to reduce each transition from `O(n)` to `O(1)`.

## 3. Cases that decide correctness

| Case | Required result |
| --- | --- |
| `k = 0` | `1`: the increasing permutation. |
| `k > n(n-1)/2` | `0`. |
| Maximum inversion count | `1`: the decreasing permutation. |
| `n = 1` | Only `k = 0` is possible. |
| Sliding window crosses zero | Do not access a negative DP index. |

## 4. Brute force: enumerate every permutation

```python
from itertools import permutations


def count_permutations_with_inversions_brute_force(size: int, target: int) -> int:
    if size < 1 or target < 0:
        raise ValueError("size must be positive and target nonnegative")

    answer = 0
    for permutation in permutations(range(size)):
        inversions = sum(
            permutation[first] > permutation[second]
            for first in range(size)
            for second in range(first + 1, size)
        )
        answer += inversions == target
    return answer
```

**Complexity:** `O(n! n^2)` time and `O(n)` generated-permutation memory.

## 5. Better: direct insertion DP

```python
MODULO = 1_000_000_007


def count_permutations_with_inversions_dp(size: int, target: int) -> int:
    if size < 1 or target < 0:
        raise ValueError("size must be positive and target nonnegative")
    if target > size * (size - 1) // 2:
        return 0

    previous = [0] * (target + 1)
    previous[0] = 1
    for current_size in range(2, size + 1):
        current = [0] * (target + 1)
        for inversions in range(target + 1):
            current[inversions] = (
                sum(
                    previous[inversions - added]
                    for added in range(min(current_size - 1, inversions) + 1)
                )
                % MODULO
            )
        previous = current
    return previous[target]
```

**Complexity:** `O(n^2 k)` time and `O(k)` memory.

## 6. Expert solution: sliding-window transition sums

```python
MODULO = 1_000_000_007


def count_permutations_with_inversions(size: int, target: int) -> int:
    if size < 1 or target < 0:
        raise ValueError("size must be positive and target nonnegative")
    if target > size * (size - 1) // 2:
        return 0

    previous = [0] * (target + 1)
    previous[0] = 1
    for current_size in range(2, size + 1):
        current = [0] * (target + 1)
        window_sum = 0
        for inversions in range(target + 1):
            window_sum += previous[inversions]
            if inversions >= current_size:
                window_sum -= previous[inversions - current_size]
            current[inversions] = window_sum % MODULO
        previous = current
    return previous[target]
```

### Why the expert code is correct

- Removing the largest element from any size-`s` permutation leaves one unique
  size-`s-1` permutation.
- Its insertion position adds exactly one value from `0..s-1`, so the DP sum
  covers every permutation once.
- At inversion count `x`, the maintained window contains exactly previous
  states `x, x-1, ..., x-(s-1)`.
- Therefore the optimized transition equals the direct recurrence.

**Complexity:** `O(nk)` time and `O(k)` memory.

## 7. What to remember

Inserting the new maximum adds a bounded inversion count. Bounded-sum DP
transitions are sliding windows.
