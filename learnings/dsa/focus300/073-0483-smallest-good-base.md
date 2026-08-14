# Focus300 073: LeetCode 483 - Smallest Good Base

**Source:** [LeetCode 483](https://leetcode.com/problems/smallest-good-base/)  
**Difficulty:** Hard  
**Pattern:** binary search over geometric series

## Exact contract

Given the decimal string of an integer `number` from 3 through `10^18`, return
the smallest integer base `base >= 2` in which every representation digit is
one. The returned base is a decimal string.

## First principles

A representation with `exponent + 1` ones satisfies

```text
number = 1 + base + base^2 + ... + base^exponent
```

The smallest base produces the greatest possible digit count. Try exponents in
descending order and binary-search the strictly increasing geometric sum using
integer arithmetic only.

## Cases that decide correctness

- Base `number - 1` always gives representation `11`.
- The maximum exponent is at most `floor(log2(number))`.
- Floating roots can round incorrectly near `10^18` and are avoided.
- Geometric-sum construction may stop as soon as it exceeds the target.
- Return the first base found while exponents decrease.

## Brute force: test every possible base

```python
def smallest_good_base_brute(text: str) -> str:
    if not text.isascii() or not text.isdigit() or not 3 <= int(text) <= 10**18:
        raise ValueError("text must encode an integer from 3 through 10^18")

    number = int(text)
    for base in range(2, number):
        remaining = number
        while remaining and remaining % base == 1:
            remaining //= base
        if remaining == 0:
            return str(base)
    raise RuntimeError("base number - 1 always exists")
```

This takes up to `O(number log number)` digit checks.

## Better transition: fix the digit count first

For one exponent, the geometric sum is strictly increasing in the base. Binary
search therefore finds its only possible base. Descending exponents ensure the
first solution uses the smallest base.

## Expert solution: exact nested binary search

```python
def smallest_good_base(text: str) -> str:
    if not text.isascii() or not text.isdigit() or not 3 <= int(text) <= 10**18:
        raise ValueError("text must encode an integer from 3 through 10^18")

    number = int(text)

    def geometric_sum(base: int, exponent: int) -> int:
        total = 1
        power = 1
        for _ in range(exponent):
            power *= base
            total += power
            if total > number:
                break
        return total

    for exponent in range(number.bit_length() - 1, 0, -1):
        low = 2
        high = number - 1
        while low <= high:
            base = (low + high) // 2
            total = geometric_sum(base, exponent)
            if total == number:
                return str(base)
            if total < number:
                low = base + 1
            else:
                high = base - 1
    raise RuntimeError("base number - 1 always exists")
```

For each exponent, binary search is complete because the series is monotonic.
Any smaller base representation would contain more ones, so testing exponent
counts from largest to smallest makes the first returned base globally minimal.

**Complexity:** `O(log^3 number)` integer operations and `O(1)` space.
