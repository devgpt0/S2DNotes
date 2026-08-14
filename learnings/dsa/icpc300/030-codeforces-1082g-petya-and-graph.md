# ICPC300 030: Codeforces 1082G - Petya and Graph

**Source:** [Codeforces 1082G - Petya and Graph](https://codeforces.com/problemset/problem/1082/G)  
**Pattern:** maximum-weight closure reduced to minimum cut

## Exact contract

Input gives an undirected graph with `1 <= n, m <= 1000`. Vertex `i` has a
positive cost `a[i]`. Each edge gives endpoints `u`, `v` and a positive profit
`w`.

Choose any set of edges. Receiving an edge's profit requires paying the cost of
every vertex incident to at least one chosen edge. Output the maximum possible
`sum(chosen edge profits) - sum(used vertex costs)`. Choosing nothing is
allowed, so the answer is never negative.

## First principles

Treat every profitable edge as a selectable item. Selecting it forces two
dependencies: both endpoint vertices must also be selected and paid for. This
is a maximum-weight closure problem.

In a cut network, put profit items behind source edges and costs behind sink
edges. An infinite-capacity edge from a profit item to each dependency makes a
cut that selects the profit but rejects an endpoint prohibitively expensive.
The finite part of a cut is exactly the profit forfeited plus the vertex costs
paid. Therefore:

`maximum profit = total edge profit - minimum cut`.

## Cases that decide correctness

- Vertex cost is paid once even when many selected edges touch that vertex.
- All internal profitable edges should be taken after their endpoints are
  paid, because edge profits are positive.
- The empty choice gives value zero.
- The dependency capacity must exceed every possible finite cut; use
  `total profits + total vertex costs + 1`.
- Parallel edges are separate profit items and need no special handling.

## Brute force: enumerate edge subsets

```python
def maximum_graph_profit_by_edges(
    vertex_costs: list[int],
    edges: list[tuple[int, int, int]],
) -> int:
    best = 0
    for mask in range(1 << len(edges)):
        used_vertices: set[int] = set()
        profit = 0
        for edge_index, (left, right, reward) in enumerate(edges):
            if mask & (1 << edge_index):
                used_vertices.add(left)
                used_vertices.add(right)
                profit += reward
        profit -= sum(vertex_costs[vertex] for vertex in used_vertices)
        best = max(best, profit)
    return best
```

**Complexity:** `O(2^m (n+m))` time and `O(n)` space.

## Better when vertices are fewer: enumerate vertex subsets

```python
def maximum_graph_profit_by_vertices(
    vertex_costs: list[int],
    edges: list[tuple[int, int, int]],
) -> int:
    best = 0
    for mask in range(1 << len(vertex_costs)):
        value = -sum(
            cost for vertex, cost in enumerate(vertex_costs) if mask & (1 << vertex)
        )
        value += sum(
            reward
            for left, right, reward in edges
            if mask & (1 << left) and mask & (1 << right)
        )
        best = max(best, value)
    return best
```

For fixed paid vertices, taking every positive internal edge is optimal. This
changes the exponential dimension from `m` to `n`, a genuine improvement when
`n` is much smaller, but still cannot handle `n = 1000`.

## Expert solution: maximum closure via Dinic

```python
from collections import deque
import sys


class Edge:
    __slots__ = ("to", "reverse", "capacity")

    def __init__(self, to: int, reverse: int, capacity: int) -> None:
        self.to = to
        self.reverse = reverse
        self.capacity = capacity


class Dinic:
    def __init__(self, vertex_count: int) -> None:
        self.graph: list[list[Edge]] = [[] for _ in range(vertex_count)]
        self.level = [-1] * vertex_count
        self.next_edge = [0] * vertex_count

    def add_edge(self, start: int, end: int, capacity: int) -> None:
        forward = Edge(end, len(self.graph[end]), capacity)
        backward = Edge(start, len(self.graph[start]), 0)
        self.graph[start].append(forward)
        self.graph[end].append(backward)

    def build_levels(self, source: int, sink: int) -> bool:
        self.level = [-1] * len(self.graph)
        self.level[source] = 0
        queue = deque([source])
        while queue:
            node = queue.popleft()
            for edge in self.graph[node]:
                if edge.capacity > 0 and self.level[edge.to] == -1:
                    self.level[edge.to] = self.level[node] + 1
                    queue.append(edge.to)
        return self.level[sink] != -1

    def send(self, node: int, sink: int, pushed: int) -> int:
        if node == sink:
            return pushed
        while self.next_edge[node] < len(self.graph[node]):
            edge = self.graph[node][self.next_edge[node]]
            if edge.capacity > 0 and self.level[edge.to] == self.level[node] + 1:
                sent = self.send(edge.to, sink, min(pushed, edge.capacity))
                if sent:
                    edge.capacity -= sent
                    self.graph[edge.to][edge.reverse].capacity += sent
                    return sent
            self.next_edge[node] += 1
        return 0

    def max_flow(self, source: int, sink: int) -> int:
        total = 0
        infinity = 10**30
        while self.build_levels(source, sink):
            self.next_edge = [0] * len(self.graph)
            while True:
                sent = self.send(source, sink, infinity)
                if sent == 0:
                    break
                total += sent
        return total


def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    vertex_count, edge_count = data[0:2]
    vertex_costs = data[2 : 2 + vertex_count]
    offset = 2 + vertex_count
    graph_edges: list[tuple[int, int, int]] = []
    total_profit = 0

    for _ in range(edge_count):
        left, right, profit = data[offset : offset + 3]
        graph_edges.append((left - 1, right - 1, profit))
        total_profit += profit
        offset += 3

    source = 0
    first_profit_node = 1
    first_vertex_node = first_profit_node + edge_count
    sink = first_vertex_node + vertex_count
    network = Dinic(sink + 1)
    infinity = total_profit + sum(vertex_costs) + 1

    for edge_index, (left, right, profit) in enumerate(graph_edges):
        profit_node = first_profit_node + edge_index
        network.add_edge(source, profit_node, profit)
        network.add_edge(profit_node, first_vertex_node + left, infinity)
        network.add_edge(profit_node, first_vertex_node + right, infinity)

    for vertex, cost in enumerate(vertex_costs):
        network.add_edge(first_vertex_node + vertex, sink, cost)

    print(total_profit - network.max_flow(source, sink))


if __name__ == "__main__":
    solve()
```

Any finite minimum cut respects every profit-to-endpoint dependency. Its
capacity charges exactly for rejected profits and selected vertex costs, so
subtracting it from all available profit gives the best valid net value.

**Complexity:** `O(V^2 E)` worst-case time for Dinic on the constructed
network and `O(V + E)` space, where the constructed graph has `n+m+2` nodes
and `O(n+m)` edges.

