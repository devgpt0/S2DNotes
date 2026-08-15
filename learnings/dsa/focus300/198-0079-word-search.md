# Focus300 198: LeetCode 79 - Word Search

**Source:** [LeetCode 79](https://leetcode.com/problems/word-search/)  
**Difficulty:** Medium  
**Pattern:** grid DFS with backtracking

## Exact contract

Determine whether the target word can be formed by moving orthogonally through adjacent grid cells without reusing a cell in the same path.

## First principles

The search is path-local, so each recursive branch needs its own visited state. A branch succeeds only if every character matches in sequence and the path stays inside the board.

## Cases that decide correctness

- A word longer than the number of cells is impossible.
- A cell may not be reused in the same path.
- Many starting cells may match the first letter.
- Dead branches must unmark visited cells before backtracking.

## Brute force

```python
def word_search_brute(board, word):
    rows = len(board)
    cols = len(board[0]) if rows else 0

    def dfs(r, c, i, seen):
        if i == len(word):
            return True
        if not (0 <= r < rows and 0 <= c < cols):
            return False
        if (r, c) in seen or board[r][c] != word[i]:
            return False
        seen.add((r, c))
        found = (
            dfs(r + 1, c, i + 1, seen)
            or dfs(r - 1, c, i + 1, seen)
            or dfs(r, c + 1, i + 1, seen)
            or dfs(r, c - 1, i + 1, seen)
        )
        seen.remove((r, c))
        return found

    return any(dfs(r, c, 0, set()) for r in range(rows) for c in range(cols))
```

Try every starting cell and every path until a full word is matched.

## Better insight

Prune immediately on character mismatch and stop the search as soon as a full match is found.

## Expert solution

```python
def word_search(board, word):
    rows = len(board)
    cols = len(board[0]) if rows else 0

    def dfs(r, c, i):
        if i == len(word):
            return True
        if not (0 <= r < rows and 0 <= c < cols):
            return False
        if board[r][c] != word[i]:
            return False
        saved = board[r][c]
        board[r][c] = "#"
        found = (
            dfs(r + 1, c, i + 1)
            or dfs(r - 1, c, i + 1)
            or dfs(r, c + 1, i + 1)
            or dfs(r, c - 1, i + 1)
        )
        board[r][c] = saved
        return found

    return any(dfs(r, c, 0) for r in range(rows) for c in range(cols))
```

Run DFS from each candidate start, track visited cells per branch, and undo state on return so the next branch starts clean.

**Complexity:** O(m*n*4^k) worst-case time and O(k) recursion space, where `k` is the word length.
