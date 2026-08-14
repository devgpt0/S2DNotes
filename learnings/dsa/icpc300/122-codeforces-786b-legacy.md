# ICPC300 122: Codeforces 786B - Legacy

**Source:** [Codeforces 786B](https://codeforces.com/problemset/problem/786/B)  
**Pattern:** range edges represented by directed segment-tree graphs

## Exact contract

There are `n` vertices, a source `s`, and `q` edge-addition queries:

- `1 v u w`: add directed edge `v -> u` of weight `w`;
- `2 v l r w`: add `v -> u` of weight `w` for every `u` in `[l,r]`;
- `3 v l r w`: add `u -> v` of weight `w` for every `u` in `[l,r]`.

After all queries, output the shortest distance from `s` to every original
vertex, or `-1` when unreachable. All weights are positive.

## First principles

A segment tree decomposes any interval into `O(log n)` canonical nodes. For
edges *to* a range, direct zero-weight edges from each segment node down to its
children; one weighted edge from `v` to every canonical node reaches exactly
the requested leaves. For edges *from* a range, reverse the zero edges in a
second tree and connect canonical nodes to `v`.

The leaves are the original graph vertices, so ordinary point edges and both
range constructions coexist in one graph. Dijkstra then solves the resulting
nonnegative shortest-path instance.

## Cases that decide correctness

- Query endpoints are inclusive and one-based.
- The outgoing and incoming segment trees need opposite zero-edge directions.
- Auxiliary nodes must never appear in the printed answer.
- Multiple and self edges are harmless to Dijkstra.
- Unreachable original vertices print `-1`.

## Brute force: expand every range edge

```python
from heapq import heappop, heappush


def legacy_expanded(
    vertex_count: int,
    source: int,
    queries: list[tuple[int, ...]],
) -> list[int]:
    graph: list[list[tuple[int, int]]] = [[] for _ in range(vertex_count)]
    for query in queries:
        query_type = query[0]
        if query_type == 1:
            _, vertex, target, weight = query
            graph[vertex - 1].append((target - 1, weight))
        elif query_type == 2:
            _, vertex, left, right, weight = query
            for target in range(left - 1, right):
                graph[vertex - 1].append((target, weight))
        else:
            _, vertex, left, right, weight = query
            for start in range(left - 1, right):
                graph[start].append((vertex - 1, weight))

    infinity = 10**30
    distance = [infinity] * vertex_count
    distance[source - 1] = 0
    queue = [(0, source - 1)]
    while queue:
        current_distance, vertex = heappop(queue)
        if current_distance != distance[vertex]:
            continue
        for neighbor, weight in graph[vertex]:
            candidate = current_distance + weight
            if candidate < distance[neighbor]:
                distance[neighbor] = candidate
                heappush(queue, (candidate, neighbor))
    return [-1 if value == infinity else value for value in distance]
```

One query can create `Theta(n)` edges, so expansion is quadratic overall.

## Better: square-root range nodes

```python
from heapq import heappop, heappush
from math import isqrt


def legacy_sqrt(
    vertex_count: int,
    source: int,
    queries: list[tuple[int, ...]],
) -> list[int]:
    block_size = isqrt(vertex_count) + 1
    block_count = (vertex_count + block_size - 1) // block_size
    outgoing_start = vertex_count
    incoming_start = vertex_count + block_count
    graph: list[list[tuple[int, int]]] = [
        [] for _ in range(vertex_count + 2 * block_count)
    ]

    for block in range(block_count):
        left = block * block_size
        right = min(vertex_count, left + block_size)
        for vertex in range(left, right):
            graph[outgoing_start + block].append((vertex, 0))
            graph[vertex].append((incoming_start + block, 0))

    def add_range_edge(
        vertex: int,
        left: int,
        right: int,
        weight: int,
        to_range: bool,
    ) -> None:
        for block in range(block_count):
            block_left = block * block_size
            block_right = min(vertex_count, block_left + block_size)
            overlap_left = max(left, block_left)
            overlap_right = min(right, block_right)
            if overlap_left >= overlap_right:
                continue
            if overlap_left == block_left and overlap_right == block_right:
                if to_range:
                    graph[vertex].append((outgoing_start + block, weight))
                else:
                    graph[incoming_start + block].append((vertex, weight))
            else:
                for endpoint in range(overlap_left, overlap_right):
                    if to_range:
                        graph[vertex].append((endpoint, weight))
                    else:
                        graph[endpoint].append((vertex, weight))

    for query in queries:
        if query[0] == 1:
            _, vertex, target, weight = query
            graph[vertex - 1].append((target - 1, weight))
        else:
            query_type, vertex, left, right, weight = query
            add_range_edge(
                vertex - 1,
                left - 1,
                right,
                weight,
                query_type == 2,
            )

    infinity = 10**30
    distance = [infinity] * len(graph)
    distance[source - 1] = 0
    queue = [(0, source - 1)]
    while queue:
        current_distance, vertex = heappop(queue)
        if current_distance != distance[vertex]:
            continue
        for neighbor, weight in graph[vertex]:
            candidate = current_distance + weight
            if candidate < distance[neighbor]:
                distance[neighbor] = candidate
                heappush(queue, (candidate, neighbor))
    return [-1 if value == infinity else value for value in distance[:vertex_count]]
```

Full blocks become one edge and boundary fragments are expanded, giving
`O(sqrt(n))` edges per range query.

## Expert solution: two segment-tree graphs

```python
import sys
from heapq import heappop, heappush


def solve() -> None:
    input_stream = sys.stdin.buffer
    vertex_count, query_count, source = map(int, input_stream.readline().split())
    graph: list[list[tuple[int, int]]] = [[] for _ in range(vertex_count)]
    outgoing = [0] * (4 * vertex_count)
    incoming = [0] * (4 * vertex_count)

    def new_node() -> int:
        graph.append([])
        return len(graph) - 1

    def build(tree_index: int, left: int, right: int) -> None:
        if right - left == 1:
            outgoing[tree_index] = left
            incoming[tree_index] = left
            return
        middle = (left + right) // 2
        build(tree_index * 2, left, middle)
        build(tree_index * 2 + 1, middle, right)
        outgoing[tree_index] = new_node()
        incoming[tree_index] = new_node()
        graph[outgoing[tree_index]].append((outgoing[tree_index * 2], 0))
        graph[outgoing[tree_index]].append((outgoing[tree_index * 2 + 1], 0))
        graph[incoming[tree_index * 2]].append((incoming[tree_index], 0))
        graph[incoming[tree_index * 2 + 1]].append((incoming[tree_index], 0))

    build(1, 0, vertex_count)

    def add_interval(
        tree_index: int,
        left: int,
        right: int,
        query_left: int,
        query_right: int,
        vertex: int,
        weight: int,
        to_range: bool,
    ) -> None:
        if query_left <= left and right <= query_right:
            if to_range:
                graph[vertex].append((outgoing[tree_index], weight))
            else:
                graph[incoming[tree_index]].append((vertex, weight))
            return
        middle = (left + right) // 2
        if query_left < middle:
            add_interval(
                tree_index * 2,
                left,
                middle,
                query_left,
                query_right,
                vertex,
                weight,
                to_range,
            )
        if middle < query_right:
            add_interval(
                tree_index * 2 + 1,
                middle,
                right,
                query_left,
                query_right,
                vertex,
                weight,
                to_range,
            )

    for _ in range(query_count):
        query = list(map(int, input_stream.readline().split()))
        if query[0] == 1:
            _, vertex, target, weight = query
            graph[vertex - 1].append((target - 1, weight))
        else:
            query_type, vertex, left, right, weight = query
            add_interval(
                1,
                0,
                vertex_count,
                left - 1,
                right,
                vertex - 1,
                weight,
                query_type == 2,
            )

    infinity = 10**30
    distance = [infinity] * len(graph)
    distance[source - 1] = 0
    queue = [(0, source - 1)]
    while queue:
        current_distance, vertex = heappop(queue)
        if current_distance != distance[vertex]:
            continue
        for neighbor, weight in graph[vertex]:
            candidate = current_distance + weight
            if candidate < distance[neighbor]:
                distance[neighbor] = candidate
                heappush(queue, (candidate, neighbor))

    print(
        " ".join(
            "-1" if value == infinity else str(value)
            for value in distance[:vertex_count]
        )
    )


if __name__ == "__main__":
    solve()
```

Each interval query adds edges only to its canonical cover. Zero edges make
those auxiliary nodes exactly equivalent to all requested point edges, so
Dijkstra returns the same distances as full expansion.

**Complexity:** `O((n + q) log n)` graph size and
`O((n + q) log^2 n)` time with a binary heap.
