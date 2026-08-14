# ICPC300 120: CSES - Writing Numbers

**Source:** [CSES - Writing Numbers](https://cses.fi/problemset/task/1086/)  
**Pattern:** positional digit counting plus binary search  
**Goal:** Given `copies_per_digit` copies of every decimal digit, find the
largest `k` for which writing every integer from `1` through `k` uses at most
that many copies of each digit.

## 1. First principles

Feasibility is monotone: if `1..k` can be written, every smaller prefix can;
once a digit runs out, every larger prefix also fails. This permits binary
search on `k`.

For a fixed decimal position, full cycles of length `10 * position` contribute
the same number of every nonzero digit. Zero needs a correction because leading
zeros are not written.

## 2. Cases that decide correctness

- With zero available copies, the answer is `0`.
- A number may exhaust any one digit; all ten counts must fit.
- Repeated digits in one number consume multiple copies.
- Leading zeros never consume copies.
- The answer can be much larger than the given copy count, so the upper search
  bound is discovered by doubling.

## 3. Brute force: write the numbers one by one

```python
def maximum_written_brute(copies_per_digit: int) -> int:
    if copies_per_digit < 0:
        raise ValueError("copies_per_digit must be nonnegative")
    used = [0] * 10
    number = 0
    while True:
        candidate = number + 1
        required = [0] * 10
        for character in str(candidate):
            required[int(character)] += 1
        if any(used[digit] + required[digit] > copies_per_digit for digit in range(10)):
            return number
        for digit in range(10):
            used[digit] += required[digit]
        number = candidate
```

**Complexity:** `O(k log k)` time and `O(1)` auxiliary space for the returned
answer `k`.

## 4. Better: digit DP inside binary search

```python
from functools import cache


def maximum_written_digit_dp(copies_per_digit: int) -> int:
    if copies_per_digit < 0:
        raise ValueError("copies_per_digit must be nonnegative")

    def digit_counts(limit: int) -> tuple[int, ...]:
        digits = tuple(int(character) for character in str(limit))

        @cache
        def solve(
            position: int, tight: bool, started: bool
        ) -> tuple[int, tuple[int, ...]]:
            if position == len(digits):
                return 1, (0,) * 10
            upper = digits[position] if tight else 9
            total_ways = 0
            total_counts = [0] * 10
            for digit in range(upper + 1):
                next_started = started or digit != 0
                ways, counts = solve(
                    position + 1,
                    tight and digit == upper,
                    next_started,
                )
                total_ways += ways
                for value in range(10):
                    total_counts[value] += counts[value]
                if next_started:
                    total_counts[digit] += ways
            return total_ways, tuple(total_counts)

        return solve(0, True, False)[1]

    def fits(limit: int) -> bool:
        return max(digit_counts(limit)) <= copies_per_digit

    low = 0
    high = 1
    while fits(high):
        low = high
        high *= 2
    while low + 1 < high:
        middle = (low + high) // 2
        if fits(middle):
            low = middle
        else:
            high = middle
    return low
```

**Complexity:** `O(log^2 k)` digit-DP work and `O(log k)` memoization states
per feasibility test.

## 5. Expert solution: positional formulas inside binary search

```python
def maximum_written_positional(copies_per_digit: int) -> int:
    if copies_per_digit < 0:
        raise ValueError("copies_per_digit must be nonnegative")

    def digit_counts(limit: int) -> list[int]:
        counts = [0] * 10
        factor = 1
        while factor <= limit:
            lower = limit % factor
            current = (limit // factor) % 10
            higher = limit // (factor * 10)

            for digit in range(1, 10):
                counts[digit] += higher * factor
                if current > digit:
                    counts[digit] += factor
                elif current == digit:
                    counts[digit] += lower + 1

            if higher > 0:
                counts[0] += (higher - 1) * factor
                if current == 0:
                    counts[0] += lower + 1
                else:
                    counts[0] += factor
            factor *= 10
        return counts

    def fits(limit: int) -> bool:
        return max(digit_counts(limit)) <= copies_per_digit

    low = 0
    high = 1
    while fits(high):
        low = high
        high *= 2
    while low + 1 < high:
        middle = (low + high) // 2
        if fits(middle):
            low = middle
        else:
            high = middle
    return low
```

### Why the expert code is correct

The positional formula counts every written occurrence in `1..limit` exactly
once at its decimal position, with the zero correction removing leading-zero
representations. Therefore `fits` is exact. Binary search returns the final
true value of the monotone feasibility predicate, which is precisely the
largest writable prefix.

**Complexity:** `O(log^2 k)` time and `O(1)` auxiliary space.

## 6. What to remember

```text
prefix digit usage only increases -> binary search the answer
full positional cycles -> closed-form digit counts
digit zero -> subtract leading-zero blocks
```
