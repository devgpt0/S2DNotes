# 138. Gerald and Giant Chess — Codeforces 559C

**Source:** [Codeforces 559C - Gerald and Giant Chess](https://codeforces.com/problemset/problem/559/C)  
**Difficulty:** 2200

## 1. Problem in plain words

Start at cell `(1, 1)` of an `h × w` board and reach `(h, w)`. A move goes one cell right or one cell down. Some listed cells are blocked. Count valid paths modulo `1_000_000_007`.

## 2. First principles

Without obstacles, a path from `(r₁, c₁)` to `(r₂, c₂)` uses a fixed number of down and right moves, so its count is

`C((r₂-r₁) + (c₂-c₁), r₂-r₁)`.

Only blocked cells matter. Sort them with the destination. For each point, count all paths to it and subtract paths whose first relevant blocked point is an earlier obstacle.

## 3. Cases that define correctness

- A blocked start or destination yields zero.
- An obstacle contributes only to points weakly below and right of it.
- Obstacles not lying on any monotone route to a point do not affect that point.
- All subtraction is performed modulo the source modulus.

## 4. Brute force

Explore every right/down path and stop when it reaches a blocked cell.

```python
MODULO = 1_000_000_007


def count_chess_paths_brute_force(
    height: int, width: int, blocked_cells: list[tuple[int, int]]
) -> int:
    if height <= 0 or width <= 0:
        raise ValueError("board dimensions must be positive")
    blocked = set(blocked_cells)
    if any(
        not 1 <= row <= height or not 1 <= column <= width for row, column in blocked
    ):
        raise ValueError("blocked cell is outside the board")
    if (1, 1) in blocked or (height, width) in blocked:
        return 0

    stack = [(1, 1)]
    answer = 0
    while stack:
        row, column = stack.pop()
        if (row, column) == (height, width):
            answer += 1
            continue
        if row < height and (row + 1, column) not in blocked:
            stack.append((row + 1, column))
        if column < width and (row, column + 1) not in blocked:
            stack.append((row, column + 1))
    return answer % MODULO
```

The time is proportional to the number of explored path prefixes, exponential in `h + w`; stack space is `O(h + w)` per active route.

## 5. Better approach: board dynamic programming

Let `dp[column]` hold the path count for the current row. It already contains paths arriving from above; adding the previous column supplies paths from the left.

```python
MODULO = 1_000_000_007


def count_chess_paths_grid_dp(
    height: int, width: int, blocked_cells: list[tuple[int, int]]
) -> int:
    if height <= 0 or width <= 0:
        raise ValueError("board dimensions must be positive")
    blocked = set(blocked_cells)
    if any(
        not 1 <= row <= height or not 1 <= column <= width for row, column in blocked
    ):
        raise ValueError("blocked cell is outside the board")

    dp = [0] * width
    dp[0] = 1
    for row in range(1, height + 1):
        for column in range(1, width + 1):
            if (row, column) in blocked:
                dp[column - 1] = 0
            elif column > 1:
                dp[column - 1] = (dp[column - 1] + dp[column - 2]) % MODULO
    return dp[-1]
```

Time is `O(hw)` and space is `O(w)`.

## 6. Expert solution: sparse obstacle DP

Precompute factorials for binomial coefficients. At each sorted obstacle or destination, subtract paths already assigned to every reachable earlier obstacle.

```python
MODULO = 1_000_000_007


def count_chess_paths(
    height: int, width: int, blocked_cells: list[tuple[int, int]]
) -> int:
    if height <= 0 or width <= 0:
        raise ValueError("board dimensions must be positive")
    if len(set(blocked_cells)) != len(blocked_cells):
        raise ValueError("blocked cells must be distinct")
    if any(
        not 1 <= row <= height or not 1 <= column <= width
        for row, column in blocked_cells
    ):
        raise ValueError("blocked cell is outside the board")
    blocked = set(blocked_cells)
    if (1, 1) in blocked or (height, width) in blocked:
        return 0

    maximum = height + width
    factorial = [1] * (maximum + 1)
    for value in range(1, maximum + 1):
        factorial[value] = factorial[value - 1] * value % MODULO
    inverse_factorial = [1] * (maximum + 1)
    inverse_factorial[maximum] = pow(factorial[maximum], MODULO - 2, MODULO)
    for value in range(maximum, 0, -1):
        inverse_factorial[value - 1] = inverse_factorial[value] * value % MODULO

    def combinations(total: int, chosen: int) -> int:
        if chosen < 0 or chosen > total:
            return 0
        return (
            factorial[total]
            * inverse_factorial[chosen]
            % MODULO
            * inverse_factorial[total - chosen]
            % MODULO
        )

    points = sorted([*blocked_cells, (height, width)])
    ways = [0] * len(points)
    for index, (row, column) in enumerate(points):
        current = combinations(row + column - 2, row - 1)
        for previous in range(index):
            old_row, old_column = points[previous]
            if old_row <= row and old_column <= column:
                paths_between = combinations(
                    row - old_row + column - old_column, row - old_row
                )
                current -= ways[previous] * paths_between
        ways[index] = current % MODULO
    return ways[-1]
```

## 7. Why the expert solution is correct

Every monotone path to a point either avoids all earlier obstacles or has a unique first earlier obstacle on it. `ways[obstacle]` counts valid prefixes whose first blocked endpoint is that obstacle, and the binomial factor counts every continuation to the current point. Subtracting these disjoint classes leaves exactly obstacle-free paths. The destination is processed by the same recurrence.

For `k` obstacles, time is `O(k² + h + w)` and space is `O(k + h + w)`.
