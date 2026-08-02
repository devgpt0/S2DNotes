# Kruskal's Minimum Spanning Tree

## Idea

Kruskal builds a minimum spanning tree (MST) by considering undirected edges
from lightest to heaviest and taking an edge only when it joins two components.

## Visual model

```text
sort edges -> smallest safe edge -> merge components -> repeat
```

## Classroom board: choose light edges without cycles

```text
edges sorted: A-B(1), B-C(2), A-C(3), C-D(5)
take A-B -> joins two groups
take B-C -> joins two groups
skip A-C -> A and C already connected; would make a cycle
take C-D -> all four connected; total 8
```

## Steps

1. Sort all edges by weight.
2. Start a [DSU](../03-data-structures/08-disjoint-set-union.md).
3. Add an edge when its endpoints are in different DSU components.
4. Stop after choosing `V - 1` edges; otherwise the graph is disconnected.

## First-principles derivation

Start with isolated vertices and consider edges from lightest to heaviest. An
edge joining two different components cannot create a cycle and is the
cheapest available way to join those groups.

DSU maintains the invariant that selected edges form a forest and identifies
whether endpoints are already connected.

## Pattern recognition

Use Kruskal for sparse undirected weighted graphs, especially when edges are
already listed or connectivity is naturally handled by DSU.

## Implementation

The code uses the `Dsu` class from the linked note.

### C++

```cpp
struct Edge { int first; int second; long long weight; };

long long kruskal(int vertexCount, std::vector<Edge> edges) {
    std::sort(edges.begin(), edges.end(), [](const Edge& left, const Edge& right) {
        return left.weight < right.weight;
    });
    Dsu dsu(vertexCount);
    long long cost = 0;
    int chosen = 0;
    for (const Edge& edge : edges) {
        if (!dsu.unite(edge.first, edge.second)) continue;
        cost += edge.weight;
        if (++chosen == vertexCount - 1) return cost;
    }
    return vertexCount == 1 ? 0 : -1;
}
```

### Python

```python
def kruskal(vertex_count: int, edges: list[tuple[int, int, int]]) -> int:
    dsu = Dsu(vertex_count)
    cost = 0
    chosen = 0
    for weight, first, second in sorted(edges):
        if not dsu.unite(first, second):
            continue
        cost += weight
        chosen += 1
        if chosen == vertex_count - 1:
            return cost
    return 0 if vertex_count == 1 else -1
```

### Java

```java
record Edge(int first, int second, long weight) {}

static long kruskal(int vertexCount, List<Edge> input) {
    List<Edge> edges = new ArrayList<>(input);
    edges.sort(Comparator.comparingLong(Edge::weight));
    Dsu dsu = new Dsu(vertexCount);
    long cost = 0;
    int chosen = 0;
    for (Edge edge : edges) {
        if (!dsu.unite(edge.first(), edge.second())) continue;
        cost += edge.weight();
        if (++chosen == vertexCount - 1) return cost;
    }
    return vertexCount == 1 ? 0 : -1;
}
```

## Why it works

The cut property says the lightest edge crossing any component cut is safe for
some MST. DSU rejects exactly the edges that would create a cycle.

## Complexity

Sorting dominates: `O(E log E)` time and `O(V + E)` space including input.

## Common mistakes

- Using Kruskal on a directed graph.
- Forgetting to detect a disconnected graph.
- Sorting endpoints instead of weights.
- Stopping after examining `V - 1` edges rather than choosing them.
