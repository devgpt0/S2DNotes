# Segment Tree

## Idea

A segment tree stores an answer for every recursively split range. It supports
point updates and range queries in `O(log n)`.

## Visual model

```text
                 [0, 8)
             /             \
          [0, 4)          [4, 8)
         /      \         /      \
      [0, 2)  [2, 4)   [4, 6)  [6, 8)
```

## Classroom board: query `[2, 7)`

```text
root [0,8) only partly overlaps -> split
left [0,4) partly overlaps      -> use full node [2,4)
right [4,8) partly overlaps     -> use full node [4,6) + leaf [6,7)

chosen nodes [2,4), [4,6), [6,7) are disjoint
and together cover exactly [2,7)
```

We never visit individual values inside a node that is fully covered.

## Steps

1. Put array values in leaves.
2. Combine two children to build each parent.
3. For a query, ignore disjoint nodes, use fully covered nodes, and split
   partially covered nodes.
4. For an update, change one leaf and rebuild its ancestors.

## First-principles derivation

Store answers for recursively split ranges. A query can then reuse a whole
stored node whenever its range is fully covered.

The chosen nodes are disjoint and their ranges combine to exactly the requested
range; an update rebuilds only ancestors containing the changed index.

## Pattern recognition

Use it for interleaved updates and associative range queries such as sum,
minimum, maximum, GCD, or a custom combined state.

## Implementation: iterative range sum

### C++

```cpp
class SegmentTree {
   public:
    explicit SegmentTree(const std::vector<int>& values)
        : size_(values.size()), tree_(2 * values.size(), 0) {
        for (int index = 0; index < size_; ++index) tree_[size_ + index] = values[index];
        for (int index = size_ - 1; index > 0; --index) tree_[index] = tree_[2 * index] + tree_[2 * index + 1];
    }

    void set(int index, long long value) {
        index += size_;
        tree_[index] = value;
        while (index > 1) {
            index /= 2;
            tree_[index] = tree_[2 * index] + tree_[2 * index + 1];
        }
    }

    long long query(int left, int right) const {
        long long sum = 0;
        for (left += size_, right += size_; left < right; left /= 2, right /= 2) {
            if (left % 2 == 1) sum += tree_[left++];
            if (right % 2 == 1) sum += tree_[--right];
        }
        return sum;
    }

   private:
    int size_;
    std::vector<long long> tree_;
};
```

### Python

```python
class SegmentTree:
    def __init__(self, values: list[int]) -> None:
        self.size = len(values)
        self.tree = [0] * self.size + values.copy()
        for index in range(self.size - 1, 0, -1):
            self.tree[index] = self.tree[2 * index] + self.tree[2 * index + 1]

    def set(self, index: int, value: int) -> None:
        index += self.size
        self.tree[index] = value
        while index > 1:
            index //= 2
            self.tree[index] = self.tree[2 * index] + self.tree[2 * index + 1]

    def query(self, left: int, right: int) -> int:
        left += self.size
        right += self.size
        total = 0
        while left < right:
            if left & 1:
                total += self.tree[left]
                left += 1
            if right & 1:
                right -= 1
                total += self.tree[right]
            left //= 2
            right //= 2
        return total
```

### Java

```java
final class SegmentTree {
    private final int size;
    private final long[] tree;

    SegmentTree(int[] values) {
        size = values.length;
        tree = new long[2 * size];
        for (int index = 0; index < size; index++) tree[size + index] = values[index];
        for (int index = size - 1; index > 0; index--) tree[index] = tree[2 * index] + tree[2 * index + 1];
    }

    void set(int index, long value) {
        index += size;
        tree[index] = value;
        while (index > 1) {
            index /= 2;
            tree[index] = tree[2 * index] + tree[2 * index + 1];
        }
    }

    long query(int left, int right) {
        long sum = 0;
        for (left += size, right += size; left < right; left /= 2, right /= 2) {
            if ((left & 1) == 1) sum += tree[left++];
            if ((right & 1) == 1) sum += tree[--right];
        }
        return sum;
    }
}
```

## Why it works

The selected tree nodes are disjoint and exactly cover `[left, right)`. An
update changes only nodes whose ranges contain that position.

## Complexity

Build is `O(n)`; update and query are `O(log n)`; space is `O(n)`.

## Common mistakes

- Mixing inclusive and half-open queries.
- Using the wrong identity (`0` for sum, infinity for minimum).
- Combining children in the wrong order for non-commutative states.
