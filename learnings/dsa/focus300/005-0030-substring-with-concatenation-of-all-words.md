# Focus300 005: LeetCode 30 - Substring with Concatenation of All Words

**Source:** [LeetCode 30](https://leetcode.com/problems/substring-with-concatenation-of-all-words/)  
**Difficulty:** Hard  
**Pattern:** fixed-token sliding windows by alignment

## Exact contract

Given a string and a nonempty list of equal-length words, return every start
index where a substring is the concatenation of all words in any order. Every
word occurrence, including duplicates, must be used exactly once.

## First principles

A valid window begins at one of `word_length` offsets. Within one offset, every
boundary advances by exactly one word. Maintain token counts and shrink the
left edge whenever the newest token exceeds its required multiplicity.

An unknown token invalidates the whole aligned window. When the window contains
exactly the required number of tokens, record its left edge and slide one token
to preserve overlapping answers.

## Cases that decide correctness

- Duplicate words require counts, not a set.
- All words have the same positive length by contract.
- Answers may overlap.
- A token absent from the target resets one alignment only.
- The result is empty when the total concatenation is longer than the string.

## Brute force: validate every possible start

```python
from collections import Counter


def find_substring_brute(source: str, words: list[str]) -> list[int]:
    if not words:
        return []
    word_length = len(words[0])
    window_length = word_length * len(words)
    required = Counter(words)
    answers: list[int] = []
    for start in range(len(source) - window_length + 1):
        found = Counter(
            source[index : index + word_length]
            for index in range(start, start + window_length, word_length)
        )
        if found == required:
            answers.append(start)
    return answers
```

This takes `O(nk)` token work for `k` words, plus substring allocation costs.

## Better insight: token boundaries have only `word_length` alignments

Within one alignment, each token enters and leaves the frequency window once.
That turns repeated full-window recounting into a linear scan.

## Expert solution: aligned sliding windows

```python
from collections import Counter


def find_substring(source: str, words: list[str]) -> list[int]:
    if not words:
        return []
    word_length = len(words[0])
    if word_length == 0 or any(len(word) != word_length for word in words):
        raise ValueError("words must have one shared positive length")
    required = Counter(words)
    word_count = len(words)
    answers: list[int] = []

    for offset in range(word_length):
        left = offset
        used = 0
        window: Counter[str] = Counter()
        for right in range(offset, len(source) - word_length + 1, word_length):
            token = source[right : right + word_length]
            if token not in required:
                window.clear()
                used = 0
                left = right + word_length
                continue

            window[token] += 1
            used += 1
            while window[token] > required[token]:
                removed = source[left : left + word_length]
                window[removed] -= 1
                used -= 1
                left += word_length
            if used == word_count:
                answers.append(left)
                removed = source[left : left + word_length]
                window[removed] -= 1
                used -= 1
                left += word_length
    answers.sort()
    return answers
```

Every aligned candidate enters and leaves once, and the count invariant exactly
matches the required word multiset.

**Complexity:** `O(n)` token operations and `O(k)` frequency space, excluding
fixed-length slice creation.
