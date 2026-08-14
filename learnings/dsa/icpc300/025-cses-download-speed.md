# ICPC300 025: CSES - Download Speed

**Source:** [CSES - Download Speed](https://cses.fi/problemset/task/1694/)  
**Pattern:** maximum flow with Dinic's algorithm

## Exact contract

Input describes a directed network with `2 <= n <= 500` computers and
`1 <= m <= 1000` connections. Each connection gives `a`, `b`, and capacity
`c` (`1 <= c <= 10^9`) for a directed link from `a` to `b`. Parallel links
are allowed. Output the maximum total download rate that can be sent from
computer `1` to computer `n`.

## First principles

A feasible flow never exceeds an edge capacity and conserves flow at every
vertex except source and sink. Sending flow creates a reverse residual edge:
later augmentations may cancel earlier choices instead of being trapped by
them.

The max-flow min-cut theorem says the greatest feasible flow equals the least
total capacity of edges crossing from a source-side vertex set to its
complement. The brute force uses cuts; the efficient algorithms construct the
same value through residual augmenting paths.

## Cases that decide correctness

- Connections are directed; capacity `a -> b` says nothing about `b -> a`.
- Parallel capacities must add or remain as separate residual edges.
- Capacities and the answer require Python integers (or 64-bit integers in
  fixed-width languages).
- A reverse residual edge starts with capacity zero but becomes usable after
  sending flow.

## Brute force: enumerate every source-side cut

```python
def max_flow_by_cuts(vertex_count: int, edges: list[tuple[int, int, int]]) -> int:
    best = sum(capacity for _, _, capacity in edges)

    for mask in range(1 << (vertex_count - 2)):
        source_side = [False] * vertex_count
        source_side[0] = True
        for vertex in range(1, vertex_count - 1):
            source_side[vertex] = bool(mask & (1 << (vertex - 1)))

        cut_capacity = sum(
            capacity
            for start, end, capacity in edges
            if source_side[start] and not source_side[end]
        )
        best = min(best, cut_capacity)

    return best
```

This is an executable form of the min-cut definition.

**Complexity:** `O(2^(n-2) m)` time and `O(n)` space.

## Better: Edmonds-Karp shortest augmenting paths

```python
from collections import deque


def max_flow_edmonds_karp(vertex_count: int, edges: list[tuple[int, int, int]]) -> int:
    capacity = [[0] * vertex_count for _ in range(vertex_count)]
    graph = [[] for _ in range(vertex_count)]

    for start, end, edge_capacity in edges:
        capacity[start][end] += edge_capacity
        if end not in graph[start]:
            graph[start].append(end)
            graph[end].append(start)

    source = 0
    sink = vertex_count - 1
    total_flow = 0

    while True:
        parent = [-1] * vertex_count
        parent[source] = source
        queue = deque([source])

        while queue and parent[sink] == -1:
            node = queue.popleft()
            for neighbor in graph[node]:
                if parent[neighbor] == -1 and capacity[node][neighbor] > 0:
                    parent[neighbor] = node
                    queue.append(neighbor)

        if parent[sink] == -1:
            return total_flow

        added = 10**30
        node = sink
        while node != source:
            previous = parent[node]
            added = min(added, capacity[previous][node])
            node = previous

        node = sink
        while node != source:
            previous = parent[node]
            capacity[previous][node] -= added
            capacity[node][previous] += added
            node = previous
        total_flow += added
```

BFS prevents pathological augmenting-path choices, giving
`O(V E^2)` time. The `O(V^2)` capacity matrix is acceptable only because this
source has at most 500 vertices.

## Expert solution: Dinic's blocking flows

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
        if start == end:
            return
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

    def send_flow(self, node: int, sink: int, pushed: int) -> int:
        if node == sink:
            return pushed

        while self.next_edge[node] < len(self.graph[node]):
            edge = self.graph[node][self.next_edge[node]]
            if edge.capacity > 0 and self.level[edge.to] == self.level[node] + 1:
                sent = self.send_flow(edge.to, sink, min(pushed, edge.capacity))
                if sent > 0:
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
                sent = self.send_flow(source, sink, infinity)
                if sent == 0:
                    break
                total += sent
        return total


def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    vertex_count, edge_count = data[0], data[1]
    network = Dinic(vertex_count)
    offset = 2
    for _ in range(edge_count):
        start, end, capacity = data[offset : offset + 3]
        network.add_edge(start - 1, end - 1, capacity)
        offset += 3
    print(network.max_flow(0, vertex_count - 1))


if __name__ == "__main__":
    solve()
```

The level graph keeps only shortest residual progress toward the sink. Reusing
the `next_edge` pointer makes one phase a blocking flow: no more source-sink
path remains in that level graph.

**Complexity:** `O(V^2 E)` worst-case time for general capacities and
`O(V + E)` space.

