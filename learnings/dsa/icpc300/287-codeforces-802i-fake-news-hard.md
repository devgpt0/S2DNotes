# ICPC300 287: Codeforces 802I - Fake News (hard)

**Source:** [Codeforces 802I - Fake News (hard)](https://codeforces.com/problemset/problem/802/I)  
**Rating:** 2400  
**Pattern:** suffix automaton with end-position occurrence counts  
**Goal:** For each lowercase string, sum `occurrences(substring)^2` over all
distinct nonempty substrings.

## 1. First principles

Every non-root suffix-automaton state represents all substring lengths in

```text
length[link[state]] + 1 .. length[state]
```

All those substrings have the same end-position set and therefore the same
occurrence count. Their entire contribution is the interval length times the
square of that count.

## 2. Cases that decide correctness

- Equal substring text is counted once, regardless of its positions.
- Overlapping occurrences count separately.
- Clone states start with zero terminal occurrences.
- Occurrences propagate from longer states to suffix links.
- The empty substring represented by the root is excluded.

## 3. Brute force: count every substring text

```python
def fake_news_scores_brute(strings: list[str]) -> list[int]:
    if not strings or any(
        not text or any(not "a" <= character <= "z" for character in text)
        for text in strings
    ):
        raise ValueError("strings must be nonempty lowercase text")

    answers: list[int] = []
    for text in strings:
        occurrences: dict[str, int] = {}
        for left in range(len(text)):
            for right in range(left + 1, len(text) + 1):
                substring = text[left:right]
                occurrences[substring] = occurrences.get(substring, 0) + 1
        answers.append(sum(count * count for count in occurrences.values()))
    return answers
```

**Complexity:** `O(n^3)` time with substring materialization and `O(n^2)` space.

## 4. Better transition: group substrings by end-position set

A suffix automaton has only linear many states, and a state groups exactly the
substrings with one end-position set. Mark each newly added prefix endpoint,
then propagate those marks through suffix links in decreasing length order.

## 5. Expert solution: aggregate each automaton state once

```python
def fake_news_scores(strings: list[str]) -> list[int]:
    if not strings or any(
        not text or any(not "a" <= character <= "z" for character in text)
        for text in strings
    ):
        raise ValueError("strings must be nonempty lowercase text")

    answers: list[int] = []
    for text in strings:
        transitions: list[dict[str, int]] = [{}]
        links = [-1]
        lengths = [0]
        occurrences = [0]
        last = 0

        for character in text:
            current = len(transitions)
            transitions.append({})
            links.append(0)
            lengths.append(lengths[last] + 1)
            occurrences.append(1)
            state = last
            while state != -1 and character not in transitions[state]:
                transitions[state][character] = current
                state = links[state]
            if state == -1:
                links[current] = 0
            else:
                target = transitions[state][character]
                if lengths[state] + 1 == lengths[target]:
                    links[current] = target
                else:
                    clone = len(transitions)
                    transitions.append(transitions[target].copy())
                    links.append(links[target])
                    lengths.append(lengths[state] + 1)
                    occurrences.append(0)
                    while state != -1 and transitions[state].get(character) == target:
                        transitions[state][character] = clone
                        state = links[state]
                    links[target] = links[current] = clone
            last = current

        order = sorted(range(1, len(lengths)), key=lengths.__getitem__, reverse=True)
        for state in order:
            occurrences[links[state]] += occurrences[state]
        answers.append(
            sum(
                (lengths[state] - lengths[links[state]])
                * occurrences[state]
                * occurrences[state]
                for state in range(1, len(lengths))
            )
        )
    return answers
```

### Why the expert code is correct

Every distinct nonempty substring belongs to exactly one state and one length
inside that state's suffix-link interval. End-position propagation computes
its exact number of occurrences. Multiplying the squared count by the number
of represented lengths therefore adds each distinct substring's required
contribution exactly once.

**Complexity:** `O(total length)` expected time and space.

## 6. What to remember

```text
distinct substrings -> suffix-automaton states and length intervals
occurrence count -> end positions propagated through suffix links
same end positions -> aggregate the whole interval
```
