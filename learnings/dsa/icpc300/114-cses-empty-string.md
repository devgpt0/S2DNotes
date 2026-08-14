# ICPC300 114: CSES - Empty String

**Source:** [CSES - Empty String](https://cses.fi/problemset/task/1080/)  
**Pattern:** interval DP with interleaving counts  
**Goal:** Count ways to delete the whole string by repeatedly removing two
equal adjacent characters, modulo `1_000_000_007`.

Different choices of adjacent positions are different deletion sequences.

## 1. First principles

In an interval, pair its first character with the character removed alongside
it. Everything between that pair must disappear first. Deletions in this
left block and the suffix can interleave, producing a binomial coefficient.

For partner `p` in half-open interval `[left,right)`:

```text
inside ways * suffix ways
* choose(total_pairs, pairs_in_left_block)
```

## 2. Cases that decide correctness

- Odd-length intervals have zero ways.
- The empty interval has one completed deletion sequence.
- Pair endpoints must contain equal characters.
- The partner offset from `left` must be odd.
- Independent block deletions can interleave in binomially many orders.

## 3. Brute force: try every adjacent equal pair

```python
def empty_string_brute(text: str, modulo: int = 1_000_000_007) -> int:
    if modulo <= 0:
        raise ValueError("modulo must be positive")
    if len(text) % 2 == 1:
        return 0
    if not text:
        return 1

    total = 0
    for index in range(len(text) - 1):
        if text[index] == text[index + 1]:
            total += empty_string_brute(text[:index] + text[index + 2 :], modulo)
    return total % modulo
```

**Complexity:** exponential time and `O(n)` recursion depth.

## 4. Better: memoize remaining strings

```python
from functools import cache


def empty_string_memoized(text: str, modulo: int = 1_000_000_007) -> int:
    if modulo <= 0:
        raise ValueError("modulo must be positive")

    @cache
    def count(remaining: str) -> int:
        if not remaining:
            return 1
        if len(remaining) % 2 == 1:
            return 0
        total = 0
        for index in range(len(remaining) - 1):
            if remaining[index] == remaining[index + 1]:
                total += count(remaining[:index] + remaining[index + 2 :])
        return total % modulo

    return count(text)
```

**Complexity:** exponential worst-case states, but each distinct remaining
string is solved once.

## 5. Expert solution: interval DP

```python
def empty_string_interval_dp(text: str, modulo: int = 1_000_000_007) -> int:
    if modulo <= 0:
        raise ValueError("modulo must be positive")
    if len(text) % 2 == 1:
        return 0

    pair_count = len(text) // 2
    choose = [[0] * (pair_count + 1) for _ in range(pair_count + 1)]
    for total in range(pair_count + 1):
        choose[total][0] = choose[total][total] = 1
        for selected in range(1, total):
            choose[total][selected] = (
                choose[total - 1][selected - 1] + choose[total - 1][selected]
            ) % modulo

    length = len(text)
    dynamic = [[0] * (length + 1) for _ in range(length + 1)]
    for index in range(length + 1):
        dynamic[index][index] = 1

    for interval_length in range(2, length + 1, 2):
        total_pairs = interval_length // 2
        for left in range(length - interval_length + 1):
            right = left + interval_length
            total = 0
            for partner in range(left + 1, right, 2):
                if text[left] != text[partner]:
                    continue
                left_block_pairs = (partner - left + 1) // 2
                total += (
                    dynamic[left + 1][partner]
                    * dynamic[partner + 1][right]
                    * choose[total_pairs][left_block_pairs]
                )
            dynamic[left][right] = total % modulo
    return dynamic[0][length]
```

### Why the expert code is correct

Every complete deletion has one unique character paired with the interval's
first character. Its inside and suffix deletions are independent, and the
binomial factor counts every valid interleaving exactly once.

**Complexity:** `O(n^3)` time and `O(n^2)` space.

## 6. What to remember

```text
pair the first character
inside must vanish before that pair closes
interleave left-block and suffix operations with a binomial coefficient
```
