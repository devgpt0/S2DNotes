# Graph Representation

## Idea

A graph has vertices and edges. An adjacency list stores, for every vertex,
only its neighbors. It is the standard representation for sparse contest
graphs.

## Visual model

```text
edges: 0-1, 0-2, 2-3
0: [1, 2]
1: [0]
2: [0, 3]
3: [2]
```

## Steps

1. Create one empty neighbor list per vertex.
2. For directed edge `from -> to`, add `to` to `from`.
3. For an undirected edge, also add the reverse direction.
4. Store `(neighbor, weight)` for weighted graphs.

## First-principles derivation

A graph is a set of vertices plus relationships. The representation should make
the operations used by the algorithm cheap.

```text
need neighbors often -> adjacency list
need edge lookup often on a small graph -> adjacency matrix
need process/sort all edges -> edge list
```

For an undirected edge, both endpoint lists must describe the same relationship.

## Classroom board: build an adjacency list

Undirected edges are `(0,1), (0,2), (1,3)`.

```text
start
0: []
1: []
2: []
3: []

add 0-1          add 0-2          add 1-3
0: [1]           0: [1,2]         0: [1,2]
1: [0]           1: [0]           1: [0,3]
2: []            2: [0]           2: [0]
3: []            3: []            3: [1]
```

There are six stored neighbor entries because each of the three undirected
edges appears in both directions.

## Pattern recognition

Use an adjacency list when algorithms must visit neighbors and `E` is much
smaller than `V^2`. Use a matrix when constant-time edge lookup or dense
all-pairs processing matters.

## Implementation: undirected adjacency list

### C++

```cpp
std::vector<std::vector<int>> buildGraph(
    int vertexCount,
    const std::vector<std::pair<int, int>>& edges) {
    std::vector<std::vector<int>> graph(vertexCount);
    for (const auto& [first, second] : edges) {
        graph[first].push_back(second);
        graph[second].push_back(first);
    }
    return graph;
}
```

### Python

```python
def build_graph(vertex_count: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    graph = [[] for _ in range(vertex_count)]
    for first, second in edges:
        graph[first].append(second)
        graph[second].append(first)
    return graph
```

### Java

```java
static List<List<Integer>> buildGraph(int vertexCount, int[][] edges) {
    List<List<Integer>> graph = new ArrayList<>(vertexCount);
    for (int vertex = 0; vertex < vertexCount; vertex++) graph.add(new ArrayList<>());
    for (int[] edge : edges) {
        graph.get(edge[0]).add(edge[1]);
        graph.get(edge[1]).add(edge[0]);
    }
    return graph;
}
```

## Why it works

Every edge is stored beside each endpoint that can traverse it. Therefore
iterating `graph[v]` visits exactly the outgoing neighbors of `v`.

## Complexity

Build time and space are `O(V + E)`; an undirected edge is stored twice.

## Common mistakes

- Forgetting the reverse edge in an undirected graph.
- Mixing one-based input labels with zero-based arrays.
- Losing edge IDs when parallel edges must be distinguished.
- Using 32-bit weights when path sums can overflow.
