# ICPC300 062: CSES - Required Substring

**Source:** [CSES - Required Substring](https://cses.fi/problemset/task/1112/)  
**Pattern:** KMP automaton dynamic programming  
**Goal:** Count, modulo `1_000_000_007`, uppercase English strings of length
`n` that contain the required pattern at least once.

## 1. Problem in plain words

There are `26^n` possible strings. We only need to remember how much of the
pattern matches the current suffix, not the whole prefix built so far.

Once the full pattern has appeared, later characters cannot make the string
invalid. The full-match state is therefore absorbing.

## 2. First principles

The KMP prefix function tells where to fall back after a mismatch while
preserving the longest suffix that is also a pattern prefix.

Automaton state `j` means the built string ends with `pattern[:j]`, and no
longer pattern prefix matches that suffix. For each of 26 next characters,
transition to the new matched length. State `m = len(pattern)` means the
required substring has occurred and remains state `m` forever.

DP over positions and these `m+1` states counts all strings without storing
them.

## 3. Cases that decide correctness

| Case | Required result |
| --- | --- |
| Pattern longer than final string | `0`. |
| Pattern length equals `n` | Exactly one matching string. |
| Pattern overlaps with itself | KMP fallback preserves valid overlaps. |
| Pattern appears more than once | Count the full string once. |
| Match completes before the end | Stay in the absorbing state. |

## 4. Brute force: generate all uppercase strings

```python
from itertools import product

MODULO = 1_000_000_007
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def count_strings_with_pattern_brute_force(length: int, pattern: str) -> int:
    if (
        length < 0
        or not pattern
        or any(character not in ALPHABET for character in pattern)
    ):
        raise ValueError("length must be nonnegative and pattern uppercase")
    return (
        sum(
            pattern in "".join(characters)
            for characters in product(ALPHABET, repeat=length)
        )
        % MODULO
    )
```

**Complexity:** `O(26^n * n)` time and `O(n)` generated-string memory.

## 5. Better: memoize position and current matched prefix

This top-down version reduces the state count to `O(nm)`. It computes KMP
fallback during transitions, so the same state-character transition is still
repeated at different positions.

```python
from functools import lru_cache

MODULO = 1_000_000_007
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def count_strings_with_pattern_memoized(length: int, pattern: str) -> int:
    if (
        length < 0
        or not pattern
        or any(character not in ALPHABET for character in pattern)
    ):
        raise ValueError("length must be nonnegative and pattern uppercase")

    prefix = [0] * len(pattern)
    for index in range(1, len(pattern)):
        matched = prefix[index - 1]
        while matched and pattern[index] != pattern[matched]:
            matched = prefix[matched - 1]
        if pattern[index] == pattern[matched]:
            matched += 1
        prefix[index] = matched

    def advance(matched: int, character: str) -> int:
        if matched == len(pattern):
            return matched
        while matched and character != pattern[matched]:
            matched = prefix[matched - 1]
        if character == pattern[matched]:
            matched += 1
        return matched

    @lru_cache(maxsize=None)
    def count(position: int, matched: int) -> int:
        if position == length:
            return int(matched == len(pattern))
        return (
            sum(
                count(position + 1, advance(matched, character))
                for character in ALPHABET
            )
            % MODULO
        )

    return count(0, 0)
```

**Complexity:** `O(nm * 26 * m)` worst-case time for repeated fallback work and
`O(nm)` memoization memory.

## 6. Expert solution: precompute the KMP automaton

```python
MODULO = 1_000_000_007
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def count_strings_with_pattern(length: int, pattern: str) -> int:
    if (
        length < 0
        or not pattern
        or any(character not in ALPHABET for character in pattern)
    ):
        raise ValueError("length must be nonnegative and pattern uppercase")

    pattern_length = len(pattern)
    prefix = [0] * pattern_length
    for index in range(1, pattern_length):
        matched = prefix[index - 1]
        while matched and pattern[index] != pattern[matched]:
            matched = prefix[matched - 1]
        if pattern[index] == pattern[matched]:
            matched += 1
        prefix[index] = matched

    transitions = [[0] * len(ALPHABET) for _ in range(pattern_length + 1)]
    for matched in range(pattern_length):
        for character_index, character in enumerate(ALPHABET):
            next_matched = matched
            while next_matched and character != pattern[next_matched]:
                next_matched = prefix[next_matched - 1]
            if character == pattern[next_matched]:
                next_matched += 1
            transitions[matched][character_index] = next_matched
    transitions[pattern_length] = [pattern_length] * len(ALPHABET)

    dp = [0] * (pattern_length + 1)
    dp[0] = 1
    for _ in range(length):
        next_dp = [0] * (pattern_length + 1)
        for matched, ways in enumerate(dp):
            for next_matched in transitions[matched]:
                next_dp[next_matched] = (next_dp[next_matched] + ways) % MODULO
        dp = next_dp
    return dp[pattern_length]
```

### Why the expert code is correct

- A KMP state records exactly the longest pattern prefix matching the current
  suffix, which is all history relevant to a future match.
- Precomputed transitions apply the exact KMP fallback rule for every next
  uppercase character.
- The absorbing full-match state groups all strings that have already
  satisfied the requirement, regardless of later characters.
- Position DP considers every one of the 26 choices once from every state, so
  it counts exactly all valid length-`n` strings.

**Complexity:** `O(26m^2 + 26nm)` time as written and `O(26m + m)` working
memory. The source pattern bound makes transition construction small.

## 7. What to remember

When a DP only cares whether a pattern has appeared, use KMP matched-prefix
length as the state and make the full-match state absorbing.
