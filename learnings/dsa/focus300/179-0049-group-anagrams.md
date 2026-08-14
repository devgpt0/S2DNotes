# Focus300 179: LeetCode 49 - Group Anagrams

**Source:** [LeetCode 49](https://leetcode.com/problems/group-anagrams/)  
**Difficulty:** Medium  
**Pattern:** canonical multiset signatures

## Exact contract

Group a non-empty list of lowercase English strings so that two strings share a
group exactly when one is an anagram of the other. Empty strings are valid.
Group order and order within a group do not matter.

## First principles

Anagrams have the same character multiset. A sorted string is a simple canonical
key; for lowercase English input, a 26-count tuple is a linear-time key that
avoids sorting each word.

## Cases that decide correctness

- Repeated identical strings remain repeated elements in one group.
- Every empty string has the same all-zero signature.
- Strings of different lengths cannot share a count signature.
- Result order is irrelevant, but no input occurrence may be lost.
- Character counts, not character positions, determine membership.

## Brute force: compare against one representative per group

```python
def group_anagrams_brute(words: list[str]) -> list[list[str]]:
    if not words or any(
        character not in "abcdefghijklmnopqrstuvwxyz"
        for word in words
        for character in word
    ):
        raise ValueError("words must contain lowercase English strings")

    groups: list[list[str]] = []
    for word in words:
        for group in groups:
            if sorted(word) == sorted(group[0]):
                group.append(word)
                break
        else:
            groups.append([word])
    return groups
```

Repeated representative comparisons take `O(w^2 * l log l)` time.

## Better solution: hash the sorted spelling

```python
def group_anagrams_sorted(words: list[str]) -> list[list[str]]:
    if not words or any(
        character not in "abcdefghijklmnopqrstuvwxyz"
        for word in words
        for character in word
    ):
        raise ValueError("words must contain lowercase English strings")

    groups: dict[str, list[str]] = {}
    for word in words:
        key = "".join(sorted(word))
        groups.setdefault(key, []).append(word)
    return list(groups.values())
```

This reduces grouping to `O(w * l log l)` time with `O(wl)` output and keys.

## Expert solution: fixed-size frequency signatures

```python
def group_anagrams(words: list[str]) -> list[list[str]]:
    if not words or any(
        character not in "abcdefghijklmnopqrstuvwxyz"
        for word in words
        for character in word
    ):
        raise ValueError("words must contain lowercase English strings")

    groups: dict[tuple[int, ...], list[str]] = {}
    for word in words:
        counts = [0] * 26
        for character in word:
            counts[ord(character) - ord("a")] += 1
        groups.setdefault(tuple(counts), []).append(word)
    return list(groups.values())
```

The tuple is equal exactly for equal lowercase character multisets and is
hashable, so each word is scanned once.

**Complexity:** `O(total input characters)` time and `O(w)` signatures beyond
the returned strings.
