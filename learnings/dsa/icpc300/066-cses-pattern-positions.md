# ICPC300 066: CSES - Pattern Positions

**Source:** [CSES - Pattern Positions](https://cses.fi/problemset/task/2104/)  
**Pattern:** suffix automaton with minimum end positions  
**Goal:** For each pattern, output its earliest one-based starting position in
the text, or `-1` when it does not occur.

## 1. Problem in plain words

For text `ababa`, pattern `aba` first starts at position `1`, while pattern
`ba` first starts at position `2`. Overlapping occurrences are allowed.

All substrings represented by one suffix-automaton state have the same set of
ending positions. If that state's minimum ending position is known, any
pattern reaching it has an immediate earliest-start answer.

## 2. First principles

Each newly created non-clone automaton state corresponds to a text prefix
ending at its current zero-based position. Give it that position. Clone states
begin with no direct occurrence.

Propagate minimum end positions from longer states to their suffix links in
decreasing `max_length` order. The suffix link's substrings occur at every end
position of the child, so taking the minimum is correct.

After traversing a pattern of length `m` to state `v`, its earliest one-based
start is `min_end[v] - m + 2`.

## 3. Cases that decide correctness

| Case | Required behavior |
| --- | --- |
| Pattern equals the text | Position `1`. |
| Pattern occurs several times | Return the smallest start. |
| Overlapping occurrences | They remain valid occurrences. |
| Missing transition while traversing | Return `-1`. |
| Pattern represented by a clone class | Propagated minimum end is still exact. |

## 4. Brute force: use direct substring comparison

```python
def earliest_pattern_positions_brute_force(text: str, patterns: list[str]) -> list[int]:
    if not text or any(not pattern for pattern in patterns):
        raise ValueError("text and patterns must be nonempty")
    answers: list[int] = []
    for pattern in patterns:
        position = text.find(pattern)
        answers.append(position + 1 if position != -1 else -1)
    return answers
```

**Complexity:** up to `O(qnL)` character work for `q` patterns of maximum
length `L`.

## 5. Better: KMP independently for every pattern

KMP avoids restarting text comparisons after a mismatch, giving linear work
per query in the text plus pattern length.

```python
def earliest_pattern_positions_kmp(text: str, patterns: list[str]) -> list[int]:
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

        matched = 0
        answer = -1
        for index, character in enumerate(text):
            while matched and character != pattern[matched]:
                matched = prefix[matched - 1]
            if character == pattern[matched]:
                matched += 1
            if matched == len(pattern):
                answer = index - len(pattern) + 2
                break
        answers.append(answer)
    return answers
```

**Complexity:** `O(sum(n + pattern_length))` time and `O(L)` extra memory.

## 6. Expert solution: one suffix automaton for all queries

```python
def earliest_pattern_positions(text: str, patterns: list[str]) -> list[int]:
    if not text or any(not pattern for pattern in patterns):
        raise ValueError("text and patterns must be nonempty")

    infinity = len(text) + 1
    transitions: list[dict[str, int]] = [{}]
    suffix_link = [-1]
    max_length = [0]
    minimum_end = [infinity]
    last = 0

    for position, character in enumerate(text):
        current = len(transitions)
        transitions.append({})
        suffix_link.append(0)
        max_length.append(max_length[last] + 1)
        minimum_end.append(position)

        previous = last
        while previous != -1 and character not in transitions[previous]:
            transitions[previous][character] = current
            previous = suffix_link[previous]
        if previous == -1:
            suffix_link[current] = 0
        else:
            next_state = transitions[previous][character]
            if max_length[previous] + 1 == max_length[next_state]:
                suffix_link[current] = next_state
            else:
                clone = len(transitions)
                transitions.append(transitions[next_state].copy())
                suffix_link.append(suffix_link[next_state])
                max_length.append(max_length[previous] + 1)
                minimum_end.append(infinity)
                while (
                    previous != -1
                    and transitions[previous].get(character) == next_state
                ):
                    transitions[previous][character] = clone
                    previous = suffix_link[previous]
                suffix_link[next_state] = clone
                suffix_link[current] = clone
        last = current

    order = sorted(range(len(transitions)), key=max_length.__getitem__, reverse=True)
    for state in order:
        parent = suffix_link[state]
        if parent != -1:
            minimum_end[parent] = min(minimum_end[parent], minimum_end[state])

    answers: list[int] = []
    for pattern in patterns:
        state = 0
        for character in pattern:
            if character not in transitions[state]:
                state = -1
                break
            state = transitions[state][character]
        if state == -1:
            answers.append(-1)
        else:
            answers.append(minimum_end[state] - len(pattern) + 2)
    return answers
```

### Why the expert code is correct

- Automaton traversal succeeds exactly for substrings of the text.
- New states record actual prefix ending positions; suffix-link propagation
  transfers every occurrence end to all suffix classes that occur there.
- Decreasing maximum-length order ensures a state is complete before updating
  its suffix link.
- All substrings represented by the reached state share its end-position set,
  so converting its minimum end gives the pattern's earliest start.

**Complexity:** `O(n log n + total_pattern_length)` time as written because of
the state sort, and `O(n)` automaton memory.

## 7. What to remember

Occurrence positions are suffix-automaton state data. Propagate minimum end
positions through suffix links, then each pattern query is one automaton walk.
