# ICPC300 295: Codeforces 1353F - Decreasing Heights

**Source:** [Codeforces 1353F - Decreasing Heights](https://codeforces.com/problemset/problem/1353/F)  
**Rating:** 2200  
**Pattern:** enumerate a path baseline, then grid DP  
**Goal:** Choose a top-left to bottom-right path using down and right moves.
Only decrease heights so consecutive path cells increase by exactly one;
minimize the total decrease on the path.

## 1. First principles

If the chosen start height is `base`, cell `(row, column)` on any monotone path
must finish at `base + row + column`. It is usable only when its original
height is at least that target.

For an optimal path, increasing `base` reduces every cost until some path cell
becomes tight. Thus `base` equals
`height[row][column] - row - column` for at least one grid cell.

## 2. Cases that decide correctness

- The baseline cannot exceed the original top-left height.
- Cells below their required target are unreachable, not negative-cost.
- The cost includes both path endpoints.
- A one-cell grid costs zero.
- Every candidate baseline uses an independent DP table.

## 3. Brute force: enumerate monotone paths

```python
def minimum_decrease_cost_brute(heights: list[list[int]]) -> int:
    if (
        not heights
        or not heights[0]
        or any(len(row) != len(heights[0]) for row in heights)
        or any(type(value) is not int or value < 0 for row in heights for value in row)
    ):
        raise ValueError("heights must be a nonempty nonnegative rectangular grid")
    row_count = len(heights)
    column_count = len(heights[0])
    answer = 10**100

    def search(row: int, column: int, path: list[tuple[int, int]]) -> None:
        nonlocal answer
        path.append((row, column))
        if row == row_count - 1 and column == column_count - 1:
            base = min(
                heights[path_row][path_column] - path_row - path_column
                for path_row, path_column in path
            )
            cost = sum(
                heights[path_row][path_column] - base - path_row - path_column
                for path_row, path_column in path
            )
            answer = min(answer, cost)
        else:
            if row + 1 < row_count:
                search(row + 1, column, path)
            if column + 1 < column_count:
                search(row, column + 1, path)
        path.pop()

    search(0, 0, [])
    return answer
```

**Complexity:** `O(C(r+c, r) * (r+c))` time and `O(r+c)` stack space.

## 4. Better approach: try every integer baseline

For a fixed baseline, the cheapest monotone path is an ordinary grid DP. The
baseline range can be huge, so only values that make some cell tight should be
tested.

## 5. Expert solution: candidate baselines and shortest path DP

```python
def minimum_decrease_cost(heights: list[list[int]]) -> int:
    if (
        not heights
        or not heights[0]
        or any(len(row) != len(heights[0]) for row in heights)
        or any(type(value) is not int or value < 0 for row in heights for value in row)
    ):
        raise ValueError("heights must be a nonempty nonnegative rectangular grid")
    row_count = len(heights)
    column_count = len(heights[0])
    candidates = {
        heights[row][column] - row - column
        for row in range(row_count)
        for column in range(column_count)
        if heights[row][column] - row - column <= heights[0][0]
    }
    infinity = 10**100
    answer = infinity
    for base in candidates:
        dp = [[infinity] * column_count for _ in range(row_count)]
        for row in range(row_count):
            for column in range(column_count):
                target = base + row + column
                if heights[row][column] < target:
                    continue
                cost = heights[row][column] - target
                if row == 0 and column == 0:
                    dp[row][column] = cost
                else:
                    previous = infinity
                    if row:
                        previous = min(previous, dp[row - 1][column])
                    if column:
                        previous = min(previous, dp[row][column - 1])
                    dp[row][column] = previous + cost
        answer = min(answer, dp[-1][-1])
    return answer
```

### Why the expert code is correct

Fixing a baseline fixes every path cell's target, and the DP minimizes the sum
over all feasible monotone paths. Any optimal path can raise its baseline until
one cell is tight, so the candidate set contains an optimal baseline. Taking
the best candidate is therefore globally optimal.

**Complexity:** `O((r c)^2)` time and `O(r c)` space.

## 6. What to remember

```text
monotone step increases height by one -> target is base + row + column
only decreases allowed -> reject cells below target
optimal baseline -> tight at some cell
```
