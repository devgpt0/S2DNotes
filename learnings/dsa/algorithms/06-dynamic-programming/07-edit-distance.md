# Edit Distance

## Idea

Edit distance is the minimum number of insertions, deletions, and replacements
needed to change one string into another.

## Visual model

For prefix lengths `i` and `j`:

```text
same final character -> dp[i-1][j-1]
otherwise 1 + min(insert, delete, replace)
```

## Classroom board: change `cat` to `cut`

```text
c matches c -> no edit
a differs u -> replace a with u (one edit)
t matches t -> no edit
answer = 1
```

At a mismatch, DP also checks whether inserting or deleting leads to fewer
total edits.

## Steps

1. Transforming an empty prefix costs the other prefix's length.
2. Process both prefix lengths in increasing order.
3. Copy the diagonal cost when final characters match.
4. Otherwise add one to the best of insertion, deletion, and replacement.

## First-principles derivation

To transform two prefixes, examine their final characters. Equal characters
need no operation; unequal characters end with exactly one insertion,
deletion, or replacement.

Each operation reduces the problem to a smaller pair of prefixes, producing
the DP transition.

## Pattern recognition

Use it for minimum edits between sequences, fuzzy matching, or alignment where
the allowed local operations have costs.

## Implementation

### C++

```cpp
int editDistance(const std::string& source, const std::string& target) {
    std::vector<int> previous(target.size() + 1);
    std::iota(previous.begin(), previous.end(), 0);
    for (int row = 1; row <= static_cast<int>(source.size()); ++row) {
        std::vector<int> current(target.size() + 1);
        current[0] = row;
        for (int column = 1; column <= static_cast<int>(target.size()); ++column) {
            if (source[row - 1] == target[column - 1]) current[column] = previous[column - 1];
            else current[column] = 1 + std::min({current[column - 1], previous[column], previous[column - 1]});
        }
        previous = std::move(current);
    }
    return previous.back();
}
```

### Python

```python
def edit_distance(source: str, target: str) -> int:
    previous = list(range(len(target) + 1))
    for row, source_character in enumerate(source, start=1):
        current = [row] + [0] * len(target)
        for column, target_character in enumerate(target, start=1):
            if source_character == target_character:
                current[column] = previous[column - 1]
            else:
                current[column] = 1 + min(
                    current[column - 1],
                    previous[column],
                    previous[column - 1],
                )
        previous = current
    return previous[-1]
```

### Java

```java
static int editDistance(String source, String target) {
    int[] previous = new int[target.length() + 1];
    for (int column = 0; column <= target.length(); column++) previous[column] = column;
    for (int row = 1; row <= source.length(); row++) {
        int[] current = new int[target.length() + 1];
        current[0] = row;
        for (int column = 1; column <= target.length(); column++) {
            if (source.charAt(row - 1) == target.charAt(column - 1)) current[column] = previous[column - 1];
            else current[column] = 1 + Math.min(current[column - 1], Math.min(previous[column], previous[column - 1]));
        }
        previous = current;
    }
    return previous[target.length()];
}
```

## Why it works

Every optimal transformation ends in exactly one of four cases: matching
characters, insertion, deletion, or replacement. The transition tries all of
them.

## Complexity

Time is `O(nm)` and extra space is `O(m)`.

## Common mistakes

- Mixing the meaning of insertion and deletion table neighbors.
- Forgetting empty-prefix base cases.
- Using unit-cost DP when operations have different costs.
