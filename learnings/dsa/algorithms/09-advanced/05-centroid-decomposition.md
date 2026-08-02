# Centroid Decomposition

## Idea

A centroid is a tree vertex whose removal leaves no component larger than half
the tree. Repeatedly choosing centroids builds a decomposition tree of height
`O(log n)`.

## Visual model

```text
original tree -> remove centroid -> smaller components -> decompose each
```

## Classroom board: split a path of seven nodes

```text
0-1-2-3-4-5-6
centroid is 3
remove 3 -> components [0,1,2] and [4,5,6]
each component has at most half the nodes; repeat independently
```

## Steps

1. Compute sizes inside the current unremoved component.
2. Walk to a child larger than half until none exists; that vertex is centroid.
3. Mark it removed and record its centroid-tree parent.
4. Recursively decompose each remaining neighbor component.

## First-principles derivation

Choose a centroid whose removal leaves no component larger than half. Solve or
store information through that centroid, then recurse independently into the
smaller components.

Because component size at least halves, each original vertex belongs to only
`O(log n)` decomposition levels.

## Classroom board: decompose a five-vertex path

```text
original: 0 - 1 - 2 - 3 - 4

centroid = 2
remove 2:
left component  0-1
right component 3-4

choose centroid 0 (or 1) for left
choose centroid 3 (or 4) for right

centroid tree:
        2
       / \
      0   3
      |   |
      1   4
```

Exact child choice can vary when a component has two valid centroids; the
balance guarantee remains the same.

## Pattern recognition

Use it for dynamic distance queries or path-counting problems where updates and
queries can aggregate information through `O(log n)` centroid ancestors.

## Implementation: build centroid parent tree

### C++

```cpp
std::vector<int> centroidDecomposition(const std::vector<std::vector<int>>& tree) {
    std::vector<int> subtree(tree.size()), parent(tree.size(), -1);
    std::vector<bool> removed(tree.size(), false);
    std::function<int(int, int)> sizes = [&](int vertex, int previous) {
        subtree[vertex] = 1;
        for (int child : tree[vertex]) if (child != previous && !removed[child]) subtree[vertex] += sizes(child, vertex);
        return subtree[vertex];
    };
    std::function<int(int, int, int)> find = [&](int vertex, int previous, int total) {
        for (int child : tree[vertex]) if (child != previous && !removed[child] && subtree[child] > total / 2) return find(child, vertex, total);
        return vertex;
    };
    std::function<void(int, int)> build = [&](int start, int centroidParent) {
        int centroid = find(start, -1, sizes(start, -1));
        parent[centroid] = centroidParent;
        removed[centroid] = true;
        for (int neighbor : tree[centroid]) if (!removed[neighbor]) build(neighbor, centroid);
    };
    build(0, -1);
    return parent;
}
```

### Python

```python
def centroid_decomposition(tree: list[list[int]]) -> list[int]:
    subtree = [0] * len(tree)
    parent = [-1] * len(tree)
    removed = [False] * len(tree)

    def sizes(vertex: int, previous: int) -> int:
        subtree[vertex] = 1
        for child in tree[vertex]:
            if child != previous and not removed[child]:
                subtree[vertex] += sizes(child, vertex)
        return subtree[vertex]

    def find(vertex: int, previous: int, total: int) -> int:
        for child in tree[vertex]:
            if child != previous and not removed[child] and subtree[child] > total // 2:
                return find(child, vertex, total)
        return vertex

    def build(start: int, centroid_parent: int) -> None:
        centroid = find(start, -1, sizes(start, -1))
        parent[centroid] = centroid_parent
        removed[centroid] = True
        for neighbor in tree[centroid]:
            if not removed[neighbor]:
                build(neighbor, centroid)

    build(0, -1)
    return parent
```

### Java

```java
static int[] centroidDecomposition(List<List<Integer>> tree) {
    int[] subtree = new int[tree.size()];
    int[] parent = new int[tree.size()];
    Arrays.fill(parent, -1);
    boolean[] removed = new boolean[tree.size()];
    buildCentroid(tree, 0, -1, subtree, parent, removed);
    return parent;
}

static void buildCentroid(List<List<Integer>> tree, int start, int centroidParent, int[] subtree, int[] parent, boolean[] removed) {
    int total = centroidSizes(tree, start, -1, subtree, removed);
    int centroid = findCentroid(tree, start, -1, total, subtree, removed);
    parent[centroid] = centroidParent;
    removed[centroid] = true;
    for (int neighbor : tree.get(centroid)) if (!removed[neighbor]) buildCentroid(tree, neighbor, centroid, subtree, parent, removed);
}

static int centroidSizes(List<List<Integer>> tree, int vertex, int previous, int[] subtree, boolean[] removed) {
    subtree[vertex] = 1;
    for (int child : tree.get(vertex)) if (child != previous && !removed[child]) subtree[vertex] += centroidSizes(tree, child, vertex, subtree, removed);
    return subtree[vertex];
}

static int findCentroid(List<List<Integer>> tree, int vertex, int previous, int total, int[] subtree, boolean[] removed) {
    for (int child : tree.get(vertex)) {
        if (child != previous && !removed[child] && subtree[child] > total / 2) return findCentroid(tree, child, vertex, total, subtree, removed);
    }
    return vertex;
}
```

## Why it works

Moving into a component larger than half strictly approaches the unique heavy
side; when none exists, the centroid condition holds. Each recursive component
has at most half the prior size.

## Complexity

Build time is `O(n log n)` and space is `O(n)`.

## Common mistakes

- Including removed vertices in size calculations.
- Reusing stale subtree sizes across components.
- Assuming centroid-tree parent edges are original tree edges.
