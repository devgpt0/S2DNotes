# Disjoint-Set Union (DSU)

## Idea

DSU tracks groups that merge over time. It answers “are these two items in the
same group?” and joins groups efficiently.

## Visual model

```text
1 -> 1      4 -> 4        union(1, 4)       4 -> 1
2 -> 1      5 -> 4        ------------>     5 -> 4 -> 1
3 -> 1                                    2,3 -> 1
```

## Classroom board: connect groups

```text
start: {0} {1} {2} {3}
union(0,1): {0,1} {2} {3}
union(2,3): {0,1} {2,3}
union(1,3): roots differ -> {0,1,2,3}
union(0,2): roots same -> this edge would create a cycle
```

Members do not need the same direct parent; `find` follows parents to one group
representative.

## Steps

1. Start each item as its own parent.
2. `find(x)` follows parents to the representative and compresses the path.
3. `union(a, b)` joins representatives, attaching the smaller tree to the
   larger tree.

## First-principles derivation

Repeatedly exploring a graph to ask “are these connected?” wastes work when
components only merge. Give every component a representative and join those
representatives.

The invariant is: two vertices are connected exactly when their representative
roots are equal.

## Pattern recognition

Use DSU for online component merging, Kruskal's MST, redundant edges, or
connectivity queries with additions but no deletions.

## Implementation

### C++

```cpp
class Dsu {
   public:
    explicit Dsu(int size) : parent_(size), size_(size, 1) {
        std::iota(parent_.begin(), parent_.end(), 0);
    }

    int find(int value) {
        if (parent_[value] != value) parent_[value] = find(parent_[value]);
        return parent_[value];
    }

    bool unite(int first, int second) {
        first = find(first);
        second = find(second);
        if (first == second) return false;
        if (size_[first] < size_[second]) std::swap(first, second);
        parent_[second] = first;
        size_[first] += size_[second];
        return true;
    }

   private:
    std::vector<int> parent_;
    std::vector<int> size_;
};
```

### Python

```python
class Dsu:
    def __init__(self, size: int) -> None:
        self.parent = list(range(size))
        self.size = [1] * size

    def find(self, value: int) -> int:
        while self.parent[value] != value:
            self.parent[value] = self.parent[self.parent[value]]
            value = self.parent[value]
        return value

    def unite(self, first: int, second: int) -> bool:
        first = self.find(first)
        second = self.find(second)
        if first == second:
            return False
        if self.size[first] < self.size[second]:
            first, second = second, first
        self.parent[second] = first
        self.size[first] += self.size[second]
        return True
```

### Java

```java
final class Dsu {
    private final int[] parent;
    private final int[] size;

    Dsu(int count) {
        parent = new int[count];
        size = new int[count];
        for (int value = 0; value < count; value++) {
            parent[value] = value;
            size[value] = 1;
        }
    }

    int find(int value) {
        while (parent[value] != value) {
            parent[value] = parent[parent[value]];
            value = parent[value];
        }
        return value;
    }

    boolean unite(int first, int second) {
        first = find(first);
        second = find(second);
        if (first == second) return false;
        if (size[first] < size[second]) {
            int temporary = first;
            first = second;
            second = temporary;
        }
        parent[second] = first;
        size[first] += size[second];
        return true;
    }
}
```

## Why it works

Every set has one representative. Union changes only one representative's
parent, so membership remains correct. Compression and size balancing keep
trees shallow.

## Complexity

Each operation is `O(alpha(n))` amortized, effectively constant. Space is
`O(n)`.

## Common mistakes

- Comparing raw parents instead of `find` results.
- Updating size on the child root instead of the new root.
- Using standard DSU when edges can be deleted.
