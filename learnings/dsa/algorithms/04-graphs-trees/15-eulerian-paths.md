# Eulerian Paths and Circuits

## Idea

An Eulerian path uses every edge exactly once. Hierholzer's algorithm keeps
walking unused edges, then adds a vertex to the answer only when it has no edge
left.

## Visual model

```text
walk unused edges -> get stuck -> append while backtracking -> reverse answer
```

## Classroom board: use edges, not vertices, once

```text
edges A->B, B->C, C->A, A->D
walk A-B-C-A-D uses all four edges once
vertex A appears twice; that is allowed
```

Hierholzer adds vertices to the final path while backtracking, so the collected
list must be reversed.

## Steps for a directed graph

1. Check degrees: a path has one `out = in + 1` start, one `in = out + 1` end,
   and equality elsewhere; a circuit has equality everywhere.
2. Store outgoing edges and consume each once.
3. Push the start. If the top has an edge, follow it; otherwise move the top to
   the answer.
4. Reverse the answer and verify it contains `E + 1` vertices.

## First-principles derivation

An Eulerian walk consumes edges, not vertices. Every time an internal vertex is
entered, another unused edge must leave it, so degrees must pair up.

Hierholzer's algorithm follows unused edges until stuck, then places vertices
into the final route while backtracking.

## Classroom board: use every edge once

```text
edges: 0-1, 1-2, 2-0, 0-3

degrees:
0: 3 odd
1: 2 even
2: 2 even
3: 1 odd

exactly two odd vertices -> Eulerian path exists from 0 to 3

walk: 0 -> 1 -> 2 -> 0 -> 3
used:   01   12   20   03   (every edge once)
```

With zero odd vertices the walk can start and finish at the same vertex.

## Pattern recognition

Look for “use every edge/ticket/domino exactly once.” This is about edges;
Hamiltonian paths use every vertex and are a different, much harder problem.

## Implementation: directed graph

### C++

```cpp
std::vector<int> eulerianPath(int vertexCount, const std::vector<std::pair<int, int>>& edges) {
    std::vector<std::vector<int>> graph(vertexCount);
    std::vector<int> indegree(vertexCount), outdegree(vertexCount);
    for (auto [from, to] : edges) {
        graph[from].push_back(to);
        ++outdegree[from];
        ++indegree[to];
    }
    int start = edges.empty() ? 0 : edges.front().first;
    int starts = 0, ends = 0;
    for (int vertex = 0; vertex < vertexCount; ++vertex) {
        const int difference = outdegree[vertex] - indegree[vertex];
        if (difference == 1) { start = vertex; ++starts; }
        else if (difference == -1) ++ends;
        else if (difference != 0) return {};
    }
    if (!((starts == 0 && ends == 0) || (starts == 1 && ends == 1))) return {};
    std::vector<int> stack{start}, path;
    while (!stack.empty()) {
        const int vertex = stack.back();
        if (!graph[vertex].empty()) {
            const int neighbor = graph[vertex].back();
            graph[vertex].pop_back();
            stack.push_back(neighbor);
        } else {
            path.push_back(vertex);
            stack.pop_back();
        }
    }
    if (path.size() != edges.size() + 1) return {};
    std::reverse(path.begin(), path.end());
    return path;
}
```

### Python

```python
def eulerian_path(vertex_count: int, edges: list[tuple[int, int]]) -> list[int]:
    graph = [[] for _ in range(vertex_count)]
    indegree = [0] * vertex_count
    outdegree = [0] * vertex_count
    for source, target in edges:
        graph[source].append(target)
        outdegree[source] += 1
        indegree[target] += 1
    start = edges[0][0] if edges else 0
    starts = ends = 0
    for vertex in range(vertex_count):
        difference = outdegree[vertex] - indegree[vertex]
        if difference == 1:
            start = vertex
            starts += 1
        elif difference == -1:
            ends += 1
        elif difference != 0:
            return []
    if (starts, ends) not in ((0, 0), (1, 1)):
        return []
    stack = [start]
    path: list[int] = []
    while stack:
        vertex = stack[-1]
        if graph[vertex]:
            stack.append(graph[vertex].pop())
        else:
            path.append(stack.pop())
    return path[::-1] if len(path) == len(edges) + 1 else []
```

### Java

```java
static List<Integer> eulerianPath(int vertexCount, int[][] edges) {
    List<Deque<Integer>> graph = new ArrayList<>();
    for (int i = 0; i < vertexCount; i++) graph.add(new ArrayDeque<>());
    int[] indegree = new int[vertexCount];
    int[] outdegree = new int[vertexCount];
    for (int[] edge : edges) {
        graph.get(edge[0]).addLast(edge[1]);
        outdegree[edge[0]]++;
        indegree[edge[1]]++;
    }
    int start = edges.length == 0 ? 0 : edges[0][0];
    int starts = 0;
    int ends = 0;
    for (int vertex = 0; vertex < vertexCount; vertex++) {
        int difference = outdegree[vertex] - indegree[vertex];
        if (difference == 1) { start = vertex; starts++; }
        else if (difference == -1) ends++;
        else if (difference != 0) return List.of();
    }
    if (!((starts == 0 && ends == 0) || (starts == 1 && ends == 1))) return List.of();
    Deque<Integer> stack = new ArrayDeque<>();
    List<Integer> path = new ArrayList<>();
    stack.addLast(start);
    while (!stack.isEmpty()) {
        int vertex = stack.peekLast();
        if (!graph.get(vertex).isEmpty()) stack.addLast(graph.get(vertex).removeLast());
        else path.add(stack.removeLast());
    }
    if (path.size() != edges.length + 1) return List.of();
    Collections.reverse(path);
    return path;
}
```

## Why it works

Every edge is removed exactly once. Backtracking joins closed edge-trails into
one trail; the length check rejects disconnected edge-containing components.

## Complexity

Time and space are `O(V + E)`.

## Common mistakes

- Checking only degrees and not whether all edges were reached.
- Confusing directed and undirected degree rules.
- Reversing neither the backtracking output nor the final answer.
