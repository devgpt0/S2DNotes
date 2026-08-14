# ICPC300 233: Codeforces 1208E - Let Them Slide

**Source:** [Codeforces 1208E - Let Them Slide](https://codeforces.com/problemset/problem/1208/E)  
**Difficulty:** 2200  
**Pattern:** per-row sliding maxima with constant-range aggregation

## Exact contract

Each integer row has length at most `width` and may be shifted to any consecutive
positions inside that width. For every output column independently, maximize
the sum by choosing each row's shift, and return the `width` maxima.

## First principles

Rows are independent, so maximize one row's contribution to one column. At
column `c`, possible row indices form

`[max(0,c-(width-length)), min(length-1,c)]`.

If some shift avoids `c`, zero is also available. When `width >= 2*length`, a
wide middle range sees the complete row and has one constant contribution;
only `O(length)` edge columns need individual work.

## Cases that decide correctness

- Negative values lose to zero when the row can avoid a column.
- In the forced overlap of all shifts, zero is not an option.
- A row already as wide as the output is forced everywhere.
- The constant plateau is inclusive at both ends.
- Contributions from different rows add independently.

## Brute force: test every shift for every column

```python
def let_them_slide_brute(rows: list[list[int]], width: int) -> list[int]:
    if (
        type(width) is not int
        or width < 1
        or any(
            not row or len(row) > width or any(type(value) is not int for value in row)
            for row in rows
        )
    ):
        raise ValueError("rows must be nonempty integer rows fitting the width")
    answer = [0] * width
    for row in rows:
        gap = width - len(row)
        for column in range(width):
            best: int | None = None
            for start in range(gap + 1):
                contribution = (
                    row[column - start] if start <= column < start + len(row) else 0
                )
                best = contribution if best is None else max(best, contribution)
            if best is None:
                raise RuntimeError("every row has at least one shift")
            answer[column] += best
    return answer
```

This takes `O(width^2)` per row in the worst case.

## Better approach: scan all columns with a monotone deque

The possible row-index interval moves monotonically, so a deque gives
`O(width)` per row. The expert method avoids scanning a wide constant plateau
and reduces this to `O(row_length)`.

## Expert solution: edge scans plus a difference-array plateau

```python
from collections import deque


def let_them_slide(rows: list[list[int]], width: int) -> list[int]:
    if (
        type(width) is not int
        or width < 1
        or any(
            not row or len(row) > width or any(type(value) is not int for value in row)
            for row in rows
        )
    ):
        raise ValueError("rows must be nonempty integer rows fitting the width")

    answer = [0] * width
    range_add = [0] * (width + 1)

    for row in rows:
        length = len(row)
        gap = width - length
        if width >= 2 * length:
            prefix_maximum = row[0]
            for column in range(length - 1):
                prefix_maximum = max(prefix_maximum, row[column])
                answer[column] += max(0, prefix_maximum)

            suffix_maximum = row[-1]
            for column in range(width - 1, gap, -1):
                row_index = column - gap
                suffix_maximum = max(suffix_maximum, row[row_index])
                answer[column] += max(0, suffix_maximum)

            plateau_value = max(0, max(row))
            plateau_left = length - 1
            plateau_right = gap + 1
            range_add[plateau_left] += plateau_value
            range_add[plateau_right] -= plateau_value
            continue

        maximums: deque[int] = deque()
        next_row_index = 0
        for column in range(width):
            right = min(length - 1, column)
            while next_row_index <= right:
                while maximums and row[maximums[-1]] <= row[next_row_index]:
                    maximums.pop()
                maximums.append(next_row_index)
                next_row_index += 1
            left = max(0, column - gap)
            while maximums[0] < left:
                maximums.popleft()
            contribution = row[maximums[0]]
            if not gap <= column < length:
                contribution = max(0, contribution)
            answer[column] += contribution

    added = 0
    for column in range(width):
        added += range_add[column]
        answer[column] += added
    return answer
```

The deque returns the maximum over exactly the row indices that can cover a
column. Zero is added only outside the intersection of all shifts, and the
full-row plateau is accumulated once by range difference.

**Complexity:** `O(width + total_row_length)` time and `O(width)` space.
