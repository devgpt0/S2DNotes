# ICPC300 098: CSES - Moving Robots

**Source:** [CSES - Moving Robots](https://cses.fi/problemset/task/1726/)  
**Pattern:** independent Markov-chain distributions

## Exact contract

Initially each square of an `8 x 8` board contains one robot. Every robot makes
exactly `k` moves. At each move it chooses uniformly among the horizontally or
vertically adjacent squares that remain on the board. Output the expected
number of empty squares after all moves, with six decimal places.

## First principles

Fix a target square. For a robot starting at `s`, compute probability
`p[s][target]` that it ends there. Robots move independently, so the target is
empty with probability `product_s(1-p[s][target])`. Sum this probability over
all 64 targets by linearity of expectation.

## Cases that decide correctness

- Corner, edge, and interior squares have two, three, and four legal moves.
- Robot destinations are not mutually exclusive, but robot movements are
  independent.
- Linearity of expectation does not require empty-square events to be
  independent.
- At `k = 0`, every square is occupied and the answer is zero.

## Brute force: enumerate each robot's paths

```python
from fractions import Fraction


def moving_robots_paths(steps: int) -> Fraction:
    neighbors = [[] for _ in range(64)]
    for square in range(64):
        row, column = divmod(square, 8)
        for row_change, column_change in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            next_row = row + row_change
            next_column = column + column_change
            if 0 <= next_row < 8 and 0 <= next_column < 8:
                neighbors[square].append(next_row * 8 + next_column)

    empty_probability = [Fraction(1) for _ in range(64)]
    for start in range(64):
        outcomes = [Fraction(0) for _ in range(64)]

        def enumerate_paths(
            square: int, moves_left: int, probability: Fraction
        ) -> None:
            if moves_left == 0:
                outcomes[square] += probability
                return
            share = probability / len(neighbors[square])
            for neighbor in neighbors[square]:
                enumerate_paths(neighbor, moves_left - 1, share)

        enumerate_paths(start, steps, Fraction(1))
        for target, probability in enumerate(outcomes):
            empty_probability[target] *= 1 - probability
    return sum(empty_probability, Fraction(0))
```

Exact fractions make this definition faithful, but it explores up to four
branches per move and therefore takes exponential time in `k`.

## Better for huge step counts: dense matrix exponentiation

```python
def moving_robots_matrix(steps: int) -> float:
    size = 64
    transition = [[0.0] * size for _ in range(size)]
    for square in range(size):
        row, column = divmod(square, 8)
        adjacent = []
        for row_change, column_change in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            next_row = row + row_change
            next_column = column + column_change
            if 0 <= next_row < 8 and 0 <= next_column < 8:
                adjacent.append(next_row * 8 + next_column)
        for neighbor in adjacent:
            transition[square][neighbor] = 1.0 / len(adjacent)

    def multiply(
        left: list[list[float]], right: list[list[float]]
    ) -> list[list[float]]:
        product = [[0.0] * size for _ in range(size)]
        for row in range(size):
            for middle, left_value in enumerate(left[row]):
                if left_value:
                    for column, right_value in enumerate(right[middle]):
                        product[row][column] += left_value * right_value
        return product

    result = [[float(row == column) for column in range(size)] for row in range(size)]
    while steps:
        if steps & 1:
            result = multiply(result, transition)
        transition = multiply(transition, transition)
        steps >>= 1

    return sum(
        __import__("math").prod(1.0 - result[start][target] for start in range(size))
        for target in range(size)
    )
```

Matrix powers reduce dependence on `k` to `O(64^3 log k)`, but dense work is
unnecessary for the source's small step bound.

## Expert solution: sparse per-start distributions

```python
import sys


def solve() -> None:
    steps = int(sys.stdin.readline())
    neighbors = [[] for _ in range(64)]
    for square in range(64):
        row, column = divmod(square, 8)
        for row_change, column_change in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            next_row = row + row_change
            next_column = column + column_change
            if 0 <= next_row < 8 and 0 <= next_column < 8:
                neighbors[square].append(next_row * 8 + next_column)

    empty_probability = [1.0] * 64
    for start in range(64):
        probability = [0.0] * 64
        probability[start] = 1.0
        for _ in range(steps):
            next_probability = [0.0] * 64
            for square, chance in enumerate(probability):
                if chance:
                    share = chance / len(neighbors[square])
                    for neighbor in neighbors[square]:
                        next_probability[neighbor] += share
            probability = next_probability
        for target, chance in enumerate(probability):
            empty_probability[target] *= 1.0 - chance

    print(f"{sum(empty_probability):.6f}")


if __name__ == "__main__":
    solve()
```

Each robot DP is its exact endpoint distribution. Independence gives each
empty-square product, and linearity makes their sum the expected count.

**Complexity:** `O(64^2 k)` time with a constant of at most four transitions
and `O(64)` working space.
