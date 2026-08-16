# Focus300 293: LeetCode 289 - Game of Life

**Source:** [LeetCode 289](https://leetcode.com/problems/game-of-life/)  
**Difficulty:** Medium  
**Pattern:** in-place state transition encoding

## Exact contract

Advance the board by one Game of Life step using the neighbor-count rules.

## First principles

Each cell's next state depends only on its current state and the count of live neighbors. Encoding the transition in extra bits or sentinel values lets the board be updated in place.


## Classroom board: see the repeated work once

```text
brute force tries every choice.
the optimized solution keeps only the state that must survive to the
next step.
```



## Step-by-step transformation

1. Read the input and identify the smallest state that still determines the answer.
2. Process one element, node, or row at a time while preserving that state.
3. Discard work that can no longer change the result.
4. Convert the surviving state into the output the problem requests.

The examples and code below show this transformation on the specific problem instance.


## Diagram: input to output

```text

        input
            |
            v
        core invariant
            |
            v
        process one step at a time
            |
            v
        output
```

The note shows the main idea, the repeated work, and the small state that turns the input into the output.

## Cases that decide correctness

- Cells at the border have fewer neighbors.
- A live cell with too few or too many neighbors dies.
- A dead cell with exactly three live neighbors becomes alive.
- The update must not interfere with neighbor counts in the same round.

## Brute force

```python
def game_of_life_brute(board):
    rows = len(board)
    cols = len(board[0]) if rows else 0
    copy = [row[:] for row in board]
    for r in range(rows):
        for c in range(cols):
            live = 0
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr == dc == 0:
                        continue
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols:
                        live += copy[nr][nc]
            if copy[r][c] == 1 and live not in (2, 3):
                board[r][c] = 0
            if copy[r][c] == 0 and live == 3:
                board[r][c] = 1
```

Copy the board and compute the next generation from the copy.

## Better insight

Store both the old and new state in the same cell while scanning.

## Expert solution

```python
def game_of_life(board):
    rows = len(board)
    cols = len(board[0]) if rows else 0
    for r in range(rows):
        for c in range(cols):
            live = 0
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr == dc == 0:
                        continue
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols:
                        live += board[nr][nc] & 1
            if board[r][c] == 1 and live in (2, 3):
                board[r][c] = 3
            if board[r][c] == 0 and live == 3:
                board[r][c] = 2
    for r in range(rows):
        for c in range(cols):
            board[r][c] >>= 1
```

Count neighbors from the old-state bit and write the next-state bit separately, then finalize the board with a second pass.

**Complexity:** O(m*n) time and O(1) extra space.
