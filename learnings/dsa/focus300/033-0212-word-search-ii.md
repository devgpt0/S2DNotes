# Focus300 033: LeetCode 212 - Word Search II

**Source:** [LeetCode 212 - Word Search II](https://leetcode.com/problems/word-search-ii/)  
**Difficulty:** Hard  
**Pattern:** trie-guided board backtracking  

## Exact contract

Return all dictionary words that can be formed in a rectangular character
board by moving horizontally or vertically. A board cell may be used at most
once within one word. The functions return unique matches in sorted order.

## First principles

A single-word DFS rejects a path as soon as its next character differs. With
many words, a trie shares those prefix checks: one board traversal advances all
dictionary words having the current prefix.

## Cases that decide correctness

- A cell may be reused by different searches, never twice on one path.
- Prefix words and longer words can both match.
- Duplicate input words produce one output word.
- Four-directional adjacency excludes diagonals.
- A word longer than the cell count cannot match.

## Brute force: run a complete DFS for every word

```python
def board_words_brute(board: list[list[str]], words: list[str]) -> list[str]:
    if (
        not board
        or not board[0]
        or any(len(row) != len(board[0]) for row in board)
        or any(
            not isinstance(character, str) or len(character) != 1
            for row in board
            for character in row
        )
        or any(not isinstance(word, str) or not word for word in words)
    ):
        raise ValueError("invalid board or words")
    row_count = len(board)
    column_count = len(board[0])

    def exists(word: str) -> bool:
        visited: set[tuple[int, int]] = set()

        def search(row: int, column: int, offset: int) -> bool:
            if board[row][column] != word[offset]:
                return False
            if offset == len(word) - 1:
                return True
            visited.add((row, column))
            for row_change, column_change in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                next_row = row + row_change
                next_column = column + column_change
                if (
                    0 <= next_row < row_count
                    and 0 <= next_column < column_count
                    and (next_row, next_column) not in visited
                    and search(next_row, next_column, offset + 1)
                ):
                    visited.remove((row, column))
                    return True
            visited.remove((row, column))
            return False

        return any(
            search(row, column, 0)
            for row in range(row_count)
            for column in range(column_count)
        )

    return sorted({word for word in words if exists(word)})
```

**Complexity:** `O(w r c 4^L)` time in the worst case and `O(L)` path space.

## Better approach: prefix-set pruning

Store every dictionary prefix in a hash set and run one DFS from every cell.
This shares traversal but repeatedly materializes prefix strings. A trie stores
the same prefix relation directly.

## Expert solution: trie search with exhausted-branch pruning

```python
from dataclasses import dataclass, field


@dataclass
class TrieNode:
    children: dict[str, "TrieNode"] = field(default_factory=dict)
    word: str | None = None


def board_words(board: list[list[str]], words: list[str]) -> list[str]:
    if (
        not board
        or not board[0]
        or any(len(row) != len(board[0]) for row in board)
        or any(
            not isinstance(character, str) or len(character) != 1
            for row in board
            for character in row
        )
        or any(not isinstance(word, str) or not word for word in words)
    ):
        raise ValueError("invalid board or words")

    root = TrieNode()
    for word in set(words):
        node = root
        for character in word:
            node = node.children.setdefault(character, TrieNode())
        node.word = word

    row_count = len(board)
    column_count = len(board[0])
    visited: set[tuple[int, int]] = set()
    found: list[str] = []

    def search(row: int, column: int, parent: TrieNode) -> None:
        character = board[row][column]
        node = parent.children.get(character)
        if node is None:
            return
        if node.word is not None:
            found.append(node.word)
            node.word = None

        visited.add((row, column))
        for row_change, column_change in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            next_row = row + row_change
            next_column = column + column_change
            if (
                0 <= next_row < row_count
                and 0 <= next_column < column_count
                and (next_row, next_column) not in visited
            ):
                search(next_row, next_column, node)
        visited.remove((row, column))

        if node.word is None and not node.children:
            del parent.children[character]

    for row in range(row_count):
        for column in range(column_count):
            search(row, column, root)
    return sorted(found)
```

The trie admits exactly dictionary prefixes. Clearing a found terminal prevents
duplicates; deleting an exhausted branch removes only prefixes that cannot
produce another answer.

**Complexity:** `O(total word characters + r c 4^L)` worst-case time and
`O(total word characters + L)` space.

