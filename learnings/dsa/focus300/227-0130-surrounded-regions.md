# Focus300 227: LeetCode 130 - Surrounded Regions

**Source:** [LeetCode 130](https://leetcode.com/problems/surrounded-regions/)  
**Difficulty:** Medium  
**Pattern:** border flood fill

## Exact contract

Flip every surrounded `O` region to `X` while preserving `O` cells connected to the border.

## First principles

A region survives exactly when it reaches the border. That means the safe cells are the ones found by flooding outward from the border `O`s before any flips happen.


## Classroom board: protect the border first

```text
    X X X X
    X O O X
    X X O X
    X O X X

    flood from border O cells, then flip only the interior O region.
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

- Border-connected `O`s must never be flipped.
- A fully enclosed `O` region should be converted entirely.
- A board with no `O`s is already stable.
- The transformation should distinguish temporary marks from final values.

## Brute force

```python
def solve_brute(board):
    if not board:
        return
    rows = len(board)
    cols = len(board[0])
    safe = set()

    def dfs(r, c):
        if not (0 <= r < rows and 0 <= c < cols) or board[r][c] != "O" or (r, c) in safe:
            return
        safe.add((r, c))
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    for r in range(rows):
        dfs(r, 0)
        dfs(r, cols - 1)
    for c in range(cols):
        dfs(0, c)
        dfs(rows - 1, c)
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == "O" and (r, c) not in safe:
                board[r][c] = "X"
```

Test each region separately to see whether it touches the border.

## Better insight

Flood-fill from the border first, mark safe cells, and flip only the unmarked `O`s.

## Expert solution

```python
def solve(board):
    if not board:
        return
    rows = len(board)
    cols = len(board[0])

    def flood(r, c):
        if not (0 <= r < rows and 0 <= c < cols) or board[r][c] != "O":
            return
        board[r][c] = "S"
        flood(r + 1, c)
        flood(r - 1, c)
        flood(r, c + 1)
        flood(r, c - 1)

    for r in range(rows):
        flood(r, 0)
        flood(r, cols - 1)
    for c in range(cols):
        flood(0, c)
        flood(rows - 1, c)
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == "O":
                board[r][c] = "X"
            elif board[r][c] == "S":
                board[r][c] = "O"
```

Mark border-connected regions, then sweep the board once to convert the remaining `O`s and restore the marked cells.

**Complexity:** O(m*n) time and O(m*n) worst-case recursion or queue space.
