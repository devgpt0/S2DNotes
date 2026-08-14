# 139. Pictures with Kittens (hard version) — Codeforces 1077F2

**Source:** [Codeforces 1077F2 - Pictures with Kittens (hard version)](https://codeforces.com/problemset/problem/1077/F2)  
**Difficulty:** 2300

## 1. Problem in plain words

Choose exactly `x` array positions with maximum total value. The first chosen position must be among the first `k`, the last must be among the last `k`, and the gap between consecutive chosen positions cannot exceed `k`. Print `-1` if no valid choice exists.

## 2. First principles

Let `dp[t][i]` be the best sum after choosing exactly `t` elements with position `i` chosen last. Then

`dp[t][i] = value[i] + max(dp[t-1][j])` for `i-k <= j < i`.

The hard version is about evaluating every sliding-window maximum in constant amortized time with a monotone deque.

## 3. Cases that define correctness

- The first chosen zero-based index must be `< k`.
- A gap of exactly `k` is allowed.
- The final chosen index must be at least `n - k`.
- Having enough total positions does not guarantee the boundary and gap rules are feasible.

## 4. Brute force

Enumerate all `x`-position combinations and check the three placement rules.

```python
from itertools import combinations


def maximum_kitten_beauty_brute_force(
    values: list[int], max_gap: int, chosen: int
) -> int:
    size = len(values)
    if not 1 <= max_gap <= size or not 1 <= chosen <= size:
        raise ValueError("invalid max_gap or chosen count")
    if any(value <= 0 for value in values):
        raise ValueError("source values must be positive")

    best = -1
    for positions in combinations(range(size), chosen):
        if positions[0] >= max_gap or positions[-1] < size - max_gap:
            continue
        if any(
            positions[index] - positions[index - 1] > max_gap
            for index in range(1, chosen)
        ):
            continue
        best = max(best, sum(values[index] for index in positions))
    return best
```

Time is `O(C(n, x) · x)` and auxiliary space is `O(x)`.

## 5. Better approach: direct dynamic programming

Use the recurrence literally and scan up to `k` predecessor states for every `(chosen count, last position)` pair.

```python
def maximum_kitten_beauty_dp(values: list[int], max_gap: int, chosen: int) -> int:
    size = len(values)
    if not 1 <= max_gap <= size or not 1 <= chosen <= size:
        raise ValueError("invalid max_gap or chosen count")
    if any(value <= 0 for value in values):
        raise ValueError("source values must be positive")

    impossible = -(10**40)
    previous = [impossible] * size
    for index in range(min(size, max_gap)):
        previous[index] = values[index]

    for _ in range(2, chosen + 1):
        current = [impossible] * size
        for index in range(size):
            best_previous = max(
                previous[max(0, index - max_gap) : index], default=impossible
            )
            if best_previous != impossible:
                current[index] = best_previous + values[index]
        previous = current

    answer = max(previous[max(0, size - max_gap) :], default=impossible)
    return -1 if answer == impossible else answer
```

Time is `O(xnk)` and space is `O(n)`.

## 6. Expert solution: monotone deque transitions

For one DP layer, predecessor windows move right one index at a time. Keep candidate indices in decreasing order of their previous-layer value. The front is always the maximum valid predecessor.

```python
from collections import deque


def maximum_kitten_beauty(values: list[int], max_gap: int, chosen: int) -> int:
    size = len(values)
    if not 1 <= max_gap <= size or not 1 <= chosen <= size:
        raise ValueError("invalid max_gap or chosen count")
    if any(value <= 0 for value in values):
        raise ValueError("source values must be positive")

    impossible = -(10**40)
    previous = [impossible] * size
    for index in range(min(size, max_gap)):
        previous[index] = values[index]

    for _ in range(2, chosen + 1):
        current = [impossible] * size
        candidates: deque[int] = deque()
        for index in range(size):
            predecessor = index - 1
            if predecessor >= 0 and previous[predecessor] != impossible:
                while candidates and previous[candidates[-1]] <= previous[predecessor]:
                    candidates.pop()
                candidates.append(predecessor)
            while candidates and candidates[0] < index - max_gap:
                candidates.popleft()
            if candidates:
                current[index] = previous[candidates[0]] + values[index]
        previous = current

    answer = max(previous[max(0, size - max_gap) :], default=impossible)
    return -1 if answer == impossible else answer
```

## 7. Why the expert solution is correct

The DP state records exactly the chosen count and final position. Its predecessor range is precisely the allowed gap window, while initialization and final filtering enforce the first and last `k` positions. The deque contains exactly valid predecessor indices and removes a back value only when a later index is at least as good and remains valid at least as long. Its front is therefore the recurrence maximum.

Each index enters and leaves a deque once per layer, giving `O(nx)` time and `O(n)` space.
