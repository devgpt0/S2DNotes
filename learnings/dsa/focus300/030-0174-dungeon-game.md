# Focus300 030: LeetCode 174 - Dungeon Game

**Source:** [LeetCode 174](https://leetcode.com/problems/dungeon-game/)  
**Difficulty:** Hard  
**Pattern:** reverse minimum-required-health DP

## Exact contract

Starting at the top-left cell, move only right or down to the bottom-right.
Each cell adds its integer value to health. Health must remain at least one
after every cell. Return the minimum positive initial health that permits a
valid path.

## First principles

Forward DP cannot keep only the currently largest health: a path with less
current health may have required much less initial health. Reverse the state.

If the cheaper next cell requires `need`, entering the current cell requires
`max(1, need-dungeon[row][column])`. The destination follows the same formula
with a virtual next requirement of one.


## Classroom board: store the repeated state once

```text
brute force recomputes the same subproblem many times.
dp keeps the smallest useful state and extends it one step at a time.
```



## Step-by-step transformation

1. Turn the input into subproblems, prefixes, or states that can be reused.
2. Fill the base cases first so later states have something correct to build on.
3. Update each new state from earlier states while keeping the recurrence valid.
4. Read the answer from the final table entry or the best state collected at the end.

Dynamic-programming style notes transform the input by compressing many repeated choices into a small set of reusable states.


## Diagram: state table to answer

```text

            input
                |
                v
            base states
                |
                v
            reuse smaller states
                |
                v
            final dp answer
```

These notes compress repeated choices into reusable states, then read the answer from the last state that matters.

## Cases that decide correctness

- Health may never become zero, even at the destination.
- Positive rooms can reduce future required health only down to one.
- The best path is chosen by minimum required entry health, not maximum sum.
- A one-cell dungeon uses `max(1,1-cell)`.
- Grid values may be negative, zero, or positive.

## Brute force: enumerate every right/down path

```python
def calculate_minimum_hp_brute(dungeon: list[list[int]]) -> int:
    row_count = len(dungeon)
    column_count = len(dungeon[0])
    answer = 10**30

    def search(row: int, column: int, total: int, minimum: int) -> None:
        nonlocal answer
        total += dungeon[row][column]
        minimum = min(minimum, total)
        if row + 1 == row_count and column + 1 == column_count:
            answer = min(answer, max(1, 1 - minimum))
            return
        if row + 1 < row_count:
            search(row + 1, column, total, minimum)
        if column + 1 < column_count:
            search(row, column + 1, total, minimum)

    search(0, 0, 0, 0)
    return answer
```

This explores `binomial(rows+columns-2, rows-1)` paths.

## Better approach: full reverse DP table

```python
def calculate_minimum_hp_table(dungeon: list[list[int]]) -> int:
    row_count = len(dungeon)
    column_count = len(dungeon[0])
    infinity = 10**30
    required = [[infinity] * (column_count + 1) for _ in range(row_count + 1)]
    required[row_count][column_count - 1] = 1
    required[row_count - 1][column_count] = 1
    for row in range(row_count - 1, -1, -1):
        for column in range(column_count - 1, -1, -1):
            next_required = min(required[row + 1][column], required[row][column + 1])
            required[row][column] = max(1, next_required - dungeon[row][column])
    return required[0][0]
```

This is `O(rows*columns)` time and space.

## Expert solution: one rolling row of required health

```python
def calculate_minimum_hp(dungeon: list[list[int]]) -> int:
    row_count = len(dungeon)
    column_count = len(dungeon[0])
    infinity = 10**30
    required = [infinity] * (column_count + 1)
    required[column_count - 1] = 1
    for row in range(row_count - 1, -1, -1):
        required[column_count] = infinity
        for column in range(column_count - 1, -1, -1):
            next_required = min(required[column], required[column + 1])
            required[column] = max(1, next_required - dungeon[row][column])
    return required[0]
```

During the reverse scan, `required[column]` is the cell below and
`required[column+1]` is the cell to the right, exactly the two legal moves.

**Complexity:** `O(rows*columns)` time and `O(columns)` space.
