# ICPC300 263: Codeforces 932E - Team Work

**Source:** [Codeforces 932E - Team Work](https://codeforces.com/problemset/problem/932/E)  
**Rating:** 2300  
**Pattern:** Stirling transform of powers into falling factorials  
**Goal:** Compute `sum(C(n, i) * i^k for i = 0..n)` modulo
`1_000_000_007` for nonnegative `n` and `k`.

## 1. First principles

Ordinary powers expand through Stirling numbers of the second kind:

```text
i^k = sum(S(k, j) * falling(i, j), j = 0..k)
```

Choosing an `i`-element subset and then an ordered `j`-tuple inside it can
instead be done by choosing the ordered tuple from all `n` elements, followed
by any subset of the remaining elements. Therefore

```text
sum(C(n, i) * falling(i, j)) = falling(n, j) * 2^(n-j).
```

## 2. Cases that decide correctness

- `k = 0` gives `2^n`, including the conventional value `0^0 = 1`.
- Terms with `j > n` vanish because the falling factorial is zero.
- `n = 0` is valid.
- Every multiplication and addition is reduced modulo the prime.
- Only one Stirling row is needed.

## 3. Brute force: use the definition

```python
from math import comb


MODULO = 1_000_000_007


def teamwork_sum_brute(size: int, power: int) -> int:
    if type(size) is not int or type(power) is not int or size < 0 or power < 0:
        raise ValueError("size and power must be nonnegative integers")
    return (
        sum(comb(size, chosen) * chosen**power for chosen in range(size + 1)) % MODULO
    )
```

**Complexity:** `O(n log k)` arithmetic operations with large intermediate
integers.

## 4. Better approach: subset DP by chosen cardinality

Pascal's recurrence can generate every `C(n, i)` modulo the prime before
summing. It removes large integers but remains linear in `n`, which is too
large in the source constraints.

## 5. Expert solution: one Stirling row

```python
MODULO = 1_000_000_007


def teamwork_sum(size: int, power: int) -> int:
    if type(size) is not int or type(power) is not int or size < 0 or power < 0:
        raise ValueError("size and power must be nonnegative integers")

    stirling = [0] * (power + 1)
    stirling[0] = 1
    for exponent in range(1, power + 1):
        for groups in range(exponent, 0, -1):
            stirling[groups] = (
                stirling[groups - 1] + groups * stirling[groups]
            ) % MODULO
        stirling[0] = 0

    answer = 0
    falling = 1
    for groups in range(min(size, power) + 1):
        if groups:
            falling = falling * (size - groups + 1) % MODULO
        answer += stirling[groups] * falling * pow(2, size - groups, MODULO)
        answer %= MODULO
    return answer
```

### Why the expert code is correct

The Stirling recurrence partitions `power` labeled positions into `groups`
nonempty groups. Substituting the falling-factorial expansion and swapping the
two sums applies the ordered-tuple identity above to each group count, so the
computed terms equal the original binomial-power sum exactly.

**Complexity:** `O(k^2 + k log MODULO)` time and `O(k)` space.

## 6. What to remember

```text
power -> Stirling numbers times falling factorials
binomial sum of falling(i, j) -> falling(n, j) * 2^(n-j)
huge n disappears -> only k-sized work remains
```
