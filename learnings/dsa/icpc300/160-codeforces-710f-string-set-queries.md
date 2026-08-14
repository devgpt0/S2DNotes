# ICPC300 160: Codeforces 710F - String Set Queries

**Source:** [Codeforces 710F - String Set Queries](https://codeforces.com/problemset/problem/710/F)  
**Rating:** 2500  
**Pattern:** logarithmic collection of immutable Aho-Corasick automatons  
**Goal:** Maintain a set of lowercase patterns. Type `1` adds a pattern, type
`2` removes one, and type `3` asks for the total number of overlapping
occurrences of every active pattern in a text.

## 1. First principles

A static Aho-Corasick automaton answers one text against many patterns in one
scan, but inserting into its trie can change failure links throughout the
automaton. Make updates logarithmic by keeping automaton blocks of sizes
`1, 2, 4, ...`, like carries in a binary counter:

```text
insert singleton -> merge equal-sized blocks -> rebuild one larger automaton
query text        -> sum the answer from every occupied block
```

Deletion is handled by a second identical structure. Insert deleted patterns
there and return `added_count - removed_count`.

## 2. Cases that decide correctness

- Occurrences may overlap: pattern `aa` occurs twice in `aaa`.
- A query sums occurrences for every active pattern, not just distinct match
  positions.
- Adding an already active pattern and removing an inactive one are invalid.
- A removed pattern may later be added again.
- Failure-link outputs must include patterns ending at suffix states.

## 3. Brute force: search once per active pattern

```python
def string_set_queries_brute(
    operations: list[tuple[int, str]],
) -> list[int]:
    active: set[str] = set()
    answers: list[int] = []
    for kind, text in operations:
        if kind not in (1, 2, 3):
            raise ValueError("operation kind must be 1, 2, or 3")
        if not text or any(not "a" <= character <= "z" for character in text):
            raise ValueError("strings must contain lowercase English letters")
        if kind == 1:
            if text in active:
                raise ValueError("pattern is already active")
            active.add(text)
        elif kind == 2:
            if text not in active:
                raise ValueError("pattern is not active")
            active.remove(text)
        else:
            total = 0
            for pattern in active:
                start = 0
                while True:
                    position = text.find(pattern, start)
                    if position == -1:
                        break
                    total += 1
                    start = position + 1
            answers.append(total)
    return answers
```

**Complexity:** A query takes `O(|text| * number of active patterns)` in the
worst case; updates take expected `O(1)` set time.

## 4. Better transition: immutable static automatons

Rebuilding one automaton after every modification gives linear text queries
but can repeatedly rebuild the entire set. Power-of-two blocks retain the same
static automaton logic while ensuring each inserted character participates in
only logarithmically many rebuilds.

## 5. Expert solution: binary-counter Aho-Corasick forests

```python
from collections import deque


class _AhoAutomaton:
    def __init__(self, patterns: tuple[str, ...]) -> None:
        self.transitions: list[dict[str, int]] = [{}]
        self.failure = [0]
        self.output = [0]

        for pattern in patterns:
            state = 0
            for character in pattern:
                next_state = self.transitions[state].get(character)
                if next_state is None:
                    next_state = len(self.transitions)
                    self.transitions[state][character] = next_state
                    self.transitions.append({})
                    self.failure.append(0)
                    self.output.append(0)
                state = next_state
            self.output[state] += 1

        queue: deque[int] = deque(self.transitions[0].values())
        while queue:
            state = queue.popleft()
            self.output[state] += self.output[self.failure[state]]
            for character, next_state in self.transitions[state].items():
                fallback = self.failure[state]
                while fallback and character not in self.transitions[fallback]:
                    fallback = self.failure[fallback]
                self.failure[next_state] = self.transitions[fallback].get(character, 0)
                queue.append(next_state)

    def count(self, text: str) -> int:
        state = 0
        total = 0
        for character in text:
            while state and character not in self.transitions[state]:
                state = self.failure[state]
            state = self.transitions[state].get(character, 0)
            total += self.output[state]
        return total


class _AhoForest:
    def __init__(self) -> None:
        self.blocks: list[tuple[tuple[str, ...], _AhoAutomaton] | None] = []

    def insert(self, pattern: str) -> None:
        merged_patterns = (pattern,)
        level = 0
        while level < len(self.blocks) and self.blocks[level] is not None:
            block = self.blocks[level]
            if block is None:
                raise RuntimeError("occupied block disappeared")
            merged_patterns += block[0]
            self.blocks[level] = None
            level += 1
        new_block = (
            merged_patterns,
            _AhoAutomaton(merged_patterns),
        )
        if level == len(self.blocks):
            self.blocks.append(new_block)
        else:
            self.blocks[level] = new_block

    def count(self, text: str) -> int:
        return sum(block[1].count(text) for block in self.blocks if block is not None)


def string_set_queries_aho(
    operations: list[tuple[int, str]],
) -> list[int]:
    active: set[str] = set()
    added = _AhoForest()
    removed = _AhoForest()
    answers: list[int] = []

    for kind, text in operations:
        if kind not in (1, 2, 3):
            raise ValueError("operation kind must be 1, 2, or 3")
        if not text or any(not "a" <= character <= "z" for character in text):
            raise ValueError("strings must contain lowercase English letters")
        if kind == 1:
            if text in active:
                raise ValueError("pattern is already active")
            active.add(text)
            added.insert(text)
        elif kind == 2:
            if text not in active:
                raise ValueError("pattern is not active")
            active.remove(text)
            removed.insert(text)
        else:
            answers.append(added.count(text) - removed.count(text))
    return answers
```

### Why the expert code is correct

Every insertion history appears in exactly one occupied added block, and every
deletion history appears in exactly one removed block. Each block's automaton
counts all overlapping occurrences of its stored patterns, including suffix
matches through accumulated failure outputs. Summing added blocks and
subtracting removed blocks leaves exactly one contribution from each currently
active pattern.

**Complexity:** Amortized `O(L log u)` rebuilding over update strings of total
length `L`; a text query is `O(|text| log u)`, and space is `O(L)`, for `u`
updates.

## 6. What to remember

```text
static many-pattern matching -> Aho-Corasick
dynamic insertion -> power-of-two rebuilt blocks
dynamic deletion -> second additive structure, then subtract
```
