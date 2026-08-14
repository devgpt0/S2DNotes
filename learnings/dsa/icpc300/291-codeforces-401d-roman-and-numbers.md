# ICPC300 291: Codeforces 401D - Roman and Numbers

**Source:** [Codeforces 401D - Roman and Numbers](https://codeforces.com/problemset/problem/401/D)  
**Rating:** 2200  
**Pattern:** duplicate-aware digit-mask DP  
**Goal:** Count distinct permutations of the supplied decimal digits whose
value is divisible by `divisor`. As in the source, zero may be the first digit.

## 1. First principles

Appending digit `d` changes a remainder `r` to `(10*r + d) % divisor`. A mask
records which digit occurrences have been used.

Equal digits must not create factorially many copies of the same string. Sort
the digits and allow occurrence `i` only after occurrence `i-1` of the same
digit has been used. Every distinct permutation then has one canonical path.

## 2. Cases that decide correctness

- Repeated zeros are indistinguishable.
- Leading zeroes still participate in the fixed-length permutation.
- `divisor = 1` accepts every distinct permutation.
- The input digit string must be nonempty.
- Sparse remainder maps avoid allocating every mask-remainder pair.

## 3. Brute force: enumerate distinct permutations

```python
from itertools import permutations


def divisible_permutations_brute(digits: str, divisor: int) -> int:
    if not digits or any(character not in "0123456789" for character in digits):
        raise ValueError("digits must be a nonempty decimal string")
    if type(divisor) is not int or divisor <= 0:
        raise ValueError("divisor must be positive")

    answer = 0
    for order in set(permutations(digits)):
        remainder = 0
        for character in order:
            remainder = (10 * remainder + int(character)) % divisor
        answer += remainder == 0
    return answer
```

**Complexity:** `O(n! * n)` time and up to `O(n! * n)` stored characters.

## 4. Better approach: count labeled occurrences, then divide

A standard mask DP may label equal occurrences and divide its final count by
the factorial of each digit frequency. Canonical duplicate skipping avoids
that postprocessing and visits fewer masks.

## 5. Expert solution: canonical duplicate-mask transitions

```python
def divisible_permutations(digits: str, divisor: int) -> int:
    if not digits or any(character not in "0123456789" for character in digits):
        raise ValueError("digits must be a nonempty decimal string")
    if type(divisor) is not int or divisor <= 0:
        raise ValueError("divisor must be positive")

    ordered = sorted(map(int, digits))
    full_mask = (1 << len(ordered)) - 1
    dp: dict[int, dict[int, int]] = {0: {0: 1}}
    for mask in range(full_mask + 1):
        remainders = dp.get(mask)
        if remainders is None:
            continue
        for index, digit in enumerate(ordered):
            if mask >> index & 1:
                continue
            if (
                index > 0
                and digit == ordered[index - 1]
                and not mask >> (index - 1) & 1
            ):
                continue
            next_mask = mask | 1 << index
            next_remainders = dp.setdefault(next_mask, {})
            for remainder, count in remainders.items():
                next_remainder = (10 * remainder + digit) % divisor
                next_remainders[next_remainder] = (
                    next_remainders.get(next_remainder, 0) + count
                )
    return dp[full_mask].get(0, 0)
```

### Why the expert code is correct

The remainder transition exactly models decimal concatenation. Sorting and the
previous-equal-used rule select one ordering of indistinguishable occurrences,
so every distinct digit string reaches the full mask once and only once.

**Complexity:** `O(R n)` time and `O(R)` space for the number `R` of reachable
mask-remainder states.

## 6. What to remember

```text
digit append -> remainder transition
used occurrences -> bitmask
equal digits -> use identical occurrences from left to right
```
