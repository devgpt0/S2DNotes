# ICPC300 168: Codeforces 662C - Binary Table

**Source:** [Codeforces 662C](https://codeforces.com/problemset/problem/662/C)  
**Pattern:** xor convolution with the Walsh-Hadamard transform

## Exact contract

Given an `n x m` binary table with `n <= 20`, any rows and any columns may be
inverted. Output the minimum possible number of `1` cells.

## First principles

Encode each column as an `n`-bit mask. If row-flip mask `x` is chosen, a column
mask `y` becomes `x xor y`. The column can then be flipped or kept, so its best
cost is

`cost[z] = min(popcount(z), n - popcount(z))`.

If `frequency[y]` counts input columns of mask `y`, the total for row mask `x`
is the xor convolution

`sum(frequency[y] * cost[x xor y])`.

The Walsh-Hadamard transform evaluates this value for all `2^n` row masks at
once.

## Cases that decide correctness

- Row flips are shared by all columns; column flips are chosen independently.
- A column and its bitwise complement have the same optimized cost.
- The transform is over xor, not ordinary polynomial convolution.
- Divide every inverse-transformed coefficient by `2^n` exactly.
- Duplicate columns must contribute with their frequency.

## Brute force: enumerate row and column flip masks

```python
def binary_table_brute(rows: list[str]) -> int:
    row_count = len(rows)
    column_count = len(rows[0])
    best = row_count * column_count
    for row_flips in range(1 << row_count):
        for column_flips in range(1 << column_count):
            ones = 0
            for row in range(row_count):
                for column in range(column_count):
                    bit = int(rows[row][column])
                    bit ^= row_flips >> row & 1
                    bit ^= column_flips >> column & 1
                    ones += bit
            best = min(best, ones)
    return best
```

There are `2^(n+m)` flip choices.

## Better: enumerate only row flips

```python
def binary_table_row_masks(rows: list[str]) -> int:
    row_count = len(rows)
    column_count = len(rows[0])
    column_masks = [0] * column_count
    for row, text in enumerate(rows):
        for column, bit in enumerate(text):
            if bit == "1":
                column_masks[column] |= 1 << row

    best = row_count * column_count
    for row_flips in range(1 << row_count):
        ones = 0
        for column_mask in column_masks:
            count = (column_mask ^ row_flips).bit_count()
            ones += min(count, row_count - count)
        best = min(best, ones)
    return best
```

Choosing each column orientation greedily removes `2^m`, but the remaining
`O(m 2^n)` work is still too large.

## Expert solution: xor Walsh-Hadamard convolution

```python
import sys


def solve() -> None:
    input_stream = sys.stdin.buffer
    row_count, column_count = map(int, input_stream.readline().split())
    column_masks = [0] * column_count
    for row in range(row_count):
        text = input_stream.readline().strip()
        for column, bit in enumerate(text):
            if bit == ord("1"):
                column_masks[column] |= 1 << row

    transform_size = 1 << row_count
    frequency = [0] * transform_size
    for mask in column_masks:
        frequency[mask] += 1
    cost = [
        min(mask.bit_count(), row_count - mask.bit_count())
        for mask in range(transform_size)
    ]

    def transform(values: list[int]) -> None:
        half = 1
        while half < len(values):
            step = half * 2
            for start in range(0, len(values), step):
                for offset in range(half):
                    first = values[start + offset]
                    second = values[start + offset + half]
                    values[start + offset] = first + second
                    values[start + offset + half] = first - second
            half = step

    transform(frequency)
    transform(cost)
    convolution = [
        first * second for first, second in zip(frequency, cost, strict=True)
    ]
    transform(convolution)
    print(min(value // transform_size for value in convolution))


if __name__ == "__main__":
    solve()
```

The transform diagonalizes xor convolution. Pointwise multiplication followed
by the same transform and exact scaling produces the cost of every row mask,
whose minimum is the answer.

**Complexity:** `O(n m + n 2^n)` time and `O(2^n + m)` space.
