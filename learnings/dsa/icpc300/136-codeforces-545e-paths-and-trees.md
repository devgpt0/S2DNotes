# 136. Paths and Trees — Codeforces 545E

**Source:** [Codeforces 545E - Paths and Trees](https://codeforces.com/problemset/problem/545/E)  
**Difficulty:** 2200

## 1. Problem in plain words

Given a connected undirected graph with positive edge weights and a source, choose a shortest-path tree rooted at that source. Among all such trees, minimize the sum of the chosen edge weights. Print that sum and the chosen original edge indices.

The functions below use zero-based vertices and return one-based edge indices, matching the source's edge numbering.

## 2. First principles

An edge `(u, v, w)` can be the parent edge of `v` exactly when `dist[u] + w = dist[v]`. After shortest distances are fixed, every non-source vertex can independently choose the lightest eligible incoming edge. Positive weights make the parent's distance smaller, so these choices cannot form a cycle.

## 3. Cases that define correctness

- Parallel edges are distinct and keep distinct source indices.
- Equal-distance relaxations may improve the tree even though they do not improve distance.
- If several eligible edges have the same weight, either is optimal; the code chooses the smaller index.
- The source has no parent edge.

## 4. Brute force: repeated relaxation

Compute distances with Bellman-Ford-style undirected relaxations, then scan every edge to choose the lightest eligible parent for each vertex.

```python
def minimum_shortest_path_tree_brute_force(
    vertex_count: int, edges: list[tuple[int, int, int]], source: int
) -> tuple[int, list[int]]:
    if vertex_count <= 0 or not 0 <= source < vertex_count:
        raise ValueError("invalid graph size or source")
    if any(weight <= 0 for _, _, weight in edges):
        raise ValueError("edge weights must be positive")

    infinity = 10**40
    distance = [infinity] * vertex_count
    distance[source] = 0
    for _ in range(vertex_count - 1):
        changed = False
        for first, second, weight in edges:
            if distance[first] + weight < distance[second]:
                distance[second] = distance[first] + weight
                changed = True
            if distance[second] + weight < distance[first]:
                distance[first] = distance[second] + weight
                changed = True
        if not changed:
            break
    if any(value == infinity for value in distance):
        raise ValueError("the graph must be connected")

    parent_weight = [infinity] * vertex_count
    parent_edge = [-1] * vertex_count
    for edge_index, (first, second, weight) in enumerate(edges, 1):
        if distance[first] + weight == distance[second] and (
            weight < parent_weight[second]
            or weight == parent_weight[second]
            and edge_index < parent_edge[second]
        ):
            parent_weight[second] = weight
            parent_edge[second] = edge_index
        if distance[second] + weight == distance[first] and (
            weight < parent_weight[first]
            or weight == parent_weight[first]
            and edge_index < parent_edge[first]
        ):
            parent_weight[first] = weight
            parent_edge[first] = edge_index

    chosen = [parent_edge[vertex] for vertex in range(vertex_count) if vertex != source]
    return sum(
        parent_weight[vertex] for vertex in range(vertex_count) if vertex != source
    ), chosen
```

Time is `O(nm)` and space is `O(n)`.

## 5. Better approach: Dijkstra, then an edge scan

Positive weights allow Dijkstra's algorithm. Once distances are known, one linear edge scan selects each lightest eligible parent.

```python
from heapq import heappop, heappush


def minimum_shortest_path_tree_two_phase(
    vertex_count: int, edges: list[tuple[int, int, int]], source: int
) -> tuple[int, list[int]]:
    if vertex_count <= 0 or not 0 <= source < vertex_count:
        raise ValueError("invalid graph size or source")

    graph: list[list[tuple[int, int]]] = [[] for _ in range(vertex_count)]
    for first, second, weight in edges:
        if weight <= 0:
            raise ValueError("edge weights must be positive")
        graph[first].append((second, weight))
        graph[second].append((first, weight))

    infinity = 10**40
    distance = [infinity] * vertex_count
    distance[source] = 0
    heap = [(0, source)]
    while heap:
        current_distance, vertex = heappop(heap)
        if current_distance != distance[vertex]:
            continue
        for neighbor, weight in graph[vertex]:
            candidate = current_distance + weight
            if candidate < distance[neighbor]:
                distance[neighbor] = candidate
                heappush(heap, (candidate, neighbor))
    if any(value == infinity for value in distance):
        raise ValueError("the graph must be connected")

    parent_weight = [infinity] * vertex_count
    parent_edge = [-1] * vertex_count
    for edge_index, (first, second, weight) in enumerate(edges, 1):
        for parent, child in ((first, second), (second, first)):
            if distance[parent] + weight == distance[child] and (
                weight < parent_weight[child]
                or weight == parent_weight[child]
                and edge_index < parent_edge[child]
            ):
                parent_weight[child] = weight
                parent_edge[child] = edge_index

    chosen = [parent_edge[vertex] for vertex in range(vertex_count) if vertex != source]
    return sum(
        parent_weight[vertex] for vertex in range(vertex_count) if vertex != source
    ), chosen
```

Time is `O((n + m) log n)` and space is `O(n + m)`.

## 6. Expert solution: tie-aware Dijkstra

During relaxation, record the arriving edge on a strict distance improvement. On an equal-distance arrival, replace it only when that edge is lighter. This produces the optimal tree without a second edge scan.

```python
from heapq import heappop, heappush


def minimum_shortest_path_tree(
    vertex_count: int, edges: list[tuple[int, int, int]], source: int
) -> tuple[int, list[int]]:
    if vertex_count <= 0 or not 0 <= source < vertex_count:
        raise ValueError("invalid graph size or source")

    graph: list[list[tuple[int, int, int]]] = [[] for _ in range(vertex_count)]
    for edge_index, (first, second, weight) in enumerate(edges, 1):
        if weight <= 0:
            raise ValueError("edge weights must be positive")
        graph[first].append((second, weight, edge_index))
        graph[second].append((first, weight, edge_index))

    infinity = 10**40
    distance = [infinity] * vertex_count
    parent_weight = [infinity] * vertex_count
    parent_edge = [-1] * vertex_count
    distance[source] = 0
    heap = [(0, source)]

    while heap:
        current_distance, vertex = heappop(heap)
        if current_distance != distance[vertex]:
            continue
        for neighbor, weight, edge_index in graph[vertex]:
            candidate = current_distance + weight
            if candidate < distance[neighbor]:
                distance[neighbor] = candidate
                parent_weight[neighbor] = weight
                parent_edge[neighbor] = edge_index
                heappush(heap, (candidate, neighbor))
            elif candidate == distance[neighbor] and (
                weight < parent_weight[neighbor]
                or weight == parent_weight[neighbor]
                and edge_index < parent_edge[neighbor]
            ):
                parent_weight[neighbor] = weight
                parent_edge[neighbor] = edge_index

    if any(value == infinity for value in distance):
        raise ValueError("the graph must be connected")
    chosen = [parent_edge[vertex] for vertex in range(vertex_count) if vertex != source]
    total = sum(
        parent_weight[vertex] for vertex in range(vertex_count) if vertex != source
    )
    return total, chosen
```

## 7. Why the expert solution is correct

Dijkstra fixes the true shortest distance of every vertex. Its recorded edge always realizes that distance; equal-distance relaxation retains the lightest such edge. Every shortest-path tree needs one eligible edge per non-source vertex, so choosing each independently lightest edge minimizes their sum. Positive weights orient every chosen edge toward smaller distance, proving the chosen edges form a tree.

Time is `O((n + m) log n)` and space is `O(n + m)`.
