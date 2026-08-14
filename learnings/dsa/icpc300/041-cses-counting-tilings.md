# ICPC300 041: CSES - Counting Tilings

**Source:** [CSES - Counting Tilings](https://cses.fi/problemset/task/2181/)  
**Pattern:** column-profile dynamic programming  
**Goal:** Count, modulo `1_000_000_007`, the ways to cover an `n x m` board
exactly with `1 x 2` and `2 x 1` dominoes.

## 1. Problem in plain words

Every cell must belong to one domino, and dominoes may not overlap or leave the
board. Rotating a domino creates the second allowed orientation.

A `2 x 2` board has two tilings: two horizontal dominoes or two vertical
dominoes. A board with an odd number of cells has none.

## 2. First principles

Process the board one column at a time. A horizontal domino started in the
previous column may already occupy cells in the current column. A bitmask of
`n` bits records exactly those occupied rows.

For one current mask, fill every remaining cell in the column:

- place a vertical domino in this column when the next row is also free;
- place a horizontal domino and set its row in the next column's mask.

After the last column, only mask `0` is legal: no domino may extend beyond the
board.

## 3. Cases that decide correctness

| Case | Required result |
| --- | --- |
| Odd board area | `0`. |
| `1 x m` | `1` when `m` is even, otherwise `0`. |
| Current row already occupied | Skip it; do not place another domino. |
| Horizontal domino in final column | Rejected because the final mask is nonzero. |
| Many tilings | Reduce additions modulo `1_000_000_007`. |

## 4. Brute force: fill the first empty cell

For a tiny board, choose the first uncovered cell and try both orientations.
This creates each tiling once because every recursive step fixes that cell.

```python
MODULO = 1_000_000_007


def count_tilings_brute_force(height: int, width: int) -> int:
    if height < 1 or width < 1:
        raise ValueError("board dimensions must be positive")
    if height * width % 2 == 1:
        return 0

    occupied = [False] * (height * width)

    def search() -> int:
        try:
            cell = occupied.index(False)
        except ValueError:
            return 1

        row, column = divmod(cell, width)
        total = 0

        if column + 1 < width and not occupied[cell + 1]:
            occupied[cell] = True
            occupied[cell + 1] = True
            total += search()
            occupied[cell] = False
            occupied[cell + 1] = False

        if row + 1 < height and not occupied[cell + width]:
            occupied[cell] = True
            occupied[cell + width] = True
            total += search()
            occupied[cell] = False
            occupied[cell + width] = False

        return total % MODULO

    return search()
```

**Complexity:** exponential in the number of cells, with `O(nm)` state space
for the occupancy array and recursion stack.

## 5. Better: generate transitions while processing each column

The mask contains only `n` boundary cells instead of the entire board. The
recursive function below completes one column and immediately contributes to
the next column's DP.

```python
MODULO = 1_000_000_007


def count_tilings_profile(height: int, width: int) -> int:
    if height < 1 or width < 1:
        raise ValueError("board dimensions must be positive")
    if height * width % 2 == 1:
        return 0

    state_count = 1 << height
    dp = [0] * state_count
    dp[0] = 1

    for _ in range(width):
        next_dp = [0] * state_count
        for current_mask, ways in enumerate(dp):
            if ways == 0:
                continue

            def fill(row: int, next_mask: int) -> None:
                while row < height and current_mask & (1 << row):
                    row += 1
                if row == height:
                    next_dp[next_mask] = (next_dp[next_mask] + ways) % MODULO
                    return

                fill(row + 1, next_mask | (1 << row))
                if row + 1 < height and not current_mask & (1 << (row + 1)):
                    fill(row + 2, next_mask)

            fill(0, 0)
        dp = next_dp

    return dp[0]
```

**Complexity:** `O(m * 2^n * T)` time, where `T` is the work to enumerate one
mask's fillings, and `O(2^n)` DP memory.

## 6. Expert solution: precompute every mask transition

The legal completions of a mask depend only on `height`, not on the column.
Precompute them once, then each column is a sparse transition pass.

```python
MODULO = 1_000_000_007


def count_tilings(height: int, width: int) -> int:
    if height < 1 or width < 1:
        raise ValueError("board dimensions must be positive")
    if height * width % 2 == 1:
        return 0

    if height > width:
        height, width = width, height

    state_count = 1 << height
    transitions: list[list[int]] = [[] for _ in range(state_count)]

    for current_mask in range(state_count):

        def generate(row: int, next_mask: int) -> None:
            while row < height and current_mask & (1 << row):
                row += 1
            if row == height:
                transitions[current_mask].append(next_mask)
                return

            generate(row + 1, next_mask | (1 << row))
            if row + 1 < height and not current_mask & (1 << (row + 1)):
                generate(row + 2, next_mask)

        generate(0, 0)

    dp = [0] * state_count
    dp[0] = 1
    for _ in range(width):
        next_dp = [0] * state_count
        for current_mask, ways in enumerate(dp):
            if ways == 0:
                continue
            for next_mask in transitions[current_mask]:
                next_dp[next_mask] = (next_dp[next_mask] + ways) % MODULO
        dp = next_dp

    return dp[0]
```

### Why the expert code is correct

- A mask records exactly the cells already covered from the left.
- Transition generation places one legal domino on the first free current-
  column cell, so it neither misses nor duplicates a completion.
- Every full tiling induces one sequence of column masks, and every generated
  sequence ending at mask `0` is a full tiling.
- Swapping dimensions only rotates the board and reduces the exponential mask
  dimension.

**Complexity:** `O(2^n F + mF)` time and `O(2^n + F)` memory, where `F` is the
total number of legal transitions over all masks and `n` is the smaller board
dimension.

## 7. What to remember

When pieces cross only the next column boundary, store that boundary as a
bitmask. Fill one column completely before advancing.
