# ICPC300 210: Codeforces 427D - Match & Catch

**Source:** [Codeforces 427D - Match & Catch](https://codeforces.com/problemset/problem/427/D)  
**Difficulty:** 2200  
**Pattern:** suffix-array adjacency with per-suffix uniqueness thresholds

## Exact contract

Given two nonempty lowercase strings, return the minimum length of a substring
that occurs exactly once in each string, counting overlapping occurrences.
Return `-1` when no such substring exists.

## First principles

For a suffix, let `repeat` be its longest common prefix with any other suffix
from the same string. A prefix of this suffix is unique exactly when its length
is greater than `repeat`.

If one substring is unique in each input, the two suffixes starting at its
occurrences are adjacent in the combined suffix array: no third suffix can lie
between two suffixes sharing that prefix. For each adjacent cross-string pair,
the smallest valid length is

`max(repeat_first, repeat_second) + 1`,

provided it does not exceed their common-prefix length.

## Cases that decide correctness

- Overlapping repeated occurrences make a substring non-unique.
- A whole string may be the shortest answer.
- Equal input strings can still have a unique long substring.
- The separator must not occur in either lowercase input.
- Suffix-array neighbors within one string determine its maximum repeated
  prefix.

## Brute force: test every substring length

```python
def match_and_catch_brute(first: str, second: str) -> int:
    if (
        not first
        or not second
        or any(character < "a" or character > "z" for character in first + second)
    ):
        raise ValueError("inputs must be nonempty lowercase strings")

    def occurrences(text: str, pattern: str) -> int:
        return sum(
            text.startswith(pattern, start)
            for start in range(len(text) - len(pattern) + 1)
        )

    for length in range(1, min(len(first), len(second)) + 1):
        for start in range(len(first) - length + 1):
            candidate = first[start : start + length]
            if occurrences(first, candidate) == occurrences(second, candidate) == 1:
                return length
    return -1
```

Repeated substring scans make the worst-case time cubic or worse.

## Better approach: no separate intermediate

Hashing can group equal substrings for one fixed length, but valid existence is
not monotone in length, so binary search is invalid. Suffix order exposes both
commonality and uniqueness thresholds in one global structure.

## Expert solution: combined suffix-array neighbors

```python
def match_and_catch(first: str, second: str) -> int:
    if (
        not first
        or not second
        or any(character < "a" or character > "z" for character in first + second)
    ):
        raise ValueError("inputs must be nonempty lowercase strings")

    def suffix_array(text: str) -> list[int]:
        size = len(text)
        order = list(range(size))
        rank = [ord(character) for character in text]
        length = 1
        while length < size:
            order.sort(
                key=lambda start: (
                    rank[start],
                    rank[start + length] if start + length < size else -1,
                )
            )
            following = [0] * size
            for index in range(1, size):
                previous = order[index - 1]
                current = order[index]
                previous_key = (
                    rank[previous],
                    rank[previous + length] if previous + length < size else -1,
                )
                current_key = (
                    rank[current],
                    rank[current + length] if current + length < size else -1,
                )
                following[current] = following[previous] + (current_key != previous_key)
            rank = following
            if rank[order[-1]] == size - 1:
                break
            length *= 2
        return order

    def adjacent_lcp(text: str, order: list[int]) -> list[int]:
        size = len(text)
        inverse = [0] * size
        for rank, start in enumerate(order):
            inverse[start] = rank
        lcp = [0] * max(0, size - 1)
        matched = 0
        for start in range(size):
            rank = inverse[start]
            if rank == size - 1:
                matched = 0
                continue
            other = order[rank + 1]
            while (
                start + matched < size
                and other + matched < size
                and text[start + matched] == text[other + matched]
            ):
                matched += 1
            lcp[rank] = matched
            if matched:
                matched -= 1
        return lcp

    def repeat_prefix_lengths(text: str) -> list[int]:
        order = suffix_array(text)
        lcp = adjacent_lcp(text, order)
        repeat = [0] * len(text)
        for rank, start in enumerate(order):
            if rank:
                repeat[start] = max(repeat[start], lcp[rank - 1])
            if rank < len(order) - 1:
                repeat[start] = max(repeat[start], lcp[rank])
        return repeat

    first_repeat = repeat_prefix_lengths(first)
    second_repeat = repeat_prefix_lengths(second)
    combined = first + "{" + second
    order = suffix_array(combined)
    lcp = adjacent_lcp(combined, order)
    separator = len(first)
    answer = len(combined) + 1

    for rank, common in enumerate(lcp):
        first_start = order[rank]
        second_start = order[rank + 1]
        if first_start == separator or second_start == separator:
            continue
        first_source = first_start < separator
        second_source = second_start < separator
        if first_source == second_source:
            continue
        if not first_source:
            first_start, second_start = second_start, first_start
        second_local = second_start - separator - 1
        needed = max(first_repeat[first_start], second_repeat[second_local]) + 1
        if needed <= common:
            answer = min(answer, needed)
    return -1 if answer > len(combined) else answer
```

Same-string adjacent LCP values give the exact uniqueness threshold for each
suffix. A unique common substring creates an adjacent cross-string suffix pair,
so checking every such pair cannot miss the optimum.

**Complexity:** `O(N log^2 N)` time with comparison-sorted doubling and `O(N)`
space, where `N` is the combined length.
