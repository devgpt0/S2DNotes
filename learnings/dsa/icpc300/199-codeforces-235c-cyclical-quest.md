# ICPC300 199: Codeforces 235C - Cyclical Quest

**Source:** [Codeforces 235C - Cyclical Quest](https://codeforces.com/problemset/problem/235/C)  
**Rating:** 2400  
**Pattern:** suffix automaton matching with suffix-link canonicalization  
**Goal:** For each query, count its distinct cyclic shifts that occur as
substrings of one fixed lowercase base string.

## 1. First principles

All cyclic shifts of a length-`m` query are the `m` length-`m` windows of
`query + query[:-1]`. A suffix automaton scans those windows together.

One automaton state represents substring lengths
`max_length[link[state]] + 1 ... max_length[state]`. For a matched window of
length `m`, climb suffix links to the unique state whose interval contains `m`.
That state is the canonical identity of the window. Counting distinct marked
states removes duplicate rotations of periodic queries.

## 2. Cases that decide correctness

- A one-character query has one cyclic shift.
- Periodic queries may have fewer distinct shifts than their length.
- A shift is counted once even if it occurs many times in the base string.
- The doubled scan stops after `2m-1` characters, producing exactly `m` windows.
- A query longer than the base cannot match any complete shift.

## 3. Brute force: build every distinct rotation

```python
def cyclic_shift_counts_brute(base: str, queries: list[str]) -> list[int]:
    if not base or any(not "a" <= character <= "z" for character in base):
        raise ValueError("base must contain lowercase English letters")
    if any(
        not query or any(not "a" <= character <= "z" for character in query)
        for query in queries
    ):
        raise ValueError("queries must contain lowercase English letters")

    answers: list[int] = []
    for query in queries:
        rotations = {query[offset:] + query[:offset] for offset in range(len(query))}
        answers.append(sum(rotation in base for rotation in rotations))
    return answers
```

**Complexity:** `O(sum(m^2 + m|base|))` time and `O(m^2)` temporary space.

## 4. Better transition: identify substrings by automaton state

Suffix automata match a stream while retaining its longest suffix that occurs
in the base. Suffix-link binary lifting then maps every successful length-`m`
window to its canonical state in logarithmic time without changing the ongoing
stream match.

## 5. Expert solution: suffix automaton plus link lifting

```python
def cyclic_shift_counts(base: str, queries: list[str]) -> list[int]:
    if not base or any(not "a" <= character <= "z" for character in base):
        raise ValueError("base must contain lowercase English letters")
    if any(
        not query or any(not "a" <= character <= "z" for character in query)
        for query in queries
    ):
        raise ValueError("queries must contain lowercase English letters")

    transitions: list[dict[str, int]] = [{}]
    suffix_link = [-1]
    maximum_length = [0]
    last = 0
    for character in base:
        current = len(transitions)
        transitions.append({})
        suffix_link.append(0)
        maximum_length.append(maximum_length[last] + 1)
        previous = last
        while previous != -1 and character not in transitions[previous]:
            transitions[previous][character] = current
            previous = suffix_link[previous]
        if previous == -1:
            suffix_link[current] = 0
        else:
            target = transitions[previous][character]
            if maximum_length[previous] + 1 == maximum_length[target]:
                suffix_link[current] = target
            else:
                clone = len(transitions)
                transitions.append(transitions[target].copy())
                suffix_link.append(suffix_link[target])
                maximum_length.append(maximum_length[previous] + 1)
                while previous != -1 and transitions[previous].get(character) == target:
                    transitions[previous][character] = clone
                    previous = suffix_link[previous]
                suffix_link[target] = clone
                suffix_link[current] = clone
        last = current

    levels = max(1, len(transitions).bit_length())
    ancestors = [[-1] * len(transitions) for _ in range(levels)]
    ancestors[0] = suffix_link.copy()
    for level in range(1, levels):
        for state in range(len(transitions)):
            middle = ancestors[level - 1][state]
            if middle != -1:
                ancestors[level][state] = ancestors[level - 1][middle]

    answers: list[int] = []
    for query in queries:
        if len(query) > len(base):
            answers.append(0)
            continue
        state = 0
        matched = 0
        seen_states: set[int] = set()
        for character in query + query[:-1]:
            while state and character not in transitions[state]:
                state = suffix_link[state]
                matched = min(matched, maximum_length[state])
            next_state = transitions[state].get(character)
            if next_state is None:
                state = 0
                matched = 0
                continue
            state = next_state
            matched += 1
            if matched < len(query):
                continue

            representative = state
            for level in range(levels - 1, -1, -1):
                ancestor = ancestors[level][representative]
                if ancestor != -1 and maximum_length[ancestor] >= len(query):
                    representative = ancestor
            seen_states.add(representative)
        answers.append(len(seen_states))
    return answers
```

### Why the expert code is correct

The doubled query exposes every rotation as one window. The automaton reports
exactly which windows occur in the base. For fixed length `m`, suffix-link
intervals partition all distinct occurring substrings, so canonical states are
equal exactly for equal rotation strings. The marked-state set therefore counts
each occurring distinct cyclic shift once.

**Complexity:** `O(|base| log |base| + sum(m log |base|))` time and
`O(|base| log |base|)` space.

## 6. What to remember

```text
cyclic shifts -> windows of query + query[:-1]
substring membership stream -> suffix automaton
fixed-length substring identity -> canonical suffix-link state
```
