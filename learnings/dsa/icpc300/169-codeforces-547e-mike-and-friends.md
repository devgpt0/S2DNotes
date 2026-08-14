# ICPC300 169: Codeforces 547E - Mike and Friends

**Source:** [Codeforces 547E](https://codeforces.com/problemset/problem/547/E)  
**Pattern:** offline Aho-Corasick queries on a failure-tree Euler tour

## Exact contract

Given `n` lowercase strings and `q` queries `(l,r,k)`, output the total number
of occurrences of string `k` across strings `l..r`. Occurrences may overlap.

## First principles

Insert all strings into one Aho-Corasick automaton. While scanning a text,
increment the automaton state reached after every character. Pattern `k`
occurs once for every visited state whose failure chain contains `terminal[k]`.
In the failure-link tree, those states are exactly the terminal node's subtree.

Turn each range query into prefix events: count at prefix `r` minus count at
prefix `l-1`. Process input strings in order, add their visited states to a
Fenwick tree over the failure tree's Euler order, and answer each event with
one subtree sum.

## Cases that decide correctness

- Count overlapping occurrences by recording every reached text position.
- Identical pattern strings share a terminal node and therefore answers.
- Prefix `0` events must be processed before any text is added.
- Failure-tree subtrees use half-open Euler intervals.
- Query `k` identifies one of the original strings, not an arbitrary new
  pattern.

## Brute force: test every start in every selected text

```python
def mike_friends_brute(
    strings: list[str], queries: list[tuple[int, int, int]]
) -> list[int]:
    answers = []
    for left, right, pattern_index in queries:
        pattern = strings[pattern_index - 1]
        occurrences = 0
        for text in strings[left - 1 : right]:
            occurrences += sum(
                text.startswith(pattern, start) for start in range(len(text))
            )
        answers.append(occurrences)
    return answers
```

Repeated prefix comparisons can multiply text and pattern lengths.

## Better: KMP independently for every selected text

```python
def mike_friends_kmp(
    strings: list[str], queries: list[tuple[int, int, int]]
) -> list[int]:
    answers = []
    for left, right, pattern_index in queries:
        pattern = strings[pattern_index - 1]
        prefix = [0] * len(pattern)
        border = 0
        for index in range(1, len(pattern)):
            while border and pattern[index] != pattern[border]:
                border = prefix[border - 1]
            if pattern[index] == pattern[border]:
                border += 1
            prefix[index] = border

        occurrences = 0
        for text in strings[left - 1 : right]:
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

KMP is linear in the selected text lengths, but the same strings are rescanned
for many queries.

## Expert solution: prefix events and failure-subtree sums

```python
import sys
from collections import deque


def solve() -> None:
    input_stream = sys.stdin.buffer
    string_count, query_count = map(int, input_stream.readline().split())
    strings = [input_stream.readline().strip() for _ in range(string_count)]

    transitions = [[-1] * 26]
    terminal = []
    for text in strings:
        state = 0
        for character in text:
            letter = character - ord("a")
            if transitions[state][letter] == -1:
                transitions[state][letter] = len(transitions)
                transitions.append([-1] * 26)
            state = transitions[state][letter]
        terminal.append(state)

    failure = [0] * len(transitions)
    queue = deque()
    for letter in range(26):
        child = transitions[0][letter]
        if child == -1:
            transitions[0][letter] = 0
        else:
            queue.append(child)
    while queue:
        state = queue.popleft()
        for letter in range(26):
            child = transitions[state][letter]
            if child == -1:
                transitions[state][letter] = transitions[failure[state]][letter]
            else:
                failure[child] = transitions[failure[state]][letter]
                queue.append(child)

    failure_tree = [[] for _ in range(len(transitions))]
    for state in range(1, len(transitions)):
        failure_tree[failure[state]].append(state)

    entry = [0] * len(transitions)
    exit_time = [0] * len(transitions)
    timer = 0
    stack = [(0, False)]
    while stack:
        state, exiting = stack.pop()
        if exiting:
            exit_time[state] = timer
            continue
        entry[state] = timer
        timer += 1
        stack.append((state, True))
        for child in reversed(failure_tree[state]):
            stack.append((child, False))

    events: list[list[tuple[int, int, int]]] = [[] for _ in range(string_count + 1)]
    for query_index in range(query_count):
        left, right, pattern_index = map(int, input_stream.readline().split())
        pattern_state = terminal[pattern_index - 1]
        events[right].append((pattern_state, query_index, 1))
        events[left - 1].append((pattern_state, query_index, -1))

    fenwick = [0] * (len(transitions) + 1)

    def add(position: int) -> None:
        position += 1
        while position < len(fenwick):
            fenwick[position] += 1
            position += position & -position

    def prefix_sum(position: int) -> int:
        result = 0
        while position:
            result += fenwick[position]
            position -= position & -position
        return result

    answers = [0] * query_count
    for processed in range(string_count + 1):
        if processed:
            state = 0
            for character in strings[processed - 1]:
                state = transitions[state][character - ord("a")]
                add(entry[state])
        for pattern_state, query_index, sign in events[processed]:
            occurrences = prefix_sum(exit_time[pattern_state]) - prefix_sum(
                entry[pattern_state]
            )
            answers[query_index] += sign * occurrences

    print("\n".join(map(str, answers)))


if __name__ == "__main__":
    solve()
```

Every text position contributes once at its reached state. Failure-subtree sums
count exactly the patterns ending there, and signed prefix events turn those
cumulative counts into the requested string-index range.

**Complexity:** `O(total_string_length * log S + q log S + 26S)` time and
`O(S+q)` space, where `S` is the automaton size.
