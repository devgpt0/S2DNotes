# Focus300 023: LeetCode 126 - Word Ladder II

**Source:** [LeetCode 126](https://leetcode.com/problems/word-ladder-ii/)  
**Difficulty:** Hard  
**Pattern:** BFS shortest-path DAG plus backtracking

## Exact contract

Return every shortest sequence from `beginWord` to `endWord`. Consecutive words
must differ in exactly one character, and every transformed word must be in
`wordList`. The begin word need not be listed; if the end word is absent,
return an empty list.

## First principles

BFS assigns the minimum distance to each reachable word. When an edge reaches
a word at exactly its known next-layer distance, record the current word as
another predecessor. Edges to later layers are irrelevant to shortest paths.

After BFS first reaches the end layer, finish that layer's predecessor
discoveries, then backtrack through the predecessor DAG to enumerate all and
only shortest sequences.

## Cases that decide correctness

- The end word must occur in the dictionary.
- Multiple parents in the same BFS layer must all be retained.
- A word must not be re-enqueued at a longer distance.
- Begin and end words are included in every returned sequence.
- Sequence order is not significant to the source judge.

## Brute force: build the complete one-letter graph

```python
from collections import defaultdict, deque


def word_ladders_brute(
    begin_word: str, end_word: str, word_list: list[str]
) -> list[list[str]]:
    words = set(word_list)
    if end_word not in words:
        return []
    words.add(begin_word)
    ordered = list(words)
    graph: dict[str, list[str]] = {word: [] for word in ordered}
    for first_index, first in enumerate(ordered):
        for second in ordered[first_index + 1 :]:
            if sum(a != b for a, b in zip(first, second, strict=True)) == 1:
                graph[first].append(second)
                graph[second].append(first)

    distance = {begin_word: 0}
    parents: dict[str, list[str]] = defaultdict(list)
    queue = deque([begin_word])
    while queue:
        word = queue.popleft()
        for neighbor in graph[word]:
            next_distance = distance[word] + 1
            if neighbor not in distance:
                distance[neighbor] = next_distance
                queue.append(neighbor)
            if distance[neighbor] == next_distance:
                parents[neighbor].append(word)

    answers: list[list[str]] = []
    path = [end_word]

    def build(word: str) -> None:
        if word == begin_word:
            answers.append(path[::-1])
            return
        for parent in parents[word]:
            path.append(parent)
            build(parent)
            path.pop()

    if end_word in distance:
        build(end_word)
    return answers
```

Building all word pairs takes `O(N^2 L)` time.

## Better insight: generate only dictionary neighbors

Each word has at most `25L` one-character mutations. Generating them during BFS
avoids materializing the dense all-pairs comparison graph.

## Expert solution: mutation BFS and predecessor DAG

```python
from collections import defaultdict, deque


def find_ladders(
    begin_word: str, end_word: str, word_list: list[str]
) -> list[list[str]]:
    dictionary = set(word_list)
    if end_word not in dictionary:
        return []
    dictionary.add(begin_word)
    distance = {begin_word: 0}
    parents: dict[str, list[str]] = defaultdict(list)
    queue = deque([begin_word])
    end_distance: int | None = None

    while queue:
        word = queue.popleft()
        if end_distance is not None and distance[word] >= end_distance:
            continue
        next_distance = distance[word] + 1
        for index, original in enumerate(word):
            for character in "abcdefghijklmnopqrstuvwxyz":
                if character == original:
                    continue
                neighbor = word[:index] + character + word[index + 1 :]
                if neighbor not in dictionary:
                    continue
                if neighbor not in distance:
                    distance[neighbor] = next_distance
                    queue.append(neighbor)
                if distance[neighbor] == next_distance:
                    parents[neighbor].append(word)
                    if neighbor == end_word:
                        end_distance = next_distance

    if end_word not in distance:
        return []
    answers: list[list[str]] = []
    path = [end_word]

    def build(word: str) -> None:
        if word == begin_word:
            answers.append(path[::-1])
            return
        for parent in parents[word]:
            path.append(parent)
            build(parent)
            path.pop()

    build(end_word)
    return answers
```

Distance labels restrict the recorded graph to shortest-path edges, and every
shortest predecessor is discovered before BFS moves beyond the end layer.

**Complexity:** `O(N L alphabet + output)` time and `O(N+output)` graph space.
