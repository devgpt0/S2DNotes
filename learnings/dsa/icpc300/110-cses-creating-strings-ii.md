# ICPC300 110: CSES - Creating Strings II

**Source:** [CSES - Creating Strings II](https://cses.fi/problemset/task/1715/)  
**Pattern:** multinomial coefficient modulo a prime  
**Goal:** Count, modulo `1_000_000_007`, distinct strings obtainable by
permuting all characters of the given lowercase string.

## 1. Problem in plain words

If all `n` character occurrences were different, there would be `n!`
permutations. Occurrences of the same character are indistinguishable. For each
character appearing `f` times, the `f!` internal reorderings create no new
string, so divide by every frequency factorial.

For `aab`, the answer is `3! / 2! = 3`.

## 2. First principles

The number of distinct multiset permutations is:

`n! / product(frequency[c]!)`.

Modulo a prime, division by nonzero `x` means multiplication by
`x^(MODULO-2)`. Precompute factorials and inverse factorials through `n`, then
multiply the relevant inverse factorial for each character count.

## 3. Cases that decide correctness

| Case | Required result |
| --- | --- |
| One character | `1`. |
| All characters equal | `1`. |
| All characters distinct | `n!`. |
| Several repeated groups | Divide by every frequency factorial. |
| Lowercase source alphabet | Reject characters outside `a..z`. |

## 4. Brute force: generate every permutation string

```python
from itertools import permutations


def count_distinct_permutations_brute_force(text: str) -> int:
    if not text or any(not "a" <= character <= "z" for character in text):
        raise ValueError("text must be nonempty lowercase English letters")
    return len({"".join(order) for order in permutations(text)})
```

**Complexity:** `O(n! n)` time and potentially `O(n! n)` memory.

## 5. Better: insert equal-character groups with binomial choices

After arranging `used` characters, place the next group of `count` identical
characters by choosing its positions among `used + count`. Multiplying these
binomial choices telescopes to the multinomial coefficient.

```python
from collections import Counter
from math import comb

MODULO = 1_000_000_007


def count_distinct_permutations_by_groups(text: str) -> int:
    if not text or any(not "a" <= character <= "z" for character in text):
        raise ValueError("text must be nonempty lowercase English letters")

    answer = 1
    used = 0
    for count in Counter(text).values():
        answer = answer * comb(used + count, count) % MODULO
        used += count
    return answer
```

**Complexity:** polynomial big-integer binomial work and `O(alphabet_size)`
memory; it is useful for moderate strings but not the largest source input.

## 6. Expert solution: factorials and inverse factorials

```python
from collections import Counter

MODULO = 1_000_000_007


def count_distinct_permutations(text: str) -> int:
    if not text or any(not "a" <= character <= "z" for character in text):
        raise ValueError("text must be nonempty lowercase English letters")

    factorial = [1] * (len(text) + 1)
    for value in range(1, len(text) + 1):
        factorial[value] = factorial[value - 1] * value % MODULO

    inverse_factorial = [1] * (len(text) + 1)
    inverse_factorial[-1] = pow(factorial[-1], MODULO - 2, MODULO)
    for value in range(len(text), 0, -1):
        inverse_factorial[value - 1] = inverse_factorial[value] * value % MODULO

    answer = factorial[len(text)]
    for count in Counter(text).values():
        answer = answer * inverse_factorial[count] % MODULO
    return answer
```

### Why the expert code is correct

- Labeling all character occurrences gives `n!` positional orders.
- Permuting the `f` equal copies of one character leaves the visible string
  unchanged, so every visible result is counted exactly `product(f!)` times.
- Frequencies are below the prime modulus under source bounds, making each
  factorial invertible.
- Modular inverse factorial multiplication implements the exact multinomial
  division.

**Complexity:** `O(n + alphabet_size)` time and `O(n)` memory.

## 7. What to remember

Distinct permutations of a multiset are a multinomial coefficient:
`n! * product(inverse_factorial[frequency])` modulo the prime.
