# ICPC300 215: Codeforces 1051F - The Shortest Statement

**Source:** [Codeforces 1051F](https://codeforces.com/problemset/problem/1051/F)  
**Pattern:** spanning-tree LCA plus special-vertex Dijkstra

## Exact contract

A connected undirected weighted graph has only a small number of edges beyond
a spanning tree. For each query `(u,v)`, output their shortest-path distance.

## First principles

A spanning tree gives one candidate distance through LCA. If a shortest path
uses any non-tree edge, it passes through an endpoint of a non-tree edge. Run
Dijkstra from every such special endpoint. Then

`min(tree_distance(u,v), dist_s[u] + dist_s[v] for every special s)`

is exact: every expression is a valid walk, and choosing a special vertex on
an optimal non-tree path reproduces that path's length.

## Cases that decide correctness

- Parallel edges can make one endpoint special even when another parallel edge
  entered the tree.
- The spanning-tree candidate is still needed.
- All edge weights are positive.
- Deduplicate special endpoints before Dijkstra.
- Store wide distances.

## Brute force: all-pairs Floyd-Warshall

```python
def shortest_statement_brute(
    vertex_count: int,
    edges: list[tuple[int, int, int]],
    queries: list[tuple[int, int]],
) -> list[int]:
    infinity = 10**30
    distance = [[infinity] * vertex_count for _ in range(vertex_count)]
    for vertex in range(vertex_count):
        distance[vertex][vertex] = 0
    for first, second, weight in edges:
        distance[first][second] = min(distance[first][second], weight)
        distance[second][first] = min(distance[second][first], weight)
    for middle in range(vertex_count):
        for first in range(vertex_count):
            for second in range(vertex_count):
                distance[first][second] = min(
                    distance[first][second],
                    distance[first][middle] + distance[middle][second],
                )
    return [distance[first][second] for first, second in queries]
```

This is cubic and only suitable for small verification cases.

## Better insight: only cycle endpoints can improve a tree route

Removing non-tree edges leaves a tree. Any route that differs from its unique
tree path must enter the extra-edge structure through a non-tree endpoint.

## Expert solution: sparse-cycle distance oracle

```python
import sys
from array import array
from heapq import heappop, heappush


class DisjointSet:
    def __init__(self, size: int) -> None:
        self.parent = list(range(size))
        self.size = [1] * size

    def find(self, vertex: int) -> int:
        while vertex != self.parent[vertex]:
            self.parent[vertex] = self.parent[self.parent[vertex]]
            vertex = self.parent[vertex]
        return vertex

    def union(self, first: int, second: int) -> bool:
        first = self.find(first)
        second = self.find(second)
        if first == second:
            return False
        if self.size[first] < self.size[second]:
            first, second = second, first
        self.parent[second] = first
        self.size[first] += self.size[second]
        return True


def solve() -> None:
    input_stream = sys.stdin.buffer
    vertex_count, edge_count = map(int, input_stream.readline().split())
    graph: list[list[tuple[int, int]]] = [[] for _ in range(vertex_count)]
    tree: list[list[tuple[int, int]]] = [[] for _ in range(vertex_count)]
    special: set[int] = set()
    dsu = DisjointSet(vertex_count)
    for _ in range(edge_count):
        first, second, weight = map(int, input_stream.readline().split())
        first -= 1
        second -= 1
        graph[first].append((second, weight))
        graph[second].append((first, weight))
        if dsu.union(first, second):
            tree[first].append((second, weight))
            tree[second].append((first, weight))
        else:
            special.add(first)
            special.add(second)

    depth = [0] * vertex_count
    root_distance = [0] * vertex_count
    parent = [-1] * vertex_count
    parent[0] = 0
    order = [0]
    for vertex in order:
        for neighbor, weight in tree[vertex]:
            if parent[neighbor] == -1:
                parent[neighbor] = vertex
                depth[neighbor] = depth[vertex] + 1
                root_distance[neighbor] = root_distance[vertex] + weight
                order.append(neighbor)

    ancestors = [array("i", parent)]
    while 1 << len(ancestors) <= vertex_count:
        previous = ancestors[-1]
        ancestors.append(
            array("i", (previous[previous[v]] for v in range(vertex_count)))
        )

    def lowest_common_ancestor(first: int, second: int) -> int:
        if depth[first] < depth[second]:
            first, second = second, first
        difference = depth[first] - depth[second]
        for level in range(len(ancestors)):
            if difference >> level & 1:
                first = ancestors[level][first]
        if first == second:
            return first
        for level in range(len(ancestors) - 1, -1, -1):
            if ancestors[level][first] != ancestors[level][second]:
                first = ancestors[level][first]
                second = ancestors[level][second]
        return parent[first]

    infinity = 10**18
    special_distances: list[array] = []
    for start in special:
        distance = array("q", [infinity]) * vertex_count
        distance[start] = 0
        queue = [(0, start)]
        while queue:
            current_distance, vertex = heappop(queue)
            if current_distance != distance[vertex]:
                continue
            for neighbor, weight in graph[vertex]:
                candidate = current_distance + weight
                if candidate < distance[neighbor]:
                    distance[neighbor] = candidate
                    heappush(queue, (candidate, neighbor))
        special_distances.append(distance)

    query_count = int(input_stream.readline())
    output = []
    for _ in range(query_count):
        first, second = map(int, input_stream.readline().split())
        first -= 1
        second -= 1
        ancestor = lowest_common_ancestor(first, second)
        answer = (
            root_distance[first] + root_distance[second] - 2 * root_distance[ancestor]
        )
        for distance in special_distances:
            answer = min(answer, distance[first] + distance[second])
        output.append(str(answer))
    print("\n".join(output))


if __name__ == "__main__":
    solve()
```

The tree handles paths using no extra edge; every other shortest path is
captured through at least one precomputed special endpoint.

**Complexity:** `O((n+m)s log n + (n+q) log n + qs)` time and `O(ns+n log n+m)`
space, where `s` is the number of special vertices.
