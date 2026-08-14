# Focus300 071: LeetCode 479 - Largest Palindrome Product

**Source:** [LeetCode 479](https://leetcode.com/problems/largest-palindrome-product/)  
**Difficulty:** Hard  
**Pattern:** descending palindrome construction and factor search

## Exact contract

Given `n` from 1 through 8, find the largest palindrome that is a product of
two `n`-digit integers and return that palindrome modulo `1337`.

## First principles

Testing factor pairs repeats many non-palindromic products. For `n >= 2`, build
even-length palindromes in descending order by mirroring a possible leading
half. The first palindrome with an `n`-digit divisor is globally largest.
Testing factors only down to the square root is sufficient.

## Cases that decide correctness

- `n = 1` returns `9`, from `9 * 1`.
- Both factors must have exactly `n` digits.
- The palindrome is compared before applying modulo `1337`.
- A found divisor needs a quotient inside the same `n`-digit range.
- Descending candidate order permits an immediate return.

## Brute force: inspect every factor pair

```python
def largest_palindrome_product_brute(digits: int) -> int:
    if not 1 <= digits <= 8:
        raise ValueError("digits must be between 1 and 8")

    lower = 10 ** (digits - 1)
    upper = 10**digits - 1
    answer = 0
    for first in range(lower, upper + 1):
        for second in range(first, upper + 1):
            product = first * second
            text = str(product)
            if product > answer and text == text[::-1]:
                answer = product
    return answer % 1337
```

This takes `O(10^(2n))` factor checks.

## Better transition: generate only palindrome candidates

Mirroring a descending `n`-digit prefix generates the relevant `2n`-digit
palindromes in descending order. For a candidate, a divisor above its square
root uniquely exposes the paired factor below it.

## Expert solution: descending mirrored prefixes

```python
def largest_palindrome_product(digits: int) -> int:
    if not 1 <= digits <= 8:
        raise ValueError("digits must be between 1 and 8")
    if digits == 1:
        return 9

    lower = 10 ** (digits - 1)
    upper = 10**digits - 1
    for prefix in range(upper, lower - 1, -1):
        text = str(prefix)
        palindrome = int(text + text[::-1])
        factor = upper
        while factor * factor >= palindrome:
            if palindrome % factor == 0:
                other = palindrome // factor
                if lower <= other <= upper:
                    return palindrome % 1337
            factor -= 1
    raise RuntimeError("source constraints guarantee a product")
```

Prefixes are tried in strictly decreasing palindrome order. The factor loop
checks every possible larger factor of the candidate; if none works before the
square root, no valid pair exists. Therefore the first accepted candidate is
the required maximum.

**Complexity:** Worst-case `O(10^n * 10^n)` arithmetic checks, with strong
palindrome and square-root pruning, and `O(1)` space.
