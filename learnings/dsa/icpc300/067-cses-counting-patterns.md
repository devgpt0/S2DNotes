# ICPC300 067: CSES - Counting Patterns

**Source:** [CSES - Counting Patterns](https://cses.fi/problemset/task/2103/)  
**Pattern:** Aho-Corasick failure links with occurrence propagation  
**Goal:** For every pattern, count how many times it occurs in the text,
including overlapping occurrences.

## 1. Problem in plain words

In text `aaaa`, pattern `aa` occurs three times, starting at positions `1`,
`2`, and `3`. Counting must not skip ahead after a match.

Searching each pattern independently repeats the same text scan. Aho-Corasick
combines all patterns into one trie automaton.

## 2. First principles

Trie edges match pattern prefixes. A failure link from node `v` points to the
longest proper suffix of `v`'s trie string that is also a trie prefix. During a
text scan, failure links recover after mismatches without restarting.

Increment a visit counter only for the automaton state reached after each text
character. If state `v` is visited, every pattern represented by a suffix-link
ancestor of `v` also ends there. Propagate visit counts from deeper states to
their failure links in reverse breadth-first order. A pattern's terminal node
then holds its total occurrences.

## 3. Cases that decide correctness

| Case | Required behavior |
| --- | --- |
| Overlapping matches | Count every ending position. |
| One pattern is a suffix of another | Failure propagation counts both. |
| Duplicate query patterns | Return the same count for each query. |
| Pattern longer than text | Count `0`. |
| No automaton edge for a character | Follow failure links to root as needed. |

## 4. Brute force: test every starting position

```python
def count_pattern_occurrences_brute_force(text: str, patterns: list[str]) -> list[int]:
    if not text or any(not pattern for pattern in patterns):
        raise ValueError("text and patterns must be nonempty")
    return [
        sum(
            text.startswith(pattern, start)
            for start in range(len(text) - len(pattern) + 1)
        )
        for pattern in patterns
    ]
```

**Complexity:** `O(sum(n * pattern_length))` time and `O(1)` auxiliary memory.

## 5. Better: KMP once per pattern

KMP makes each individual search linear and resets to the longest border after
a match so overlaps remain countable.

```python
def count_pattern_occurrences_kmp(text: str, patterns: list[str]) -> list[int]:
    if not text or any(not pattern for pattern in patterns):
        raise ValueError("text and patterns must be nonempty")

    answers: list[int] = []
    for pattern in patterns:
        prefix = [0] * len(pattern)
        for index in range(1, len(pattern)):
            matched = prefix[index - 1]
            while matched and pattern[index] != pattern[matched]:
                matched = prefix[matched - 1]
            if pattern[index] == pattern[matched]:
                matched += 1
            prefix[index] = matched

        occurrences = 0
        matched = 0
        for character in text:
            while matched and character != pattern[matched]:
                matched = prefix[matched - 1]
            if character == pattern[matched]:
                matched += 1
            if matched == len(pattern):
                occurrences += 1
                matched = prefix[matched - 1]
        answers.append(occurrences)
    return answers
```

**Complexity:** `O(sum(n + pattern_length))` time and `O(L)` memory.

## 6. Expert solution: one Aho-Corasick text scan

```python
from collections import deque


def count_pattern_occurrences(text: str, patterns: list[str]) -> list[int]:
    if not text or any(not pattern for pattern in patterns):
        raise ValueError("text and patterns must be nonempty")

    children: list[dict[str, int]] = [{}]
    failure = [0]
    terminal_nodes: list[int] = []

    for pattern in patterns:
        node = 0
        for character in pattern:
            if character not in children[node]:
                children[node][character] = len(children)
                children.append({})
                failure.append(0)
            node = children[node][character]
        terminal_nodes.append(node)

    queue = deque(children[0].values())
    breadth_first_order: list[int] = []
    while queue:
        node = queue.popleft()
        breadth_first_order.append(node)
        for character, child in children[node].items():
            fallback = failure[node]
            while fallback and character not in children[fallback]:
                fallback = failure[fallback]
            failure[child] = children[fallback].get(character, 0)
            queue.append(child)

    visits = [0] * len(children)
    state = 0
    for character in text:
        while state and character not in children[state]:
            state = failure[state]
        state = children[state].get(character, 0)
        visits[state] += 1

    for node in reversed(breadth_first_order):
        visits[failure[node]] += visits[node]
    return [visits[node] for node in terminal_nodes]
```

### Why the expert code is correct

- Trie traversal plus failure links leaves the automaton in the state for the
  longest pattern prefix that is a suffix of the scanned text prefix.
- A visit at state `v` means the string of every failure ancestor also ends at
  that position.
- Reverse breadth-first propagation transfers each visit to all such suffix
  states exactly once per failure-tree edge.
- A terminal node therefore accumulates exactly all ending positions of its
  pattern, including overlaps.

**Complexity:** `O(total_pattern_length + text_length + reported_queries)`
expected time and `O(total_pattern_length)` memory for the source alphabet.

## 7. What to remember

Aho-Corasick finds all pattern endings in one scan. Count state visits first,
then propagate them upward through failure links.
