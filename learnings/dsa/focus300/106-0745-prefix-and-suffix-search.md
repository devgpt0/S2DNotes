# Focus300 106: LeetCode 745 - Prefix and Suffix Search

**Source:** [LeetCode 745](https://leetcode.com/problems/prefix-and-suffix-search/)  
**Difficulty:** Hard  
**Pattern:** precomputed composite lookup keys

## Exact contract

Construct `WordFilter(words)`. For each `f(prefix, suffix)` query, return the
largest index of a word that starts with `prefix` and ends with `suffix`, or
`-1` when no word matches. Words and queries use lowercase English letters;
words may repeat.

## First principles

The answer depends only on a prefix/suffix pair. Since source words are short,
enumerate every pair for every word once. Processing indices from smallest to
largest lets a dictionary assignment retain the required largest index.

## Cases that decide correctness

- Return the largest matching index, not the first match.
- Duplicate words retain the later index.
- Prefix and suffix may overlap inside a short word.
- A query whose prefix or suffix is longer than a word cannot match it.
- No match returns `-1`.

## Brute force: scan words backward per query

```python
class WordFilterBrute:
    def __init__(self, words: list[str]) -> None:
        if not words or any(
            not word.isascii() or not word.isalpha() or not word.islower()
            for word in words
        ):
            raise ValueError("words must be non-empty lowercase strings")
        self._words = tuple(words)

    def f(self, prefix: str, suffix: str) -> int:
        if not (
            prefix.isascii()
            and prefix.isalpha()
            and prefix.islower()
            and suffix.isascii()
            and suffix.isalpha()
            and suffix.islower()
        ):
            raise ValueError("prefix and suffix must be lowercase strings")
        for index in range(len(self._words) - 1, -1, -1):
            word = self._words[index]
            if word.startswith(prefix) and word.endswith(suffix):
                return index
        return -1
```

Each query costs `O(w * l)`, where `w` is the number of words and `l` is their
maximum length.

## Better solution: intersect prefix and suffix index lists

```python
class WordFilterInverted:
    def __init__(self, words: list[str]) -> None:
        if not words or any(
            not word.isascii() or not word.isalpha() or not word.islower()
            for word in words
        ):
            raise ValueError("words must be non-empty lowercase strings")
        self._prefixes: dict[str, list[int]] = {}
        self._suffixes: dict[str, list[int]] = {}
        for index, word in enumerate(words):
            for length in range(1, len(word) + 1):
                self._prefixes.setdefault(word[:length], []).append(index)
                self._suffixes.setdefault(word[-length:], []).append(index)

    def f(self, prefix: str, suffix: str) -> int:
        if not (
            prefix.isascii()
            and prefix.isalpha()
            and prefix.islower()
            and suffix.isascii()
            and suffix.isalpha()
            and suffix.islower()
        ):
            raise ValueError("prefix and suffix must be lowercase strings")
        left = self._prefixes.get(prefix, [])
        right = self._suffixes.get(suffix, [])
        first = len(left) - 1
        second = len(right) - 1
        while first >= 0 and second >= 0:
            if left[first] == right[second]:
                return left[first]
            if left[first] > right[second]:
                first -= 1
            else:
                second -= 1
        return -1
```

This uses `O(wl)` preprocessing space. A query can still inspect `O(w)` indices.

## Expert solution: precompute every prefix/suffix pair

```python
class WordFilter:
    def __init__(self, words: list[str]) -> None:
        if not words or any(
            not word.isascii() or not word.isalpha() or not word.islower()
            for word in words
        ):
            raise ValueError("words must be non-empty lowercase strings")
        self._largest_index: dict[tuple[str, str], int] = {}
        for index, word in enumerate(words):
            for prefix_length in range(1, len(word) + 1):
                prefix = word[:prefix_length]
                for suffix_length in range(1, len(word) + 1):
                    self._largest_index[(prefix, word[-suffix_length:])] = index

    def f(self, prefix: str, suffix: str) -> int:
        if not (
            prefix.isascii()
            and prefix.isalpha()
            and prefix.islower()
            and suffix.isascii()
            and suffix.isalpha()
            and suffix.islower()
        ):
            raise ValueError("prefix and suffix must be lowercase strings")
        return self._largest_index.get((prefix, suffix), -1)
```

Every valid query key has already been assigned the largest matching index.
The source's small maximum word length makes the quadratic per-word build the
right tradeoff for many online queries.

**Complexity:** `O(wl^2)` preprocessing time and space, then `O(p + s)` time
to hash a query containing `p + s` characters.
