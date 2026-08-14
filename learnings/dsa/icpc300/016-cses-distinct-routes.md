# ICPC300 016: CSES - Distinct Routes

**Source:** [CSES - Distinct Routes](https://cses.fi/problemset/task/1711/)  
**Pattern:** unit-capacity maximum flow plus flow decomposition  
**Goal:** Find the maximum number of directed routes from city `1` to city `n`
that share no flight, and output the actual routes.

## 1. Problem in plain words

Routes may share cities but not directed edges. Parallel flights are distinct
edges and may support different routes.

Give every flight capacity `1`. Sending one unit of flow along an edge means
one selected route uses that flight. Integral maximum flow therefore gives the
maximum number of edge-disjoint routes. The remaining task is to turn used
flow edges back into explicit paths.

The functions below use cities `0` through `n - 1`; add one when formatting
the source output.

## 2. First principles

Any collection of `k` edge-disjoint routes defines a feasible flow of value
`k`. Conversely, an integral flow can be decomposed into source-to-sink paths
and directed cycles. Discarding cycles preserves the flow value, leaving the
required routes.

The max-flow min-cut theorem proves optimality: a maximum flow has the same
value as a minimum set of flights whose removal separates source and sink, so
no larger route collection exists.

## 3. Cases that decide correctness

| Case | Required behavior |
| --- | --- |
| No source-to-sink path | Return an empty list. |
| Parallel flights | Treat their capacities separately. |
| Routes meet at a city | Allowed if their edges differ. |
| Flow contains a directed cycle | Ignore or remove it during decomposition. |
| An original reverse flight exists | Keep it distinct from a residual edge. |

## 4. Brute force: enumerate paths, then choose disjoint ones

For a tiny graph, enumerate every simple source-to-sink path by edge ID. Cycles
never help an edge-disjoint solution because deleting a cycle keeps a route
valid. Then solve the resulting set-packing problem by backtracking.

```python
def edge_disjoint_routes_brute_force(
    vertex_count: int, edges: list[tuple[int, int]]
) -> list[list[int]]:
    source = 0
    sink = vertex_count - 1
    graph: list[list[int]] = [[] for _ in range(vertex_count)]
    for edge_id, (start, _) in enumerate(edges):
        graph[start].append(edge_id)

    paths: list[tuple[list[int], frozenset[int]]] = []

    def enumerate_paths(
        node: int,
        seen_vertices: set[int],
        route: list[int],
        route_edges: list[int],
    ) -> None:
        if node == sink:
            paths.append((route.copy(), frozenset(route_edges)))
            return
        for edge_id in graph[node]:
            neighbor = edges[edge_id][1]
            if neighbor in seen_vertices:
                continue
            seen_vertices.add(neighbor)
            route.append(neighbor)
            route_edges.append(edge_id)
            enumerate_paths(neighbor, seen_vertices, route, route_edges)
            route_edges.pop()
            route.pop()
            seen_vertices.remove(neighbor)

    enumerate_paths(source, {source}, [source], [])
    best: list[list[int]] = []

    def choose(
        path_index: int, used_edges: set[int], selected: list[list[int]]
    ) -> None:
        nonlocal best
        if len(selected) + len(paths) - path_index <= len(best):
            return
        if path_index == len(paths):
            best = [route.copy() for route in selected]
            return

        route, path_edges = paths[path_index]
        if used_edges.isdisjoint(path_edges):
            selected.append(route)
            choose(path_index + 1, used_edges | path_edges, selected)
            selected.pop()
        choose(path_index + 1, used_edges, selected)

    choose(0, set(), [])
    return best
```

**Complexity:** exponential in both the number of simple paths and the path
selection step. Use it only as a tiny oracle.

## 5. Better: Edmonds-Karp finds the maximum count

Breadth-first search repeatedly finds a shortest augmenting path in the
residual graph. This computes the route count, but the capacity matrix merges
parallel flights, so it deliberately does not solve the source's path-output
requirement.

```python
from collections import deque


def maximum_edge_disjoint_route_count(
    vertex_count: int, edges: list[tuple[int, int]]
) -> int:
    source = 0
    sink = vertex_count - 1
    residual = [[0] * vertex_count for _ in range(vertex_count)]
    graph: list[set[int]] = [set() for _ in range(vertex_count)]
    for start, end in edges:
        residual[start][end] += 1
        graph[start].add(end)
        graph[end].add(start)

    flow = 0
    while True:
        parent = [-1] * vertex_count
        parent[source] = source
        queue = deque([source])
        while queue and parent[sink] == -1:
            node = queue.popleft()
            for neighbor in graph[node]:
                if parent[neighbor] == -1 and residual[node][neighbor] > 0:
                    parent[neighbor] = node
                    queue.append(neighbor)

        if parent[sink] == -1:
            return flow

        node = sink
        while node != source:
            previous = parent[node]
            residual[previous][node] -= 1
            residual[node][previous] += 1
            node = previous
        flow += 1
```

**Complexity:** `O(V E^2)` time and `O(V^2)` memory.

## 6. Expert solution: Dinic flow and explicit decomposition

Each original flight keeps its own residual edge object, preserving parallel
edges. After Dinic finishes, an original unit edge with residual capacity `0`
carries one unit of flow. Repeated DFS finds a used source-to-sink path, removes
its edges, and safely skips any used-flow cycles.

```python
from collections import deque


class FlowEdge:
    __slots__ = ("to", "reverse", "capacity")

    def __init__(self, to: int, reverse: int, capacity: int) -> None:
        self.to = to
        self.reverse = reverse
        self.capacity = capacity


def edge_disjoint_routes(
    vertex_count: int, edges: list[tuple[int, int]]
) -> list[list[int]]:
    if vertex_count < 2:
        raise ValueError("source and sink must be different cities")

    source = 0
    sink = vertex_count - 1
    graph: list[list[FlowEdge]] = [[] for _ in range(vertex_count)]
    original_edges: list[tuple[int, FlowEdge]] = []

    def add_edge(start: int, end: int) -> None:
        forward = FlowEdge(end, len(graph[end]), 1)
        backward = FlowEdge(start, len(graph[start]), 0)
        graph[start].append(forward)
        graph[end].append(backward)
        original_edges.append((start, forward))

    for start, end in edges:
        if not 0 <= start < vertex_count or not 0 <= end < vertex_count:
            raise ValueError("flight endpoint is outside the graph")
        add_edge(start, end)

    flow_value = 0
    while True:
        level = [-1] * vertex_count
        level[source] = 0
        queue = deque([source])
        while queue:
            node = queue.popleft()
            for edge in graph[node]:
                if edge.capacity > 0 and level[edge.to] == -1:
                    level[edge.to] = level[node] + 1
                    queue.append(edge.to)
        if level[sink] == -1:
            break

        next_edge = [0] * vertex_count

        def send_flow(node: int, pushed: int) -> int:
            if node == sink:
                return pushed
            while next_edge[node] < len(graph[node]):
                edge = graph[node][next_edge[node]]
                if edge.capacity > 0 and level[edge.to] == level[node] + 1:
                    sent = send_flow(edge.to, min(pushed, edge.capacity))
                    if sent > 0:
                        edge.capacity -= sent
                        graph[edge.to][edge.reverse].capacity += sent
                        return sent
                next_edge[node] += 1
            return 0

        while True:
            sent = send_flow(source, vertex_count)
            if sent == 0:
                break
            flow_value += sent

    used_graph: list[list[int]] = [[] for _ in range(vertex_count)]
    destinations: list[int] = []
    active: list[bool] = []
    for start, edge in original_edges:
        edge_id = len(destinations)
        destinations.append(edge.to)
        active.append(edge.capacity == 0)
        if edge.capacity == 0:
            used_graph[start].append(edge_id)

    def find_used_path(node: int, seen: list[bool]) -> list[int] | None:
        if node == sink:
            return []
        seen[node] = True
        for edge_id in used_graph[node]:
            if not active[edge_id]:
                continue
            neighbor = destinations[edge_id]
            if seen[neighbor]:
                continue
            suffix = find_used_path(neighbor, seen)
            if suffix is not None:
                return [edge_id, *suffix]
        return None

    routes: list[list[int]] = []
    for _ in range(flow_value):
        path_edges = find_used_path(source, [False] * vertex_count)
        if path_edges is None:
            raise RuntimeError("integral flow decomposition failed")
        route = [source]
        for edge_id in path_edges:
            active[edge_id] = False
            route.append(destinations[edge_id])
        routes.append(route)

    return routes
```

### Why the expert code is correct

- Unit capacities enforce that no original flight carries two routes.
- Integral augmentations produce an integral maximum flow.
- Flow conservation guarantees a used source-to-sink path remains until all
  `flow_value` units are removed; DFS backtracking avoids closed cycles.
- Decomposition removes each used edge at most once from returned routes, so
  the routes are edge-disjoint and their count equals maximum flow.

Dinic uses `O(V^2 E)` worst-case time on a general network and `O(V + E)`
residual memory. The straightforward decomposition costs `O(FE)`, where `F`
is the number of returned routes, which fits this source's network size.

## 7. What to remember

Unit capacity turns edge-disjoint paths into integral flow. When a problem asks
for the paths, the algorithm is not finished until that flow is decomposed.
