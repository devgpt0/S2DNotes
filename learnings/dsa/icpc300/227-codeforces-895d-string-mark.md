# ICPC300 227: Codeforces 895D - String Mark

**Source:** [Codeforces 895D - String Mark](https://codeforces.com/problemset/problem/895/D)  
**Rating:** 2300  
**Pattern:** multiset permutation ranks with a Fenwick tree  
**Goal:** Count distinct permutations of the first lowercase string that are
strictly lexicographically between the first and second strings, modulo
`1_000_000_007`.

## 1. First principles

Count multiset permutations smaller than a boundary. At a position with
`remaining` characters and `total` possible arrangements, fixing one available
character `c` first leaves

```text
total * count[c] / remaining
```

arrangements. Summing `count[c]` over characters smaller than the boundary
character gives the entire contribution at once. A Fenwick tree maintains that
smaller-character count during removals.

The answer is `rank(second) - rank(first) - 1`; the subtraction removes the
first string itself.

## 2. Cases that decide correctness

- Equal letters are indistinguishable, so multinomial counts are required.
- The second boundary need not have the first string's character multiset.
- If a boundary character is unavailable, rank scanning stops at that position.
- Both boundaries are strict.
- Source length is below the modulus, so every `remaining` value is invertible.

## 3. Brute force: generate every distinct permutation

```python
from itertools import permutations


MODULO = 1_000_000_007


def string_mark_count_brute(first: str, second: str) -> int:
    if (
        not first
        or len(first) != len(second)
        or first >= second
        or any(not "a" <= character <= "z" for character in first + second)
    ):
        raise ValueError("boundaries must be ordered lowercase strings")
    candidates = {"".join(order) for order in permutations(first)}
    return sum(first < candidate < second for candidate in candidates) % MODULO
```

**Complexity:** `O(n! * n)` time and space.

## 4. Better transition: rank a boundary without listing permutations

At each boundary position, all smaller available next letters form contiguous
lexicographic blocks. Their combined size depends only on the total count of
those letters, while the chosen equal letter updates the multinomial total for
the next position.

## 5. Expert solution: multinomial rank with dynamic counts

```python
MODULO = 1_000_000_007


def string_mark_count(first: str, second: str) -> int:
    if (
        not first
        or len(first) != len(second)
        or first >= second
        or any(not "a" <= character <= "z" for character in first + second)
    ):
        raise ValueError("boundaries must be ordered lowercase strings")

    size = len(first)
    factorial = [1] * (size + 1)
    for value in range(1, size + 1):
        factorial[value] = factorial[value - 1] * value % MODULO
    inverse_factorial = [1] * (size + 1)
    inverse_factorial[size] = pow(factorial[size], MODULO - 2, MODULO)
    for value in range(size, 0, -1):
        inverse_factorial[value - 1] = inverse_factorial[value] * value % MODULO
    inverses = [0] * (size + 1)
    inverses[1] = 1
    for value in range(2, size + 1):
        inverses[value] = MODULO - (MODULO // value) * inverses[MODULO % value] % MODULO

    initial_counts = [0] * 26
    for character in first:
        initial_counts[ord(character) - ord("a")] += 1

    def rank(boundary: str) -> int:
        counts = initial_counts.copy()
        fenwick = [0] * 27

        def add(index: int, amount: int) -> None:
            index += 1
            while index < len(fenwick):
                fenwick[index] += amount
                index += index & -index

        def prefix_sum(index: int) -> int:
            total = 0
            while index:
                total += fenwick[index]
                index -= index & -index
            return total

        total_arrangements = factorial[size]
        for count in counts:
            total_arrangements = total_arrangements * inverse_factorial[count] % MODULO
        for index, count in enumerate(counts):
            add(index, count)

        answer = 0
        remaining = size
        for character in boundary:
            character_index = ord(character) - ord("a")
            smaller_count = prefix_sum(character_index)
            answer += (
                total_arrangements * smaller_count * inverses[remaining]
            ) % MODULO
            answer %= MODULO
            if counts[character_index] == 0:
                break
            total_arrangements = (
                total_arrangements * counts[character_index] * inverses[remaining]
            ) % MODULO
            counts[character_index] -= 1
            add(character_index, -1)
            remaining -= 1
        return answer

    return (rank(second) - rank(first) - 1) % MODULO
```

### Why the expert code is correct

For each prefix equal to the boundary so far, choosing any smaller available
letter creates exactly the counted multinomial block, and those blocks are
disjoint. Continuing with the equal letter updates the remaining-arrangement
count by its exact frequency ratio. Thus `rank` counts precisely the valid
permutations below a boundary, and the rank difference leaves only strict
interior strings.

**Complexity:** `O(n log 26)` time and `O(n+26)` space.

## 6. What to remember

```text
lexicographic interval -> difference of ranks
duplicate letters -> multinomial arrangements
smaller available letters -> Fenwick prefix count
```
