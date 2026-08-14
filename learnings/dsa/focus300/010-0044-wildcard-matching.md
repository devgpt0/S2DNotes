# Focus300 010: LeetCode 44 - Wildcard Matching

**Source:** [LeetCode 44](https://leetcode.com/problems/wildcard-matching/)  
**Difficulty:** Hard  
**Pattern:** greedy matching with the most recent star checkpoint

## Exact contract

Return whether the entire string `s` matches wildcard pattern `p`. A question
mark matches exactly one character. A star matches any sequence, including the
empty sequence.

## First principles

Without a star, the next source and pattern characters must match immediately.
At a star, first let it match empty and remember both positions. If a later
mismatch occurs, expand that most recent star by one more source character and
retry the pattern suffix after it.

Only the most recent star matters: expanding an earlier star instead would
give the later star fewer options and cannot rescue a match the latest one
cannot represent.

## Cases that decide correctness

- Matching is anchored to the whole string.
- Star may match zero characters.
- Question mark must consume exactly one character.
- Consecutive stars are harmless.
- After the source is consumed, only trailing stars may remain.

## Brute force: explore empty and consuming star branches

```python
def wildcard_match_brute(source: str, pattern: str) -> bool:
    def search(source_index: int, pattern_index: int) -> bool:
        if pattern_index == len(pattern):
            return source_index == len(source)
        if pattern[pattern_index] == "*":
            return search(source_index, pattern_index + 1) or (
                source_index < len(source) and search(source_index + 1, pattern_index)
            )
        return (
            source_index < len(source)
            and pattern[pattern_index] in (source[source_index], "?")
            and search(source_index + 1, pattern_index + 1)
        )

    return search(0, 0)
```

Repeated star branches make this exponential.

## Better approach: rolling dynamic programming

```python
def wildcard_match_dp(source: str, pattern: str) -> bool:
    previous = [False] * (len(pattern) + 1)
    previous[0] = True
    for index, character in enumerate(pattern, start=1):
        previous[index] = previous[index - 1] and character == "*"

    for source_character in source:
        current = [False] * (len(pattern) + 1)
        for pattern_length, pattern_character in enumerate(pattern, start=1):
            if pattern_character == "*":
                current[pattern_length] = (
                    current[pattern_length - 1] or previous[pattern_length]
                )
            elif pattern_character in (source_character, "?"):
                current[pattern_length] = previous[pattern_length - 1]
        previous = current
    return previous[-1]
```

This is `O(|s||p|)` time and `O(|p|)` space.

## Expert solution: greedy star expansion

```python
def is_wildcard_match(source: str, pattern: str) -> bool:
    source_index = 0
    pattern_index = 0
    star_index = -1
    star_source_start = -1

    while source_index < len(source):
        if pattern_index < len(pattern) and pattern[pattern_index] in (
            source[source_index],
            "?",
        ):
            source_index += 1
            pattern_index += 1
        elif pattern_index < len(pattern) and pattern[pattern_index] == "*":
            star_index = pattern_index
            star_source_start = source_index
            pattern_index += 1
        elif star_index != -1:
            star_source_start += 1
            source_index = star_source_start
            pattern_index = star_index + 1
        else:
            return False

    return all(character == "*" for character in pattern[pattern_index:])
```

Every retry expands the latest star by one source character; neither pointer
ever needs an exponential branch tree.

**Complexity:** `O(|s|+|p|)` time and `O(1)` space.
