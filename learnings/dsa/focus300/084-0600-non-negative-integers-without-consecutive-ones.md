# Focus300 084: LeetCode 600 - Non-negative Integers without Consecutive Ones

**Source:** [LeetCode 600](https://leetcode.com/problems/non-negative-integers-without-consecutive-ones/)  
**Difficulty:** Hard  
**Pattern:** Fibonacci counts over a binary prefix

## Exact contract

Given an integer `n` with `0 <= n <= 1_000_000_000`, count the integers in the
inclusive range `[0, n]` whose binary representation does not contain `11`.
Leading zeroes are irrelevant; zero is valid.

## First principles

Let `ways[length]` count valid binary suffixes of exactly `length` positions.
Such a suffix starts with `0` followed by any valid suffix, or with `10`
followed by any valid shorter suffix, so the counts are Fibonacci-like. While
scanning `n` from its highest bit, choosing `0` where `n` has `1` completes a
whole smaller branch immediately.

## Cases that decide correctness

- `0` contributes one valid number.
- The range is inclusive, so add `n` itself when its bits stay valid.
- Once the prefix of `n` contains `11`, `n` and all equal-prefix continuations
  are invalid and the scan stops.
- Counts for a remaining zero-bit suffix and one-bit suffix are different.
- Boolean values are rejected even though `bool` subclasses `int` in Python.

## Brute force: inspect every number

```python
def count_without_consecutive_ones_brute(limit: int) -> int:
    if type(limit) is not int:
        raise TypeError("limit must be an integer")
    if not 0 <= limit <= 1_000_000_000:
        raise ValueError("limit must be between 0 and 1000000000")
    return sum("11" not in format(value, "b") for value in range(limit + 1))
```

This takes `O(n log n)` time to build and inspect all binary representations.

## Better approach: memoized binary digit DP

A digit DP can track `(bit index, previous bit, already smaller)` and memoize
the two non-tight dimensions. It runs in `O(log n)` time, but the iterative
prefix count below needs fewer states and exposes the Fibonacci structure.

## Expert solution: count smaller branches during one scan

```python
def count_without_consecutive_ones(limit: int) -> int:
    if type(limit) is not int:
        raise TypeError("limit must be an integer")
    if not 0 <= limit <= 1_000_000_000:
        raise ValueError("limit must be between 0 and 1000000000")

    bit_count = limit.bit_length()
    ways = [0] * (bit_count + 2)
    ways[0] = 1
    ways[1] = 2
    for length in range(2, bit_count + 1):
        ways[length] = ways[length - 1] + ways[length - 2]

    answer = 0
    previous_bit = 0
    for bit in range(bit_count - 1, -1, -1):
        if limit & (1 << bit):
            answer += ways[bit]
            if previous_bit == 1:
                return answer
            previous_bit = 1
        else:
            previous_bit = 0
    return answer + 1
```

At each set bit, `ways[bit]` counts every valid number that first becomes
smaller there. If no adjacent set bits terminate the scan, the final `+1`
counts `n` itself.

**Complexity:** `O(log n)` time and `O(log n)` space for the count table.
