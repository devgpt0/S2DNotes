# Longest Common Subsequence (LCS)

## Idea

A subsequence keeps order but may skip characters. `dp[i][j]` stores the LCS
length of the first `i` characters of one string and first `j` of the other.

## Visual model

```text
equal final characters -> diagonal + 1
different characters   -> skip one final character from either string
```

## Classroom board: compare final characters

```text
first = "ab", second = "acb"
final b == b -> keep b and solve prefixes "a" and "ac"
their LCS is "a"
result length = 1 + 1 = 2 ("ab")
```

When final characters differ, try skipping either one; at least one skip must
appear in an optimal answer.

## Steps

1. Create a `(firstLength + 1) x (secondLength + 1)` zero table.
2. Visit prefixes in increasing length.
3. On equality, extend `dp[i-1][j-1]`.
4. Otherwise take `max(dp[i-1][j], dp[i][j-1])`.

## First-principles derivation

For two prefixes, if their last characters match, an optimal common subsequence
can extend by that character. Otherwise at least one last character is unused,
so try removing either one.

The state `dp[i][j]` contains all information needed for the first `i` and
first `j` characters.

## Pattern recognition

Use it for order-preserving similarity, minimum insert/delete transformations,
or sequence alignment without requiring contiguous matches.

## Implementation

### C++

```cpp
int lcsLength(const std::string& first, const std::string& second) {
    std::vector<int> previous(second.size() + 1), current(second.size() + 1);
    for (char left : first) {
        for (int column = 1; column <= static_cast<int>(second.size()); ++column) {
            if (left == second[column - 1]) current[column] = previous[column - 1] + 1;
            else current[column] = std::max(previous[column], current[column - 1]);
        }
        std::swap(previous, current);
    }
    return previous.back();
}
```

### Python

```python
def lcs_length(first: str, second: str) -> int:
    previous = [0] * (len(second) + 1)
    for left in first:
        current = [0] * (len(second) + 1)
        for column, right in enumerate(second, start=1):
            if left == right:
                current[column] = previous[column - 1] + 1
            else:
                current[column] = max(previous[column], current[column - 1])
        previous = current
    return previous[-1]
```

### Java

```java
static int lcsLength(String first, String second) {
    int[] previous = new int[second.length() + 1];
    int[] current = new int[second.length() + 1];
    for (int row = 1; row <= first.length(); row++) {
        Arrays.fill(current, 0);
        for (int column = 1; column <= second.length(); column++) {
            if (first.charAt(row - 1) == second.charAt(column - 1)) current[column] = previous[column - 1] + 1;
            else current[column] = Math.max(previous[column], current[column - 1]);
        }
        int[] temporary = previous;
        previous = current;
        current = temporary;
    }
    return previous[second.length()];
}
```

## Why it works

If final characters match, some optimal LCS can use them. Otherwise an optimal
answer skips at least one of them, and both skip choices are compared.

## Complexity

Time is `O(nm)` and extra space is `O(m)`.

## Common mistakes

- Confusing subsequence with substring.
- Reusing a one-dimensional array in the wrong direction.
- Expecting compressed DP to reconstruct the actual sequence without storing
  choices or recomputing.
