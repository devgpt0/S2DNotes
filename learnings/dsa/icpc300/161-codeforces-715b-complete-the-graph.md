# ICPC300 161: Codeforces 715B - Complete The Graph

**Source:** [Codeforces 715B](https://codeforces.com/problemset/problem/715/B)  
**Pattern:** constructive Dijkstra with lower-bound potentials

## Exact contract

An undirected graph has positive weighted edges and edges whose input weight is
zero. Replace every zero by a positive integer at most `10^18` so that the
shortest-path distance from given vertex `s` to vertex `t` is exactly `L`.
Print `NO` if impossible; otherwise print `YES` and every edge with its final
weight in input order.

## First principles

First assign every unknown edge weight `1` and run Dijkstra from `t`. Let
`lower[v]` be the smallest possible remaining distance from `v` to `t`. If
`lower[s] > L`, even minimum weights are too large.

Run Dijkstra from `s`. When scanning an originally unknown edge `u-v`, raise
its shared weight to at least

`L - distance[u] - lower[v]`.

This prevents the currently formed route through `v` from finishing below
`L`, while never raising an edge more than necessary. A final Dijkstra verifies
the exact distance; verification also makes failure explicit for disconnected
or otherwise impossible instances.

## Cases that decide correctness

- Zero means an unspecified positive weight, not a zero-cost edge.
- The graph is undirected, so both adjacency entries share one edge weight.
- Several unknown edges can occur on the constructed shortest path.
- A minimum-weight shortest path longer than `L` is immediately impossible.
- Print all edges, including known edges and unused unknown edges.

## Brute force: enumerate small unknown weights

```python
from heapq import heappop, heappush
from itertools import product


def complete_graph_brute(
    vertex_count: int,
    edges: list[tuple[int, int, int]],
    target_distance: int,
    source: int,
    target: int,
) -> list[int] | None:
    unknown = [index for index, edge in enumerate(edges) if edge[2] == 0]
    graph = [[] for _ in range(vertex_count)]
    for edge_index, (first, second, _) in enumerate(edges):
        graph[first].append((second, edge_index))
        graph[second].append((first, edge_index))

    def shortest(weights: list[int]) -> int:
        infinity = 10**30
        distance = [infinity] * vertex_count
        distance[source] = 0
        queue = [(0, source)]
        while queue:
            current_distance, vertex = heappop(queue)
            if current_distance != distance[vertex]:
                continue
            for neighbor, edge_index in graph[vertex]:
                candidate = current_distance + weights[edge_index]
                if candidate < distance[neighbor]:
                    distance[neighbor] = candidate
                    heappush(queue, (candidate, neighbor))
        return distance[target]

    for replacements in product(range(1, target_distance + 2), repeat=len(unknown)):
        weights = [weight for _, _, weight in edges]
        for edge_index, weight in zip(unknown, replacements, strict=True):
            weights[edge_index] = weight
        if shortest(weights) == target_distance:
            return weights
    return None
```

Testing `L+1` is enough to disable an unknown edge in a small brute instance,
but the search is exponential in the number of unknown edges.

## Better insight: minimum and maximum assignments are not enough

Checking all unknown weights as `1` detects targets below the attainable
minimum. Assigning every unknown edge a huge weight can detect a known-edge
route that is already too short. Those two checks do not construct interacting
unknown weights, so there is no separate exact intermediate algorithm; the
second Dijkstra performs the necessary per-edge construction.

## Expert solution: raise unknown edges during Dijkstra

```python
import sys
from heapq import heappop, heappush


def construct_weights(
    vertex_count: int,
    edges: list[tuple[int, int, int]],
    target_distance: int,
    source: int,
    target: int,
) -> list[int] | None:
    graph: list[list[tuple[int, int]]] = [[] for _ in range(vertex_count)]
    weights = []
    unknown = []
    for edge_index, (first, second, weight) in enumerate(edges):
        graph[first].append((second, edge_index))
        graph[second].append((first, edge_index))
        weights.append(max(1, weight))
        unknown.append(weight == 0)

    infinity = 10**30

    def dijkstra(start: int) -> list[int]:
        distance = [infinity] * vertex_count
        distance[start] = 0
        queue = [(0, start)]
        while queue:
            current_distance, vertex = heappop(queue)
            if current_distance != distance[vertex]:
                continue
            for neighbor, edge_index in graph[vertex]:
                candidate = current_distance + weights[edge_index]
                if candidate < distance[neighbor]:
                    distance[neighbor] = candidate
                    heappush(queue, (candidate, neighbor))
        return distance

    lower = dijkstra(target)
    if lower[source] > target_distance:
        return None

    distance = [infinity] * vertex_count
    distance[source] = 0
    queue = [(0, source)]
    while queue:
        current_distance, vertex = heappop(queue)
        if current_distance != distance[vertex]:
            continue
        for neighbor, edge_index in graph[vertex]:
            if unknown[edge_index]:
                required = target_distance - current_distance - lower[neighbor]
                weights[edge_index] = max(weights[edge_index], required)
            candidate = current_distance + weights[edge_index]
            if candidate < distance[neighbor]:
                distance[neighbor] = candidate
                heappush(queue, (candidate, neighbor))

    if dijkstra(source)[target] != target_distance:
        return None
    return weights


def solve() -> None:
    input_stream = sys.stdin.buffer
    vertex_count, edge_count, target_distance, source, target = map(
        int, input_stream.readline().split()
    )
    edges = []
    for _ in range(edge_count):
        first, second, weight = map(int, input_stream.readline().split())
        edges.append((first, second, weight))

    weights = construct_weights(vertex_count, edges, target_distance, source, target)
    if weights is None:
        print("NO")
        return
    print("YES")
    for (first, second, _), weight in zip(edges, weights, strict=True):
        print(first, second, weight)


if __name__ == "__main__":
    solve()
```

The first distances are lower bounds under every legal assignment. Each raised
edge makes the currently considered completion reach at least `L`; Dijkstra's
settling order preserves that invariant. The explicit final check proves the
printed graph meets the contract.

**Complexity:** three Dijkstra runs, `O((n+m) log n)` time and `O(n+m)` space.
