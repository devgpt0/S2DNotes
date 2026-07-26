# Problem 27: Longest Common Subsequence (LeetCode #1143)

**Difficulty:** Medium  
**Core pattern:** Two-string dynamic programming

## Problem statement

Return the length of the longest sequence that appears in both strings while
preserving order. Characters do not need to be adjacent.

## Example

```text
text1 = "abcde"
text2 = "ace"

a b c d e
|   |   |
a   c   e

LCS = "ace", length = 3
```

## Observation

At state `(i, j)`:

- if `text1[i] == text2[j]`, use that character and move both indices;
- otherwise, skip one character from either string and take the better result.

```text
equal:      dp[i][j] = 1 + dp[i+1][j+1]
different:  dp[i][j] = max(dp[i+1][j], dp[i][j+1])
```

## DP table direction

```text
dp[i][j] depends on:

      dp[i][j] -> dp[i][j+1]
          |
          v
      dp[i+1][j] and dp[i+1][j+1]

Therefore fill from bottom-right toward top-left.
```

## Solution 1: Enumerate Subsequences

### Observation

Generate subsequences of one string and test them against the other. This takes
exponential time.

### Algorithm

1. Recursively choose or skip each character from the first string.
2. At a complete subsequence, test whether it appears in the second string.
3. Keep the largest valid length.

### C++ code

```cpp
class Solution {
   private:
    bool isSubsequence(const string& candidate, const string& text) {
        int index = 0;
        for (char character : text) {
            if (index < static_cast<int>(candidate.size()) &&
                candidate[index] == character) {
                ++index;
            }
        }
        return index == static_cast<int>(candidate.size());
    }

    void generate(const string& first, const string& second, int index,
                  string& candidate, int& best) {
        if (index == static_cast<int>(first.size())) {
            if (isSubsequence(candidate, second)) {
                best = max(best, static_cast<int>(candidate.size()));
            }
            return;
        }

        generate(first, second, index + 1, candidate, best);
        candidate.push_back(first[index]);
        generate(first, second, index + 1, candidate, best);
        candidate.pop_back();
    }

   public:
    int longestCommonSubsequence(string first, string second) {
        string candidate;
        int best = 0;
        generate(first, second, 0, candidate, best);
        return best;
    }
};
```

### Complexity

- Time: `O(2^m * n)`
- Space: `O(m)` recursion space

## How we derive the optimal solution

```text
Generate every subsequence
          |
          v
Many choices reach the same pair of remaining suffixes
          |
          v
Define state (i, j): LCS of suffixes starting at i and j
          |
          v
Equal characters -> take both; otherwise skip one side
          |
          v
Memoization or bottom-up DP: O(mn)
```

## Optimized / CP approach: Bottom-up DP

### Algorithm

1. Create `(m + 1) x (n + 1)` zero-filled DP table.
2. Iterate `i` and `j` backward.
3. Use the equal/different recurrence above.
4. Return `dp[0][0]`.

### Complexity

- Time: `O(mn)`
- Space: `O(mn)`

## Pattern to remember

```text
Two sequences + preserve order + choose/skip items
        => 2D dynamic programming

characters equal     -> take both
characters different -> skip from one side
```

## C++

```cpp
class Solution {
   public:
    int longestCommonSubsequence(string first, string second) {
        int rows = first.size();
        int columns = second.size();
        vector<vector<int>> dp(rows + 1, vector<int>(columns + 1, 0));

        for (int row = rows - 1; row >= 0; --row) {
            for (int column = columns - 1; column >= 0; --column) {
                if (first[row] == second[column]) {
                    dp[row][column] = 1 + dp[row + 1][column + 1];
                } else {
                    dp[row][column] =
                        max(dp[row + 1][column], dp[row][column + 1]);
                }
            }
        }
        return dp[0][0];
    }
};
```

## Python

```python
class Solution:
    def longest_common_subsequence(self, first: str, second: str) -> int:
        rows = len(first)
        columns = len(second)
        dp = [[0] * (columns + 1) for _ in range(rows + 1)]

        for row in range(rows - 1, -1, -1):
            for column in range(columns - 1, -1, -1):
                if first[row] == second[column]:
                    dp[row][column] = 1 + dp[row + 1][column + 1]
                else:
                    dp[row][column] = max(
                        dp[row + 1][column],
                        dp[row][column + 1],
                    )

        return dp[0][0]
```

## Java

```java
class Solution {
    public int longestCommonSubsequence(String first, String second) {
        int rows = first.length();
        int columns = second.length();
        int[][] dp = new int[rows + 1][columns + 1];

        for (int row = rows - 1; row >= 0; row--) {
            for (int column = columns - 1; column >= 0; column--) {
                if (first.charAt(row) == second.charAt(column)) {
                    dp[row][column] = 1 + dp[row + 1][column + 1];
                } else {
                    dp[row][column] = Math.max(dp[row + 1][column], dp[row][column + 1]);
                }
            }
        }
        return dp[0][0];
    }
}
```

## Go

```go
func longestCommonSubsequence(first, second string) int {
	rows, columns := len(first), len(second)
	dp := make([][]int, rows+1)
	for row := range dp {
		dp[row] = make([]int, columns+1)
	}

	for row := rows - 1; row >= 0; row-- {
		for column := columns - 1; column >= 0; column-- {
			if first[row] == second[column] {
				dp[row][column] = 1 + dp[row+1][column+1]
			} else {
				dp[row][column] = max(
					dp[row+1][column],
					dp[row][column+1],
				)
			}
		}
	}
	return dp[0][0]
}
```

## Common mistakes

- Confusing subsequences with substrings.
- Moving both indices when characters differ.
- Filling the DP table before its dependent cells are available.
