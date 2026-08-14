# ICPC300 023: CSES - Beautiful Subgrids

**Source:** [CSES - Beautiful Subgrids](https://cses.fi/problemset/task/2137/)  
**Pattern:** row-pair counting with packed bitsets

## Exact contract

Input gives `n` (`1 <= n <= 3000`) and an `n x n` binary grid. Count
axis-aligned subgrids whose four corner cells are all `1`. A subgrid uses two
distinct rows and two distinct columns. Output the number of such subgrids.

## First principles

Fix the top and bottom rows. Every column containing `1` in both rows can be a
vertical side of a valid subgrid. If the two rows have `c` such common
columns, choosing any two of them gives one subgrid, so this row pair
contributes `c * (c - 1) // 2`.

The remaining task is to count common one-bits for every pair of rows. Python
integers are packed bitsets: bitwise AND finds common columns and `bit_count()`
counts them in optimized native code.

## Cases that decide correctness

- Rows and columns must both be distinct; one common column contributes zero.
- Each subgrid has one unique unordered pair of rows and one unique unordered
  pair of columns, so it is counted exactly once.
- `n = 1`, all-zero rows, and rows with one common `1` produce zero.
- The answer can be much larger than 32-bit range.
- Preserve leading zeroes when reading a row; converting the whole binary
  string to an integer still keeps every column as a consistent bit position.

## Brute force: inspect every rectangle

```python
def count_beautiful_subgrids_brute(grid: list[str]) -> int:
    size = len(grid)
    answer = 0
    for top in range(size):
        for bottom in range(top + 1, size):
            for left in range(size):
                for right in range(left + 1, size):
                    answer += (
                        grid[top][left] == "1"
                        and grid[top][right] == "1"
                        and grid[bottom][left] == "1"
                        and grid[bottom][right] == "1"
                    )
    return answer
```

This mirrors the definition and is a useful tiny-grid oracle.

**Complexity:** `O(n^4)` time and `O(1)` extra space.

## Better: count common columns for each row pair

```python
def count_beautiful_subgrids_cubic(grid: list[str]) -> int:
    size = len(grid)
    answer = 0
    for top in range(size):
        for bottom in range(top + 1, size):
            common_columns = sum(
                grid[top][column] == "1" and grid[bottom][column] == "1"
                for column in range(size)
            )
            answer += common_columns * (common_columns - 1) // 2
    return answer
```

The combinatorial count removes the two column loops, reducing four dimensions
to three.

**Complexity:** `O(n^3)` time and `O(1)` extra space.

## Expert solution: pack every row into one integer

```python
import sys


def solve() -> None:
    input_stream = sys.stdin.buffer
    size = int(input_stream.readline())
    row_masks = [int(input_stream.readline().strip(), 2) for _ in range(size)]

    answer = 0
    for bottom in range(size):
        bottom_mask = row_masks[bottom]
        for top in range(bottom):
            common_columns = (row_masks[top] & bottom_mask).bit_count()
            answer += common_columns * (common_columns - 1) // 2

    print(answer)


if __name__ == "__main__":
    solve()
```

For each row pair, AND leaves a set bit exactly at the columns where both
corners are `1`. Choosing two set bits creates every valid subgrid for that row
pair and no invalid one.

**Complexity:** `O(n^3 / w)` bit operations, where `w` is the machine-word
size used inside Python's big integers, and `O(n^2 / w)` packed-bit space.

