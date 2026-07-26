# Problem 18: Number of Islands (LeetCode #200)

**Difficulty:** Medium  
**Core pattern:** Connected components in a grid

## Problem statement

The grid contains land (`'1'`) and water (`'0'`). Land is connected vertically
and horizontally, not diagonally. Return the number of separate islands.

## Example

```text
1 1 0 0 0
1 1 0 0 0
0 0 1 0 0
0 0 0 1 1

Components:
[top-left]  [center]  [bottom-right]
Answer = 3
```

## Observation

The first time we see unvisited land, we have found a new island. We must then
visit every land cell connected to it so that the same island is not counted
again.

## Flood-fill diagram

```text
Scan each cell
     |
     +-- water or visited land --> skip
     |
     +-- unvisited land --------> islands += 1
                                      |
                                      v
                              DFS/BFS flood fill
                              up, down, left, right
```

## Solution 1: DFS with a Separate Visited Matrix

### Observation

Starting a fresh connectivity search from every land cell repeats work and may
take `O((mn)^2)` time.

### Algorithm

1. Create a `visited` matrix.
2. Scan every grid cell.
3. When unvisited land is found, count one island.
4. DFS through its four-directionally connected land and mark it visited.

### C++ code

```cpp
class Solution {
   public:
    int numIslands(vector<vector<char>>& grid) {
        int rows = grid.size();
        int columns = grid[0].size();
        vector<vector<bool>> visited(rows, vector<bool>(columns, false));

        function<void(int, int)> visit = [&](int row, int column) {
            if (row < 0 || row >= rows || column < 0 || column >= columns ||
                grid[row][column] != '1' || visited[row][column]) {
                return;
            }

            visited[row][column] = true;
            visit(row - 1, column);
            visit(row + 1, column);
            visit(row, column - 1);
            visit(row, column + 1);
        };

        int islands = 0;
        for (int row = 0; row < rows; ++row) {
            for (int column = 0; column < columns; ++column) {
                if (grid[row][column] == '1' && !visited[row][column]) {
                    ++islands;
                    visit(row, column);
                }
            }
        }
        return islands;
    }
};
```

### Complexity

- Time: `O(rows * columns)`
- Space: `O(rows * columns)` for visited state and recursion

## How we derive the optimal solution

```text
DFS with a separate visited matrix
               |
               v
The grid already has two states: land and water
               |
               v
Visited land can be changed to water
               |
               v
Reuse the input grid as visited state
               |
               v
Same O(rows*columns) time, no separate visited matrix
```

The natural flood-fill traversal is already time-optimal because every cell may
need inspection. The improvement removes auxiliary state rather than time.

## Optimized / CP approach: DFS flood fill

### Algorithm

1. Scan the grid row by row.
2. When a cell is `'1'`, increment the island count.
3. Run DFS from that cell.
4. During DFS, change every connected `'1'` to `'0'`.
5. Continue scanning; the marked island cannot be counted again.

### Why it works

One DFS visits exactly one connected component. Since visited land is marked,
each land cell belongs to one DFS and each component increments the answer once.

### Complexity

- Time: `O(rows * columns)`
- Space: `O(rows * columns)` in the worst case for recursion

## Pattern to remember

```text
Grid + connected regions + count/group/area
        => flood fill (DFS or BFS)

Outer loop discovers components.
Inner DFS/BFS consumes one complete component.
```

## C++

```cpp
class Solution {
   private:
    void flood(vector<vector<char>>& grid, int row, int column) {
        int rows = grid.size();
        int columns = grid[0].size();

        if (row < 0 || row >= rows || column < 0 || column >= columns) {
            return;
        }
        if (grid[row][column] != '1') {
            return;
        }

        grid[row][column] = '0';
        flood(grid, row - 1, column);
        flood(grid, row + 1, column);
        flood(grid, row, column - 1);
        flood(grid, row, column + 1);
    }

   public:
    int numIslands(vector<vector<char>>& grid) {
        int islands = 0;

        for (int row = 0; row < (int)grid.size(); ++row) {
            for (int column = 0; column < (int)grid[0].size(); ++column) {
                if (grid[row][column] == '1') {
                    ++islands;
                    flood(grid, row, column);
                }
            }
        }

        return islands;
    }
};
```

## Python

```python
class Solution:
    def num_islands(self, grid: list[list[str]]) -> int:
        rows = len(grid)
        columns = len(grid[0])

        def flood(row: int, column: int) -> None:
            if row < 0 or row >= rows or column < 0 or column >= columns:
                return
            if grid[row][column] != "1":
                return

            grid[row][column] = "0"
            flood(row - 1, column)
            flood(row + 1, column)
            flood(row, column - 1)
            flood(row, column + 1)

        islands = 0
        for row in range(rows):
            for column in range(columns):
                if grid[row][column] == "1":
                    islands += 1
                    flood(row, column)

        return islands
```

## Java

```java
class Solution {
    public int numIslands(char[][] grid) {
        int islands = 0;

        for (int row = 0; row < grid.length; row++) {
            for (int column = 0; column < grid[0].length; column++) {
                if (grid[row][column] == '1') {
                    islands++;
                    flood(grid, row, column);
                }
            }
        }

        return islands;
    }

    private void flood(char[][] grid, int row, int column) {
        if (row < 0 || row >= grid.length || column < 0 || column >= grid[0].length
            || grid[row][column] != '1') {
            return;
        }

        grid[row][column] = '0';
        flood(grid, row - 1, column);
        flood(grid, row + 1, column);
        flood(grid, row, column - 1);
        flood(grid, row, column + 1);
    }
}
```

## Go

```go
func numIslands(grid [][]byte) int {
	rows := len(grid)
	columns := len(grid[0])

	var flood func(int, int)
	flood = func(row, column int) {
		if row < 0 || row >= rows || column < 0 || column >= columns {
			return
		}
		if grid[row][column] != '1' {
			return
		}

		grid[row][column] = '0'
		flood(row-1, column)
		flood(row+1, column)
		flood(row, column-1)
		flood(row, column+1)
	}

	islands := 0
	for row := range grid {
		for column := range grid[row] {
			if grid[row][column] == '1' {
				islands++
				flood(row, column)
			}
		}
	}

	return islands
}
```

## Common mistakes

- Treating diagonal cells as connected.
- Counting land before marking its complete component.
- Forgetting that this implementation intentionally modifies the grid.
