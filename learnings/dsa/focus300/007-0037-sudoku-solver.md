# Focus300 007: LeetCode 37 - Sudoku Solver

**Source:** [LeetCode 37](https://leetcode.com/problems/sudoku-solver/)  
**Difficulty:** Hard  
**Pattern:** constraint propagation with minimum-remaining-values backtracking

## Exact contract

Mutate a valid partially filled `9 x 9` Sudoku board so every row, column, and
`3 x 3` box contains digits `1` through `9` exactly once. Empty cells contain
`.`. The source guarantees one solution.

## First principles

Backtracking is complete because every blank tries every digit consistent with
the three relevant constraints. Bit masks make candidate calculation a few
integer operations. Choosing the blank with the fewest candidates first is the
minimum-remaining-values heuristic: it exposes contradictions early and
shrinks the search tree without removing any legal solution.


## Classroom board: see the repeated work once

```text
brute force tries every choice.
the optimized solution keeps only the state that must survive to the
next step.
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

- Given digits are immutable.
- A candidate must be absent from its row, column, and box simultaneously.
- Every placement must be undone on a failed branch.
- A zero-candidate blank rejects the branch immediately.
- Mutation is the output; the function returns `None`.

## Brute force: scan constraints for the first blank

```python
def solve_sudoku_brute(board: list[list[str]]) -> None:
    digits = "123456789"

    def valid(row: int, column: int, digit: str) -> bool:
        if digit in board[row]:
            return False
        if any(board[index][column] == digit for index in range(9)):
            return False
        box_row = row // 3 * 3
        box_column = column // 3 * 3
        return all(
            board[current_row][current_column] != digit
            for current_row in range(box_row, box_row + 3)
            for current_column in range(box_column, box_column + 3)
        )

    def search() -> bool:
        for row in range(9):
            for column in range(9):
                if board[row][column] != ".":
                    continue
                for digit in digits:
                    if valid(row, column, digit):
                        board[row][column] = digit
                        if search():
                            return True
                        board[row][column] = "."
                return False
        return True

    if not search():
        raise ValueError("board has no solution")
```

This repeatedly scans rows, columns, and boxes and may explore an exponential
search tree.

## Better approach: bit masks with a fixed blank order

```python
def solve_sudoku_masks(board: list[list[str]]) -> None:
    full_mask = (1 << 9) - 1
    row_mask = [0] * 9
    column_mask = [0] * 9
    box_mask = [0] * 9
    blanks: list[tuple[int, int]] = []
    for row in range(9):
        for column in range(9):
            character = board[row][column]
            if character == ".":
                blanks.append((row, column))
                continue
            bit = 1 << (int(character) - 1)
            box = row // 3 * 3 + column // 3
            if row_mask[row] & bit or column_mask[column] & bit or box_mask[box] & bit:
                raise ValueError("board violates Sudoku constraints")
            row_mask[row] |= bit
            column_mask[column] |= bit
            box_mask[box] |= bit

    def search(index: int) -> bool:
        if index == len(blanks):
            return True
        row, column = blanks[index]
        box = row // 3 * 3 + column // 3
        candidates = full_mask & ~(row_mask[row] | column_mask[column] | box_mask[box])
        while candidates:
            bit = candidates & -candidates
            candidates -= bit
            board[row][column] = str(bit.bit_length())
            row_mask[row] |= bit
            column_mask[column] |= bit
            box_mask[box] |= bit
            if search(index + 1):
                return True
            row_mask[row] ^= bit
            column_mask[column] ^= bit
            box_mask[box] ^= bit
        board[row][column] = "."
        return False

    if not search(0):
        raise ValueError("board has no solution")
```

Masks reduce candidate checks to `O(1)`, while fixed ordering can still choose
a highly ambiguous blank too early.

## Expert solution: bit masks plus minimum remaining values

```python
def solve_sudoku(board: list[list[str]]) -> None:
    full_mask = (1 << 9) - 1
    row_mask = [0] * 9
    column_mask = [0] * 9
    box_mask = [0] * 9
    blanks: list[tuple[int, int]] = []
    for row in range(9):
        for column in range(9):
            character = board[row][column]
            if character == ".":
                blanks.append((row, column))
                continue
            bit = 1 << (int(character) - 1)
            box = row // 3 * 3 + column // 3
            if row_mask[row] & bit or column_mask[column] & bit or box_mask[box] & bit:
                raise ValueError("board violates Sudoku constraints")
            row_mask[row] |= bit
            column_mask[column] |= bit
            box_mask[box] |= bit

    def candidate_mask(row: int, column: int) -> int:
        box = row // 3 * 3 + column // 3
        return full_mask & ~(row_mask[row] | column_mask[column] | box_mask[box])

    def search(index: int) -> bool:
        if index == len(blanks):
            return True
        best_index = index
        best_count = 10
        for candidate_index in range(index, len(blanks)):
            row, column = blanks[candidate_index]
            count = candidate_mask(row, column).bit_count()
            if count < best_count:
                best_count = count
                best_index = candidate_index
                if count <= 1:
                    break
        if best_count == 0:
            return False

        blanks[index], blanks[best_index] = blanks[best_index], blanks[index]
        row, column = blanks[index]
        box = row // 3 * 3 + column // 3
        candidates = candidate_mask(row, column)
        while candidates:
            bit = candidates & -candidates
            candidates -= bit
            board[row][column] = str(bit.bit_length())
            row_mask[row] |= bit
            column_mask[column] |= bit
            box_mask[box] |= bit
            if search(index + 1):
                return True
            row_mask[row] ^= bit
            column_mask[column] ^= bit
            box_mask[box] ^= bit
        board[row][column] = "."
        blanks[index], blanks[best_index] = blanks[best_index], blanks[index]
        return False

    if not search(0):
        raise ValueError("board has no solution")
```

MRV changes only branch order, so completeness is preserved while typical
search falls dramatically.

**Complexity:** exponential worst-case time, `O(81)` masks, blanks, and stack.
