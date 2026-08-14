# Focus300 170: LeetCode 36 - Valid Sudoku

**Source:** [LeetCode 36](https://leetcode.com/problems/valid-sudoku/)  
**Difficulty:** Medium  
**Pattern:** simultaneous row, column, and box constraints

## Exact contract

Validate only the filled cells of a `9 x 9` Sudoku board. Each digit `1..9`
must appear at most once in its row, column, and `3 x 3` box; `.` denotes an
empty cell. The board need not be solvable or complete.

## First principles

Each filled cell participates in exactly three independent units. While scanning
once, map its digit to one bit and its box to `(row//3)*3 + column//3`. Seeing
that bit already set in any of the three masks proves a duplicate; otherwise set
it in all three.

## Cases that decide correctness

- Empty cells impose no constraint.
- The same digit may occur in different rows, columns, and boxes.
- A board can satisfy local uniqueness but still be unsolvable; it is valid here.
- Box membership depends on both row and column integer division by three.
- Every cell must be one character from `.` or `1..9`.

## Brute force: rescan all three peer groups for each digit

```python
def valid_sudoku_brute(board: list[list[str]]) -> bool:
    if (
        type(board) is not list
        or len(board) != 9
        or any(type(row) is not list or len(row) != 9 for row in board)
    ):
        raise ValueError("board must be a 9 x 9 list matrix")
    if any(
        type(cell) is not str or len(cell) != 1 or cell not in ".123456789"
        for row in board
        for cell in row
    ):
        raise ValueError("each cell must be '.' or one digit from 1 through 9")

    for row in range(9):
        for column in range(9):
            digit = board[row][column]
            if digit == ".":
                continue
            if any(
                other_column != column and board[row][other_column] == digit
                for other_column in range(9)
            ):
                return False
            if any(
                other_row != row and board[other_row][column] == digit
                for other_row in range(9)
            ):
                return False
            box_row = row // 3 * 3
            box_column = column // 3 * 3
            for other_row in range(box_row, box_row + 3):
                for other_column in range(box_column, box_column + 3):
                    if (other_row, other_column) != (row, column) and board[other_row][
                        other_column
                    ] == digit:
                        return False
    return True
```

This repeatedly scans peers instead of sharing information across cells.

## Better insight: a seen-set check is identical for every constraint unit

Nine bits represent the used digits for one row, column, or box. A single board
scan can update all 27 masks.

## Expert solution: row, column, and box bitmasks

```python
def valid_sudoku(board: list[list[str]]) -> bool:
    if (
        type(board) is not list
        or len(board) != 9
        or any(type(row) is not list or len(row) != 9 for row in board)
    ):
        raise ValueError("board must be a 9 x 9 list matrix")
    if any(
        type(cell) is not str or len(cell) != 1 or cell not in ".123456789"
        for row in board
        for cell in row
    ):
        raise ValueError("each cell must be '.' or one digit from 1 through 9")

    row_masks = [0] * 9
    column_masks = [0] * 9
    box_masks = [0] * 9
    for row in range(9):
        for column in range(9):
            digit = board[row][column]
            if digit == ".":
                continue
            bit = 1 << (ord(digit) - ord("1"))
            box = row // 3 * 3 + column // 3
            if (
                row_masks[row] & bit
                or column_masks[column] & bit
                or box_masks[box] & bit
            ):
                return False
            row_masks[row] |= bit
            column_masks[column] |= bit
            box_masks[box] |= bit
    return True
```

Each mask contains exactly the digits seen earlier in its unit, so a repeated
bit is equivalent to violating the Sudoku rule.

**Complexity:** `O(81)` time and `O(27)` integer-mask space, both constant.
