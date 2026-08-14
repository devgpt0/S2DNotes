# ICPC300 027: CSES - Parcel Delivery

**Source:** [CSES - Parcel Delivery](https://cses.fi/problemset/task/2121/)  
**Pattern:** minimum-cost flow with potentials

## Exact contract

Input gives `n` cities, `m` directed routes, and a required parcel count `k`
(`2 <= n <= 500`, `1 <= m <= 1000`). Each route is described by
`a b c r`: at most `c` parcels can travel from `a` to `b`, and each parcel on
that route costs `r`. Deliver exactly `k` parcels from city `1` to city `n` at
minimum total cost. Output that cost, or `-1` when the network cannot carry
`k` parcels.

## First principles

This is flow with two edge attributes: capacity limits quantity and cost
prices each unit. After sending flow through an edge, its residual reverse edge
has negative cost. Using it means cancelling previously sent flow, which is
essential when a later path reveals a better global arrangement.

The successive-shortest-augmenting-path method repeatedly sends as much flow
as possible along a cheapest residual source-sink path. Vertex potentials turn
all reachable reduced edge costs nonnegative, so Dijkstra remains valid even
though reverse edges have negative original cost.

## Cases that decide correctness

- The goal is exactly `k`; a cheaper partial delivery is not an answer.
- One shortest path can carry more than one parcel, so augment by its
  bottleneck rather than one unit.
- Parallel directed routes remain separate because their costs can differ.
- If the sink becomes unreachable before `k` units arrive, print `-1`.
- Potentials start at zero because all original forward prices are
  nonnegative.

## Brute force: choose one simple route per parcel

```python
def parcel_cost_brute(
    vertex_count: int,
    routes: list[tuple[int, int, int, int]],
    required_flow: int,
) -> int:
    graph: list[list[int]] = [[] for _ in range(vertex_count)]
    for route_id, (start, _, _, _) in enumerate(routes):
        graph[start].append(route_id)

    paths: list[tuple[list[int], int]] = []

    def enumerate_paths(
        node: int, visited: set[int], edge_ids: list[int], cost: int
    ) -> None:
        if node == vertex_count - 1:
            paths.append((edge_ids.copy(), cost))
            return
        for route_id in graph[node]:
            _, neighbor, _, price = routes[route_id]
            if neighbor not in visited:
                visited.add(neighbor)
                edge_ids.append(route_id)
                enumerate_paths(neighbor, visited, edge_ids, cost + price)
                edge_ids.pop()
                visited.remove(neighbor)

    enumerate_paths(0, {0}, [], 0)
    remaining = [capacity for _, _, capacity, _ in routes]
    best = 10**30

    def search(delivered: int, current_cost: int) -> None:
        nonlocal best
        if current_cost >= best:
            return
        if delivered == required_flow:
            best = current_cost
            return
        for edge_ids, path_cost in paths:
            if all(remaining[edge_id] > 0 for edge_id in edge_ids):
                for edge_id in edge_ids:
                    remaining[edge_id] -= 1
                search(delivered + 1, current_cost + path_cost)
                for edge_id in edge_ids:
                    remaining[edge_id] += 1

    search(0, 0)
    return -1 if best == 10**30 else best
```

With nonnegative prices an optimal flow needs no cost-increasing cycle, so it
can be decomposed into simple routes. The enumeration is exponential and only
serves as a tiny-instance oracle.

## Better: shortest augmenting paths with SPFA

```python
from collections import deque


def min_cost_flow_spfa(
    vertex_count: int,
    routes: list[tuple[int, int, int, int]],
    required_flow: int,
) -> int:
    graph: list[list[list[int]]] = [[] for _ in range(vertex_count)]

    def add_edge(start: int, end: int, capacity: int, cost: int) -> None:
        forward = [end, len(graph[end]), capacity, cost]
        backward = [start, len(graph[start]), 0, -cost]
        graph[start].append(forward)
        graph[end].append(backward)

    for start, end, capacity, cost in routes:
        if start != end:
            add_edge(start, end, capacity, cost)

    source = 0
    sink = vertex_count - 1
    flow = 0
    total_cost = 0
    infinity = 10**30

    while flow < required_flow:
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
                if capacity > 0 and candidate < distance[neighbor]:
                    distance[neighbor] = candidate
                    parent_node[neighbor] = node
                    parent_edge[neighbor] = edge_index
                    if not in_queue[neighbor]:
                        queue.append(neighbor)
                        in_queue[neighbor] = True

        if distance[sink] == infinity:
            return -1

        added = required_flow - flow
        node = sink
        while node != source:
            previous = parent_node[node]
            edge = graph[previous][parent_edge[node]]
            added = min(added, edge[2])
            node = previous

        node = sink
        while node != source:
            previous = parent_node[node]
            edge = graph[previous][parent_edge[node]]
            edge[2] -= added
            graph[node][edge[1]][2] += added
            node = previous

        flow += added
        total_cost += added * distance[sink]

    return total_cost
```

SPFA handles negative reverse edges directly and is often adequate here, but
it has poor `O(VE)` worst-case time per augmentation.

## Expert solution: potentials and Dijkstra

```python
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

    def add_edge(self, start: int, end: int, capacity: int, cost: int) -> None:
        if start == end:
            return
        forward = CostEdge(end, len(self.graph[end]), capacity, cost)
        backward = CostEdge(start, len(self.graph[start]), 0, -cost)
        self.graph[start].append(forward)
        self.graph[end].append(backward)

    def send(self, source: int, sink: int, required: int) -> int | None:
        vertex_count = len(self.graph)
        potential = [0] * vertex_count
        flow = 0
        total_cost = 0
        infinity = 10**30

        while flow < required:
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

            added = required - flow
            path_cost = 0
            node = sink
            while node != source:
                previous = parent_node[node]
                edge = self.graph[previous][parent_edge[node]]
                added = min(added, edge.capacity)
                path_cost += edge.cost
                node = previous

            node = sink
            while node != source:
                previous = parent_node[node]
                edge = self.graph[previous][parent_edge[node]]
                edge.capacity -= added
                self.graph[node][edge.reverse].capacity += added
                node = previous

            flow += added
            total_cost += added * path_cost

        return total_cost


def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    vertex_count, route_count, required = data[0:3]
    network = MinCostFlow(vertex_count)
    offset = 3
    for _ in range(route_count):
        start, end, capacity, cost = data[offset : offset + 4]
        network.add_edge(start - 1, end - 1, capacity, cost)
        offset += 4

    answer = network.send(0, vertex_count - 1, required)
    print(-1 if answer is None else answer)


if __name__ == "__main__":
    solve()
```

Reduced costs are nonnegative after each potential update, so Dijkstra returns
a true cheapest residual path. Augmenting its entire bottleneck preserves
integrality and minimizes the cost for every achieved flow value in order.

**Complexity:** `O(A E log V)` time and `O(V + E)` space, where `A` is the
number of augmentations; one augmentation may send many parcels.

