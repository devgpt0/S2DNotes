# ICPC300 108: CSES - Counting Bishops

**Source:** [CSES - Counting Bishops](https://cses.fi/problemset/task/2176/)  
**Pattern:** color separation and Ferrers-board rook DP  
**Goal:** Count placements of exactly `k` bishops on an `n x n` chessboard so
no two bishops attack each other.

## 1. Problem in plain words

Bishops attack along both diagonal directions. A bishop never changes square
color, so bishops on black squares cannot attack bishops on white squares.

Count valid placements independently by color, then choose how many of the
`k` bishops use each color and convolve the two counts.

## 2. First principles

Treat each northwest-southeast diagonal of one color as a row. Its squares
intersect distinct northeast-southwest diagonals, which act as columns. After
sorting row lengths, these available column sets form a Ferrers board.

If a row has `length` squares and `placed-1` columns are already occupied,
there are `length-(placed-1)` choices for placing the next bishop in that row.
For one color:

`next[placed] += previous[placed-1] * (length-placed+1)`.

Skipping the row carries `previous[placed]` forward.

## 3. Cases that decide correctness

| Case | Required result |
| --- | --- |
| `k = 0` | `1`: place nothing. |
| `n = 1, k = 1` | `1`. |
| Too many bishops | `0`. |
| Bishops on opposite colors | They never attack each other. |
| Two bishops share either diagonal | Reject the placement. |

## 4. Brute force: choose square subsets

```python
from itertools import combinations


def count_bishop_placements_brute_force(size: int, bishop_count: int) -> int:
    if size < 1 or bishop_count < 0:
        raise ValueError("size must be positive and bishop count nonnegative")
    if bishop_count > size * size:
        return 0

    answer = 0
    for placement in combinations(range(size * size), bishop_count):
        descending: set[int] = set()
        ascending: set[int] = set()
        valid = True
        for square in placement:
            row, column = divmod(square, size)
            if row - column in descending or row + column in ascending:
                valid = False
                break
            descending.add(row - column)
            ascending.add(row + column)
        answer += valid
    return answer
```

**Complexity:** `O(C(n^2,k) * k)` time and `O(k)` memory.

## 5. Better: backtrack independently on each square color

```python
def count_bishop_placements_by_color(size: int, bishop_count: int) -> int:
    if size < 1 or bishop_count < 0:
        raise ValueError("size must be positive and bishop count nonnegative")

    squares = [[], []]
    for row in range(size):
        for column in range(size):
            squares[(row + column) % 2].append((row, column))

    def color_counts(color_squares: list[tuple[int, int]]) -> list[int]:
        ways = [0] * (bishop_count + 1)
        descending: set[int] = set()
        ascending: set[int] = set()

        def search(index: int, placed: int) -> None:
            if placed > bishop_count:
                return
            if index == len(color_squares):
                ways[placed] += 1
                return
            search(index + 1, placed)
            row, column = color_squares[index]
            if row - column not in descending and row + column not in ascending:
                descending.add(row - column)
                ascending.add(row + column)
                search(index + 1, placed + 1)
                descending.remove(row - column)
                ascending.remove(row + column)

        search(0, 0)
        return ways

    black = color_counts(squares[0])
    white = color_counts(squares[1])
    return sum(
        black[black_count] * white[bishop_count - black_count]
        for black_count in range(bishop_count + 1)
    )
```

**Complexity:** exponential in roughly half the board instead of the full
board, with `O(n^2)` recursion depth and state.

## 6. Expert solution: diagonal-length DP by color

```python
def count_bishop_placements(size: int, bishop_count: int) -> int:
    if size < 1 or bishop_count < 0:
        raise ValueError("size must be positive and bishop count nonnegative")
    if bishop_count > size * size:
        return 0

    diagonal_lengths: list[list[int]] = [[], []]
    for difference in range(-(size - 1), size):
        diagonal = [
            (row, row - difference)
            for row in range(size)
            if 0 <= row - difference < size
        ]
        row, column = diagonal[0]
        diagonal_lengths[(row + column) % 2].append(len(diagonal))

    def color_counts(lengths: list[int]) -> list[int]:
        ways = [0] * (bishop_count + 1)
        ways[0] = 1
        for length in sorted(lengths):
            next_ways = ways.copy()
            for placed in range(1, bishop_count + 1):
                available = length - (placed - 1)
                if available > 0:
                    next_ways[placed] += ways[placed - 1] * available
            ways = next_ways
        return ways

    black = color_counts(diagonal_lengths[0])
    white = color_counts(diagonal_lengths[1])
    return sum(
        black[black_count] * white[bishop_count - black_count]
        for black_count in range(bishop_count + 1)
    )
```

### Why the expert code is correct

- Opposite colors are independent because a bishop stays on its square color.
- For one color, choosing at most one square per diagonal in each direction is
  exactly the nonattacking condition.
- Sorted diagonal rows form nested column sets; after `j-1` bishops occupy
  columns, a row of length `L` has `L-j+1` legal remaining columns.
- Convolution considers every split of the total bishops between colors once.

**Complexity:** `O(nk + k)` time and `O(k)` DP memory, excluding short diagonal
lists.

## 7. What to remember

Bishops split by board color. Within one color, diagonals turn the board into a
Ferrers rook-placement DP.
