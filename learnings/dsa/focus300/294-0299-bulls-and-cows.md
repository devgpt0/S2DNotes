# Focus300 294: LeetCode 299 - Bulls and Cows

**Source:** [LeetCode 299](https://leetcode.com/problems/bulls-and-cows/)  
**Difficulty:** Easy  
**Pattern:** frequency accounting

## Exact contract

Return the number of bulls and cows for the secret and guess strings.

## First principles

A bull is a position match; a cow is a value match in the wrong position. Counting exact matches first and then balancing the leftover frequencies prevents double counting.

## Cases that decide correctness

- A character can contribute to at most one cow after bull removal.
- Repeated digits or letters need frequency balancing.
- Positions that already match are bulls, not cows.
- The output format must separate bulls and cows clearly.

## Brute force

```python
from collections import Counter

def get_hint_brute(secret, guess):
    bulls = sum(a == b for a, b in zip(secret, guess))
    s = Counter(secret)
    g = Counter(guess)
    cows = sum(min(s[d], g[d]) for d in s) - bulls
    return f"{bulls}A{cows}B"
```

Compare every unmatched position against every other position.

## Better insight

Track exact matches and leftover frequency differences in one pass.

## Expert solution

```python
from collections import Counter

def get_hint(secret, guess):
    bulls = sum(a == b for a, b in zip(secret, guess))
    s = Counter(secret)
    g = Counter(guess)
    cows = sum(min(s[d], g[d]) for d in s) - bulls
    return f"{bulls}A{cows}B"
```

Count bulls directly, then use a frequency balance to compute cows from the unmatched characters.

**Complexity:** O(n) time and O(1) space for fixed-size alphabets.
