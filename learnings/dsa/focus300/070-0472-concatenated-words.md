# Focus300 070: LeetCode 472 - Concatenated Words

**Source:** [LeetCode 472](https://leetcode.com/problems/concatenated-words/)  
**Difficulty:** Hard  
**Pattern:** incremental word-break DP by word length

## Exact contract

Return every word that can be formed by concatenating at least two shorter
words from the same unique input list. A component word may be reused. Output
order is irrelevant.

## First principles

Process words from shortest to longest. When testing a word, every valid
component is strictly shorter and has already been inserted. A prefix DP stores
the maximum number of dictionary pieces reaching each index. The word is
concatenated exactly when its final index is reachable with at least two pieces.

A trie shares prefix checks and avoids allocating every substring candidate.

## Cases that decide correctness

- At least two component words are required.
- The whole word must not validate itself as one component.
- Component words may repeat.
- Empty strings are not useful components.
- Several words may have the same length; none can be a proper component of another.

## Brute force: recursively try every split while excluding the word itself

```python
def concatenated_words_brute(words: list[str]) -> list[str]:
    dictionary = set(words)
    answers: list[str] = []

    def piece_count(word: str, start: int, pieces: int) -> bool:
        if start == len(word):
            return pieces >= 2
        for end in range(start + 1, len(word) + 1):
            if word[start:end] in dictionary and piece_count(word, end, pieces + 1):
                return True
        return False

    for word in words:
        dictionary.remove(word)
        if word and piece_count(word, 0, 0):
            answers.append(word)
        dictionary.add(word)
    return answers
```

Repeated suffix searches make this exponential.

## Better approach: length order plus hash-set word-break DP

```python
def concatenated_words_dp(words: list[str]) -> list[str]:
    known: set[str] = set()
    answers: list[str] = []
    for word in sorted(words, key=len):
        pieces = [-1] * (len(word) + 1)
        pieces[0] = 0
        for end in range(1, len(word) + 1):
            for start in range(end):
                if pieces[start] >= 0 and word[start:end] in known:
                    pieces[end] = max(pieces[end], pieces[start] + 1)
        if pieces[-1] >= 2:
            answers.append(word)
        if word:
            known.add(word)
    return answers
```

This is polynomial but creates `O(length^2)` slices per word.

## Expert solution: incremental trie with piece-count DP

```python
class TrieNode:
    def __init__(self) -> None:
        self.children: dict[str, TrieNode] = {}
        self.terminal = False


def find_all_concatenated_words(words: list[str]) -> list[str]:
    root = TrieNode()
    answers: list[str] = []

    def insert(word: str) -> None:
        node = root
        for character in word:
            node = node.children.setdefault(character, TrieNode())
        node.terminal = True

    def count_pieces(word: str) -> int:
        pieces = [-1] * (len(word) + 1)
        pieces[0] = 0
        for start in range(len(word)):
            if pieces[start] < 0:
                continue
            node = root
            for end in range(start, len(word)):
                node = node.children.get(word[end])
                if node is None:
                    break
                if node.terminal:
                    pieces[end + 1] = max(pieces[end + 1], pieces[start] + 1)
        return pieces[-1]

    for word in sorted(words, key=len):
        if word and count_pieces(word) >= 2:
            answers.append(word)
        if word:
            insert(word)
    return answers
```

Length ordering excludes self-use, while trie traversal visits only prefixes
that exist in the known shorter-word dictionary.

**Complexity:** `O(total candidate prefix traversal + output)` time and
`O(total input characters)` trie space.
