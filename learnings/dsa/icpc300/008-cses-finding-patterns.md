# ICPC300 008: CSES - Finding Patterns

**Source:** [CSES - Finding Patterns](https://cses.fi/problemset/task/2102/)  
**Pattern:** Aho-Corasick automaton  
**Goal:** For every pattern, decide whether it occurs in one fixed text.

## 1. First principles

Searching each pattern separately repeats work. A trie shares common pattern
prefixes. Its **failure link** points from a trie state to the longest proper
suffix that is also a trie prefix, so a mismatch reuses the longest possible
match instead of restarting.

While scanning the text, mark each reached state. A pattern may be a suffix of
that state, so propagate marks through failure links in decreasing depth.

```text
patterns: he, she
state for "she" --failure--> state for "he"

reaching "she" proves both patterns occur
```

## 2. Cases that decide correctness

| Case | Required behavior |
| --- | --- |
| Pattern longer than text | Report `False`. |
| Duplicate patterns | Return the same result for every copy. |
| One pattern is another's suffix | A visit to the longer state must mark the suffix state. |
| Overlapping matches | Reuse failure links; do not skip text characters. |
| Match ends at the final text character | Report it normally. |

Source patterns are non-empty lowercase strings; these implementations reject
empty patterns explicitly.

## 3. Brute force: compare at every start

Try every possible start position and compare characters directly.

```python
def finding_patterns_brute(text: str, patterns: list[str]) -> list[bool]:
    if any(not pattern for pattern in patterns):
        raise ValueError("patterns must be non-empty")

    answers: list[bool] = []
    for pattern in patterns:
        found = False
        for start in range(len(text) - len(pattern) + 1):
            matches = True
            for offset, character in enumerate(pattern):
                if text[start + offset] != character:
                    matches = False
                    break
            if matches:
                found = True
                break
        answers.append(found)
    return answers
```

**Complexity:** `O(sum(n * pattern_length))` worst-case time and `O(1)`
extra space.

## 4. Better: KMP once per pattern

The KMP prefix table records the longest border of each pattern prefix. A
mismatch then preserves the longest suffix that can still become a match.

```python
def finding_patterns_kmp(text: str, patterns: list[str]) -> list[bool]:
    if any(not pattern for pattern in patterns):
        raise ValueError("patterns must be non-empty")

    def occurs(pattern: str) -> bool:
        prefix = [0] * len(pattern)
        matched = 0
        for index in range(1, len(pattern)):
            while matched > 0 and pattern[index] != pattern[matched]:
                matched = prefix[matched - 1]
            if pattern[index] == pattern[matched]:
                matched += 1
            prefix[index] = matched

        matched = 0
        for character in text:
            while matched > 0 and character != pattern[matched]:
                matched = prefix[matched - 1]
            if character == pattern[matched]:
                matched += 1
            if matched == len(pattern):
                return True
        return False

    return [occurs(pattern) for pattern in patterns]
```

**Complexity:** `O(total_pattern_length + n * pattern_count)` time and
`O(max_pattern_length)` extra space.

## 5. Expert solution: Aho-Corasick

Build all patterns into one trie, compute failure links in BFS order, and scan
the text once. Reverse BFS order guarantees a visited deeper state marks every
terminal suffix state before that suffix is inspected.

```python
from collections import deque


def finding_patterns_aho_corasick(text: str, patterns: list[str]) -> list[bool]:
    if any(not pattern for pattern in patterns):
        raise ValueError("patterns must be non-empty")

    transitions: list[dict[str, int]] = [{}]
    failure = [0]
    terminal_state: list[int] = []

    for pattern in patterns:
        state = 0
        for character in pattern:
            next_state = transitions[state].get(character)
            if next_state is None:
                next_state = len(transitions)
                transitions[state][character] = next_state
                transitions.append({})
                failure.append(0)
            state = next_state
        terminal_state.append(state)

    queue: deque[int] = deque()
    breadth_first_order: list[int] = []
    for state in transitions[0].values():
        queue.append(state)

    while queue:
        state = queue.popleft()
        breadth_first_order.append(state)
        for character, next_state in transitions[state].items():
            fallback = failure[state]
            while fallback and character not in transitions[fallback]:
                fallback = failure[fallback]
            failure[next_state] = transitions[fallback].get(character, 0)
            queue.append(next_state)

    visited = [False] * len(transitions)
    visited[0] = True
    state = 0
    for character in text:
        while state and character not in transitions[state]:
            state = failure[state]
        state = transitions[state].get(character, 0)
        visited[state] = True

    for state in reversed(breadth_first_order):
        if visited[state]:
            visited[failure[state]] = True

    return [visited[state] for state in terminal_state]
```

### Why the expert code is correct

- The current trie state is the longest pattern prefix that is a suffix of the
  text read so far.
- Its failure ancestors are exactly the shorter pattern-prefix suffixes, so
  reverse propagation marks every pattern ending at that text position.
- Every text character is consumed once, and each requested terminal state is
  checked independently, including duplicates.

**Complexity:** linear in the text plus trie construction for a fixed
alphabet, with `O(total_pattern_length)` trie space.

## 6. What to remember

```text
one pattern       -> KMP
many patterns     -> one trie + failure links
visited state     -> also visit its failure ancestors
```
