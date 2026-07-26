# Problem 28: Edit Distance (LeetCode #72)

**Difficulty:** Medium  
**Core pattern:** Two-string dynamic programming

## Problem statement

Return the minimum insertions, deletions, and replacements required to transform
`word1` into `word2`.

## Example

```text
word1 = "horse"
word2 = "ros"

horse -> rorse   replace h with r
rorse -> rose    delete r
rose  -> ros     delete e

answer = 3
```

## Observation

Let `dp[i][j]` be the cost to transform the first `i` characters of `word1`
into the first `j` characters of `word2`.

```text
same final character: dp[i][j] = dp[i-1][j-1]

different:
insert  -> dp[i][j-1]
delete  -> dp[i-1][j]
replace -> dp[i-1][j-1]

dp[i][j] = 1 + minimum of those three
```

## Table diagram

```text
                   word2 prefix
                      j-1     j
                        \     ^
word1 prefix i-1  ->  replace insert
             i         delete [i,j]
```

## Solution 1: Recursive Brute Force

### Observation

At every mismatch, try insertion, deletion, and replacement. Overlapping states
make this exponential.

### Algorithm

1. Compare characters at positions `i` and `j`.
2. If they match, move both indices without cost.
3. Otherwise recursively try insert, delete, and replace.
4. Add one operation and return the minimum branch.

### C++ code

```cpp
class Solution {
   private:
    int solve(const string& first, const string& second, int i, int j) {
        if (i == static_cast<int>(first.size())) {
            return second.size() - j;
        }
        if (j == static_cast<int>(second.size())) {
            return first.size() - i;
        }
        if (first[i] == second[j]) {
            return solve(first, second, i + 1, j + 1);
        }

        int insert = solve(first, second, i, j + 1);
        int remove = solve(first, second, i + 1, j);
        int replace = solve(first, second, i + 1, j + 1);
        return 1 + min({insert, remove, replace});
    }

   public:
    int minDistance(string word1, string word2) {
        return solve(word1, word2, 0, 0);
    }
};
```

### Complexity

- Time: exponential, approximately `O(3^(m+n))`
- Space: `O(m + n)` recursion depth

## How we derive the optimal solution

```text
Try insert, delete, and replace at every mismatch
                  |
                  v
The same (i, j) suffix state is solved repeatedly
                  |
                  v
Cache every state with memoization
                  |
                  v
Express the same states as a 2D prefix table
                  |
                  v
Bottom-up DP: O(mn) time and O(mn) space
```

## Optimized / CP approach: Bottom-up DP

### Algorithm

1. Create a `(m + 1) x (n + 1)` table.
2. Initialize `dp[i][0] = i` deletions and `dp[0][j] = j` insertions.
3. Fill the table using the recurrence above.
4. Return `dp[m][n]`.

### Complexity

- Time: `O(mn)`
- Space: `O(mn)`

## Pattern to remember

```text
Minimum operations to transform one sequence into another
        => DP over two prefixes

Base row = insert everything
Base col = delete everything
```

## C++

```cpp
class Solution {
   public:
    int minDistance(string word1, string word2) {
        int rows = word1.size();
        int columns = word2.size();
        vector<vector<int>> dp(rows + 1, vector<int>(columns + 1, 0));

        for (int row = 0; row <= rows; ++row) {
            dp[row][0] = row;
        }
        for (int column = 0; column <= columns; ++column) {
            dp[0][column] = column;
        }

        for (int row = 1; row <= rows; ++row) {
            for (int column = 1; column <= columns; ++column) {
                if (word1[row - 1] == word2[column - 1]) {
                    dp[row][column] = dp[row - 1][column - 1];
                } else {
                    dp[row][column] =
                        1 + min({dp[row - 1][column], dp[row][column - 1],
                                 dp[row - 1][column - 1]});
                }
            }
        }
        return dp[rows][columns];
    }
};
```

## Python

```python
class Solution:
    def min_distance(self, word1: str, word2: str) -> int:
        rows = len(word1)
        columns = len(word2)
        dp = [[0] * (columns + 1) for _ in range(rows + 1)]

        for row in range(rows + 1):
            dp[row][0] = row
        for column in range(columns + 1):
            dp[0][column] = column

        for row in range(1, rows + 1):
            for column in range(1, columns + 1):
                if word1[row - 1] == word2[column - 1]:
                    dp[row][column] = dp[row - 1][column - 1]
                else:
                    dp[row][column] = 1 + min(
                        dp[row - 1][column],
                        dp[row][column - 1],
                        dp[row - 1][column - 1],
                    )

        return dp[rows][columns]
```

## Java

```java
class Solution {
    public int minDistance(String word1, String word2) {
        int rows = word1.length();
        int columns = word2.length();
        int[][] dp = new int[rows + 1][columns + 1];

        for (int row = 0; row <= rows; row++) {
            dp[row][0] = row;
        }
        for (int column = 0; column <= columns; column++) {
            dp[0][column] = column;
        }

        for (int row = 1; row <= rows; row++) {
            for (int column = 1; column <= columns; column++) {
                if (word1.charAt(row - 1) == word2.charAt(column - 1)) {
                    dp[row][column] = dp[row - 1][column - 1];
                } else {
                    int insert = dp[row][column - 1];
                    int delete = dp[row - 1][column];
                    int replace = dp[row - 1][column - 1];
                    dp[row][column] = 1 + Math.min(insert, Math.min(delete, replace));
                }
            }
        }
        return dp[rows][columns];
    }
}
```

## Go

```go
func minDistance(word1, word2 string) int {
	rows, columns := len(word1), len(word2)
	dp := make([][]int, rows+1)
	for row := range dp {
		dp[row] = make([]int, columns+1)
		dp[row][0] = row
	}
	for column := 0; column <= columns; column++ {
		dp[0][column] = column
	}

	for row := 1; row <= rows; row++ {
		for column := 1; column <= columns; column++ {
			if word1[row-1] == word2[column-1] {
				dp[row][column] = dp[row-1][column-1]
			} else {
				dp[row][column] = 1 + min(
					dp[row-1][column],
					dp[row][column-1],
					dp[row-1][column-1],
				)
			}
		}
	}
	return dp[rows][columns]
}
```

## Common mistakes

- Forgetting the empty-string base cases.
- Mixing prefix indices with string indices (`i` uses `word1[i - 1]`).
- Adding one when the final characters already match.
