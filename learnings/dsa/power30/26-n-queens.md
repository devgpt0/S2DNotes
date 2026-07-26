# Problem 26: N-Queens (LeetCode #51)

**Difficulty:** Hard  
**Core pattern:** Constraint backtracking

## Problem statement

Place `n` queens on an `n x n` board so that no two queens share a row, column,
or diagonal. Return all valid boards.

## Example

```text
n = 4

. Q . .      . . Q .
. . . Q      Q . . .
Q . . .      . . . Q
. . Q .      . Q . .

Two valid boards exist.
```

## Observation

Place exactly one queen per row. A position `(row, column)` is unsafe when one
of these identifiers is already used:

```text
column          = column
down diagonal   = row - column
up diagonal     = row + column
```

## Search diagram

```text
row 0: try each safe column
          |
row 1: try each safe column
          |
        conflict? -> prune immediately
          |
row n: complete board -> save answer
```

## Solution 1: Generate Column Permutations, Then Validate

### Observation

Choose `n` cells from `n^2` cells, then validate them. This explores a huge
number of impossible boards.

### Algorithm

1. Assign one distinct column to every row.
2. Generate every permutation of columns.
3. After a complete placement, check every queen pair for diagonal conflict.
4. Save valid boards.

### C++ code

```cpp
class Solution {
   private:
    bool valid(const vector<int>& columnByRow) {
        for (int first = 0; first < static_cast<int>(columnByRow.size());
             ++first) {
            for (int second = first + 1;
                 second < static_cast<int>(columnByRow.size()); ++second) {
                if (abs(first - second) ==
                    abs(columnByRow[first] - columnByRow[second])) {
                    return false;
                }
            }
        }
        return true;
    }

   public:
    vector<vector<string>> solveNQueens(int n) {
        vector<int> columnByRow(n);
        iota(columnByRow.begin(), columnByRow.end(), 0);
        vector<vector<string>> answer;

        do {
            if (!valid(columnByRow)) {
                continue;
            }

            vector<string> board(n, string(n, '.'));
            for (int row = 0; row < n; ++row) {
                board[row][columnByRow[row]] = 'Q';
            }
            answer.push_back(board);
        } while (next_permutation(columnByRow.begin(), columnByRow.end()));

        return answer;
    }
};
```

### Complexity

- Time: `O(n! * n^2)`
- Space: `O(n)` excluding output

## How we derive the optimal solution

```text
Build a complete placement, then check conflicts
                 |
                 v
Invalid partial placements still generate many descendants
                 |
                 v
Track used columns and diagonals while placing each queen
                 |
                 v
Reject a conflict immediately
                 |
                 v
Backtracking explores only valid prefixes
```

## Optimized / CP approach

### Algorithm

1. Recurse one row at a time.
2. Try every column in the current row.
3. Skip used columns and diagonals.
4. Mark the three constraints and place `Q`.
5. Recurse to the next row.
6. Undo the placement and marks.
7. Save a copy when `row == n`.

### Complexity

- Time: approximately `O(n!)`, plus output construction
- Auxiliary space: `O(n)` apart from the board and output

## Pattern to remember

```text
Place objects under constraints
        => backtracking

choose -> mark constraints -> explore -> unmark -> unchoose
```

## C++

```cpp
class Solution {
   public:
    vector<vector<string>> solveNQueens(int n) {
        vector<vector<string>> answer;
        vector<string> board(n, string(n, '.'));
        vector<bool> columns(n, false);
        vector<bool> downDiagonal(2 * n - 1, false);
        vector<bool> upDiagonal(2 * n - 1, false);

        function<void(int)> search = [&](int row) {
            if (row == n) {
                answer.push_back(board);
                return;
            }

            for (int column = 0; column < n; ++column) {
                int down = row - column + n - 1;
                int up = row + column;
                if (columns[column] || downDiagonal[down] || upDiagonal[up]) {
                    continue;
                }

                board[row][column] = 'Q';
                columns[column] = downDiagonal[down] = upDiagonal[up] = true;
                search(row + 1);
                columns[column] = downDiagonal[down] = upDiagonal[up] = false;
                board[row][column] = '.';
            }
        };

        search(0);
        return answer;
    }
};
```

## Python

```python
class Solution:
    def solve_n_queens(self, n: int) -> list[list[str]]:
        answer: list[list[str]] = []
        board = [["."] * n for _ in range(n)]
        columns: set[int] = set()
        down_diagonals: set[int] = set()
        up_diagonals: set[int] = set()

        def search(row: int) -> None:
            if row == n:
                answer.append(["".join(line) for line in board])
                return

            for column in range(n):
                down = row - column
                up = row + column
                if column in columns or down in down_diagonals or up in up_diagonals:
                    continue

                board[row][column] = "Q"
                columns.add(column)
                down_diagonals.add(down)
                up_diagonals.add(up)

                search(row + 1)

                columns.remove(column)
                down_diagonals.remove(down)
                up_diagonals.remove(up)
                board[row][column] = "."

        search(0)
        return answer
```

## Java

```java
class Solution {
    public List<List<String>> solveNQueens(int n) {
        List<List<String>> answer = new ArrayList<>();
        char[][] board = new char[n][n];
        for (char[] row : board) {
            Arrays.fill(row, '.');
        }

        search(0, board, new boolean[n], new boolean[2 * n - 1], new boolean[2 * n - 1], answer);
        return answer;
    }

    private void search(int row, char[][] board, boolean[] columns, boolean[] downDiagonal,
        boolean[] upDiagonal, List<List<String>> answer) {
        int n = board.length;
        if (row == n) {
            List<String> solution = new ArrayList<>();
            for (char[] line : board) {
                solution.add(new String(line));
            }
            answer.add(solution);
            return;
        }

        for (int column = 0; column < n; column++) {
            int down = row - column + n - 1;
            int up = row + column;
            if (columns[column] || downDiagonal[down] || upDiagonal[up]) {
                continue;
            }

            board[row][column] = 'Q';
            columns[column] = downDiagonal[down] = upDiagonal[up] = true;
            search(row + 1, board, columns, downDiagonal, upDiagonal, answer);
            columns[column] = downDiagonal[down] = upDiagonal[up] = false;
            board[row][column] = '.';
        }
    }
}
```

## Go

```go
func solveNQueens(n int) [][]string {
	answer := [][]string{}
	board := make([][]byte, n)
	for row := range board {
		board[row] = bytes.Repeat([]byte{'.'}, n)
	}
	columns := make([]bool, n)
	downDiagonal := make([]bool, 2*n-1)
	upDiagonal := make([]bool, 2*n-1)

	var search func(int)
	search = func(row int) {
		if row == n {
			solution := make([]string, n)
			for index := range board {
				solution[index] = string(board[index])
			}
			answer = append(answer, solution)
			return
		}

		for column := 0; column < n; column++ {
			down := row - column + n - 1
			up := row + column
			if columns[column] || downDiagonal[down] || upDiagonal[up] {
				continue
			}

			board[row][column] = 'Q'
			columns[column], downDiagonal[down], upDiagonal[up] = true, true, true
			search(row + 1)
			columns[column], downDiagonal[down], upDiagonal[up] = false, false, false
			board[row][column] = '.'
		}
	}

	search(0)
	return answer
}
```

## Common mistakes

- Checking the whole board for every placement instead of using sets/arrays.
- Forgetting to undo one of the three constraints.
- Saving references to the mutable board rather than copying it.
