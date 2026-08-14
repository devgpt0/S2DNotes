# ICPC300 230: Codeforces 696D - Legen...

**Source:** [Codeforces 696D - Legen...](https://codeforces.com/problemset/problem/696/D)  
**Rating:** 2500  
**Pattern:** Aho-Corasick automaton with max-plus matrix exponentiation  
**Goal:** Construct a lowercase string of the required length maximizing the
total number of occurrences of all given patterns. Occurrences may overlap, and
duplicate input patterns score separately.

## 1. First principles

An Aho-Corasick state identifies every pattern ending after the current prefix.
Propagate terminal counts through failure links so entering a state earns the
number of patterns ending there.

Build a max-plus transition matrix:

```text
matrix[state][next_state] = maximum score earned by one character transition
```

Max-plus multiplication composes lengths, replacing addition by maximum and
multiplication by addition. Binary exponentiation reaches very large lengths.

## 2. Cases that decide correctness

- Overlapping pattern occurrences all score.
- Failure-link suffix patterns score at the same position.
- Duplicate patterns increment the terminal score more than once.
- Different characters reaching the same state keep the same best transition.
- The empty prefix begins at the automaton root with score zero.

## 3. Brute force: enumerate every lowercase string

```python
from itertools import product


ALPHABET = "abcdefghijklmnopqrstuvwxyz"


def maximum_pattern_score_brute(patterns: list[str], length: int) -> int:
    if length <= 0 or not patterns:
        raise ValueError("length and patterns must be nonempty")
    if any(
        not pattern or any(not "a" <= character <= "z" for character in pattern)
        for pattern in patterns
    ):
        raise ValueError("patterns must contain lowercase English letters")

    answer = 0
    for characters in product(ALPHABET, repeat=length):
        text = "".join(characters)
        score = 0
        for pattern in patterns:
            for start in range(length - len(pattern) + 1):
                score += text.startswith(pattern, start)
        answer = max(answer, score)
    return answer
```

**Complexity:** `O(26^length * length * total_pattern_length)` time and
`O(length)` space.

## 4. Better transition: optimize over automaton states

For a fixed current automaton state, the earlier generated characters matter
only through their accumulated score. The same one-character state transition
is repeated `length` times, making this a longest walk of fixed length in a
small weighted graph.

## 5. Expert solution: max-plus power of the automaton graph

```python
from collections import deque


ALPHABET = "abcdefghijklmnopqrstuvwxyz"


def maximum_pattern_score(patterns: list[str], length: int) -> int:
    if length <= 0 or not patterns:
        raise ValueError("length and patterns must be nonempty")
    if any(
        not pattern or any(not "a" <= character <= "z" for character in pattern)
        for pattern in patterns
    ):
        raise ValueError("patterns must contain lowercase English letters")

    transitions: list[dict[str, int]] = [{}]
    failure = [0]
    output = [0]
    for pattern in patterns:
        state = 0
        for character in pattern:
            next_state = transitions[state].get(character)
            if next_state is None:
                next_state = len(transitions)
                transitions[state][character] = next_state
                transitions.append({})
                failure.append(0)
                output.append(0)
            state = next_state
        output[state] += 1

    go = [[0] * len(ALPHABET) for _ in transitions]
    queue: deque[int] = deque()
    for symbol, character in enumerate(ALPHABET):
        child = transitions[0].get(character)
        if child is not None:
            go[0][symbol] = child
            queue.append(child)
    while queue:
        state = queue.popleft()
        output[state] += output[failure[state]]
        for symbol, character in enumerate(ALPHABET):
            child = transitions[state].get(character)
            if child is None:
                go[state][symbol] = go[failure[state]][symbol]
                continue
            failure[child] = go[failure[state]][symbol]
            go[state][symbol] = child
            queue.append(child)

    state_count = len(transitions)
    negative_infinity = -(10**18)
    transition_matrix = [[negative_infinity] * state_count for _ in range(state_count)]
    for state in range(state_count):
        for next_state in go[state]:
            transition_matrix[state][next_state] = max(
                transition_matrix[state][next_state], output[next_state]
            )

    def multiply(first: list[list[int]], second: list[list[int]]) -> list[list[int]]:
        result = [[negative_infinity] * state_count for _ in range(state_count)]
        for start in range(state_count):
            for middle in range(state_count):
                if first[start][middle] == negative_infinity:
                    continue
                first_score = first[start][middle]
                for end in range(state_count):
                    if second[middle][end] != negative_infinity:
                        result[start][end] = max(
                            result[start][end],
                            first_score + second[middle][end],
                        )
        return result

    result = [[negative_infinity] * state_count for _ in range(state_count)]
    for state in range(state_count):
        result[state][state] = 0
    power = transition_matrix
    exponent = length
    while exponent:
        if exponent & 1:
            result = multiply(result, power)
        power = multiply(power, power)
        exponent >>= 1
    return max(result[0])
```

### Why the expert code is correct

The automaton transition records the exact set of patterns ending after each
new character, including suffix outputs. A max-plus matrix entry is therefore
the best score for a fixed-length walk between two states. Matrix composition
considers every intermediate state and adds segment scores; exponentiation
enumerates all strings of the requested length and keeps the maximum.

**Complexity:** `O(S^3 log length + total_pattern_length * 26)` time and
`O(S^2)` space for `S` automaton states.

## 6. What to remember

```text
pattern occurrence score -> Aho-Corasick output count
generated string -> weighted automaton walk
fixed huge walk length -> max-plus matrix exponentiation
```
