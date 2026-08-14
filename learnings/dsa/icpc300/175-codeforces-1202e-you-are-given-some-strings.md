# ICPC300 175: Codeforces 1202E - You Are Given Some Strings

**Source:** [Codeforces 1202E - You Are Given Some Strings](https://codeforces.com/problemset/problem/1202/E)  
**Pattern:** two Aho-Corasick scans joined at text boundaries

## Exact contract

Given a lowercase text and a list of nonempty lowercase strings, count triples
`(first, second, start)` for which `patterns[first] + patterns[second]` occurs
in the text at `start`. Pattern indices are distinct choices, so duplicate
pattern strings retain their multiplicity.

## First principles

Every concatenation occurrence has one unique boundary between its two
patterns. At each text boundary, multiply:

- the number of listed patterns ending immediately before it;
- the number of listed patterns starting immediately after it.

An Aho-Corasick scan computes all ending counts together. Scan the reversed
text with reversed patterns to obtain starting counts.

## Cases that decide correctness

- Boundaries exist only between adjacent text characters.
- Overlapping occurrences count independently.
- Duplicate patterns multiply the number of index pairs.
- Failure-link output counts must include suffix patterns.
- No empty pattern is allowed; otherwise a boundary is not unique.

## Brute force: test every ordered pair

```python
def given_strings_brute(text: str, patterns: list[str]) -> int:
    if not text or any(character < "a" or character > "z" for character in text):
        raise ValueError("text must be nonempty and lowercase")
    if not patterns or any(
        not pattern or any(character < "a" or character > "z" for character in pattern)
        for pattern in patterns
    ):
        raise ValueError("patterns must be nonempty lowercase strings")

    answer = 0
    for first in patterns:
        for second in patterns:
            combined = first + second
            answer += sum(
                text.startswith(combined, start)
                for start in range(len(text) - len(combined) + 1)
            )
    return answer
```

This repeats matching for every ordered pattern pair.

## Better approach: KMP once per listed pattern

KMP records how many patterns end at each text position. Repeating the same
work on reversed strings gives start counts without testing all pairs.

```python
def given_strings_kmp(text: str, patterns: list[str]) -> int:
    if not text or any(character < "a" or character > "z" for character in text):
        raise ValueError("text must be nonempty and lowercase")
    if not patterns or any(
        not pattern or any(character < "a" or character > "z" for character in pattern)
        for pattern in patterns
    ):
        raise ValueError("patterns must be nonempty lowercase strings")

    def ending_counts(source: str, words: list[str]) -> list[int]:
        counts = [0] * len(source)
        for word in words:
            prefix = [0] * len(word)
            border = 0
            for index in range(1, len(word)):
                while border and word[index] != word[border]:
                    border = prefix[border - 1]
                if word[index] == word[border]:
                    border += 1
                prefix[index] = border

            matched = 0
            for index, character in enumerate(source):
                while matched and character != word[matched]:
                    matched = prefix[matched - 1]
                if character == word[matched]:
                    matched += 1
                if matched == len(word):
                    counts[index] += 1
                    matched = prefix[matched - 1]
        return counts

    endings = ending_counts(text, patterns)
    reversed_endings = ending_counts(
        text[::-1], [pattern[::-1] for pattern in patterns]
    )
    starts = reversed_endings[::-1]
    return sum(
        endings[boundary] * starts[boundary + 1] for boundary in range(len(text) - 1)
    )
```

The time is `O(|text| * n + total_pattern_length)` and the space is linear in
the text and longest pattern.

## Expert solution: two Aho-Corasick scans

```python
from collections import deque


def count_given_string_pairs(text: str, patterns: list[str]) -> int:
    if not text or any(character < "a" or character > "z" for character in text):
        raise ValueError("text must be nonempty and lowercase")
    if not patterns or any(
        not pattern or any(character < "a" or character > "z" for character in pattern)
        for pattern in patterns
    ):
        raise ValueError("patterns must be nonempty lowercase strings")

    def ending_counts(source: str, words: list[str]) -> list[int]:
        transitions = [[0] * 26]
        terminal_count = [0]
        for word in words:
            state = 0
            for character in word:
                letter = ord(character) - ord("a")
                child = transitions[state][letter]
                if child == 0:
                    child = len(transitions)
                    transitions[state][letter] = child
                    transitions.append([0] * 26)
                    terminal_count.append(0)
                state = child
            terminal_count[state] += 1

        failure = [0] * len(transitions)
        queue: deque[int] = deque()
        for child in transitions[0]:
            if child:
                queue.append(child)

        while queue:
            state = queue.popleft()
            terminal_count[state] += terminal_count[failure[state]]
            for letter in range(26):
                child = transitions[state][letter]
                if child:
                    failure[child] = transitions[failure[state]][letter]
                    queue.append(child)
                else:
                    transitions[state][letter] = transitions[failure[state]][letter]

        counts = [0] * len(source)
        state = 0
        for index, character in enumerate(source):
            state = transitions[state][ord(character) - ord("a")]
            counts[index] = terminal_count[state]
        return counts

    endings = ending_counts(text, patterns)
    reversed_endings = ending_counts(
        text[::-1], [pattern[::-1] for pattern in patterns]
    )
    starts = reversed_endings[::-1]
    return sum(endings[index] * starts[index + 1] for index in range(len(text) - 1))
```

Each automaton state stores the multiplicity of patterns ending at that state
or along its failure chain. Therefore each product at a boundary counts exactly
all ordered pattern-index pairs whose concatenation occurs there.

**Complexity:** `O(total_pattern_length + 26S + |text|)` time and `O(26S + |text|)`
space, where `S` is the number of trie states.
