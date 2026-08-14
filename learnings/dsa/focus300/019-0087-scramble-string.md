# Focus300 019: LeetCode 87 - Scramble String

**Source:** [LeetCode 87](https://leetcode.com/problems/scramble-string/)  
**Difficulty:** Hard  
**Pattern:** memoized interval-pair recursion

## Exact contract

Given two nonempty lowercase strings of equal length at most 30, return whether
the second can be produced from the first by recursively splitting a string
into two nonempty parts and optionally swapping the two children at any split.

## First principles

At the root of any valid scramble tree, some split either preserves child
order or swaps it. Therefore a pair of equal-length substrings is valid if one
split produces two valid aligned pairs or two valid crossed pairs. Unequal
character multisets can be rejected immediately.

## Cases that decide correctness

- Equal strings are valid without making a split.
- Different character counts make a state impossible.
- Both preserved and swapped child order must be tested.
- Split positions range from one through `length - 1`.
- Repeated letters make memoization essential.

## Brute force: recurse over every split tree

```python
from collections import Counter


def is_scramble_brute(first: str, second: str) -> bool:
    if (
        not first
        or len(first) != len(second)
        or any(not "a" <= character <= "z" for character in first + second)
    ):
        raise ValueError("strings must be equal-length lowercase text")

    def search(left: str, right: str) -> bool:
        if left == right:
            return True
        if Counter(left) != Counter(right):
            return False
        for split in range(1, len(left)):
            if search(left[:split], right[:split]) and search(
                left[split:], right[split:]
            ):
                return True
            if search(left[:split], right[-split:]) and search(
                left[split:], right[:-split]
            ):
                return True
        return False

    return search(first, second)
```

This directly follows the definition but revisits the same substring pairs
exponentially many times.

## Better approach: memoize substring pairs

```python
from collections import Counter
from functools import cache


def is_scramble_memoized(first: str, second: str) -> bool:
    if (
        not first
        or len(first) != len(second)
        or any(not "a" <= character <= "z" for character in first + second)
    ):
        raise ValueError("strings must be equal-length lowercase text")

    @cache
    def search(left: str, right: str) -> bool:
        if left == right:
            return True
        if Counter(left) != Counter(right):
            return False
        return any(
            (
                search(left[:split], right[:split])
                and search(left[split:], right[split:])
            )
            or (
                search(left[:split], right[-split:])
                and search(left[split:], right[:-split])
            )
            for split in range(1, len(left))
        )

    return search(first, second)
```

Memoization makes each distinct substring-pair state execute once.

## Expert solution: index states with prefix character counts

```python
from functools import cache


def is_scramble(first: str, second: str) -> bool:
    if (
        not first
        or len(first) != len(second)
        or any(not "a" <= character <= "z" for character in first + second)
    ):
        raise ValueError("strings must be equal-length lowercase text")

    def prefixes(text: str) -> list[list[int]]:
        counts = [[0] * 26]
        for character in text:
            current = counts[-1].copy()
            current[ord(character) - ord("a")] += 1
            counts.append(current)
        return counts

    first_counts = prefixes(first)
    second_counts = prefixes(second)

    def same_counts(first_start: int, second_start: int, length: int) -> bool:
        return all(
            first_counts[first_start + length][character]
            - first_counts[first_start][character]
            == second_counts[second_start + length][character]
            - second_counts[second_start][character]
            for character in range(26)
        )

    @cache
    def search(first_start: int, second_start: int, length: int) -> bool:
        if length == 1:
            return first[first_start] == second[second_start]
        if not same_counts(first_start, second_start, length):
            return False
        for split in range(1, length):
            if search(first_start, second_start, split) and search(
                first_start + split, second_start + split, length - split
            ):
                return True
            if search(first_start, second_start + length - split, split) and search(
                first_start + split, second_start, length - split
            ):
                return True
        return False

    return search(0, 0, len(first))
```

Every recursive scramble has one root split in one of the two tested orders,
and every accepted combination constructs such a tree. Index states avoid
substring copies, while prefix counts reject incompatible states in constant
alphabet time.

**Complexity:** `O(n^4)` time and `O(n^3)` cached states.
