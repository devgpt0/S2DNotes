# Focus300 102: LeetCode 730 - Count Different Palindromic Subsequences

**Source:** [LeetCode 730](https://leetcode.com/problems/count-different-palindromic-subsequences/)  
**Difficulty:** Hard  
**Pattern:** interval dynamic programming with duplicate removal

## Exact contract

Given a non-empty string `text` of at most `1000` characters from `a` through
`d`, count its distinct, non-empty palindromic subsequence strings. Different
index choices that spell the same string count once. Return the count modulo
`1_000_000_007`.

## First principles

For unequal interval ends, inclusion-exclusion combines the intervals that
drop either end. Equal ends wrap every inner palindrome, but also create the
single-character and doubled-end palindromes. Equal copies inside determine
whether those two additions are new or duplicate existing wrapped families.

## Cases that decide correctness

- Distinct strings, not index selections, are counted.
- A one-character interval contributes exactly one palindrome.
- With equal ends, zero, one, or at least two equal inner characters require
  `+2`, `+1`, or subtraction of the duplicated middle interval.
- Intermediate differences may be negative; reduce every state modulo the
  modulus.
- Only source alphabet characters `a`, `b`, `c`, and `d` are accepted.

## Brute force: enumerate every subsequence

```python
def count_palindromes_brute(text: str) -> int:
    if not text or any(character not in "abcd" for character in text):
        raise ValueError("text must be non-empty and use only a through d")

    palindromes: set[str] = set()
    for mask in range(1, 1 << len(text)):
        candidate = "".join(
            character for index, character in enumerate(text) if mask & (1 << index)
        )
        if candidate == candidate[::-1]:
            palindromes.add(candidate)
    return len(palindromes) % 1_000_000_007
```

This takes `O(n * 2^n)` time and exponential space in the number of distinct
subsequences.

## Better solution: scan for matching inner boundaries

```python
def count_palindromes_better(text: str) -> int:
    if not text or any(character not in "abcd" for character in text):
        raise ValueError("text must be non-empty and use only a through d")

    modulus = 1_000_000_007
    length = len(text)
    counts = [[0] * length for _ in range(length)]
    for index in range(length):
        counts[index][index] = 1

    for width in range(2, length + 1):
        for left in range(length - width + 1):
            right = left + width - 1
            if text[left] != text[right]:
                counts[left][right] = (
                    counts[left + 1][right]
                    + counts[left][right - 1]
                    - counts[left + 1][right - 1]
                ) % modulus
                continue

            low = left + 1
            high = right - 1
            while low <= high and text[low] != text[left]:
                low += 1
            while low <= high and text[high] != text[left]:
                high -= 1
            inner = counts[left + 1][right - 1] if width > 2 else 0
            if low > high:
                counts[left][right] = (2 * inner + 2) % modulus
            elif low == high:
                counts[left][right] = (2 * inner + 1) % modulus
            else:
                duplicate = counts[low + 1][high - 1] if low + 1 <= high - 1 else 0
                counts[left][right] = (2 * inner - duplicate) % modulus

    return counts[0][length - 1]
```

Scanning inward makes this `O(n^3)` time and `O(n^2)` space.

## Expert solution: precompute the nearest equal positions

```python
def count_palindromic_subsequences(text: str) -> int:
    if not text or any(character not in "abcd" for character in text):
        raise ValueError("text must be non-empty and use only a through d")

    modulus = 1_000_000_007
    length = len(text)
    next_equal = [length] * length
    previous_equal = [-1] * length
    latest: dict[str, int] = {}
    for index in range(length - 1, -1, -1):
        next_equal[index] = latest.get(text[index], length)
        latest[text[index]] = index
    latest.clear()
    for index, character in enumerate(text):
        previous_equal[index] = latest.get(character, -1)
        latest[character] = index

    counts = [[0] * length for _ in range(length)]
    for index in range(length):
        counts[index][index] = 1

    for width in range(2, length + 1):
        for left in range(length - width + 1):
            right = left + width - 1
            if text[left] != text[right]:
                counts[left][right] = (
                    counts[left + 1][right]
                    + counts[left][right - 1]
                    - counts[left + 1][right - 1]
                ) % modulus
                continue

            inner = counts[left + 1][right - 1] if width > 2 else 0
            low = next_equal[left]
            high = previous_equal[right]
            if low > high:
                value = 2 * inner + 2
            elif low == high:
                value = 2 * inner + 1
            else:
                duplicate = counts[low + 1][high - 1] if low + 1 <= high - 1 else 0
                value = 2 * inner - duplicate
            counts[left][right] = value % modulus

    return counts[0][length - 1]
```

Nearest-equal lookup makes every interval transition constant time. The three
equal-end cases add exactly the new boundary palindromes and remove exactly the
family counted twice.

**Complexity:** `O(n^2)` time and `O(n^2)` space.
