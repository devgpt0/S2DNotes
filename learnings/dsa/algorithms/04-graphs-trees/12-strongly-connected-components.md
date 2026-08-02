# Strongly Connected Components (Kosaraju)

## Idea

In a directed graph, a strongly connected component (SCC) is a maximal group
where every vertex can reach every other vertex. Kosaraju uses two DFS passes.

## Visual model

```text
first pass on graph: finishing order
second pass on reversed graph: one SCC per new DFS
```

## Classroom board: compress mutual reachability

```text
A -> B -> C -> A     C -> D

A,B,C can all reach one another -> one SCC [ABC]
D cannot return                -> SCC [D]
compressed graph: [ABC] -> [D], which has no cycle
```

## Steps

1. DFS the original graph and append each vertex after its descendants finish.
2. Reverse every edge.
3. Process vertices in reverse finishing order.
4. Each DFS in the reversed graph assigns one component ID.

## First-principles derivation

Inside a strongly connected component, every vertex can reach every other
vertex, so the whole component behaves like one super-vertex.

Compressing all SCCs removes every directed cycle between components; the
result is a DAG.

## Classroom board: compress mutual reachability

```text
0 -> 1 -> 2 -> 3 <-> 4
^         |
|---------|

SCC A = {0,1,2} because each reaches the other two
SCC B = {3,4}   because 3 and 4 reach each other

compressed graph:
[A] -> [B]
```

There cannot be an edge path back from `B` to `A`; otherwise all five
vertices would be one SCC.

## Pattern recognition

Use SCCs to compress directed cycles into a DAG, solve mutual reachability,
2-SAT, or reason about directed dependencies.

## Implementation

### C++

```cpp
std::vector<int> stronglyConnectedComponents(const std::vector<std::vector<int>>& graph) {
    const int size = graph.size();
    std::vector<std::vector<int>> reversed(size);
    std::vector<bool> visited(size, false);
    std::vector<int> order;
    for (int vertex = 0; vertex < size; ++vertex) for (int neighbor : graph[vertex]) reversed[neighbor].push_back(vertex);
    std::function<void(int)> finish = [&](int vertex) {
        visited[vertex] = true;
        for (int neighbor : graph[vertex]) if (!visited[neighbor]) finish(neighbor);
        order.push_back(vertex);
    };
    for (int vertex = 0; vertex < size; ++vertex) if (!visited[vertex]) finish(vertex);
    std::vector<int> component(size, -1);
    std::function<void(int, int)> assign = [&](int vertex, int id) {
        component[vertex] = id;
        for (int neighbor : reversed[vertex]) if (component[neighbor] == -1) assign(neighbor, id);
    };
    int id = 0;
    for (auto iterator = order.rbegin(); iterator != order.rend(); ++iterator) {
        if (component[*iterator] == -1) assign(*iterator, id++);
    }
    return component;
}
```

### Python

```python
def strongly_connected_components(graph: list[list[int]]) -> list[int]:
    reversed_graph = [[] for _ in graph]
    for vertex, neighbors in enumerate(graph):
        for neighbor in neighbors:
            reversed_graph[neighbor].append(vertex)
    visited = [False] * len(graph)
    order: list[int] = []

    def finish(vertex: int) -> None:
        visited[vertex] = True
        for neighbor in graph[vertex]:
            if not visited[neighbor]:
                finish(neighbor)
        order.append(vertex)

    for vertex in range(len(graph)):
        if not visited[vertex]:
            finish(vertex)
    component = [-1] * len(graph)

    def assign(vertex: int, identifier: int) -> None:
        component[vertex] = identifier
        for neighbor in reversed_graph[vertex]:
            if component[neighbor] == -1:
                assign(neighbor, identifier)

    identifier = 0
    for vertex in reversed(order):
        if component[vertex] == -1:
            assign(vertex, identifier)
            identifier += 1
    return component
```

### Java

```java
static int[] stronglyConnectedComponents(List<List<Integer>> graph) {
    List<List<Integer>> reversed = new ArrayList<>();
    for (int i = 0; i < graph.size(); i++) reversed.add(new ArrayList<>());
    for (int vertex = 0; vertex < graph.size(); vertex++) {
        for (int neighbor : graph.get(vertex)) reversed.get(neighbor).add(vertex);
    }
    boolean[] visited = new boolean[graph.size()];
    List<Integer> order = new ArrayList<>();
    for (int vertex = 0; vertex < graph.size(); vertex++) if (!visited[vertex]) finish(graph, vertex, visited, order);
    int[] component = new int[graph.size()];
    Arrays.fill(component, -1);
    int identifier = 0;
    for (int index = order.size() - 1; index >= 0; index--) {
        int vertex = order.get(index);
        if (component[vertex] == -1) assign(reversed, vertex, identifier++, component);
    }
    return component;
}

static void finish(List<List<Integer>> graph, int vertex, boolean[] visited, List<Integer> order) {
    visited[vertex] = true;
    for (int neighbor : graph.get(vertex)) if (!visited[neighbor]) finish(graph, neighbor, visited, order);
    order.add(vertex);
}

static void assign(List<List<Integer>> graph, int vertex, int id, int[] component) {
    component[vertex] = id;
    for (int neighbor : graph.get(vertex)) if (component[neighbor] == -1) assign(graph, neighbor, id, component);
}
```

## Why it works

The first unassigned vertex in reverse finishing order belongs to a source SCC
of the remaining reversed condensation graph, so its DFS cannot leak into an
unassigned different SCC.

## Complexity

Time and space are `O(V + E)`.

## Common mistakes

- Processing finishing order forward.
- Reversing vertices instead of edges.
- Using recursive DFS beyond the language's safe stack depth.
