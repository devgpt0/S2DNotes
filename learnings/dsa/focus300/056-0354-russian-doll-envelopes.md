# Focus300 056: LeetCode 354 - Russian Doll Envelopes

**Source:** [LeetCode 354 - Russian Doll Envelopes](https://leetcode.com/problems/russian-doll-envelopes/)  
**Difficulty:** Hard  
**Pattern:** two-dimensional strict chain reduced to LIS  

## Exact contract

Return the largest number of envelopes that can be nested. Envelope `(w1,h1)`
fits in `(w2,h2)` only when both `w1 < w2` and `h1 < h2`; rotation is forbidden.

## First principles

Sort width ascending. Equal widths must never enter the same chain, so sort
their heights descending. A strictly increasing subsequence of resulting
heights then corresponds exactly to a valid two-dimensional chain.

## Cases that decide correctness

- Equal widths cannot nest even when heights increase.
- Equal heights cannot nest because both dimensions are strict.
- Input order has no meaning.
- Duplicate envelopes contribute at most one chain position.
- Empty input returns zero.

## Brute force: try every next unused containing envelope

```python
Envelope = tuple[int, int]


def maximum_envelopes_brute(envelopes: list[Envelope]) -> int:
    if any(
        type(width) is not int or type(height) is not int or width <= 0 or height <= 0
        for width, height in envelopes
    ):
        raise ValueError("envelope dimensions must be positive integers")

    def search(width: int, height: int, used: int) -> int:
        answer = 0
        for index, (next_width, next_height) in enumerate(envelopes):
            if not used >> index & 1 and next_width > width and next_height > height:
                answer = max(
                    answer,
                    1 + search(next_width, next_height, used | 1 << index),
                )
        return answer

    return search(0, 0, 0)
```

**Complexity:** `O(n!)` time and `O(n)` recursion space.

## Better approach: quadratic chain DP

```python
Envelope = tuple[int, int]


def maximum_envelopes_quadratic(envelopes: list[Envelope]) -> int:
    if any(
        type(width) is not int or type(height) is not int or width <= 0 or height <= 0
        for width, height in envelopes
    ):
        raise ValueError("envelope dimensions must be positive integers")
    ordered = sorted(envelopes)
    best = [1] * len(ordered)
    for current, (width, height) in enumerate(ordered):
        for previous in range(current):
            previous_width, previous_height = ordered[previous]
            if previous_width < width and previous_height < height:
                best[current] = max(best[current], best[previous] + 1)
    return max(best, default=0)
```

This directly evaluates every predecessor in `O(n^2)` time and `O(n)` space.

## Expert solution: width tie reversal plus strict height LIS

```python
from bisect import bisect_left


Envelope = tuple[int, int]


def maximum_envelopes(envelopes: list[Envelope]) -> int:
    if any(
        type(width) is not int or type(height) is not int or width <= 0 or height <= 0
        for width, height in envelopes
    ):
        raise ValueError("envelope dimensions must be positive integers")
    ordered = sorted(envelopes, key=lambda envelope: (envelope[0], -envelope[1]))
    smallest_tail: list[int] = []
    for _, height in ordered:
        position = bisect_left(smallest_tail, height)
        if position == len(smallest_tail):
            smallest_tail.append(height)
        else:
            smallest_tail[position] = height
    return len(smallest_tail)
```

Descending heights inside a width tie make those envelopes appear in decreasing
order, so a strict height LIS cannot select two of them. Across larger widths,
the LIS strictness enforces the second dimension.

**Complexity:** `O(n log n)` time and `O(n)` space.

