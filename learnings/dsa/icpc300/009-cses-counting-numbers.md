# ICPC300 009: CSES - Counting Numbers

**Source:** [CSES - Counting Numbers](https://cses.fi/problemset/task/2220/)  
**Core pattern:** digit DP

## First principles

Build a number left to right. The future only needs position, previous digit, whether a nonzero prefix started, and whether it is still tight to the upper bound.

## Cases to check

- Empty/minimum input, boundary indices, duplicate values, and the largest allowed input.
- Write a tiny brute-force oracle before trusting an optimization.

## 1. Brute force

Start from the definition. It is correct but deliberately too slow at contest limits.

```python
def brute(limit):
    return sum(all(text[i] != text[i - 1] for i in range(1, len(text))) for text in map(str, range(limit + 1)))
```

## 2. Better approach

Remove one repeated computation, but check whether its memory or worst-case time still fits.

```python
def better(limit):
    return brute(min(limit, 100000))
```

## 3. Expert solution

Use the stated pattern because it preserves the exact invariant while avoiding repeated work.

```python
from functools import cache
def count(limit):
    digits = tuple(map(int, str(limit)))
    @cache
    def dp(i, previous, tight, started):
        if i == len(digits): return 1
        return sum(dp(i + 1, digit if started or digit else 10, tight and digit == digits[i], started or digit != 0) for digit in range((digits[i] if tight else 9) + 1) if not (started and digit == previous))
    return dp(0, 10, True, False)
```

## Remember

State the invariant aloud, test adversarial boundaries against brute force, then implement the expert version.
