# Prim's Minimum Spanning Tree

## Idea

Prim grows one minimum spanning tree. A min-heap stores the cheapest edges that
leave the already chosen vertices.

## Visual model

```text
[vertices inside MST] -- cheapest crossing edge --> [new vertex]
```

## Classroom board: grow one tree

```text
inside {A}; crossing edges A-B(4), A-C(1)
take A-C(1) -> inside {A,C}
new crossing edge C-B(2) beats A-B(4)
take C-B(2) -> total 3
```

Only edges crossing from inside to outside are candidates.

## Steps

1. Push `(0, start)` into a min-heap.
2. Pop the cheapest edge to an unvisited vertex.
3. Add its cost and mark the vertex visited.
4. Push edges from that vertex to unvisited neighbors.
5. All vertices must be visited for an MST to exist.

## First-principles derivation

Grow one connected tree. Across the cut between the tree and unvisited
vertices, the lightest crossing edge is safe for some minimum spanning tree.

The heap can contain stale crossing edges; accept an edge only when its target
is still outside the tree.

## Pattern recognition

Use Prim when the graph is given as adjacency lists or is dense/implicit and
edge costs can be generated from the current tree.

## Implementation

### C++

```cpp
long long prim(const std::vector<std::vector<std::pair<int, int>>>& graph) {
    using State = std::pair<long long, int>;
    std::priority_queue<State, std::vector<State>, std::greater<>> heap;
    std::vector<bool> visited(graph.size(), false);
    heap.push({0, 0});
    long long cost = 0;
    int chosen = 0;
    while (!heap.empty()) {
        const auto [weight, vertex] = heap.top();
        heap.pop();
        if (visited[vertex]) continue;
        visited[vertex] = true;
        cost += weight;
        ++chosen;
        for (const auto& [neighbor, edgeWeight] : graph[vertex]) {
            if (!visited[neighbor]) heap.push({edgeWeight, neighbor});
        }
    }
    return chosen == static_cast<int>(graph.size()) ? cost : -1;
}
```

### Python

```python
import heapq


def prim(graph: list[list[tuple[int, int]]]) -> int:
    visited = [False] * len(graph)
    heap = [(0, 0)]
    cost = 0
    chosen = 0
    while heap:
        weight, vertex = heapq.heappop(heap)
        if visited[vertex]:
            continue
        visited[vertex] = True
        cost += weight
        chosen += 1
        for neighbor, edge_weight in graph[vertex]:
            if not visited[neighbor]:
                heapq.heappush(heap, (edge_weight, neighbor))
    return cost if chosen == len(graph) else -1
```

### Java

```java
record Edge(int to, int weight) {}
record State(long weight, int vertex) {}

static long prim(List<List<Edge>> graph) {
    boolean[] visited = new boolean[graph.size()];
    PriorityQueue<State> heap = new PriorityQueue<>(Comparator.comparingLong(State::weight));
    heap.add(new State(0, 0));
    long cost = 0;
    int chosen = 0;
    while (!heap.isEmpty()) {
        State state = heap.remove();
        if (visited[state.vertex()]) continue;
        visited[state.vertex()] = true;
        cost += state.weight();
        chosen++;
        for (Edge edge : graph.get(state.vertex())) {
            if (!visited[edge.to()]) heap.add(new State(edge.weight(), edge.to()));
        }
    }
    return chosen == graph.size() ? cost : -1;
}
```

## Why it works

At every step, the heap minimum is the lightest edge crossing the current tree
cut. The MST cut property says choosing it is safe.

## Complexity

With a binary heap, time is `O(E log V)` and extra space is `O(V + E)`.

## Common mistakes

- Adding the cost again for a stale heap entry.
- Forgetting the graph must be undirected.
- Returning a forest cost for a disconnected graph.
