# Bridges

## Idea

A bridge is an undirected edge whose removal increases the number of connected
components. DFS tracks discovery time and the earliest ancestor reachable from
each subtree.

## Visual model

`low[child] > discovery[parent]` means the child subtree has no back edge that
crosses above the parent edge, so that edge is a bridge.

## Classroom board: edge with no escape route

```text
triangle A-B-C-A, plus C-D
triangle edges have another route around the cycle
C-D has no other route from D's subtree to C or above
remove C-D -> D disconnects -> bridge
```

## Steps

1. Give each vertex a discovery time on DFS entry.
2. Initialize `low[vertex]` to that time.
3. After a child returns, merge its low value.
4. Record the edge when the child's low value is greater than the parent's
   discovery time.
5. Use edge IDs so parallel edges are handled correctly.

## First-principles derivation

A DFS tree edge `parent -> child` is a bridge when the child's entire subtree
has no alternate edge reaching the parent or an ancestor.

`low[child]` records the earliest discovery time reachable from that subtree.
The edge is a bridge exactly when `low[child] > tin[parent]`.

## Classroom board: edge with no escape route

```text
0 ----- 1
       / \
      2---3

DFS tree: 0 -> 1 -> 2 -> 3
edge 3-1 lets the {1,2,3} area reach discovery time of 1

low[3] = tin[1]
low[2] = tin[1]
low[1] = tin[1]

for edge 0-1: low[1] > tin[0] -> bridge
triangle edges: alternate route exists -> not bridges
```

## Pattern recognition

Use bridges for critical roads/connections or edges that are not part of any
cycle in an undirected graph.

## Implementation

### C++

```cpp
std::vector<std::pair<int, int>> findBridges(int vertexCount, const std::vector<std::pair<int, int>>& edges) {
    std::vector<std::vector<std::pair<int, int>>> graph(vertexCount);
    for (int id = 0; id < static_cast<int>(edges.size()); ++id) {
        auto [first, second] = edges[id];
        graph[first].push_back({second, id});
        graph[second].push_back({first, id});
    }
    std::vector<int> discovery(vertexCount, -1), low(vertexCount);
    std::vector<std::pair<int, int>> bridges;
    int timer = 0;
    std::function<void(int, int)> dfs = [&](int vertex, int parentEdge) {
        discovery[vertex] = low[vertex] = timer++;
        for (auto [neighbor, edgeId] : graph[vertex]) {
            if (edgeId == parentEdge) continue;
            if (discovery[neighbor] == -1) {
                dfs(neighbor, edgeId);
                low[vertex] = std::min(low[vertex], low[neighbor]);
                if (low[neighbor] > discovery[vertex]) bridges.push_back({vertex, neighbor});
            } else {
                low[vertex] = std::min(low[vertex], discovery[neighbor]);
            }
        }
    };
    for (int vertex = 0; vertex < vertexCount; ++vertex) if (discovery[vertex] == -1) dfs(vertex, -1);
    return bridges;
}
```

### Python

```python
def find_bridges(vertex_count: int, edges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    graph = [[] for _ in range(vertex_count)]
    for edge_id, (first, second) in enumerate(edges):
        graph[first].append((second, edge_id))
        graph[second].append((first, edge_id))
    discovery = [-1] * vertex_count
    low = [0] * vertex_count
    bridges: list[tuple[int, int]] = []
    timer = 0

    def dfs(vertex: int, parent_edge: int) -> None:
        nonlocal timer
        discovery[vertex] = low[vertex] = timer
        timer += 1
        for neighbor, edge_id in graph[vertex]:
            if edge_id == parent_edge:
                continue
            if discovery[neighbor] == -1:
                dfs(neighbor, edge_id)
                low[vertex] = min(low[vertex], low[neighbor])
                if low[neighbor] > discovery[vertex]:
                    bridges.append((vertex, neighbor))
            else:
                low[vertex] = min(low[vertex], discovery[neighbor])

    for vertex in range(vertex_count):
        if discovery[vertex] == -1:
            dfs(vertex, -1)
    return bridges
```

### Java

```java
record EdgeRef(int to, int id) {}

static List<int[]> findBridges(int vertexCount, int[][] edges) {
    List<List<EdgeRef>> graph = new ArrayList<>();
    for (int i = 0; i < vertexCount; i++) graph.add(new ArrayList<>());
    for (int id = 0; id < edges.length; id++) {
        graph.get(edges[id][0]).add(new EdgeRef(edges[id][1], id));
        graph.get(edges[id][1]).add(new EdgeRef(edges[id][0], id));
    }
    int[] discovery = new int[vertexCount];
    Arrays.fill(discovery, -1);
    int[] low = new int[vertexCount];
    int[] timer = {0};
    List<int[]> bridges = new ArrayList<>();
    for (int vertex = 0; vertex < vertexCount; vertex++) {
        if (discovery[vertex] == -1) bridgeDfs(graph, vertex, -1, discovery, low, timer, bridges);
    }
    return bridges;
}

static void bridgeDfs(List<List<EdgeRef>> graph, int vertex, int parentEdge, int[] discovery, int[] low, int[] timer, List<int[]> bridges) {
    discovery[vertex] = low[vertex] = timer[0]++;
    for (EdgeRef edge : graph.get(vertex)) {
        if (edge.id() == parentEdge) continue;
        if (discovery[edge.to()] == -1) {
            bridgeDfs(graph, edge.to(), edge.id(), discovery, low, timer, bridges);
            low[vertex] = Math.min(low[vertex], low[edge.to()]);
            if (low[edge.to()] > discovery[vertex]) bridges.add(new int[] {vertex, edge.to()});
        } else low[vertex] = Math.min(low[vertex], discovery[edge.to()]);
    }
}
```

## Why it works

`low[child]` records the highest ancestor reachable without using the parent
edge. If none reaches the parent or above, removing that edge disconnects the
child subtree.

## Complexity

Time and space are `O(V + E)`.

## Common mistakes

- Using the child discovery time instead of `low[child]` in the bridge test.
- Skipping the parent vertex rather than the parent edge, which breaks parallel
  edges.
- Running DFS from only one component.
