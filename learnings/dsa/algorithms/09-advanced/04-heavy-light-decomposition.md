# Heavy-Light Decomposition (HLD)

## Idea

HLD splits a tree into chains. Following the largest child keeps the same
chain; every other edge starts a new chain. Any tree path crosses only
`O(log n)` chains.

## Visual model

```text
heavy edge: child with largest subtree -> stay in chain
light edge: every other child          -> start new chain
```

## Classroom board: why few light edges

```text
a light child has at most half its parent's subtree size
after one light edge: remaining size <= n/2
after two: <= n/4
after k: <= n/2^k
therefore a path crosses at most O(log n) light edges/chains
```

## Steps

1. DFS to compute parent, depth, subtree size, and heavy child.
2. Assign consecutive positions along each heavy chain.
3. Store vertex values in that position order.
4. Split a path into chain ranges; query each range with a segment tree.

## First-principles derivation

A tree path can cross many arbitrary edges. Choose one heavy child per vertex,
usually the child with largest subtree, so any root-to-vertex path changes
light chains only `O(log n)` times.

Map each heavy chain to consecutive array positions; path queries become a
small number of range queries.

## Classroom board: split one tree path

```text
        0
       / \
      1   2
     / \   \
    3   4   5

heavy chains chosen:
chain A: 0-1-3
chain B: 2-5
chain C: 4

query path 4 -> 5:
segment 4 -> 4       (chain C)
segment 1 -> 0       (chain A)
segment 2 -> 5       (chain B)

combine the three base-array ranges
```

Each time the algorithm jumps from a chain head to its parent, it crosses a
light edge and moves to a substantially larger subtree.

## Pattern recognition

Use HLD for many path/subtree queries with point or range updates on a static
tree.

## Implementation: decompose a path into base-array ranges

Ranges are half-open and work directly with the segment-tree note. Their order
is safe for commutative operations such as sum/min/max.

### C++

```cpp
class HeavyLight {
   public:
    explicit HeavyLight(const std::vector<std::vector<int>>& tree)
        : tree_(tree), parent_(tree.size(), -1), depth_(tree.size()), size_(tree.size()),
          heavy_(tree.size(), -1), head_(tree.size()), position_(tree.size()), next_(0) {
        calculate(0, -1);
        decompose(0, 0);
    }

    std::vector<std::pair<int, int>> pathRanges(int first, int second) const {
        std::vector<std::pair<int, int>> ranges;
        while (head_[first] != head_[second]) {
            if (depth_[head_[first]] < depth_[head_[second]]) std::swap(first, second);
            ranges.push_back({position_[head_[first]], position_[first] + 1});
            first = parent_[head_[first]];
        }
        if (depth_[first] > depth_[second]) std::swap(first, second);
        ranges.push_back({position_[first], position_[second] + 1});
        return ranges;
    }

   private:
    const std::vector<std::vector<int>>& tree_;
    std::vector<int> parent_, depth_, size_, heavy_, head_, position_;
    int next_;

    int calculate(int vertex, int parent) {
        parent_[vertex] = parent;
        size_[vertex] = 1;
        int largest = 0;
        for (int child : tree_[vertex]) if (child != parent) {
            depth_[child] = depth_[vertex] + 1;
            int childSize = calculate(child, vertex);
            size_[vertex] += childSize;
            if (childSize > largest) { largest = childSize; heavy_[vertex] = child; }
        }
        return size_[vertex];
    }

    void decompose(int vertex, int head) {
        head_[vertex] = head;
        position_[vertex] = next_++;
        if (heavy_[vertex] != -1) decompose(heavy_[vertex], head);
        for (int child : tree_[vertex]) {
            if (child != parent_[vertex] && child != heavy_[vertex]) decompose(child, child);
        }
    }
};
```

### Python

```python
class HeavyLight:
    def __init__(self, tree: list[list[int]]) -> None:
        size = len(tree)
        self.tree = tree
        self.parent = [-1] * size
        self.depth = [0] * size
        self.subtree = [0] * size
        self.heavy = [-1] * size
        self.head = [0] * size
        self.position = [0] * size
        self.next_position = 0
        self._calculate(0, -1)
        self._decompose(0, 0)

    def _calculate(self, vertex: int, parent: int) -> int:
        self.parent[vertex] = parent
        self.subtree[vertex] = 1
        largest = 0
        for child in self.tree[vertex]:
            if child == parent:
                continue
            self.depth[child] = self.depth[vertex] + 1
            child_size = self._calculate(child, vertex)
            self.subtree[vertex] += child_size
            if child_size > largest:
                largest = child_size
                self.heavy[vertex] = child
        return self.subtree[vertex]

    def _decompose(self, vertex: int, head: int) -> None:
        self.head[vertex] = head
        self.position[vertex] = self.next_position
        self.next_position += 1
        if self.heavy[vertex] != -1:
            self._decompose(self.heavy[vertex], head)
        for child in self.tree[vertex]:
            if child != self.parent[vertex] and child != self.heavy[vertex]:
                self._decompose(child, child)

    def path_ranges(self, first: int, second: int) -> list[tuple[int, int]]:
        ranges: list[tuple[int, int]] = []
        while self.head[first] != self.head[second]:
            if self.depth[self.head[first]] < self.depth[self.head[second]]:
                first, second = second, first
            ranges.append((self.position[self.head[first]], self.position[first] + 1))
            first = self.parent[self.head[first]]
        if self.depth[first] > self.depth[second]:
            first, second = second, first
        ranges.append((self.position[first], self.position[second] + 1))
        return ranges
```

### Java

```java
final class HeavyLight {
    private final List<List<Integer>> tree;
    private final int[] parent, depth, subtree, heavy, head, position;
    private int nextPosition;

    HeavyLight(List<List<Integer>> tree) {
        this.tree = tree;
        int size = tree.size();
        parent = new int[size]; depth = new int[size]; subtree = new int[size];
        heavy = new int[size]; head = new int[size]; position = new int[size];
        Arrays.fill(parent, -1); Arrays.fill(heavy, -1);
        calculate(0, -1);
        decompose(0, 0);
    }

    List<int[]> pathRanges(int first, int second) {
        List<int[]> ranges = new ArrayList<>();
        while (head[first] != head[second]) {
            if (depth[head[first]] < depth[head[second]]) { int value = first; first = second; second = value; }
            ranges.add(new int[] {position[head[first]], position[first] + 1});
            first = parent[head[first]];
        }
        if (depth[first] > depth[second]) { int value = first; first = second; second = value; }
        ranges.add(new int[] {position[first], position[second] + 1});
        return ranges;
    }

    private int calculate(int vertex, int parentVertex) {
        parent[vertex] = parentVertex;
        subtree[vertex] = 1;
        int largest = 0;
        for (int child : tree.get(vertex)) if (child != parentVertex) {
            depth[child] = depth[vertex] + 1;
            int childSize = calculate(child, vertex);
            subtree[vertex] += childSize;
            if (childSize > largest) { largest = childSize; heavy[vertex] = child; }
        }
        return subtree[vertex];
    }

    private void decompose(int vertex, int chainHead) {
        head[vertex] = chainHead;
        position[vertex] = nextPosition++;
        if (heavy[vertex] != -1) decompose(heavy[vertex], chainHead);
        for (int child : tree.get(vertex)) {
            if (child != parent[vertex] && child != heavy[vertex]) decompose(child, child);
        }
    }
}
```

## Why it works

Every light edge at least halves the remaining subtree size, so a root-to-node
path crosses at most `O(log n)` light edges and therefore chains.

## Complexity

Decomposition is `O(n)`. A path becomes `O(log n)` ranges; with segment-tree
queries, a path operation is `O(log^2 n)`.

## Common mistakes

- Using unordered ranges for non-commutative operations.
- Forgetting to place heavy children first, which breaks subtree contiguity.
- Recursing too deeply on a path-shaped tree.
