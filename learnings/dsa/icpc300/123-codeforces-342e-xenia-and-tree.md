# ICPC300 123: Codeforces 342E - Xenia and Tree

**Source:** [Codeforces 342E](https://codeforces.com/problemset/problem/342/E)  
**Pattern:** centroid decomposition for dynamic nearest marked vertices

## Exact contract

An unweighted tree has `n` vertices. Vertex `1` is initially red. Process `q`
online queries:

- `1 v`: paint vertex `v` red permanently;
- `2 v`: output the distance from `v` to its nearest red vertex.

## First principles

A centroid splits its component into pieces of at most half the size. Every
vertex belongs to one component at each decomposition level, so it has only
`O(log n)` centroid ancestors.

For every vertex `v`, store `(centroid, distance(v,centroid))` at every level.
For each centroid `c`, maintain the minimum distance from `c` to any red
vertex. Painting `v` relaxes all its centroid records. A query at `v` minimizes

`distance(v,c) + best_red_distance[c]`

over the same records. The centroid where the path between `v` and the chosen
red vertex first meets the decomposition makes this bound exact.

## Cases that decide correctness

- Vertex `1` must be activated before processing queries.
- Painting an already-red vertex changes nothing.
- Tree distance counts edges, not vertices.
- The centroid itself needs a `(centroid,0)` record.
- Component searches must not cross centroids removed at earlier levels.

## Brute force: BFS for every distance query

```python
from collections import deque


def xenia_bfs(
    vertex_count: int,
    edges: list[tuple[int, int]],
    queries: list[tuple[int, int]],
) -> list[int]:
    graph = [[] for _ in range(vertex_count)]
    for first, second in edges:
        graph[first - 1].append(second - 1)
        graph[second - 1].append(first - 1)

    red = {0}
    answers = []
    for query_type, raw_vertex in queries:
        vertex = raw_vertex - 1
        if query_type == 1:
            red.add(vertex)
            continue
        distance = [-1] * vertex_count
        distance[vertex] = 0
        queue = deque([vertex])
        while queue:
            current = queue.popleft()
            if current in red:
                answers.append(distance[current])
                break
            for neighbor in graph[current]:
                if distance[neighbor] == -1:
                    distance[neighbor] = distance[current] + 1
                    queue.append(neighbor)
    return answers
```

Each type-2 query can scan the whole tree.

## Better: precompute all tree distances

```python
def xenia_all_pairs(
    vertex_count: int,
    edges: list[tuple[int, int]],
    queries: list[tuple[int, int]],
) -> list[int]:
    graph = [[] for _ in range(vertex_count)]
    for first, second in edges:
        graph[first - 1].append(second - 1)
        graph[second - 1].append(first - 1)

    distances = [[0] * vertex_count for _ in range(vertex_count)]
    for start in range(vertex_count):
        stack = [(start, -1)]
        while stack:
            vertex, parent = stack.pop()
            for neighbor in graph[vertex]:
                if neighbor != parent:
                    distances[start][neighbor] = distances[start][vertex] + 1
                    stack.append((neighbor, vertex))

    red = {0}
    answers = []
    for query_type, raw_vertex in queries:
        vertex = raw_vertex - 1
        if query_type == 1:
            red.add(vertex)
        else:
            answers.append(min(distances[vertex][target] for target in red))
    return answers
```

Queries avoid graph searches, but `O(n^2)` preprocessing and storage remain
impossible at the source limit.

## Expert solution: centroid distance records

```python
import sys


def solve() -> None:
    input_stream = sys.stdin.buffer
    vertex_count, query_count = map(int, input_stream.readline().split())
    graph = [[] for _ in range(vertex_count)]
    for _ in range(vertex_count - 1):
        first, second = map(int, input_stream.readline().split())
        graph[first - 1].append(second - 1)
        graph[second - 1].append(first - 1)

    blocked = [False] * vertex_count
    centroid_paths: list[list[tuple[int, int]]] = [[] for _ in range(vertex_count)]

    def decompose(entry: int) -> None:
        parent = {entry: -1}
        order = [entry]
        for vertex in order:
            for neighbor in graph[vertex]:
                if neighbor != parent[vertex] and not blocked[neighbor]:
                    parent[neighbor] = vertex
                    order.append(neighbor)

        subtree_size = {vertex: 1 for vertex in order}
        for vertex in reversed(order):
            if parent[vertex] != -1:
                subtree_size[parent[vertex]] += subtree_size[vertex]

        component_size = len(order)
        centroid = entry
        for vertex in order:
            largest_piece = component_size - subtree_size[vertex]
            for neighbor in graph[vertex]:
                if parent.get(neighbor) == vertex:
                    largest_piece = max(largest_piece, subtree_size[neighbor])
            if largest_piece * 2 <= component_size:
                centroid = vertex
                break

        blocked[centroid] = True
        stack = [(centroid, -1, 0)]
        while stack:
            vertex, parent_vertex, distance = stack.pop()
            centroid_paths[vertex].append((centroid, distance))
            for neighbor in graph[vertex]:
                if neighbor != parent_vertex and not blocked[neighbor]:
                    stack.append((neighbor, vertex, distance + 1))

        next_components = [
            neighbor for neighbor in graph[centroid] if not blocked[neighbor]
        ]
        for neighbor in next_components:
            decompose(neighbor)

    decompose(0)

    infinity = vertex_count + 1
    best_red_distance = [infinity] * vertex_count

    def paint(vertex: int) -> None:
        for centroid, distance in centroid_paths[vertex]:
            best_red_distance[centroid] = min(best_red_distance[centroid], distance)

    paint(0)
    answers = []
    for _ in range(query_count):
        query_type, raw_vertex = map(int, input_stream.readline().split())
        vertex = raw_vertex - 1
        if query_type == 1:
            paint(vertex)
        else:
            answer = min(
                distance + best_red_distance[centroid]
                for centroid, distance in centroid_paths[vertex]
            )
            answers.append(str(answer))
    print("\n".join(answers))


if __name__ == "__main__":
    solve()
```

Each red update stores its distance at every centroid capable of mediating a
future path. Taking the minimum over the query vertex's matching records is
therefore both an upper bound realized by a red vertex and the exact optimum.

**Complexity:** `O(n log n)` preprocessing and storage; `O(log n)` per query.
