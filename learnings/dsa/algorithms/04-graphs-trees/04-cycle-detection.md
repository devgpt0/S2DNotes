# Cycle Detection in Directed Graphs

## Idea

During DFS, color each vertex:

- `0`: unseen;
- `1`: active in the current DFS path;
- `2`: completely finished.

An edge to an active vertex closes a directed cycle.

## Visual model

```text
0 -> 1 -> 2
     ^    |
     |____|   edge to active vertex 1 => cycle
```

## Classroom board: why three colors

```text
A -> B -> C
     ^    |
     |____|

enter A: active
enter B: active
enter C: active
C sees B still active -> B is on current path -> cycle
```

An edge to a finished vertex is not a cycle back into the current path.

## Steps

1. Mark a vertex active on entry.
2. DFS into unseen neighbors.
3. Return true on an edge to an active neighbor.
4. Mark the vertex finished after all neighbors are done.
5. Start DFS from every unseen vertex.

## First-principles derivation

A cycle is an edge returning to a vertex on the current unfinished path, not
merely any previously visited vertex.

Directed DFS therefore needs three states: unseen, active, and finished. In an
undirected graph, the edge back to the parent must be ignored.

## Pattern recognition

Use three-color DFS for dependency cycles in directed graphs. For undirected
graphs, an edge to a visited vertex is a cycle only when it is not the parent
edge.

## Implementation

### C++

```cpp
bool hasCycleFrom(const std::vector<std::vector<int>>& graph, int vertex, std::vector<int>& color) {
    color[vertex] = 1;
    for (int neighbor : graph[vertex]) {
        if (color[neighbor] == 1) return true;
        if (color[neighbor] == 0 && hasCycleFrom(graph, neighbor, color)) return true;
    }
    color[vertex] = 2;
    return false;
}

bool hasDirectedCycle(const std::vector<std::vector<int>>& graph) {
    std::vector<int> color(graph.size(), 0);
    for (int vertex = 0; vertex < static_cast<int>(graph.size()); ++vertex) {
        if (color[vertex] == 0 && hasCycleFrom(graph, vertex, color)) return true;
    }
    return false;
}
```

### Python

```python
def has_directed_cycle(graph: list[list[int]]) -> bool:
    color = [0] * len(graph)

    def visit(vertex: int) -> bool:
        color[vertex] = 1
        for neighbor in graph[vertex]:
            if color[neighbor] == 1:
                return True
            if color[neighbor] == 0 and visit(neighbor):
                return True
        color[vertex] = 2
        return False

    return any(color[vertex] == 0 and visit(vertex) for vertex in range(len(graph)))
```

### Java

```java
static boolean hasDirectedCycle(List<List<Integer>> graph) {
    int[] color = new int[graph.size()];
    for (int vertex = 0; vertex < graph.size(); vertex++) {
        if (color[vertex] == 0 && hasCycleFrom(graph, vertex, color)) return true;
    }
    return false;
}

static boolean hasCycleFrom(List<List<Integer>> graph, int vertex, int[] color) {
    color[vertex] = 1;
    for (int neighbor : graph.get(vertex)) {
        if (color[neighbor] == 1) return true;
        if (color[neighbor] == 0 && hasCycleFrom(graph, neighbor, color)) return true;
    }
    color[vertex] = 2;
    return false;
}
```

## Why it works

Active vertices are exactly the current ancestor chain. An edge back into that
chain forms a closed directed path; edges to finished vertices do not.

## Complexity

Time is `O(V + E)` and space is `O(V)`.

## Common mistakes

- Using one visited boolean, which cannot separate active from finished.
- Applying the directed rule unchanged to undirected parent edges.
- Checking only the component containing vertex `0`.
