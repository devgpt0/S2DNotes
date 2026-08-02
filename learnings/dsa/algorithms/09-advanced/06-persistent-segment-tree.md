# Persistent Segment Tree

## Idea

A persistent data structure keeps old versions. A segment-tree update copies
only nodes on one root-to-leaf path and shares every unchanged node.

## Visual model

```text
old root ---- unchanged subtree (shared)
    \
new root ---- copied path ---- new leaf count
```

## Classroom board: copy only the changed path

```text
version 1 adds rank 2
version 2 adds rank 5
version 2 copies root->rank5 leaf nodes
every untouched subtree is shared with version 1
old version 1 still answers exactly the old prefix
```

## Steps for range k-th smallest

1. Coordinate-compress array values to ranks.
2. Build one root per array prefix; add the new rank to the previous root.
3. For query `[left, right)`, subtract counts of roots `right` and `left`.
4. Descend left or right according to how many range values lie in the left
   child.

## First-principles derivation

An update changes only one root-to-leaf path in a segment tree. Copy those
`O(log n)` nodes and share every untouched subtree with the previous version.

Each root is an immutable snapshot; subtracting two prefix-version frequency
trees isolates one subarray.

## Classroom board: range k-th smallest

Values are `[2,1,3]`, compressed to ranks `[2,1,3]`.

```text
root0: counts {}
root1: add 2 -> {2:1}
root2: add 1 -> {1:1,2:1}
root3: add 3 -> {1:1,2:1,3:1}

query subarray [1,3): values [1,3]
frequency tree = root3 - root1
               = {1:1, 2:0, 3:1}

k=2:
left half contains one value, so skip it
second smallest rank is 3 -> value 3
```

Old roots remain unchanged because new versions copy rather than mutate their
update path.

## Pattern recognition

Use persistence for queries over historical versions or immutable prefixes,
especially k-th/frequency queries on subarrays.

## Implementation: ranks in `[0, valueCount)`

### C++

```cpp
class PersistentSegmentTree {
    struct Node { int left = 0; int right = 0; int count = 0; };
   public:
    explicit PersistentSegmentTree(int valueCount) : valueCount_(valueCount), nodes_(1), roots_{0} {}
    void append(int rank) { roots_.push_back(update(roots_.back(), 0, valueCount_, rank)); }
    int kth(int left, int right, int k) const { return kth(roots_[left], roots_[right], 0, valueCount_, k); }
   private:
    int valueCount_;
    std::vector<Node> nodes_;
    std::vector<int> roots_;
    int update(int previous, int start, int end, int rank) {
        int current = nodes_.size();
        nodes_.push_back(nodes_[previous]);
        ++nodes_[current].count;
        if (end - start > 1) {
            int middle = start + (end - start) / 2;
            if (rank < middle) nodes_[current].left = update(nodes_[previous].left, start, middle, rank);
            else nodes_[current].right = update(nodes_[previous].right, middle, end, rank);
        }
        return current;
    }
    int kth(int leftRoot, int rightRoot, int start, int end, int k) const {
        if (end - start == 1) return start;
        int leftCount = nodes_[nodes_[rightRoot].left].count - nodes_[nodes_[leftRoot].left].count;
        int middle = start + (end - start) / 2;
        if (k <= leftCount) return kth(nodes_[leftRoot].left, nodes_[rightRoot].left, start, middle, k);
        return kth(nodes_[leftRoot].right, nodes_[rightRoot].right, middle, end, k - leftCount);
    }
};
```

### Python

```python
class PersistentSegmentTree:
    def __init__(self, value_count: int) -> None:
        self.value_count = value_count
        self.left = [0]
        self.right = [0]
        self.count = [0]
        self.roots = [0]

    def append(self, rank: int) -> None:
        self.roots.append(self._update(self.roots[-1], 0, self.value_count, rank))

    def _update(self, previous: int, start: int, end: int, rank: int) -> int:
        current = len(self.count)
        self.left.append(self.left[previous])
        self.right.append(self.right[previous])
        self.count.append(self.count[previous] + 1)
        if end - start > 1:
            middle = start + (end - start) // 2
            if rank < middle:
                self.left[current] = self._update(self.left[previous], start, middle, rank)
            else:
                self.right[current] = self._update(self.right[previous], middle, end, rank)
        return current

    def kth(self, left: int, right: int, k: int) -> int:
        return self._kth(self.roots[left], self.roots[right], 0, self.value_count, k)

    def _kth(self, left_root: int, right_root: int, start: int, end: int, k: int) -> int:
        if end - start == 1:
            return start
        left_count = self.count[self.left[right_root]] - self.count[self.left[left_root]]
        middle = start + (end - start) // 2
        if k <= left_count:
            return self._kth(self.left[left_root], self.left[right_root], start, middle, k)
        return self._kth(self.right[left_root], self.right[right_root], middle, end, k - left_count)
```

### Java

```java
final class PersistentSegmentTree {
    private record Node(Node left, Node right, int count) {}
    private final int valueCount;
    private final List<Node> roots = new ArrayList<>();

    PersistentSegmentTree(int valueCount) {
        this.valueCount = valueCount;
        roots.add(null);
    }
    void append(int rank) { roots.add(update(roots.get(roots.size() - 1), 0, valueCount, rank)); }
    int kth(int left, int right, int k) { return kth(roots.get(left), roots.get(right), 0, valueCount, k); }

    private Node update(Node previous, int start, int end, int rank) {
        Node left = previous == null ? null : previous.left();
        Node right = previous == null ? null : previous.right();
        int count = (previous == null ? 0 : previous.count()) + 1;
        if (end - start == 1) return new Node(left, right, count);
        int middle = start + (end - start) / 2;
        if (rank < middle) left = update(left, start, middle, rank);
        else right = update(right, middle, end, rank);
        return new Node(left, right, count);
    }

    private int kth(Node leftRoot, Node rightRoot, int start, int end, int k) {
        if (end - start == 1) return start;
        int leftCount = count(rightRoot == null ? null : rightRoot.left()) - count(leftRoot == null ? null : leftRoot.left());
        int middle = start + (end - start) / 2;
        if (k <= leftCount) return kth(leftRoot == null ? null : leftRoot.left(), rightRoot == null ? null : rightRoot.left(), start, middle, k);
        return kth(leftRoot == null ? null : leftRoot.right(), rightRoot == null ? null : rightRoot.right(), middle, end, k - leftCount);
    }

    private int count(Node node) { return node == null ? 0 : node.count(); }
}
```

## Why it works

Root `i` contains frequencies of the first `i` array values. Subtracting two
roots leaves exactly the query range's frequencies; descending by counts finds
the k-th rank.

## Complexity

Each append and k-th query is `O(log valueCount)`. Total space is
`O(numberOfAppends * log valueCount)`.

## Common mistakes

- Passing zero-based `k`; this implementation expects `1 <= k <= range length`.
- Returning a rank without mapping it back to the original value.
- Mutating shared nodes and destroying older versions.
