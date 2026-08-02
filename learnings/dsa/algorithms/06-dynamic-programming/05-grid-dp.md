# Grid Dynamic Programming

## Idea

Grid DP stores an answer for each cell using the cells that can move into it.
The traversal order must make those dependencies ready.

## Visual model

For moves right and down:

```text
dp[row][column] <- min(from above, from left) + cell cost
```

## Classroom board: one cell

```text
cost grid:
1 3
2 4

dp top-left = 1
dp top-right = 1+3 = 4
dp bottom-left = 1+2 = 3
dp bottom-right = min(4,3)+4 = 7
```

Every allowed path into bottom-right must come from above or left.

## Steps

1. Define the start cell's value.
2. Visit rows and columns from top-left to bottom-right.
3. For each cell, take the best valid predecessor.
4. Add the current cell cost.

## First-principles derivation

Each grid cell is a state when every valid path reaching it has the same future
choices. Its answer combines predecessor cells plus the local cost or count.

The fill order must ensure every predecessor is final before the current cell
is evaluated.

## Pattern recognition

Use grid DP when movement is acyclic, usually restricted to directions such as
right/down. If movement can cycle, think of the grid as a graph instead.

## Implementation: minimum path sum

### C++

```cpp
long long minimumPathSum(const std::vector<std::vector<int>>& grid) {
    std::vector<long long> dp(grid[0].size(), std::numeric_limits<long long>::max() / 4);
    dp[0] = 0;
    for (const auto& row : grid) {
        for (int column = 0; column < static_cast<int>(row.size()); ++column) {
            if (column > 0) dp[column] = std::min(dp[column], dp[column - 1]);
            dp[column] += row[column];
        }
    }
    return dp.back();
}
```

### Python

```python
def minimum_path_sum(grid: list[list[int]]) -> int:
    dp = [10**30] * len(grid[0])
    dp[0] = 0
    for row in grid:
        for column, cost in enumerate(row):
            if column > 0:
                dp[column] = min(dp[column], dp[column - 1])
            dp[column] += cost
    return dp[-1]
```

### Java

```java
static long minimumPathSum(int[][] grid) {
    long[] dp = new long[grid[0].length];
    Arrays.fill(dp, Long.MAX_VALUE / 4);
    dp[0] = 0;
    for (int[] row : grid) {
        for (int column = 0; column < row.length; column++) {
            if (column > 0) dp[column] = Math.min(dp[column], dp[column - 1]);
            dp[column] += row[column];
        }
    }
    return dp[dp.length - 1];
}
```

## Why it works

Every valid path into a cell ends either above it or left of it. The transition
considers both complete possibilities and keeps the cheaper one.

## Complexity

Time is `O(rows * columns)` and extra space is `O(columns)`.

## Common mistakes

- Reading `dp[column - 1]` before it represents the current row.
- Mishandling the first row or column.
- Using DP when allowed moves create cycles.
