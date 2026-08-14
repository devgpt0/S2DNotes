# ICPC300 073: CSES - Graph Girth

**Source:** [CSES - Graph Girth](https://cses.fi/problemset/task/1707/)  
**Pattern:** shortest cycle by repeated BFS

## Exact contract

Input gives an undirected graph with `2 <= n <= 2500` vertices and
`1 <= m <= 5000` edges. Output the length in edges of its shortest cycle, or
`-1` if the graph is acyclic.

## First principles

Fix a BFS root. When an edge joins two already discovered vertices and is not
the tree edge back to a parent, the two BFS-tree paths plus that edge form a
cycle of length `dist[u] + dist[v] + 1`. Running BFS from every possible root
ensures the shortest cycle is seen from one of its vertices without a longer
shared prefix.

## Cases that decide correctness

- A forest has no non-tree edge and returns `-1`.
- The parent edge in an undirected BFS is not a two-edge cycle.
- Disconnected components are covered because every vertex becomes a root.
- Once the current BFS depth cannot improve the best known cycle, deeper
  expansion may be skipped.

## Brute force: enumerate simple cycles by DFS

```python
def graph_girth_brute(vertex_count: int, edges: list[tuple[int, int]]) -> int:
    graph = [[] for _ in range(vertex_count)]
    for left, right in edges:
        graph[left].append(right)
        graph[right].append(left)
    best = vertex_count + 1

    for start in range(vertex_count):
        visited = {start}

        def search(node: int, parent: int, length: int) -> None:
            nonlocal best
            for neighbor in graph[node]:
                if neighbor == parent:
                    continue
                if neighbor == start and length >= 2:
                    best = min(best, length + 1)
                elif neighbor not in visited and length + 1 < best:
                    visited.add(neighbor)
                    search(neighbor, node, length + 1)
                    visited.remove(neighbor)

        search(start, -1, 0)
    return -1 if best == vertex_count + 1 else best
```

This explores exponentially many simple paths.

## Better: remove each edge and find its replacement path

```python
from collections import deque


def graph_girth_by_edge_removal(
    vertex_count: int,
    edges: list[tuple[int, int]],
) -> int:
    graph: list[list[tuple[int, int]]] = [[] for _ in range(vertex_count)]
    for edge_id, (left, right) in enumerate(edges):
        graph[left].append((right, edge_id))
        graph[right].append((left, edge_id))
    best = vertex_count + 1

    for removed_edge, (start, target) in enumerate(edges):
        distance = [-1] * vertex_count
        distance[start] = 0
        queue = deque([start])
        while queue and distance[target] == -1:
            node = queue.popleft()
            for neighbor, edge_id in graph[node]:
                if edge_id != removed_edge and distance[neighbor] == -1:
                    distance[neighbor] = distance[node] + 1
                    queue.append(neighbor)
        if distance[target] != -1:
            best = min(best, distance[target] + 1)
    return -1 if best == vertex_count + 1 else best
```

Every cycle is one removed edge plus a replacement path. This takes
`O(m(n+m))` time.

## Expert solution: BFS from every vertex

```python
from collections import deque
import sys


def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    vertex_count, edge_count = data[0:2]
    graph = [[] for _ in range(vertex_count)]
    offset = 2
    for _ in range(edge_count):
        left, right = data[offset] - 1, data[offset + 1] - 1
        offset += 2
        graph[left].append(right)
        graph[right].append(left)

    best = vertex_count + 1
    for start in range(vertex_count):
        distance = [-1] * vertex_count
        parent = [-1] * vertex_count
        distance[start] = 0
        queue = deque([start])

        while queue:
            node = queue.popleft()
            if 2 * distance[node] >= best:
                continue
            for neighbor in graph[node]:
                if distance[neighbor] == -1:
                    distance[neighbor] = distance[node] + 1
                    parent[neighbor] = node
                    queue.append(neighbor)
                elif parent[node] != neighbor:
                    best = min(best, distance[node] + distance[neighbor] + 1)

    print(-1 if best == vertex_count + 1 else best)


if __name__ == "__main__":
    solve()
```

For a shortest cycle and a root on it, BFS reaches its two sides by shortest
paths before their closing non-tree edge is examined. Any shared prefix would
produce an even shorter cycle, so the computed length is exact.

**Complexity:** `O(n(n+m))` time and `O(n+m)` space.
