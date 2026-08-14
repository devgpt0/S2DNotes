# ICPC300 225: Codeforces 55D - Beautiful numbers

**Source:** [Codeforces 55D - Beautiful numbers](https://codeforces.com/problemset/problem/55/D)  
**Rating:** 2500  
**Pattern:** digit DP with digit LCM and remainder modulo 2520  
**Goal:** For each inclusive range, count positive integers divisible by every
nonzero decimal digit they contain.

## 1. First principles

A number is divisible by all its nonzero digits exactly when it is divisible by
their least common multiple. Every possible digit LCM divides

```text
lcm(1, 2, ..., 9) = 2520
```

Thus a digit-DP state needs only the current LCM and the numeric prefix modulo
2520. At the end, test `remainder % digit_lcm == 0`.

## 2. Cases that decide correctness

- Digit zero imposes no divisibility requirement.
- Repeated digits do not change the LCM.
- Leading zeros are not digits of the number.
- The number zero is excluded because source ranges are positive.
- Range answers use `count(right) - count(left - 1)`.

## 3. Brute force: test every integer

```python
def beautiful_number_counts_brute(
    ranges: list[tuple[int, int]],
) -> list[int]:
    for left, right in ranges:
        if not 1 <= left <= right:
            raise ValueError("ranges must be positive and ordered")

    def is_beautiful(value: int) -> bool:
        return all(digit == "0" or value % int(digit) == 0 for digit in str(value))

    return [
        sum(is_beautiful(value) for value in range(left, right + 1))
        for left, right in ranges
    ]
```

**Complexity:** `O(sum of range lengths * log right)` time and `O(1)` space.

## 4. Better transition: compress both divisibility requirements

Remembering all seen digits is unnecessary: their LCM captures the exact final
condition. Remembering the whole prefix is also unnecessary because every LCM
divides 2520, so its remainder modulo 2520 preserves every needed remainder.

## 5. Expert solution: memoized digit DP

```python
from functools import lru_cache
from math import gcd


def beautiful_number_counts(ranges: list[tuple[int, int]]) -> list[int]:
    for left, right in ranges:
        if not 1 <= left <= right:
            raise ValueError("ranges must be positive and ordered")

    def count_up_to(limit: int) -> int:
        if limit <= 0:
            return 0
        digits = [int(character) for character in str(limit)]

        @lru_cache(maxsize=None)
        def count(
            position: int,
            remainder: int,
            digit_lcm: int,
            tight: bool,
            started: bool,
        ) -> int:
            if position == len(digits):
                return int(started and remainder % digit_lcm == 0)
            upper = digits[position] if tight else 9
            answer = 0
            for digit in range(upper + 1):
                next_started = started or digit != 0
                next_lcm = digit_lcm
                if digit != 0:
                    next_lcm = digit_lcm * digit // gcd(digit_lcm, digit)
                answer += count(
                    position + 1,
                    (remainder * 10 + digit) % 2520,
                    next_lcm,
                    tight and digit == upper,
                    next_started,
                )
            return answer

        return count(0, 0, 1, True, False)

    return [count_up_to(right) - count_up_to(left - 1) for left, right in ranges]
```

### Why the expert code is correct

The state retains the exact LCM of all nonzero digits and the prefix remainder
under a modulus divisible by every possible LCM. Every digit choice is explored
subject to the upper-bound tight flag. The terminal divisibility test is
therefore equivalent to divisibility by every nonzero digit, and prefix-count
subtraction gives each requested interval.

**Complexity:** `O(19 * 2520 * 48 * 10)` states/transitions per bound and
`O(19 * 2520 * 48)` cache space; 48 is the number of divisors of 2520.

## 6. What to remember

```text
divisible by every digit -> divisible by their LCM
all digit LCMs divide 2520 -> remainder modulo 2520
range count -> two upper-bound digit DPs
```
