# Maximum Flow (Dinic's Algorithm)

## Idea

A flow network has directed edges with capacities. Maximum flow sends as much
as possible from a source to a sink without exceeding capacities and while
conserving flow at other vertices.

Dinic repeatedly builds a BFS level graph and sends blocking flows through it.

## Visual model

```text
capacity 7, send 4:
forward residual capacity = 3
reverse residual capacity = 4  (flow can be undone later)
```

## Classroom board: residual edges undo choices

```text
A->B capacity 5; send 3
forward residual A->B becomes 2
reverse residual B->A becomes 3

later the algorithm may send flow backward to reroute those 3 units
```

## Steps

1. Add every real edge plus a zero-capacity reverse edge.
2. BFS through positive residual edges to build levels.
3. DFS only to the next level and push as much flow as possible.
4. Remember the next untried edge per vertex.
5. Repeat until the sink is unreachable.

## First-principles derivation

Flow consumes edge capacity. Sending flow forward must create equal residual
capacity backward so an earlier choice can be undone and rerouted.

An augmenting path sends its smallest remaining capacity, called the
bottleneck. When no source-to-sink residual path remains, the flow is maximum.

## Classroom board: augment and reroute

```text
capacities:
s -> a: 3    a -> t: 2
s -> b: 2    b -> t: 3
a -> b: 1

path s-a-t: bottleneck 2, send 2
remaining s-a=1, a-t=0

path s-b-t: bottleneck 2, send 2
remaining s-b=0, b-t=1

path s-a-b-t: bottleneck 1, send 1

total flow = 2 + 2 + 1 = 5
source outgoing capacity is 5, so no larger flow is possible
```

## Pattern recognition

Use flow for capacity routing, maximum disjoint paths, assignment with
capacities, or minimum cuts. First identify what one unit of flow represents.

## Implementation

### C++

```cpp
class Dinic {
    struct Edge { int to; int reverse; long long capacity; };

   public:
    explicit Dinic(int size) : graph_(size), level_(size), next_(size) {}

    void addEdge(int from, int to, long long capacity) {
        Edge forward{to, static_cast<int>(graph_[to].size()), capacity};
        Edge backward{from, static_cast<int>(graph_[from].size()), 0};
        graph_[from].push_back(forward);
        graph_[to].push_back(backward);
    }

    long long maxFlow(int source, int sink) {
        if (source == sink) throw std::invalid_argument("source and sink must differ");
        long long flow = 0;
        while (buildLevels(source, sink)) {
            std::fill(next_.begin(), next_.end(), 0);
            while (long long pushed = send(source, sink, std::numeric_limits<long long>::max())) flow += pushed;
        }
        return flow;
    }

   private:
    std::vector<std::vector<Edge>> graph_;
    std::vector<int> level_;
    std::vector<int> next_;

    bool buildLevels(int source, int sink) {
        std::fill(level_.begin(), level_.end(), -1);
        std::queue<int> queue;
        level_[source] = 0;
        queue.push(source);
        while (!queue.empty()) {
            int vertex = queue.front(); queue.pop();
            for (const Edge& edge : graph_[vertex]) {
                if (edge.capacity > 0 && level_[edge.to] == -1) {
                    level_[edge.to] = level_[vertex] + 1;
                    queue.push(edge.to);
                }
            }
        }
        return level_[sink] != -1;
    }

    long long send(int vertex, int sink, long long pushed) {
        if (vertex == sink) return pushed;
        for (int& index = next_[vertex]; index < static_cast<int>(graph_[vertex].size()); ++index) {
            Edge& edge = graph_[vertex][index];
            if (edge.capacity == 0 || level_[edge.to] != level_[vertex] + 1) continue;
            long long amount = send(edge.to, sink, std::min(pushed, edge.capacity));
            if (amount == 0) continue;
            edge.capacity -= amount;
            graph_[edge.to][edge.reverse].capacity += amount;
            return amount;
        }
        return 0;
    }
};
```

### Python

```python
from collections import deque
from dataclasses import dataclass


@dataclass
class Edge:
    to: int
    reverse: int
    capacity: int


class Dinic:
    def __init__(self, size: int) -> None:
        self.graph: list[list[Edge]] = [[] for _ in range(size)]

    def add_edge(self, source: int, target: int, capacity: int) -> None:
        forward = Edge(target, len(self.graph[target]), capacity)
        backward = Edge(source, len(self.graph[source]), 0)
        self.graph[source].append(forward)
        self.graph[target].append(backward)

    def max_flow(self, source: int, sink: int) -> int:
        if source == sink:
            raise ValueError('source and sink must differ')
        flow = 0
        while self._build_levels(source, sink):
            self.next_edge = [0] * len(self.graph)
            while pushed := self._send(source, sink, 10**30):
                flow += pushed
        return flow

    def _build_levels(self, source: int, sink: int) -> bool:
        self.level = [-1] * len(self.graph)
        self.level[source] = 0
        queue = deque([source])
        while queue:
            vertex = queue.popleft()
            for edge in self.graph[vertex]:
                if edge.capacity > 0 and self.level[edge.to] == -1:
                    self.level[edge.to] = self.level[vertex] + 1
                    queue.append(edge.to)
        return self.level[sink] != -1

    def _send(self, vertex: int, sink: int, pushed: int) -> int:
        if vertex == sink:
            return pushed
        while self.next_edge[vertex] < len(self.graph[vertex]):
            edge = self.graph[vertex][self.next_edge[vertex]]
            if edge.capacity > 0 and self.level[edge.to] == self.level[vertex] + 1:
                amount = self._send(edge.to, sink, min(pushed, edge.capacity))
                if amount:
                    edge.capacity -= amount
                    self.graph[edge.to][edge.reverse].capacity += amount
                    return amount
            self.next_edge[vertex] += 1
        return 0
```

### Java

```java
final class Dinic {
    private static final class Edge {
        final int to;
        final int reverse;
        long capacity;
        Edge(int to, int reverse, long capacity) {
            this.to = to;
            this.reverse = reverse;
            this.capacity = capacity;
        }
    }

    private final List<List<Edge>> graph;
    private final int[] level;
    private final int[] next;

    Dinic(int size) {
        graph = new ArrayList<>();
        for (int vertex = 0; vertex < size; vertex++) graph.add(new ArrayList<>());
        level = new int[size];
        next = new int[size];
    }

    void addEdge(int from, int to, long capacity) {
        Edge forward = new Edge(to, graph.get(to).size(), capacity);
        Edge backward = new Edge(from, graph.get(from).size(), 0);
        graph.get(from).add(forward);
        graph.get(to).add(backward);
    }

    long maxFlow(int source, int sink) {
        if (source == sink) throw new IllegalArgumentException("source and sink must differ");
        long flow = 0;
        while (buildLevels(source, sink)) {
            Arrays.fill(next, 0);
            long pushed;
            while ((pushed = send(source, sink, Long.MAX_VALUE)) > 0) flow += pushed;
        }
        return flow;
    }

    private boolean buildLevels(int source, int sink) {
        Arrays.fill(level, -1);
        Queue<Integer> queue = new ArrayDeque<>();
        level[source] = 0;
        queue.add(source);
        while (!queue.isEmpty()) {
            int vertex = queue.remove();
            for (Edge edge : graph.get(vertex)) {
                if (edge.capacity > 0 && level[edge.to] == -1) {
                    level[edge.to] = level[vertex] + 1;
                    queue.add(edge.to);
                }
            }
        }
        return level[sink] != -1;
    }

    private long send(int vertex, int sink, long pushed) {
        if (vertex == sink) return pushed;
        while (next[vertex] < graph.get(vertex).size()) {
            Edge edge = graph.get(vertex).get(next[vertex]);
            if (edge.capacity > 0 && level[edge.to] == level[vertex] + 1) {
                long amount = send(edge.to, sink, Math.min(pushed, edge.capacity));
                if (amount > 0) {
                    edge.capacity -= amount;
                    graph.get(edge.to).get(edge.reverse).capacity += amount;
                    return amount;
                }
            }
            next[vertex]++;
        }
        return 0;
    }
}
```

## Why it works

Reverse residual edges make every earlier choice reversible. Each blocking flow
removes all source-to-sink paths from the current level graph; when no residual
path remains, max-flow/min-cut proves the flow is maximum.

## Complexity

General Dinic is `O(V^2 E)`; it is much faster on many contest networks. Space
is `O(V + E)`.

## Common mistakes

- Forgetting reverse edges or reverse indices.
- Modifying original capacity without a residual model.
- Using `int` for large total flow.
- Passing a zero source/sink or allowing source equal to sink without defining
  the contract.
