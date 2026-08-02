# Fenwick Tree (Binary Indexed Tree)

## Idea

A Fenwick tree stores partial sums. It supports point additions and prefix sums
in `O(log n)` with less code and memory than a segment tree.

## Visual model

`index & -index` gives the size of the range owned by a 1-based tree index.

```text
index 12 = 1100₂ -> lowbit = 0100₂ = 4 -> owns four values
```

## Classroom board: prefix sum as blocks

```text
Want sum of first 7 values. Internal index 7 = 0111₂.
take tree[7] (block size 1), move 7 -> 6
take tree[6] (block size 2), move 6 -> 4
take tree[4] (block size 4), move 4 -> 0

1 + 2 + 4 values = exactly the first 7 values
```

The lowest set bit tells the size of the block owned by an internal index.

## Steps

1. Use 1-based internal indices.
2. To add at an index, repeatedly move upward with `i += i & -i`.
3. To read a prefix, repeatedly move to the previous block with
   `i -= i & -i`.
4. Compute `[left, right)` as `prefix(right) - prefix(left)`.

## First-principles derivation

A prefix sum answers queries quickly but updates slowly. A Fenwick tree stores
carefully chosen power-of-two suffix blocks so one update changes only
`O(log n)` blocks.

A prefix query repeatedly removes its lowest set bit, decomposing the prefix
into disjoint stored blocks.

## Pattern recognition

Use it for many point updates plus prefix/range sum queries, inversion counts,
or frequency/order queries after coordinate compression.

## Implementation

### C++

```cpp
class FenwickTree {
   public:
    explicit FenwickTree(int size) : tree_(size + 1, 0) {}

    void add(int index, long long delta) {
        for (int current = index + 1; current < static_cast<int>(tree_.size()); current += current & -current) {
            tree_[current] += delta;
        }
    }

    long long prefixSum(int end) const {
        long long sum = 0;
        for (int current = end; current > 0; current -= current & -current) sum += tree_[current];
        return sum;
    }

    long long rangeSum(int left, int right) const {
        return prefixSum(right) - prefixSum(left);
    }

   private:
    std::vector<long long> tree_;
};
```

### Python

```python
class FenwickTree:
    def __init__(self, size: int) -> None:
        self.tree = [0] * (size + 1)

    def add(self, index: int, delta: int) -> None:
        index += 1
        while index < len(self.tree):
            self.tree[index] += delta
            index += index & -index

    def prefix_sum(self, end: int) -> int:
        total = 0
        while end > 0:
            total += self.tree[end]
            end -= end & -end
        return total

    def range_sum(self, left: int, right: int) -> int:
        return self.prefix_sum(right) - self.prefix_sum(left)
```

### Java

```java
final class FenwickTree {
    private final long[] tree;

    FenwickTree(int size) {
        tree = new long[size + 1];
    }

    void add(int index, long delta) {
        for (int current = index + 1; current < tree.length; current += current & -current) {
            tree[current] += delta;
        }
    }

    long prefixSum(int end) {
        long sum = 0;
        for (int current = end; current > 0; current -= current & -current) sum += tree[current];
        return sum;
    }

    long rangeSum(int left, int right) {
        return prefixSum(right) - prefixSum(left);
    }
}
```

## Why it works

The visited tree blocks are disjoint and exactly cover the prefix. Updates
visit every larger block that contains the changed position.

## Complexity

Update and query are `O(log n)`; space is `O(n)`.

## Common mistakes

- Mixing the zero-based public index with the one-based internal index.
- Calling `prefixSum(end)` as if `end` were inclusive; here it is exclusive.
- Using it for arbitrary range minimum, whose inverse operation does not exist.
