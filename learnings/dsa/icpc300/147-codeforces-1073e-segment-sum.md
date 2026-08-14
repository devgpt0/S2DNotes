# 147. Segment Sum — Codeforces 1073E

**Source:** [Codeforces 1073E - Segment Sum](https://codeforces.com/problemset/problem/1073/E)  
**Difficulty:** 2200

## 1. Problem in plain words

Given `left`, `right`, and `k`, sum all integers in `[left, right]` whose decimal representation uses at most `k` distinct digits. Print the sum modulo `998_244_353`.

## 2. First principles

Compute a prefix function `S(limit)` and answer `S(right) - S(left - 1)`. A digit DP builds numbers from most significant digit to least. Its state records position, used digits, whether the prefix is already below the limit, and whether a non-leading-zero digit has started the number.

Each transition returns both a count and a sum. Placing digit `d` contributes `d × 10^remaining` to every suffix completion.

## 3. Cases that define correctness

- Leading zeros do not add digit `0` to the used set.
- The number `0` contributes zero to the sum.
- A digit already used does not increase the distinct count.
- Prefix subtraction must be normalized modulo the source modulus.

## 4. Brute force

Inspect every integer in the requested interval.

```python
MODULO = 998_244_353


def segment_sum_brute_force(left: int, right: int, max_distinct: int) -> int:
    if left < 0 or left > right or not 1 <= max_distinct <= 10:
        raise ValueError("invalid range or digit limit")

    answer = 0
    for value in range(left, right + 1):
        if len(set(str(value))) <= max_distinct:
            answer += value
    return answer % MODULO
```

Time is `O((right-left+1) log right)` and space is `O(10)`.

## 5. Better approach: memoized digit-set DP

Use an immutable tuple of used digits as the memoization key. This directly expresses the mathematics, though set construction and hashing add overhead.

```python
from functools import cache

MODULO = 998_244_353


def segment_sum_digit_sets(left: int, right: int, max_distinct: int) -> int:
    if left < 0 or left > right or not 1 <= max_distinct <= 10:
        raise ValueError("invalid range or digit limit")

    def prefix_sum(limit: int) -> int:
        if limit < 0:
            return 0
        digits = tuple(map(int, str(limit)))
        powers = [1] * (len(digits) + 1)
        for exponent in range(1, len(powers)):
            powers[exponent] = powers[exponent - 1] * 10 % MODULO

        @cache
        def dp(
            position: int, used: tuple[int, ...], tight: bool, started: bool
        ) -> tuple[int, int]:
            if position == len(digits):
                return 1, 0
            upper = digits[position] if tight else 9
            remaining = len(digits) - position - 1
            total_count = 0
            total_sum = 0
            used_set = set(used)
            for digit in range(upper + 1):
                next_started = started or digit != 0
                next_used_set = used_set if not next_started else used_set | {digit}
                if len(next_used_set) > max_distinct:
                    continue
                next_used = tuple(sorted(next_used_set))
                count, suffix_sum = dp(
                    position + 1,
                    next_used,
                    tight and digit == upper,
                    next_started,
                )
                total_count = (total_count + count) % MODULO
                total_sum += suffix_sum + digit * powers[remaining] * count
            return total_count, total_sum % MODULO

        return dp(0, (), True, False)[1]

    return (prefix_sum(right) - prefix_sum(left - 1)) % MODULO
```

There are `O(d · 2¹⁰)` logical states, each with at most ten transitions; `d` is the digit count.

## 6. Expert solution: bit-mask digit DP

Replace the tuple set by a 10-bit mask. Precomputed bit counts make the distinct-digit test constant time.

```python
from functools import cache

MODULO = 998_244_353


def segment_sum(left: int, right: int, max_distinct: int) -> int:
    if left < 0 or left > right or not 1 <= max_distinct <= 10:
        raise ValueError("invalid range or digit limit")

    bit_counts = [mask.bit_count() for mask in range(1 << 10)]

    def prefix_sum(limit: int) -> int:
        if limit < 0:
            return 0
        digits = tuple(map(int, str(limit)))
        powers = [1] * (len(digits) + 1)
        for exponent in range(1, len(powers)):
            powers[exponent] = powers[exponent - 1] * 10 % MODULO

        @cache
        def dp(position: int, mask: int, tight: bool, started: bool) -> tuple[int, int]:
            if position == len(digits):
                return 1, 0
            upper = digits[position] if tight else 9
            remaining = len(digits) - position - 1
            total_count = 0
            total_sum = 0
            for digit in range(upper + 1):
                next_started = started or digit != 0
                next_mask = mask if not next_started else mask | (1 << digit)
                if bit_counts[next_mask] > max_distinct:
                    continue
                count, suffix_sum = dp(
                    position + 1,
                    next_mask,
                    tight and digit == upper,
                    next_started,
                )
                total_count = (total_count + count) % MODULO
                total_sum += suffix_sum + digit * powers[remaining] * count
            return total_count, total_sum % MODULO

        return dp(0, 0, True, False)[1]

    return (prefix_sum(right) - prefix_sum(left - 1)) % MODULO
```

## 7. Why the expert solution is correct

Every integer up to the limit corresponds to one fixed-length digit path with leading zeros. The `started` flag prevents those zeros from entering the mask, while every real digit is included exactly once. The DP rejects exactly masks exceeding `k`, and the count-sum transition adds each placed digit at its decimal position for every valid suffix.

Time is `O(d · 2¹⁰ · 10)` and space is `O(d · 2¹⁰)`.
