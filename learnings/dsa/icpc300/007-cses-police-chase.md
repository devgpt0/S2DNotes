# ICPC300 007: CSES - Police Chase

**Source:** [CSES - Police Chase](https://cses.fi/problemset/task/1695/)  
**Pattern:** maximum flow / minimum cut  
**Goal:** Remove the fewest undirected roads so vertex `0` cannot reach vertex
`n - 1`, and report those roads.

## 1. First principles

Give every road capacity `1` in both directions. Any source-to-sink flow must
cross every separating cut, so its value cannot exceed the cut's capacity. The
max-flow/min-cut theorem says the maximum flow value equals the minimum cut.

After maximum flow, follow every residual edge with positive capacity from the
source. An original road with exactly one reachable endpoint crosses the
minimum cut.

```text
residual reachable side | residual unreachable side
          u              |              v
                         |
original road u -- v is a reported cut edge
```

## 2. Cases that decide correctness

| Case | Required behavior |
| --- | --- |
| Source and sink already disconnected | Return an empty cut. |
| Direct source-sink road | It may itself be a cut edge. |
| Parallel roads | Each physical road contributes one capacity and may need reporting. |
| Road orientation | Input is undirected; output may orient it reachable to unreachable. |
| Residual reverse edge | It must allow an earlier flow choice to be undone. |

## 3. Brute force: enumerate road subsets

Try subsets in increasing size and run reachability without the selected
roads. The first disconnecting subset is minimum.

```python
from itertools import combinations


def minimum_road_cut_brute(
    vertex_count: int,
    roads: list[tuple[int, int]],
    source: int = 0,
    sink: int | None = None,
) -> list[tuple[int, int]]:
    if vertex_count <= 0:
        raise ValueError("vertex_count must be positive")
    if sink is None:
        sink = vertex_count - 1
    if source == sink:
        raise ValueError("source and sink must be different")
    if any(
        first < 0 or first >= vertex_count or second < 0 or second >= vertex_count
        for first, second in roads
    ):
        raise ValueError("road endpoint is outside the graph")

    adjacency: list[list[tuple[int, int]]] = [[] for _ in range(vertex_count)]
    for road_index, (first, second) in enumerate(roads):
        adjacency[first].append((second, road_index))
        adjacency[second].append((first, road_index))

    for cut_size in range(len(roads) + 1):
        for cut_indices in combinations(range(len(roads)), cut_size):
            blocked = set(cut_indices)
            reachable = [False] * vertex_count
            reachable[source] = True
            stack = [source]

            while stack:
                node = stack.pop()
                for neighbor, road_index in adjacency[node]:
                    if road_index not in blocked and not reachable[neighbor]:
                        reachable[neighbor] = True
                        stack.append(neighbor)

            if reachable[sink]:
                continue

            cut: list[tuple[int, int]] = []
            for road_index in cut_indices:
                first, second = roads[road_index]
                if reachable[first]:
                    cut.append((first, second))
                else:
                    cut.append((second, first))
            return cut

    raise RuntimeError("removing every road must disconnect source and sink")
```

**Complexity:** `O(2^E * (V + E))` time and `O(V + E)` space.

## 4. Better: Edmonds-Karp

Repeated BFS chooses a shortest residual augmenting path. A capacity matrix
also combines parallel roads naturally.

```python
from collections import deque


def minimum_road_cut_edmonds_karp(
    vertex_count: int,
    roads: list[tuple[int, int]],
    source: int = 0,
    sink: int | None = None,
) -> list[tuple[int, int]]:
    if vertex_count <= 0:
        raise ValueError("vertex_count must be positive")
    if sink is None:
        sink = vertex_count - 1
    if source == sink:
        raise ValueError("source and sink must be different")
    if any(
        first < 0 or first >= vertex_count or second < 0 or second >= vertex_count
        for first, second in roads
    ):
        raise ValueError("road endpoint is outside the graph")

    residual = [[0] * vertex_count for _ in range(vertex_count)]
    adjacency: list[set[int]] = [set() for _ in range(vertex_count)]
    for first, second in roads:
        residual[first][second] += 1
        residual[second][first] += 1
        adjacency[first].add(second)
        adjacency[second].add(first)

    while True:
        parent = [-1] * vertex_count
        parent[source] = source
        queue = deque([source])

        while queue and parent[sink] == -1:
            node = queue.popleft()
            for neighbor in adjacency[node]:
                if parent[neighbor] == -1 and residual[node][neighbor] > 0:
                    parent[neighbor] = node
                    queue.append(neighbor)

        if parent[sink] == -1:
            break

        path_capacity = len(roads) + 1
        node = sink
        while node != source:
            previous = parent[node]
            path_capacity = min(path_capacity, residual[previous][node])
            node = previous

        node = sink
        while node != source:
            previous = parent[node]
            residual[previous][node] -= path_capacity
            residual[node][previous] += path_capacity
            node = previous

    reachable = [False] * vertex_count
    reachable[source] = True
    stack = [source]
    while stack:
        node = stack.pop()
        for neighbor in adjacency[node]:
            if residual[node][neighbor] > 0 and not reachable[neighbor]:
                reachable[neighbor] = True
                stack.append(neighbor)

    return [
        (first, second) if reachable[first] else (second, first)
        for first, second in roads
        if reachable[first] != reachable[second]
    ]
```

**Complexity:** `O(VE^2)` time and `O(V^2)` space.

## 5. Expert solution: Dinic's algorithm

Dinic builds a residual level graph with BFS, then sends a blocking flow with
DFS before rebuilding levels. Two directed unit-capacity arcs model each
undirected road.

```python
from collections import deque
from dataclasses import dataclass


@dataclass(slots=True)
class FlowEdge:
    destination: int
    reverse_index: int
    capacity: int


def minimum_road_cut_dinic(
    vertex_count: int,
    roads: list[tuple[int, int]],
    source: int = 0,
    sink: int | None = None,
) -> list[tuple[int, int]]:
    if vertex_count <= 0:
        raise ValueError("vertex_count must be positive")
    if sink is None:
        sink = vertex_count - 1
    if source == sink:
        raise ValueError("source and sink must be different")
    if any(
        first < 0 or first >= vertex_count or second < 0 or second >= vertex_count
        for first, second in roads
    ):
        raise ValueError("road endpoint is outside the graph")

    network: list[list[FlowEdge]] = [[] for _ in range(vertex_count)]

    def add_directed_edge(first: int, second: int) -> None:
        forward = FlowEdge(second, len(network[second]), 1)
        reverse = FlowEdge(first, len(network[first]), 0)
        network[first].append(forward)
        network[second].append(reverse)

    for first, second in roads:
        add_directed_edge(first, second)
        add_directed_edge(second, first)

    level = [-1] * vertex_count

    def build_level_graph() -> bool:
        level[:] = [-1] * vertex_count
        level[source] = 0
        queue = deque([source])
        while queue:
            node = queue.popleft()
            for edge in network[node]:
                if edge.capacity > 0 and level[edge.destination] == -1:
                    level[edge.destination] = level[node] + 1
                    queue.append(edge.destination)
        return level[sink] != -1

    def send_flow(node: int, available: int, next_edge: list[int]) -> int:
        if node == sink:
            return available

        while next_edge[node] < len(network[node]):
            edge = network[node][next_edge[node]]
            if edge.capacity > 0 and level[edge.destination] == level[node] + 1:
                pushed = send_flow(
                    edge.destination,
                    min(available, edge.capacity),
                    next_edge,
                )
                if pushed > 0:
                    edge.capacity -= pushed
                    reverse = network[edge.destination][edge.reverse_index]
                    reverse.capacity += pushed
                    return pushed
            next_edge[node] += 1
        return 0

    while build_level_graph():
        next_edge = [0] * vertex_count
        while send_flow(source, len(roads) + 1, next_edge) > 0:
            pass

    reachable = [False] * vertex_count
    reachable[source] = True
    stack = [source]
    while stack:
        node = stack.pop()
        for edge in network[node]:
            if edge.capacity > 0 and not reachable[edge.destination]:
                reachable[edge.destination] = True
                stack.append(edge.destination)

    return [
        (first, second) if reachable[first] else (second, first)
        for first, second in roads
        if reachable[first] != reachable[second]
    ]
```

### Why the expert code is correct

- Residual reverse edges make every augmentation reversible, so a local path
  choice cannot permanently block a better flow.
- Dinic stops only when no residual source-to-sink path exists, so its flow is
  maximum.
- The reachable/unreachable boundary is then a cut whose capacity equals that
  flow, making it a minimum cut.

**Complexity:** `O(V^2 E)` general worst-case time and `O(V + E)` space;
unit capacities are typically much faster at this source's limits.

## 6. What to remember

```text
undirected road -> capacity 1 in each direction
maximum flow value = minimum number of roads to remove
residual reachable XOR unreachable -> report the original road
```
