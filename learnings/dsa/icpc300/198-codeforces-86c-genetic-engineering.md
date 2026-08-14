# ICPC300 198: Codeforces 86C - Genetic engineering

**Source:** [Codeforces 86C - Genetic engineering](https://codeforces.com/problemset/problem/86/C)  
**Rating:** 2400  
**Pattern:** Aho-Corasick automaton plus trailing-uncovered DP  
**Goal:** Count DNA strings of a fixed length in which every position is
covered by at least one occurrence of a given pattern, modulo `1_000_000_009`.
Pattern occurrences may overlap.

## 1. First principles

Scan a generated string left to right. Besides the Aho-Corasick state, keep
`gap`: the number of trailing characters not yet covered by occurrences whose
right endpoint has been seen.

After appending a character, `gap` becomes `gap + 1`. If the longest pattern
ending at the new automaton state has length at least that value, its occurrence
connects to the already covered prefix and covers the whole new suffix, so the
new gap is zero. A gap reaching the maximum pattern length can never be repaired
later and is discarded.

## 2. Cases that decide correctness

- Coverage may use overlapping occurrences.
- A pattern ending through a failure link also counts.
- Only the longest ending pattern is needed: if any suffix bridges the gap, the
  longest one also bridges it.
- A fully covered completed string has gap zero.
- Generated and pattern characters are only `A`, `C`, `G`, and `T`.

## 3. Brute force: enumerate every DNA string

```python
from itertools import product


MODULO = 1_000_000_009
ALPHABET = "ACGT"


def covered_dna_count_brute(length: int, patterns: list[str]) -> int:
    if length <= 0 or not patterns:
        raise ValueError("length and patterns must be nonempty")
    if any(
        not pattern or any(character not in ALPHABET for character in pattern)
        for pattern in patterns
    ):
        raise ValueError("patterns must contain DNA characters")

    answer = 0
    for characters in product(ALPHABET, repeat=length):
        text = "".join(characters)
        covered = [False] * length
        for pattern in patterns:
            for start in range(length - len(pattern) + 1):
                if text.startswith(pattern, start):
                    for index in range(start, start + len(pattern)):
                        covered[index] = True
        if all(covered):
            answer += 1
    return answer % MODULO
```

**Complexity:** `O(4^n * n * total_pattern_length)` time and `O(n)` space.

## 4. Better transition: remember only the uncovered suffix

The entire coverage history is irrelevant once a prefix is fully covered. The
only risk is the trailing uncovered suffix; its length, together with the
automaton state, completely determines whether a newly ending pattern repairs
the gap.

## 5. Expert solution: automaton and gap DP

```python
from collections import deque


MODULO = 1_000_000_009
ALPHABET = "ACGT"


def covered_dna_count(length: int, patterns: list[str]) -> int:
    if length <= 0 or not patterns:
        raise ValueError("length and patterns must be nonempty")
    if any(
        not pattern or any(character not in ALPHABET for character in pattern)
        for pattern in patterns
    ):
        raise ValueError("patterns must contain DNA characters")

    symbol_index = {character: index for index, character in enumerate(ALPHABET)}
    transitions: list[dict[int, int]] = [{}]
    failure = [0]
    longest = [0]
    for pattern in patterns:
        state = 0
        for character in pattern:
            symbol = symbol_index[character]
            next_state = transitions[state].get(symbol)
            if next_state is None:
                next_state = len(transitions)
                transitions[state][symbol] = next_state
                transitions.append({})
                failure.append(0)
                longest.append(0)
            state = next_state
        longest[state] = max(longest[state], len(pattern))

    go = [[0] * len(ALPHABET) for _ in transitions]
    queue: deque[int] = deque()
    for symbol in range(len(ALPHABET)):
        child = transitions[0].get(symbol)
        if child is not None:
            go[0][symbol] = child
            queue.append(child)
    while queue:
        state = queue.popleft()
        longest[state] = max(longest[state], longest[failure[state]])
        for symbol in range(len(ALPHABET)):
            child = transitions[state].get(symbol)
            if child is None:
                go[state][symbol] = go[failure[state]][symbol]
                continue
            failure[child] = go[failure[state]][symbol]
            go[state][symbol] = child
            queue.append(child)

    maximum_length = max(map(len, patterns))
    dp = [[0] * maximum_length for _ in transitions]
    dp[0][0] = 1
    for _ in range(length):
        next_dp = [[0] * maximum_length for _ in transitions]
        for state, gaps in enumerate(dp):
            for gap, count in enumerate(gaps):
                if count == 0:
                    continue
                for symbol in range(len(ALPHABET)):
                    next_state = go[state][symbol]
                    extended_gap = gap + 1
                    next_gap = (
                        0 if longest[next_state] >= extended_gap else extended_gap
                    )
                    if next_gap < maximum_length:
                        next_dp[next_state][next_gap] = (
                            next_dp[next_state][next_gap] + count
                        ) % MODULO
        dp = next_dp
    return sum(gaps[0] for gaps in dp) % MODULO
```

### Why the expert code is correct

The automaton state identifies every pattern suffix ending at the current
position, and `longest` includes failure-link outputs. The gap is exactly the
distance from the covered prefix frontier. An ending occurrence extends that
frontier to the current position exactly when its length reaches across the
gap. The DP enumerates all four next characters and accepts precisely states
whose final frontier covers the entire string.

**Complexity:** `O(n S L |alphabet|)` time and `O(SL)` space for `S` automaton
states and maximum pattern length `L`.

## 6. What to remember

```text
many pattern endings -> Aho-Corasick
coverage history -> length of trailing uncovered suffix
ending pattern bridges gap -> reset gap to zero
```
