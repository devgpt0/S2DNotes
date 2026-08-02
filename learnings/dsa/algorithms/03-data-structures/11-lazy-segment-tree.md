# Lazy Segment Tree

## Idea

Lazy propagation lets a segment tree update a whole range without visiting
every leaf. A node stores a pending update that will be passed to children only
when needed.

## Visual model

```text
update fully covers node -> update node sum + store lazy value
later partial visit      -> push lazy value to both children
```

## Classroom board: delay work safely

```text
add 5 to the whole node range [0,4)
node sum increases by 5 * 4 = 20
store lazy +5; do not visit four leaves

later query [0,2):
push +5 to children [0,2) and [2,4)
read the needed child; the other child remains summarized
```

“Lazy” means postponed, not forgotten.

## Steps

1. Return for a disjoint node.
2. For full coverage, update the node and record the pending addition.
3. For partial coverage, push pending work, recurse, then recompute the parent.
4. Queries follow the same disjoint/full/partial split.

## First-principles derivation

A range update touches many leaves, but a fully covered node already represents
all of them. Store the pending operation on that node and delay child work
until a child is needed.

Each node's visible answer includes its pending update, even when descendants
have not yet received it.

## Pattern recognition

Use it when range updates and range queries are interleaved, such as adding to
every value in a range and asking range sums.

## Implementation: range add and range sum

### C++

```cpp
class LazySegmentTree {
   public:
    explicit LazySegmentTree(int size) : size_(size), tree_(4 * size), lazy_(4 * size) {}

    void add(int left, int right, long long delta) { add(1, 0, size_, left, right, delta); }
    long long query(int left, int right) { return query(1, 0, size_, left, right); }

   private:
    int size_;
    std::vector<long long> tree_;
    std::vector<long long> lazy_;

    void apply(int node, int left, int right, long long delta) {
        tree_[node] += delta * (right - left);
        lazy_[node] += delta;
    }

    void push(int node, int left, int right) {
        if (lazy_[node] == 0 || right - left == 1) return;
        const int middle = left + (right - left) / 2;
        apply(2 * node, left, middle, lazy_[node]);
        apply(2 * node + 1, middle, right, lazy_[node]);
        lazy_[node] = 0;
    }

    void add(int node, int start, int end, int left, int right, long long delta) {
        if (right <= start || end <= left) return;
        if (left <= start && end <= right) {
            apply(node, start, end, delta);
            return;
        }
        push(node, start, end);
        const int middle = start + (end - start) / 2;
        add(2 * node, start, middle, left, right, delta);
        add(2 * node + 1, middle, end, left, right, delta);
        tree_[node] = tree_[2 * node] + tree_[2 * node + 1];
    }

    long long query(int node, int start, int end, int left, int right) {
        if (right <= start || end <= left) return 0;
        if (left <= start && end <= right) return tree_[node];
        push(node, start, end);
        const int middle = start + (end - start) / 2;
        return query(2 * node, start, middle, left, right) +
               query(2 * node + 1, middle, end, left, right);
    }
};
```

### Python

```python
class LazySegmentTree:
    def __init__(self, size: int) -> None:
        self.size = size
        self.tree = [0] * (4 * size)
        self.lazy = [0] * (4 * size)

    def add(self, left: int, right: int, delta: int) -> None:
        self._add(1, 0, self.size, left, right, delta)

    def query(self, left: int, right: int) -> int:
        return self._query(1, 0, self.size, left, right)

    def _apply(self, node: int, start: int, end: int, delta: int) -> None:
        self.tree[node] += delta * (end - start)
        self.lazy[node] += delta

    def _push(self, node: int, start: int, end: int) -> None:
        if self.lazy[node] == 0 or end - start == 1:
            return
        middle = start + (end - start) // 2
        self._apply(2 * node, start, middle, self.lazy[node])
        self._apply(2 * node + 1, middle, end, self.lazy[node])
        self.lazy[node] = 0

    def _add(self, node: int, start: int, end: int, left: int, right: int, delta: int) -> None:
        if right <= start or end <= left:
            return
        if left <= start and end <= right:
            self._apply(node, start, end, delta)
            return
        self._push(node, start, end)
        middle = start + (end - start) // 2
        self._add(2 * node, start, middle, left, right, delta)
        self._add(2 * node + 1, middle, end, left, right, delta)
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    def _query(self, node: int, start: int, end: int, left: int, right: int) -> int:
        if right <= start or end <= left:
            return 0
        if left <= start and end <= right:
            return self.tree[node]
        self._push(node, start, end)
        middle = start + (end - start) // 2
        return self._query(2 * node, start, middle, left, right) + self._query(
            2 * node + 1, middle, end, left, right
        )
```

### Java

```java
final class LazySegmentTree {
    private final int size;
    private final long[] tree;
    private final long[] lazy;

    LazySegmentTree(int size) {
        this.size = size;
        tree = new long[4 * size];
        lazy = new long[4 * size];
    }

    void add(int left, int right, long delta) { add(1, 0, size, left, right, delta); }
    long query(int left, int right) { return query(1, 0, size, left, right); }

    private void apply(int node, int left, int right, long delta) {
        tree[node] += delta * (right - left);
        lazy[node] += delta;
    }

    private void push(int node, int left, int right) {
        if (lazy[node] == 0 || right - left == 1) return;
        int middle = left + (right - left) / 2;
        apply(2 * node, left, middle, lazy[node]);
        apply(2 * node + 1, middle, right, lazy[node]);
        lazy[node] = 0;
    }

    private void add(int node, int start, int end, int left, int right, long delta) {
        if (right <= start || end <= left) return;
        if (left <= start && end <= right) {
            apply(node, start, end, delta);
            return;
        }
        push(node, start, end);
        int middle = start + (end - start) / 2;
        add(2 * node, start, middle, left, right, delta);
        add(2 * node + 1, middle, end, left, right, delta);
        tree[node] = tree[2 * node] + tree[2 * node + 1];
    }

    private long query(int node, int start, int end, int left, int right) {
        if (right <= start || end <= left) return 0;
        if (left <= start && end <= right) return tree[node];
        push(node, start, end);
        int middle = start + (end - start) / 2;
        return query(2 * node, start, middle, left, right)
            + query(2 * node + 1, middle, end, left, right);
    }
}
```

## Why it works

A fully covered node knows its range length, so its sum can change immediately.
The lazy value remembers the exact update still owed to its children.

## Complexity

Each range update and query is `O(log n)`; space is `O(n)`.

## Common mistakes

- Updating a sum by `delta` instead of `delta * rangeLength`.
- Forgetting to push before a partial visit.
- Using the wrong composition order for assignment or affine updates.
