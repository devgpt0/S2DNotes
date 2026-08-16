# Focus300 024: LeetCode 127 - Word Ladder

**Source:** [LeetCode 127](https://leetcode.com/problems/word-ladder/)  
**Difficulty:** Hard  
**Pattern:** bidirectional BFS on an implicit mutation graph

## Exact contract

Return the number of words in the shortest transformation sequence from
`beginWord` to `endWord`. Each step changes exactly one character and each
transformed word must occur in `wordList`. Return zero when no sequence exists.

## First principles

Words are unweighted graph vertices, so BFS finds the shortest number of edges.
The required answer counts vertices and is therefore `edge_distance+1`.

Bidirectional BFS starts from both endpoints and always expands the smaller
frontier. When a generated neighbor belongs to the opposite frontier, the two
shortest partial paths meet.


## Classroom board: grow one frontier at a time

```text
    hit -> hot -> dot -> dog -> cog

    BFS sees the shortest transformation count first.
```



## Step-by-step transformation

1. Choose a start state such as a cell, node, or partial path.
2. Mark the state as visited or temporarily commit the choice.
3. Expand to valid neighbors or next choices while the invariant still holds.
4. Undo the temporary choice when the branch finishes, then return the collected answer.

These problems transform the input into output by exploring one branch at a time and backtracking whenever a branch can no longer produce a valid solution.


## Diagram: search and undo

```text

            start state
                |
                v
            choose one path
                |
                v
            explore neighbors
                |
                v
            undo and try next path
                |
                v
            answer
```

These notes use search, visit markers, and backtracking to turn one starting state into the final valid path or count.

## Cases that decide correctness

- The end word must be present in the dictionary.
- The begin word need not be present.
- A word removed from the unused set must not be re-enqueued.
- The returned length includes both endpoint words.
- All words have the same length by source contract.

## Brute force: build the complete graph and BFS

```python
from collections import deque


def ladder_length_brute(begin_word: str, end_word: str, word_list: list[str]) -> int:
    words = set(word_list)
    if end_word not in words:
        return 0
    words.add(begin_word)
    ordered = list(words)
    graph: dict[str, list[str]] = {word: [] for word in ordered}
    for first_index, first in enumerate(ordered):
        for second in ordered[first_index + 1 :]:
            if sum(a != b for a, b in zip(first, second, strict=True)) == 1:
                graph[first].append(second)
                graph[second].append(first)

    queue = deque([(begin_word, 1)])
    visited = {begin_word}
    while queue:
        word, length = queue.popleft()
        if word == end_word:
            return length
        for neighbor in graph[word]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, length + 1))
    return 0
```

The graph construction costs `O(N^2 L)` time.

## Better approach: one-direction mutation BFS

```python
from collections import deque


def ladder_length_bfs(begin_word: str, end_word: str, word_list: list[str]) -> int:
    unused = set(word_list)
    if end_word not in unused:
        return 0
    queue = deque([(begin_word, 1)])
    unused.discard(begin_word)
    while queue:
        word, length = queue.popleft()
        if word == end_word:
            return length
        for index, original in enumerate(word):
            for character in "abcdefghijklmnopqrstuvwxyz":
                if character == original:
                    continue
                neighbor = word[:index] + character + word[index + 1 :]
                if neighbor in unused:
                    unused.remove(neighbor)
                    queue.append((neighbor, length + 1))
    return 0
```

This avoids all-pairs graph construction but may explore almost every word from
one side.

## Expert solution: expand the smaller of two BFS frontiers

```python
def ladder_length(begin_word: str, end_word: str, word_list: list[str]) -> int:
    unused = set(word_list)
    if end_word not in unused:
        return 0
    if begin_word == end_word:
        return 1
    front = {begin_word}
    back = {end_word}
    unused.discard(begin_word)
    unused.discard(end_word)
    length = 1

    while front and back:
        if len(front) > len(back):
            front, back = back, front
        next_front: set[str] = set()
        for word in front:
            for index, original in enumerate(word):
                for character in "abcdefghijklmnopqrstuvwxyz":
                    if character == original:
                        continue
                    neighbor = word[:index] + character + word[index + 1 :]
                    if neighbor in back:
                        return length + 1
                    if neighbor in unused:
                        unused.remove(neighbor)
                        next_front.add(neighbor)
        front = next_front
        length += 1
    return 0
```

Both searches are level-synchronous; their first intersection gives the global
shortest path while smaller-frontier expansion reduces branching.

**Complexity:** `O(N L alphabet)` time and `O(N)` space.
