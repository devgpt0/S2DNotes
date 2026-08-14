# ICPC300 029: CSES - Distinct Routes II

**Source:** [CSES - Distinct Routes II](https://cses.fi/problemset/task/2130/)  
**Pattern:** unit-capacity minimum-cost flow and path decomposition

## Exact contract

Input gives `n`, `m`, and `k` (`2 <= n <= 500`, `1 <= m <= 1000`,
`1 <= k <= 10`) followed by `m` directed flights. Find exactly `k`
edge-disjoint routes from vertex `1` to vertex `n` whose total number of
flights is minimum.

If impossible, output `-1`. Otherwise output the minimum total number of
flights. Then output `k` route descriptions, each as its vertex count on one
line and its one-based vertex sequence on the next line.

## First principles

Give each input flight capacity one and cost one. A flow of value `k` is
exactly `k` edge-disjoint routes after integral-flow decomposition, and its
cost is their total number of flights.

Residual reverse edges cost `-1`: using one cancels a previously chosen
flight. That cancellation is why choosing the currently shortest unused path
greedily is not sufficient, while minimum-cost flow is.

## Cases that decide correctness

- The required flow is exactly `k`; fewer routes mean `-1`.
- Parallel flights are distinct edges and may appear in different routes.
- Routes may share vertices, but never an input edge.
- Only original edges carrying final flow belong in output; residual reverse
  edges never do.
- Extracted edges must be consumed so no flight is printed twice.

## Brute force: enumerate paths and disjoint combinations

```python
def shortest_distinct_routes_brute(
    vertex_count: int,
    edges: list[tuple[int, int]],
    required_routes: int,
) -> int:
    graph: list[list[tuple[int, int]]] = [[] for _ in range(vertex_count)]
    for edge_id, (start, end) in enumerate(edges):
        graph[start].append((end, edge_id))

    paths: list[frozenset[int]] = []

    def enumerate_paths(node: int, visited: set[int], edge_ids: list[int]) -> None:
        if node == vertex_count - 1:
            paths.append(frozenset(edge_ids))
            return
        for neighbor, edge_id in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                edge_ids.append(edge_id)
                enumerate_paths(neighbor, visited, edge_ids)
                edge_ids.pop()
                visited.remove(neighbor)

    enumerate_paths(0, {0}, [])
    best = 10**30

    def choose(
        path_index: int, used_edges: set[int], chosen: int, total_length: int
    ) -> None:
        nonlocal best
        if chosen == required_routes:
            best = min(best, total_length)
            return
        if path_index == len(paths):
            return
        choose(path_index + 1, used_edges, chosen, total_length)
        path = paths[path_index]
        if path.isdisjoint(used_edges):
            choose(
                path_index + 1,
                used_edges | set(path),
                chosen + 1,
                total_length + len(path),
            )

    choose(0, set(), 0, 0)
    return -1 if best == 10**30 else best
```

An optimal route has no cycle because every flight costs one. Path enumeration
and subset selection are nevertheless exponential.

## Better: SPFA-based minimum-cost flow

```python
from collections import deque


def shortest_distinct_route_cost_spfa(
    vertex_count: int,
    edges: list[tuple[int, int]],
    required_routes: int,
) -> int:
    graph: list[list[list[int]]] = [[] for _ in range(vertex_count)]

    def add_edge(start: int, end: int) -> None:
        forward = [end, len(graph[end]), 1, 1]
        backward = [start, len(graph[start]), 0, -1]
        graph[start].append(forward)
        graph[end].append(backward)

    for start, end in edges:
        if start != end:
            add_edge(start, end)

    source = 0
    sink = vertex_count - 1
    total_cost = 0
    infinity = 10**30

    for _ in range(required_routes):
        distance = [infinity] * vertex_count
        parent_node = [-1] * vertex_count
        parent_edge = [-1] * vertex_count
        in_queue = [False] * vertex_count
        distance[source] = 0
        queue = deque([source])
        in_queue[source] = True

        while queue:
            node = queue.popleft()
            in_queue[node] = False
            for edge_index, edge in enumerate(graph[node]):
                neighbor, _, capacity, cost = edge
                candidate = distance[node] + cost
                if capacity and candidate < distance[neighbor]:
                    distance[neighbor] = candidate
                    parent_node[neighbor] = node
                    parent_edge[neighbor] = edge_index
                    if not in_queue[neighbor]:
                        in_queue[neighbor] = True
                        queue.append(neighbor)

        if distance[sink] == infinity:
            return -1

        node = sink
        while node != source:
            previous = parent_node[node]
            edge = graph[previous][parent_edge[node]]
            edge[2] = 0
            graph[node][edge[1]][2] = 1
            node = previous
        total_cost += distance[sink]

    return total_cost
```

SPFA directly handles negative reverse costs. With `k <= 10`, its practical
work is small, but its per-augmentation worst case is `O(VE)`.

## Expert solution: potentials, Dijkstra, and decomposition

```python
from collections import deque
from heapq import heappop, heappush
import sys


class CostEdge:
    __slots__ = ("to", "reverse", "capacity", "cost")

    def __init__(self, to: int, reverse: int, capacity: int, cost: int) -> None:
        self.to = to
        self.reverse = reverse
        self.capacity = capacity
        self.cost = cost


class MinCostFlow:
    def __init__(self, vertex_count: int) -> None:
        self.graph: list[list[CostEdge]] = [[] for _ in range(vertex_count)]

    def add_flight(self, start: int, end: int) -> CostEdge | None:
        if start == end:
            return None
        forward = CostEdge(end, len(self.graph[end]), 1, 1)
        backward = CostEdge(start, len(self.graph[start]), 0, -1)
        self.graph[start].append(forward)
        self.graph[end].append(backward)
        return forward

    def send(self, source: int, sink: int, required: int) -> int | None:
        vertex_count = len(self.graph)
        potential = [0] * vertex_count
        total_cost = 0
        infinity = 10**30

        for _ in range(required):
            distance = [infinity] * vertex_count
            parent_node = [-1] * vertex_count
            parent_edge = [-1] * vertex_count
            distance[source] = 0
            heap = [(0, source)]

            while heap:
                current_distance, node = heappop(heap)
                if current_distance != distance[node]:
                    continue
                for edge_index, edge in enumerate(self.graph[node]):
                    if edge.capacity == 0:
                        continue
                    reduced_cost = edge.cost + potential[node] - potential[edge.to]
                    candidate = current_distance + reduced_cost
                    if candidate < distance[edge.to]:
                        distance[edge.to] = candidate
                        parent_node[edge.to] = node
                        parent_edge[edge.to] = edge_index
                        heappush(heap, (candidate, edge.to))

            if distance[sink] == infinity:
                return None

            for vertex in range(vertex_count):
                if distance[vertex] < infinity:
                    potential[vertex] += distance[vertex]

            node = sink
            path_cost = 0
            while node != source:
                previous = parent_node[node]
                edge = self.graph[previous][parent_edge[node]]
                path_cost += edge.cost
                node = previous

            node = sink
            while node != source:
                previous = parent_node[node]
                edge = self.graph[previous][parent_edge[node]]
                edge.capacity = 0
                self.graph[node][edge.reverse].capacity = 1
                node = previous
            total_cost += path_cost

        return total_cost


def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    vertex_count, edge_count, required_routes = data[0:3]
    network = MinCostFlow(vertex_count)
    original_edges: list[tuple[int, int, CostEdge]] = []
    offset = 3

    for _ in range(edge_count):
        start, end = data[offset] - 1, data[offset + 1] - 1
        offset += 2
        edge = network.add_flight(start, end)
        if edge is not None:
            original_edges.append((start, end, edge))

    total_cost = network.send(0, vertex_count - 1, required_routes)
    if total_cost is None:
        print(-1)
        return

    used_graph: list[list[tuple[int, int]]] = [[] for _ in range(vertex_count)]
    for edge_id, (start, end, edge) in enumerate(original_edges):
        if edge.capacity == 0:
            used_graph[start].append((end, edge_id))

    available = [True] * len(original_edges)
    routes: list[list[int]] = []
    for _ in range(required_routes):
        parent: list[tuple[int, int] | None] = [None] * vertex_count
        parent[0] = (0, -1)
        queue = deque([0])
        while queue and parent[vertex_count - 1] is None:
            node = queue.popleft()
            for neighbor, edge_id in used_graph[node]:
                if available[edge_id] and parent[neighbor] is None:
                    parent[neighbor] = (node, edge_id)
                    queue.append(neighbor)

        path = [vertex_count - 1]
        node = vertex_count - 1
        while node != 0:
            step = parent[node]
            if step is None:
                raise RuntimeError("missing predecessor on an augmenting path")
            previous, edge_id = step
            available[edge_id] = False
            node = previous
            path.append(node)
        path.reverse()
        routes.append(path)

    output = [str(total_cost)]
    for route in routes:
        output.append(str(len(route)))
        output.append(" ".join(str(vertex + 1) for vertex in route))
    print("\n".join(output))


if __name__ == "__main__":
    solve()
```

Potentials keep reduced residual costs nonnegative, so every Dijkstra phase is
valid. Unit capacities make each augmentation add one route. The final
integral flow then decomposes into exactly `k` edge-disjoint paths.

**Complexity:** `O(k E log V + kVE)` worst-case including simple BFS path
extraction, and `O(V + E)` space.
