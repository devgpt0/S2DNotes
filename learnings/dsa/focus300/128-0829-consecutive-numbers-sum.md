# Focus300 128: LeetCode 829 - Consecutive Numbers Sum

**Source:** [LeetCode 829](https://leetcode.com/problems/consecutive-numbers-sum/)  
**Difficulty:** Hard  
**Pattern:** arithmetic-series divisibility and odd-divisor counting

## Exact contract

For a positive integer `n <= 10^9`, return the number of ways to write `n` as
one or more consecutive positive integers. Different starting values or lengths
are different representations.

## First principles

A length-`k` sequence starting at `a >= 1` sums to
`k*a + k*(k-1)/2`. Thus a length works exactly when
`n - k*(k-1)/2` is a positive multiple of `k`.

Equivalently, each representation corresponds to one odd divisor of `n`.
Removing powers of two and counting divisors of the remaining odd part gives
the answer directly.

## Cases that decide correctness

- The one-term representation `[n]` always exists.
- Sequence values must stay positive; zero or negative starts are invalid.
- Powers of two have only one representation.
- Both odd-length and even-length sequences are included by the divisor result.
- Factor exponents multiply as `(exponent + 1)` in the divisor count.

## Brute force: try every positive starting value

```python
def consecutive_sum_count_brute(number: int) -> int:
    if type(number) is not int or not 1 <= number <= 1_000_000_000:
        raise ValueError("number must be an integer between 1 and 10^9")

    ways = 0
    for start in range(1, number + 1):
        total = 0
        for value in range(start, number + 1):
            total += value
            if total == number:
                ways += 1
                break
            if total > number:
                break
    return ways
```

This literal enumeration is impractical for large inputs.

## Better approach: enumerate feasible sequence lengths

```python
def consecutive_sum_count_by_length(number: int) -> int:
    if type(number) is not int or not 1 <= number <= 1_000_000_000:
        raise ValueError("number must be an integer between 1 and 10^9")

    ways = 0
    length = 1
    while length * (length - 1) // 2 < number:
        remainder = number - length * (length - 1) // 2
        if remainder % length == 0:
            ways += 1
        length += 1
    return ways
```

Only `O(sqrt(n))` positive lengths can have a positive start.

## Expert solution: count divisors of the odd part

```python
def consecutive_sum_count(number: int) -> int:
    if type(number) is not int or not 1 <= number <= 1_000_000_000:
        raise ValueError("number must be an integer between 1 and 10^9")

    odd_part = number
    while odd_part % 2 == 0:
        odd_part //= 2

    divisor_count = 1
    factor = 3
    while factor * factor <= odd_part:
        exponent = 0
        while odd_part % factor == 0:
            odd_part //= factor
            exponent += 1
        divisor_count *= exponent + 1
        factor += 2
    if odd_part > 1:
        divisor_count *= 2
    return divisor_count
```

Factoring the odd part counts exactly the odd divisors and therefore exactly
the valid consecutive-positive representations.

**Complexity:** `O(sqrt(n))` time in the trial-division worst case and `O(1)`
space.
