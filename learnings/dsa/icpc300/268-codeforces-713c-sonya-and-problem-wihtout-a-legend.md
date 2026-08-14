# ICPC300 268: Codeforces 713C - Sonya and Problem Wihtout a Legend

**Source:** [Codeforces 713C - Sonya and Problem Wihtout a Legend](https://codeforces.com/problemset/problem/713/C)  
**Rating:** 2200  
**Pattern:** L1 isotonic regression after subtracting indices  
**Goal:** Change an integer array into a strictly increasing integer array.
Changing a value by one costs one; minimize the total cost.

## 1. First principles

If the final values are `x[i]`, define `y[i] = x[i] - i`. Then
`x[i] < x[i+1]` is equivalent to `y[i] <= y[i+1]`. Apply the same transform to
the input: `shifted[i] = values[i] - i`.

This is integer L1 isotonic regression. An optimum can choose every fitted
level from the sorted observed `shifted` values. A DP over positions and the
last chosen level needs only prefix minima.

## 2. Cases that decide correctness

- Already strictly increasing input costs zero.
- Equal final shifted levels represent consecutive original values.
- Negative shifted values are valid.
- Duplicate candidate levels must remain available.
- Prefix minima enforce nondecreasing fitted levels.

## 3. Brute force: enumerate every bounded fitted sequence

```python
from itertools import combinations_with_replacement


def increasing_change_cost_brute(values: list[int]) -> int:
    if not values or any(type(value) is not int for value in values):
        raise ValueError("values must be integers")
    shifted = [value - index for index, value in enumerate(values)]
    lower = min(shifted)
    upper = max(shifted)
    return min(
        sum(abs(value - fitted) for value, fitted in zip(shifted, levels, strict=True))
        for levels in combinations_with_replacement(
            range(lower, upper + 1), len(values)
        )
    )
```

**Complexity:** exponential in the value range and array length.

## 4. Better approach: DP over the complete integer range

For each position, keep the best cost ending at every integer between the
minimum and maximum shifted values. Prefix minima give
`O(n * value_range)` time, but large coordinates make that range unusable.

## 5. Expert solution: compress levels to observed values

```python
def minimum_increasing_change_cost(values: list[int]) -> int:
    if not values or any(type(value) is not int for value in values):
        raise ValueError("values must be integers")
    shifted = [value - index for index, value in enumerate(values)]
    candidates = sorted(shifted)
    dp = [abs(shifted[0] - candidate) for candidate in candidates]
    for value in shifted[1:]:
        next_dp = [0] * len(candidates)
        prefix_best = dp[0]
        for index, candidate in enumerate(candidates):
            prefix_best = min(prefix_best, dp[index])
            next_dp[index] = prefix_best + abs(value - candidate)
        dp = next_dp
    return min(dp)
```

### Why the expert code is correct

Subtracting indices preserves every unit-change cost and converts strictness
to monotonicity. Moving any fitted plateau until it reaches an observed value
cannot increase its sum of absolute deviations, so compressed levels contain
an optimum. Each prefix minimum considers every allowed preceding level.

**Complexity:** `O(n^2)` time and `O(n)` space.

## 6. What to remember

```text
strictly increasing integers -> subtract the index
resulting task -> nondecreasing L1 fit
absolute-cost optimum -> observed values are sufficient candidates
```
