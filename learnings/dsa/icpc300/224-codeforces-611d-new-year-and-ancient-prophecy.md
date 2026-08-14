# ICPC300 224: Codeforces 611D - New Year and Ancient Prophecy

**Source:** [Codeforces 611D - New Year and Ancient Prophecy](https://codeforces.com/problemset/problem/611/D)  
**Rating:** 2200  
**Pattern:** substring-length DP with an LCP comparison table  
**Goal:** Count ways to split a decimal string into strictly increasing
positive integers without leading zeros, modulo `1_000_000_007`.

## 1. First principles

Let `dp[end][length]` count splits of `text[:end]` whose last number has the
given length. For the current number starting at `start = end - length`:

- every shorter previous number is automatically smaller;
- an equal-length previous number is allowed exactly when its substring is
  lexicographically smaller;
- longer previous numbers are never smaller.

Prefix sums over previous lengths handle the first case. An all-pairs LCP table
compares equal-length adjacent substrings in constant time.

## 2. Cases that decide correctness

- A number may be `0` nowhere: every part is positive and cannot start with zero.
- The first valid part needs no previous comparison.
- Equal numeric values are forbidden because the sequence is strictly increasing.
- Length alone decides unequal-length positive decimal numbers.
- The entire input string must be consumed.

## 3. Brute force: try every next cut

```python
MODULO = 1_000_000_007


def increasing_splits_brute(text: str) -> int:
    if not text or any(not "0" <= character <= "9" for character in text):
        raise ValueError("text must contain decimal digits")

    def count(start: int, previous: int) -> int:
        if start == len(text):
            return 1
        if text[start] == "0":
            return 0
        answer = 0
        value = 0
        for end in range(start, len(text)):
            value = value * 10 + int(text[end])
            if value > previous:
                answer += count(end + 1, value)
        return answer

    return count(0, 0) % MODULO
```

**Complexity:** Exponential time and `O(n)` recursion space.

## 4. Better transition: compare by length, then by LCP

The DP never needs to construct large integers. Shorter decimal substrings are
smaller, and equal-length substrings differ at the first character after their
common prefix. Precomputing that prefix length removes repeated comparisons.

## 5. Expert solution: quadratic length DP

```python
MODULO = 1_000_000_007


def increasing_splits(text: str) -> int:
    if not text or any(not "0" <= character <= "9" for character in text):
        raise ValueError("text must contain decimal digits")

    size = len(text)
    lcp = [[0] * (size + 1) for _ in range(size + 1)]
    for first in range(size - 1, -1, -1):
        for second in range(size - 1, first, -1):
            if text[first] == text[second]:
                lcp[first][second] = lcp[first + 1][second + 1] + 1

    dp = [[0] * (size + 1) for _ in range(size + 1)]
    prefix = [[0] * (size + 1) for _ in range(size + 1)]
    for end in range(1, size + 1):
        for length in range(1, end + 1):
            start = end - length
            ways = 0
            if text[start] != "0":
                if start == 0:
                    ways = 1
                else:
                    ways = prefix[start][min(length - 1, start)]
                    if start >= length:
                        previous_start = start - length
                        common = min(lcp[previous_start][start], length)
                        if (
                            common < length
                            and text[previous_start + common] < text[start + common]
                        ):
                            ways += dp[start][length]
            dp[end][length] = ways % MODULO
            prefix[end][length] = (prefix[end][length - 1] + dp[end][length]) % MODULO
    return prefix[size][size]
```

### Why the expert code is correct

Every split is uniquely determined by its final part and a valid split of the
preceding prefix. The transition includes exactly the shorter previous parts
and the equal-length part when LCP comparison proves it smaller. Leading-zero
parts are excluded. Induction over `end` therefore counts every valid complete
split once.

**Complexity:** `O(n^2)` time and `O(n^2)` space.

## 6. What to remember

```text
large decimal values -> compare substrings, not integers
shorter length -> smaller positive number
equal length -> LCP plus first differing digit
```
