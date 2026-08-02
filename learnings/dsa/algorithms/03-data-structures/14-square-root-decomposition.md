# Square-Root Decomposition

## Idea

Split an array into blocks of about `sqrt(n)` values and store one answer per
block. A query uses whole blocks plus a few edge values.

## Visual model

```text
[edge values | whole block | whole block | edge values]
```

## Classroom board: query with blocks of size 3

```text
indexes: 0 1 2 | 3 4 5 | 6 7 8 | 9
query [1,9)

scan edge indexes 1,2
take whole blocks [3,6) and [6,9)
no right edge remains
```

At most about one block is scanned at each edge; middle blocks use one stored
answer each.

## Steps

1. Choose block size near `sqrt(n)`.
2. Build each block's sum.
3. For a query, scan until aligned, use whole blocks, then scan the remaining
   edge.
4. For a point update, change both the value and its block sum.

## First-principles derivation

Scanning every element is slow, while maintaining a full tree may be
unnecessary. Split the array into about `sqrt(n)` blocks and precompute one
answer per block.

A query scans two partial boundary blocks and reuses every complete middle
block.

## Pattern recognition

Use it when a segment tree is unnecessary, when `O(sqrt(n))` per operation is
fast enough, or when block-level lazy ideas simplify a problem.

## Implementation: point update and range sum

### C++

```cpp
class SqrtDecomposition {
   public:
    explicit SqrtDecomposition(std::vector<long long> values)
        : values_(std::move(values)), blockSize_(std::sqrt(values_.size()) + 1),
          blocks_((values_.size() + blockSize_ - 1) / blockSize_, 0) {
        for (int index = 0; index < static_cast<int>(values_.size()); ++index) blocks_[index / blockSize_] += values_[index];
    }

    void set(int index, long long value) {
        blocks_[index / blockSize_] += value - values_[index];
        values_[index] = value;
    }

    long long query(int left, int right) const {
        long long sum = 0;
        while (left < right && left % blockSize_ != 0) sum += values_[left++];
        while (left + blockSize_ <= right) {
            sum += blocks_[left / blockSize_];
            left += blockSize_;
        }
        while (left < right) sum += values_[left++];
        return sum;
    }

   private:
    std::vector<long long> values_;
    int blockSize_;
    std::vector<long long> blocks_;
};
```

### Python

```python
from math import isqrt


class SqrtDecomposition:
    def __init__(self, values: list[int]) -> None:
        self.values = values.copy()
        self.block_size = isqrt(len(values)) + 1
        self.blocks = [0] * ((len(values) + self.block_size - 1) // self.block_size)
        for index, value in enumerate(values):
            self.blocks[index // self.block_size] += value

    def set(self, index: int, value: int) -> None:
        self.blocks[index // self.block_size] += value - self.values[index]
        self.values[index] = value

    def query(self, left: int, right: int) -> int:
        total = 0
        while left < right and left % self.block_size != 0:
            total += self.values[left]
            left += 1
        while left + self.block_size <= right:
            total += self.blocks[left // self.block_size]
            left += self.block_size
        while left < right:
            total += self.values[left]
            left += 1
        return total
```

### Java

```java
final class SqrtDecomposition {
    private final long[] values;
    private final int blockSize;
    private final long[] blocks;

    SqrtDecomposition(long[] input) {
        values = input.clone();
        blockSize = (int) Math.sqrt(values.length) + 1;
        blocks = new long[(values.length + blockSize - 1) / blockSize];
        for (int index = 0; index < values.length; index++) blocks[index / blockSize] += values[index];
    }

    void set(int index, long value) {
        blocks[index / blockSize] += value - values[index];
        values[index] = value;
    }

    long query(int left, int right) {
        long sum = 0;
        while (left < right && left % blockSize != 0) sum += values[left++];
        while (left + blockSize <= right) {
            sum += blocks[left / blockSize];
            left += blockSize;
        }
        while (left < right) sum += values[left++];
        return sum;
    }
}
```

## Why it works

The scanned edge values and selected whole blocks are disjoint and exactly
cover the query range.

## Complexity

Build is `O(n)`, point update is `O(1)`, range query is `O(sqrt(n))`, and space
is `O(n)`.

## Common mistakes

- Double-counting an edge and its block.
- Forgetting to update the block summary.
- Using a block size of zero for empty input; define a non-empty contract.
