# 172. Pig and Palindromes — Codeforces 570E

**Source:** [Codeforces 570E - Pig and Palindromes](https://codeforces.com/problemset/problem/570/E)  
**Difficulty:** 2200

## 1. Problem in plain words

Move from the top-left to the bottom-right of a letter grid using only down and right moves. Count paths whose visited-letter string is a palindrome, modulo `1_000_000_007`.

## 2. First principles

A palindrome matches characters symmetrically. Move one walker forward from the start and another backward from the end. After the same number of steps, keep only pairs of positions with equal letters. When the walkers meet or become adjacent, every matched outer choice forms one palindrome.

## 3. Cases that define correctness

- Different corner letters make the answer zero.
- With an even number of moves, walkers finish on the same cell.
- With an odd number of moves, walkers finish on adjacent cells.
- A one-cell grid has exactly one valid path.

## 4. Brute force

Enumerate every monotone path and test its complete letter string.

```python
MODULO = 1_000_000_007


def count_palindromic_grid_paths_brute_force(grid: list[str]) -> int:
    if (
        not grid
        or any(type(row) is not str or not row for row in grid)
        or any(len(row) != len(grid[0]) for row in grid)
        or any(character < "a" or character > "z" for row in grid for character in row)
    ):
        raise ValueError("grid must be nonempty and rectangular")

    height = len(grid)
    width = len(grid[0])
    answer = 0
    stack = [(0, 0, grid[0][0])]
    while stack:
        row, column, text = stack.pop()
        if row == height - 1 and column == width - 1:
            answer += text == text[::-1]
            continue
        if row + 1 < height:
            stack.append((row + 1, column, text + grid[row + 1][column]))
        if column + 1 < width:
            stack.append((row, column + 1, text + grid[row][column + 1]))
    return answer % MODULO
```

Time is proportional to `C(n+m-2, n-1)` paths and space is `O(n+m)` per path.

## 5. Better approach: memoized two-ended search

Recurse on both walkers. Equal outer letters reduce the problem to four pairs of inward moves; memoization merges repeated states.

```python
from functools import cache

MODULO = 1_000_000_007


def count_palindromic_grid_paths_memoized(grid: list[str]) -> int:
    if (
        not grid
        or any(type(row) is not str or not row for row in grid)
        or any(len(row) != len(grid[0]) for row in grid)
        or any(character < "a" or character > "z" for row in grid for character in row)
    ):
        raise ValueError("grid must be nonempty and rectangular")

    height = len(grid)
    width = len(grid[0])

    @cache
    def count(
        first_row: int, first_column: int, second_row: int, second_column: int
    ) -> int:
        if first_row > second_row or first_column > second_column:
            return 0
        if grid[first_row][first_column] != grid[second_row][second_column]:
            return 0
        distance = second_row - first_row + second_column - first_column
        if distance <= 1:
            return 1

        answer = 0
        first_moves: list[tuple[int, int]] = []
        second_moves: list[tuple[int, int]] = []
        if first_row + 1 < height:
            first_moves.append((first_row + 1, first_column))
        if first_column + 1 < width:
            first_moves.append((first_row, first_column + 1))
        if second_row > 0:
            second_moves.append((second_row - 1, second_column))
        if second_column > 0:
            second_moves.append((second_row, second_column - 1))
        for next_first_row, next_first_column in first_moves:
            for next_second_row, next_second_column in second_moves:
                answer += count(
                    next_first_row,
                    next_first_column,
                    next_second_row,
                    next_second_column,
                )
        return answer % MODULO

    return count(0, 0, height - 1, width - 1)
```

Only synchronized walker states are reached, giving `O((n+m)n²)` states when rows are the smaller grid dimension.

## 6. Expert solution: rolling synchronized-walker DP

At layer `step`, each walker's column is determined by its row. Store only `(first_row, second_row)`, advance both one step, and discard unequal letters.

```python
MODULO = 1_000_000_007


def count_palindromic_grid_paths(grid: list[str]) -> int:
    if (
        not grid
        or any(type(row) is not str or not row for row in grid)
        or any(len(row) != len(grid[0]) for row in grid)
        or any(character < "a" or character > "z" for row in grid for character in row)
    ):
        raise ValueError("grid must be nonempty and rectangular")
    if len(grid) > len(grid[0]):
        grid = ["".join(row) for row in zip(*grid)]

    height = len(grid)
    width = len(grid[0])
    total_steps = height + width - 2
    if grid[0][0] != grid[-1][-1]:
        return 0

    current = {(0, height - 1): 1}
    for step in range(total_steps // 2):
        next_step = step + 1
        following: dict[tuple[int, int], int] = {}
        for (first_row, second_row), ways in current.items():
            for next_first_row in (first_row, first_row + 1):
                first_column = next_step - next_first_row
                if not 0 <= next_first_row < height or not 0 <= first_column < width:
                    continue
                for next_second_row in (second_row, second_row - 1):
                    second_column = total_steps - next_step - next_second_row
                    if (
                        not 0 <= next_second_row < height
                        or not 0 <= second_column < width
                        or grid[next_first_row][first_column]
                        != grid[next_second_row][second_column]
                    ):
                        continue
                    state = next_first_row, next_second_row
                    following[state] = (following.get(state, 0) + ways) % MODULO
        current = following

    answer = 0
    middle_step = total_steps // 2
    for (first_row, second_row), ways in current.items():
        first_column = middle_step - first_row
        second_column = total_steps - middle_step - second_row
        distance = abs(first_row - second_row) + abs(first_column - second_column)
        if distance == total_steps % 2:
            answer += ways
    return answer % MODULO
```

## 7. Why the expert solution is correct

Every DP transition chooses one forward and one backward path edge and keeps the state exactly when the newly symmetric letters match. Thus each state counts precisely pairs of matching outer path halves. At the middle, distance zero or one makes the halves join into one complete path, and every palindromic path has one unique sequence of such paired moves.

Time is `O((n+m) · min(n,m)²)` and rolling space is `O(min(n,m)²)`.
