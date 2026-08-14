# ICPC300 239: Codeforces 1553F - Pairwise Modulo

**Source:** [Codeforces 1553F - Pairwise Modulo](https://codeforces.com/problemset/problem/1553/F)  
**Difficulty:** 2200  
**Pattern:** value-domain Fenwick counts plus remainder range adjustments

## Exact contract

Given a permutation `p` of `1..n`, for every prefix return

`sum(p[i] % p[j] + p[j] % p[i])` over all unordered index pairs in that prefix.

## First principles

When inserting `x`, split its new contribution:

- `x % y = x - floor(x/y)*y` for each previous `y`;
- `y % x = y - floor(y/x)*x`.

For the first sum, every inserted `y` range-adds adjustment `-k*y` to future
values in `[k*y,(k+1)*y)`, leaving a baseline `x` per prior value. For the
second sum, Fenwick frequency range counts accumulate `sum floor(y/x)` over
multiples of `x`.

## Cases that decide correctness

- Prefix one has sum zero.
- A smaller value modulo a larger value equals itself.
- Multiple intervals use inclusive integer endpoints.
- The permutation guarantee bounds the value domain by `n`.
- Running totals need 64-bit-range integers.

## Brute force: add every new pair

```python
def pairwise_modulo_brute(permutation: list[int]) -> list[int]:
    size = len(permutation)
    if sorted(permutation) != list(range(1, size + 1)):
        raise ValueError("input must be a permutation of 1..n")
    answer = 0
    answers: list[int] = []
    for right, value in enumerate(permutation):
        for previous in permutation[:right]:
            answer += value % previous + previous % value
        answers.append(answer)
    return answers
```

This takes `O(n^2)` time.

## Better approach: group quotients with frequency scans

Grouping values by equal floor quotient avoids visiting absent values, but a
plain frequency array still repeats too much work. Fenwick range counts and
range-adjustment point queries make each harmonic interval logarithmic.

## Expert solution: dual Fenwick contributions

```python
def pairwise_modulo_prefixes(permutation: list[int]) -> list[int]:
    size = len(permutation)
    if sorted(permutation) != list(range(1, size + 1)):
        raise ValueError("input must be a permutation of 1..n")
    counts = [0] * (size + 2)
    adjustments = [0] * (size + 3)

    def add(tree: list[int], position: int, delta: int) -> None:
        while position < len(tree):
            tree[position] += delta
            position += position & -position

    def prefix(tree: list[int], position: int) -> int:
        result = 0
        while position:
            result += tree[position]
            position -= position & -position
        return result

    def count_range(left: int, right: int) -> int:
        return prefix(counts, right) - prefix(counts, left - 1)

    def adjust_range(left: int, right: int, delta: int) -> None:
        add(adjustments, left, delta)
        add(adjustments, right + 1, -delta)

    seen = 0
    previous_sum = 0
    total = 0
    answers: list[int] = []

    for value in permutation:
        value_mod_previous = seen * value + prefix(adjustments, value)

        quotient_sum = 0
        for lower in range(value, size + 1, value):
            upper = min(size, lower + value - 1)
            quotient_sum += (lower // value) * count_range(lower, upper)
        previous_mod_value = previous_sum - value * quotient_sum
        total += value_mod_previous + previous_mod_value
        answers.append(total)

        add(counts, value, 1)
        seen += 1
        previous_sum += value
        for lower in range(value, size + 1, value):
            upper = min(size, lower + value - 1)
            adjust_range(lower, upper, -lower)
    return answers
```

The adjustment at future coordinate `x` is exactly
`-sum(floor(x/y)*y)` over inserted `y`, while quotient-group frequency counts
compute the symmetric remainder sum. Their addition is the new pair total.

**Complexity:** `O(n log^2 n)` time over the permutation's harmonic intervals
and `O(n)` space.
