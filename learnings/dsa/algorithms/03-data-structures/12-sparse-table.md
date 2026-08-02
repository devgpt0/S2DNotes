# Sparse Table

## Idea

A sparse table answers idempotent static range queries, especially minimum or
maximum, in `O(1)` after `O(n log n)` preprocessing.

## Visual model

`table[level][start]` stores a block of length `2^level`.

```text
query [left, right) = min(block starting left, block ending right)
```

The two blocks may overlap because `min(x, x) = x`.

## Classroom board: minimum of `[1, 7)`

The range length is `6`; the largest power of two not exceeding it is `4`.

```text
left block:  [1,5) length 4
right block: [3,7) length 4
union covers [1,7); middle overlaps

minimum = min(min[1,5), min[3,7))
```

Overlap is harmless for minimum: seeing the same value twice cannot change it.

## Steps

1. Store single values at level `0`.
2. Build each larger block from two half-sized blocks.
3. For a query, choose the largest power of two not exceeding its length.
4. Combine the block at the left edge and the block at the right edge.

## First-principles derivation

For an immutable array, precompute answers for every power-of-two interval.
Any range can be composed from a small number of those blocks.

For idempotent operations such as minimum, two overlapping blocks are safe
because combining the same element twice does not change the answer.

## Pattern recognition

Use it for many immutable range min/max/GCD queries. Do not use this overlapping
query for sum, because duplicated values would be counted twice.

## Implementation: range minimum

### C++

```cpp
class SparseTable {
   public:
    explicit SparseTable(const std::vector<int>& values) : logarithm_(values.size() + 1) {
        for (int length = 2; length <= static_cast<int>(values.size()); ++length) logarithm_[length] = logarithm_[length / 2] + 1;
        table_.push_back(values);
        for (int level = 1; (1 << level) <= static_cast<int>(values.size()); ++level) {
            const int length = 1 << level;
            table_.push_back(std::vector<int>(values.size() - length + 1));
            for (int start = 0; start + length <= static_cast<int>(values.size()); ++start) {
                table_[level][start] = std::min(table_[level - 1][start], table_[level - 1][start + length / 2]);
            }
        }
    }

    int query(int left, int right) const {
        const int level = logarithm_[right - left];
        return std::min(table_[level][left], table_[level][right - (1 << level)]);
    }

   private:
    std::vector<int> logarithm_;
    std::vector<std::vector<int>> table_;
};
```

### Python

```python
class SparseTable:
    def __init__(self, values: list[int]) -> None:
        self.logarithm = [0] * (len(values) + 1)
        for length in range(2, len(values) + 1):
            self.logarithm[length] = self.logarithm[length // 2] + 1
        self.table = [values.copy()]
        level = 1
        while 1 << level <= len(values):
            length = 1 << level
            previous = self.table[level - 1]
            self.table.append([
                min(previous[start], previous[start + length // 2])
                for start in range(len(values) - length + 1)
            ])
            level += 1

    def query(self, left: int, right: int) -> int:
        level = self.logarithm[right - left]
        return min(self.table[level][left], self.table[level][right - (1 << level)])
```

### Java

```java
final class SparseTable {
    private final int[] logarithm;
    private final int[][] table;

    SparseTable(int[] values) {
        logarithm = new int[values.length + 1];
        for (int length = 2; length <= values.length; length++) logarithm[length] = logarithm[length / 2] + 1;
        table = new int[logarithm[values.length] + 1][];
        table[0] = values.clone();
        for (int level = 1; level < table.length; level++) {
            int length = 1 << level;
            table[level] = new int[values.length - length + 1];
            for (int start = 0; start + length <= values.length; start++) {
                table[level][start] = Math.min(table[level - 1][start], table[level - 1][start + length / 2]);
            }
        }
    }

    int query(int left, int right) {
        int level = logarithm[right - left];
        return Math.min(table[level][left], table[level][right - (1 << level)]);
    }
}
```

## Why it works

The two chosen blocks cover the whole query. Overlap cannot change an
idempotent result such as minimum.

## Complexity

Build time and space are `O(n log n)`; each query is `O(1)`.

## Common mistakes

- Querying an empty range.
- Using overlapping blocks for sum.
- Choosing a sparse table when updates are required.
