# Focus300 117: LeetCode 782 - Transform to Chessboard

**Source:** [LeetCode 782](https://leetcode.com/problems/transform-to-chessboard/)  
**Difficulty:** Hard  
**Pattern:** binary row/column invariants and mismatch counting

## Exact contract

Given an `n x n` binary board with `2 <= n <= 30`, one move swaps any two
entire rows or any two entire columns. Return the minimum moves needed to make
both horizontally and vertically adjacent cells different, or `-1` when no
such chessboard is reachable.

## First principles

Row and column swaps cannot change the XOR parity of any four rectangle
corners. A reachable board therefore has
`board[0][0] ^ board[r][0] ^ board[0][c] ^ board[r][c] == 0` everywhere. Once
that holds, every row is the first row or its complement, and the remaining
work is independently arranging the first column and first row to alternate.


## Classroom board: see the repeated work once

```text
brute force tries every choice.
the optimized solution keeps only the state that must survive to the
next step.
```



## Step-by-step transformation

1. Compress the input into counts, prefixes, bit masks, or another compact state.
2. Update that state once per element instead of recomputing earlier work.
3. Combine the stored pieces to recover the value the problem asks for.
4. Return the final count, sum, or constructed answer.

These notes transform input into output by reducing the data to a compact invariant first, then rebuilding the answer from that invariant.


## Diagram: compress the input first

```text

            raw values
                |
                v
            counts / prefix / bit state
                |
                v
            combine stored facts
                |
                v
            final answer
```

The algorithm first compresses the input into a small invariant, then rebuilds the answer from that compact state.

## Cases that decide correctness

- For even `n`, each binary pattern must contain exactly `n / 2` ones.
- For odd `n`, the two counts may differ by one and only one alternating
  orientation has the majority bit.
- A row swap changes the first-column pattern; a column swap changes the
  first-row pattern.
- Each swap fixes two mismatched positions, so mismatch totals are halved.
- A board can have balanced counts yet still violate the rectangle invariant.

## Brute force: breadth-first search over row and column permutations

```python
from collections import deque


def chessboard_swaps_brute(board: list[list[int]]) -> int:
    if (
        type(board) is not list
        or not 2 <= len(board) <= 30
        or any(type(row) is not list or len(row) != len(board) for row in board)
    ):
        raise TypeError("board must be a square list with side between 2 and 30")
    if any(
        type(value) is not int or value not in (0, 1) for row in board for value in row
    ):
        raise ValueError("board values must be integer zeroes and ones")

    side = len(board)
    start = tuple(tuple(row) for row in board)

    def is_chessboard(state: tuple[tuple[int, ...], ...]) -> bool:
        return all(
            state[row][column] != state[row + 1][column]
            for row in range(side - 1)
            for column in range(side)
        ) and all(
            state[row][column] != state[row][column + 1]
            for row in range(side)
            for column in range(side - 1)
        )

    queue = deque([(start, 0)])
    seen = {start}
    while queue:
        state, moves = queue.popleft()
        if is_chessboard(state):
            return moves
        for first in range(side):
            for second in range(first + 1, side):
                rows = list(state)
                rows[first], rows[second] = rows[second], rows[first]
                row_state = tuple(rows)
                if row_state not in seen:
                    seen.add(row_state)
                    queue.append((row_state, moves + 1))

                columns = [list(row) for row in state]
                for row in columns:
                    row[first], row[second] = row[second], row[first]
                column_state = tuple(tuple(row) for row in columns)
                if column_state not in seen:
                    seen.add(column_state)
                    queue.append((column_state, moves + 1))
    return -1
```

The state space can contain up to `(n!)^2` row/column arrangements.

## Better approach: match one of two alternating templates

After feasibility checks, compare the first row and column with both possible
alternating bit strings. Even sizes choose the lower mismatch count; odd sizes
must choose the orientation whose bit counts match. The expert formula performs
those comparisons without constructing either template.

## Expert solution: validate rectangles, then count swaps

```python
def chessboard_swaps(board: list[list[int]]) -> int:
    if (
        type(board) is not list
        or not 2 <= len(board) <= 30
        or any(type(row) is not list or len(row) != len(board) for row in board)
    ):
        raise TypeError("board must be a square list with side between 2 and 30")
    if any(
        type(value) is not int or value not in (0, 1) for row in board for value in row
    ):
        raise ValueError("board values must be integer zeroes and ones")

    side = len(board)
    for row in range(side):
        for column in range(side):
            if board[0][0] ^ board[row][0] ^ board[0][column] ^ board[row][column]:
                return -1

    first_row_ones = sum(board[0])
    first_column_ones = sum(board[row][0] for row in range(side))
    if not side // 2 <= first_row_ones <= (side + 1) // 2:
        return -1
    if not side // 2 <= first_column_ones <= (side + 1) // 2:
        return -1

    row_mismatches = sum(board[row][0] == row % 2 for row in range(side))
    column_mismatches = sum(board[0][column] == column % 2 for column in range(side))
    if side % 2:
        if row_mismatches % 2:
            row_mismatches = side - row_mismatches
        if column_mismatches % 2:
            column_mismatches = side - column_mismatches
    else:
        row_mismatches = min(row_mismatches, side - row_mismatches)
        column_mismatches = min(column_mismatches, side - column_mismatches)
    return (row_mismatches + column_mismatches) // 2
```

The XOR test is necessary and sufficient for complementary row/column
patterns. The count constraints select valid alternating orientations, and
each row or column swap resolves exactly two selected mismatches.

**Complexity:** `O(n^2)` time and `O(1)` auxiliary space.
