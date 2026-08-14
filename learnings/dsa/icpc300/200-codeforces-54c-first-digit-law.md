# ICPC300 200: Codeforces 54C - First Digit Law

**Source:** [Codeforces 54C - First Digit Law](https://codeforces.com/problemset/problem/54/C)  
**Rating:** 2200  
**Pattern:** leading-digit range counting plus Poisson-binomial DP  
**Goal:** Choose one integer uniformly and independently from each inclusive
interval. Return the probability that at least the requested percentage of the
chosen integers begin with decimal digit `1`.

## 1. First principles

Numbers beginning with `1` form blocks

```text
[1, 1], [10, 19], [100, 199], ...
```

Intersect those blocks with each interval to obtain its success probability.
The intervals have different probabilities, so use a DP where `dp[count]` is
the probability of exactly `count` successes after the processed intervals.

## 2. Cases that decide correctness

- Interval endpoints are inclusive positive integers.
- The required count is `ceil(n * percentage / 100)`.
- A percentage of zero always succeeds.
- Selection from different intervals is independent.
- The answer is a probability, not a count modulo a prime.

## 3. Brute force: enumerate every tuple of choices

```python
from itertools import product


def first_digit_probability_brute(
    intervals: list[tuple[int, int]], percentage: int
) -> float:
    if not intervals or not 0 <= percentage <= 100:
        raise ValueError("intervals and percentage are invalid")
    for left, right in intervals:
        if not 1 <= left <= right:
            raise ValueError("interval endpoints must be positive and ordered")

    required = (len(intervals) * percentage + 99) // 100
    favorable = 0
    total = 0
    ranges = [range(left, right + 1) for left, right in intervals]
    for choices in product(*ranges):
        successes = sum(str(value).startswith("1") for value in choices)
        favorable += successes >= required
        total += 1
    return favorable / total
```

**Complexity:** `O(product of interval lengths * n)` time and `O(n)` space.

## 4. Better transition: count decimal blocks, not integers

Only `O(log right)` leading-one blocks intersect an interval. After converting
each interval to one Bernoulli probability, an ordinary count DP combines the
independent but non-identical trials.

## 5. Expert solution: digit-block counting and probability DP

```python
def first_digit_probability(intervals: list[tuple[int, int]], percentage: int) -> float:
    if not intervals or not 0 <= percentage <= 100:
        raise ValueError("intervals and percentage are invalid")
    for left, right in intervals:
        if not 1 <= left <= right:
            raise ValueError("interval endpoints must be positive and ordered")

    def leading_one_count(limit: int) -> int:
        count = 0
        power = 1
        while power <= limit:
            block_right = min(limit, 2 * power - 1)
            if block_right >= power:
                count += block_right - power + 1
            power *= 10
        return count

    probabilities: list[float] = []
    for left, right in intervals:
        favorable = leading_one_count(right) - leading_one_count(left - 1)
        probabilities.append(favorable / (right - left + 1))

    dp = [0.0] * (len(intervals) + 1)
    dp[0] = 1.0
    processed = 0
    for probability in probabilities:
        next_dp = [0.0] * (len(intervals) + 1)
        for successes in range(processed + 1):
            next_dp[successes] += dp[successes] * (1.0 - probability)
            next_dp[successes + 1] += dp[successes] * probability
        dp = next_dp
        processed += 1

    required = (len(intervals) * percentage + 99) // 100
    return sum(dp[required:])
```

### Why the expert code is correct

`leading_one_count` partitions all favorable positive integers into disjoint
decimal blocks, so every interval probability is exact. The DP applies the law
of total probability for failure and success of each independent interval.
After all trials, summing states from the ceiling threshold upward is exactly
the requested event.

**Complexity:** `O(n^2 + n log R)` time and `O(n)` space.

## 6. What to remember

```text
leading digit 1 -> union of [10^d, 2*10^d - 1]
one interval -> one Bernoulli probability
different independent probabilities -> Poisson-binomial DP
```
