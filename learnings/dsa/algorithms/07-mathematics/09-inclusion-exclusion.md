# Inclusion-Exclusion Principle

## Idea

When sets overlap, adding their sizes double-counts intersections. Inclusion-
exclusion alternates signs by subset size.

## Visual model

```text
|A union B| = |A| + |B| - |A intersection B|
```

For more sets: add single sets, subtract pair intersections, add triple
intersections, and continue.

## Classroom board: divisible by 2 or 3 through 10

```text
multiples of 2: 5
multiples of 3: 3
multiples of both (6): 1
union = 5 + 3 - 1 = 7
```

We subtract the intersection because adding both sets counted it twice.

## Steps

1. Enumerate each non-empty subset of conditions.
2. Count items satisfying every condition in that subset.
3. Add the count for odd subset size; subtract it for even subset size.

## First-principles derivation

Adding sizes of overlapping sets counts their intersection more than once.
Subtract pairwise overlaps, add triple overlaps, and continue with alternating
signs.

Each object belonging to `r` sets receives total coefficient exactly one.

## Classroom board: divisible by 2 or 3

Count values in `1..12`.

```text
A: divisible by 2 -> {2,4,6,8,10,12}, size 6
B: divisible by 3 -> {3,6,9,12},      size 4
A intersect B: divisible by 6 -> {6,12}, size 2

|A union B| = 6 + 4 - 2 = 8
values: {2,3,4,6,8,9,10,12}
```

The intersection is subtracted because `6` and `12` were each counted
twice.

## Pattern recognition

Use it for “at least one condition,” forbidden properties, divisible-by-any
counts, derangements, or union sizes when intersections are easy to count.

## Implementation: count `1..limit` divisible by any divisor

The code uses the GCD function from the
[Euclid note](01-greatest-common-divisor.md).

### C++

```cpp
long long countDivisible(long long limit, const std::vector<long long>& divisors) {
    long long answer = 0;
    for (int mask = 1; mask < (1 << divisors.size()); ++mask) {
        long long multiple = 1;
        bool tooLarge = false;
        for (int bit = 0; bit < static_cast<int>(divisors.size()); ++bit) if (mask & (1 << bit)) {
            long long divisor = divisors[bit];
            long long common = std::gcd(multiple, divisor);
            if (multiple > limit / (divisor / common)) { tooLarge = true; break; }
            multiple *= divisor / common;
        }
        if (tooLarge) continue;
        long long count = limit / multiple;
        if (__builtin_popcount(mask) & 1) answer += count;
        else answer -= count;
    }
    return answer;
}
```

### Python

```python
from math import gcd


def count_divisible(limit: int, divisors: list[int]) -> int:
    answer = 0
    for mask in range(1, 1 << len(divisors)):
        multiple = 1
        for bit, divisor in enumerate(divisors):
            if mask & (1 << bit):
                multiple = multiple // gcd(multiple, divisor) * divisor
                if multiple > limit:
                    break
        if multiple <= limit:
            count = limit // multiple
            answer += count if mask.bit_count() % 2 else -count
    return answer
```

### Java

```java
static long countDivisible(long limit, long[] divisors) {
    long answer = 0;
    for (int mask = 1; mask < 1 << divisors.length; mask++) {
        long multiple = 1;
        boolean tooLarge = false;
        for (int bit = 0; bit < divisors.length; bit++) if ((mask & (1 << bit)) != 0) {
            long factor = divisors[bit] / gcd(multiple, divisors[bit]);
            if (multiple > limit / factor) { tooLarge = true; break; }
            multiple *= factor;
        }
        if (!tooLarge) {
            long count = limit / multiple;
            answer += Integer.bitCount(mask) % 2 == 1 ? count : -count;
        }
    }
    return answer;
}
```

## Why it works

An item satisfying exactly `k` conditions is counted
`C(k,1)-C(k,2)+...+(-1)^(k+1)C(k,k) = 1` time.

## Complexity

For `m` divisors, time is `O(m 2^m)` and space is `O(1)`.

## Common mistakes

- Using product instead of LCM for intersections.
- Reversing odd/even signs.
- Allowing LCM multiplication to overflow.
- Including divisor `0`.
