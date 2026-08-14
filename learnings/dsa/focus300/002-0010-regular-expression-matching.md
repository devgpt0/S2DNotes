# Focus300 002: LeetCode 10 - Regular Expression Matching

**Source:** [LeetCode 10](https://leetcode.com/problems/regular-expression-matching/)  
**Difficulty:** Hard  
**Pattern:** full-string dynamic programming with zero-or-more transitions

## Exact contract

Return whether the entire string `s` matches pattern `p`. A dot matches any
single character. A star means zero or more copies of the immediately
preceding pattern atom. The input pattern is valid.

## First principles

At state `(i,j)`, a normal atom consumes one source and one pattern character.
For `atom*`, there are exactly two choices:

- use zero copies and skip both pattern characters;
- if the atom matches `s[i]`, consume one source character while keeping the
  same pattern state so the star may match again.

Matching is anchored at both ends; there is no substring search.

## Cases that decide correctness

- Empty source can match chains such as `a*b*`.
- Star may use zero copies even when its atom matches.
- Dot under a star matches any run of characters.
- A partial prefix match is not enough.
- Regex star semantics differ from wildcard star semantics.

## Brute force: explore both star branches

```python
def regex_match_brute(source: str, pattern: str) -> bool:
    def search(source_index: int, pattern_index: int) -> bool:
        if pattern_index == len(pattern):
            return source_index == len(source)
        matches = source_index < len(source) and pattern[pattern_index] in (
            source[source_index],
            ".",
        )
        has_star = (
            pattern_index + 1 < len(pattern) and pattern[pattern_index + 1] == "*"
        )
        if has_star:
            return search(source_index, pattern_index + 2) or (
                matches and search(source_index + 1, pattern_index)
            )
        return matches and search(source_index + 1, pattern_index + 1)

    return search(0, 0)
```

Overlapping branches make this exponential in the worst case.

## Better approach: memoize source-pattern states

```python
from functools import cache


def regex_match_memo(source: str, pattern: str) -> bool:
    @cache
    def search(source_index: int, pattern_index: int) -> bool:
        if pattern_index == len(pattern):
            return source_index == len(source)
        matches = source_index < len(source) and pattern[pattern_index] in (
            source[source_index],
            ".",
        )
        if pattern_index + 1 < len(pattern) and pattern[pattern_index + 1] == "*":
            return search(source_index, pattern_index + 2) or (
                matches and search(source_index + 1, pattern_index)
            )
        return matches and search(source_index + 1, pattern_index + 1)

    return search(0, 0)
```

This uses `O(|s||p|)` time and memo space.

## Expert solution: rolling bottom-up DP

```python
def is_regex_match(source: str, pattern: str) -> bool:
    previous = [False] * (len(pattern) + 1)
    previous[0] = True
    for pattern_length in range(2, len(pattern) + 1):
        if pattern[pattern_length - 1] == "*":
            previous[pattern_length] = previous[pattern_length - 2]

    for character in source:
        current = [False] * (len(pattern) + 1)
        for pattern_length in range(1, len(pattern) + 1):
            atom = pattern[pattern_length - 1]
            if atom == "*":
                preceding = pattern[pattern_length - 2]
                current[pattern_length] = current[pattern_length - 2] or (
                    preceding in (character, ".") and previous[pattern_length]
                )
            elif atom in (character, "."):
                current[pattern_length] = previous[pattern_length - 1]
        previous = current
    return previous[-1]
```

Each cell implements the same exhaustive recurrence, while rolling rows retain
only states needed by the next source character.

**Complexity:** `O(|s||p|)` time and `O(|p|)` space.
