# ICPC300 036: CSES - Strongly Connected Edges

**Source:** [CSES - Strongly Connected Edges](https://cses.fi/problemset/task/2177/)  
**Pattern:** bridge detection with DFS edge orientation

## Exact contract

Input gives an undirected graph with `2 <= n <= 100000` vertices and
`1 <= m <= 200000` edges. Orient every input edge so the resulting directed
graph is strongly connected. Output each directed edge in original input
order, or `IMPOSSIBLE` when no such orientation exists.

## First principles

If an undirected edge is a bridge, every route between its two sides must use
that edge. Whichever direction it receives, travel in the other direction is
impossible. A disconnected graph is also impossible.

Robbins' theorem gives the converse: every connected bridgeless undirected
graph has a strongly connected orientation. During DFS, orient tree edges away
from the root and unused back edges toward ancestors. Low-link values detect a
bridge exactly when `low[child] > tin[parent]`.

## Cases that decide correctness

- Connectivity and absence of bridges are both required.
- Track the parent edge id, not merely the parent vertex; a second parallel
  edge is a back edge and prevents the first from being a bridge.
- Every edge is printed once in input order.
- A previously oriented tree edge must not be reversed when its second
  adjacency entry is encountered.
- Recursive DFS can exceed Python's call stack on a chain of `100000` vertices;
  the expert implementation is iterative.

## Brute force: try all edge orientations

```python
def strongly_connected_orientation_brute(
    vertex_count: int,
    edges: list[tuple[int, int]],
) -> list[tuple[int, int]] | None:
    def reaches_all(graph: list[list[int]], start: int) -> bool:
        seen = [False] * vertex_count
        seen[start] = True
        stack = [start]
        while stack:
            node = stack.pop()
            for neighbor in graph[node]:
                if not seen[neighbor]:
                    seen[neighbor] = True
                    stack.append(neighbor)
        return all(seen)

    for mask in range(1 << len(edges)):
        oriented = []
        graph = [[] for _ in range(vertex_count)]
        reverse_graph = [[] for _ in range(vertex_count)]
        for edge_id, (left, right) in enumerate(edges):
            start, end = (right, left) if mask & (1 << edge_id) else (left, right)
            oriented.append((start, end))
            graph[start].append(end)
            reverse_graph[end].append(start)
        if reaches_all(graph, 0) and reaches_all(reverse_graph, 0):
            return oriented
    return None
```

**Complexity:** `O(2^m (n+m))` time and `O(n+m)` space.

## Better: recursive low-link orientation

```python
def orient_edges_recursive(
    vertex_count: int,
    edges: list[tuple[int, int]],
) -> list[tuple[int, int]] | None:
    graph: list[list[tuple[int, int]]] = [[] for _ in range(vertex_count)]
    for edge_id, (left, right) in enumerate(edges):
        graph[left].append((right, edge_id))
        graph[right].append((left, edge_id))

    discovery = [-1] * vertex_count
    low = [0] * vertex_count
    orientation: list[tuple[int, int] | None] = [None] * len(edges)
    timer = 0
    has_bridge = False

    def dfs(node: int, parent_edge: int) -> None:
        nonlocal timer, has_bridge
        discovery[node] = timer
        low[node] = timer
        timer += 1

        for neighbor, edge_id in graph[node]:
            if edge_id == parent_edge:
                continue
            if discovery[neighbor] == -1:
                orientation[edge_id] = (node, neighbor)
                dfs(neighbor, edge_id)
                low[node] = min(low[node], low[neighbor])
                if low[neighbor] > discovery[node]:
                    has_bridge = True
            else:
                low[node] = min(low[node], discovery[neighbor])
                if orientation[edge_id] is None:
                    orientation[edge_id] = (node, neighbor)

    dfs(0, -1)
    if has_bridge or any(time == -1 for time in discovery):
        return None
    return [edge for edge in orientation if edge is not None]
```

This is linear and implements Robbins' construction directly, but a deep DFS
can raise `RecursionError` at the source limit.

## Expert solution: iterative low-link DFS

```python
import sys


def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    vertex_count, edge_count = data[0:2]
    graph: list[list[tuple[int, int]]] = [[] for _ in range(vertex_count)]
    offset = 2
    for edge_id in range(edge_count):
        left, right = data[offset] - 1, data[offset + 1] - 1
        offset += 2
        graph[left].append((right, edge_id))
        graph[right].append((left, edge_id))

    discovery = [-1] * vertex_count
    low = [0] * vertex_count
    parent = [-1] * vertex_count
    parent_edge = [-1] * vertex_count
    next_edge = [0] * vertex_count
    orientation: list[tuple[int, int] | None] = [None] * edge_count
    discovery[0] = 0
    low[0] = 0
    timer = 1
    has_bridge = False
    stack = [0]

    while stack:
        node = stack[-1]
        if next_edge[node] < len(graph[node]):
            neighbor, edge_id = graph[node][next_edge[node]]
            next_edge[node] += 1
            if edge_id == parent_edge[node]:
                continue

            if discovery[neighbor] == -1:
                orientation[edge_id] = (node, neighbor)
                parent[neighbor] = node
                parent_edge[neighbor] = edge_id
                discovery[neighbor] = timer
                low[neighbor] = timer
                timer += 1
                stack.append(neighbor)
            else:
                low[node] = min(low[node], discovery[neighbor])
                if orientation[edge_id] is None:
                    orientation[edge_id] = (node, neighbor)
            continue

        stack.pop()
        if parent[node] != -1:
            previous = parent[node]
            low[previous] = min(low[previous], low[node])
            if low[node] > discovery[previous]:
                has_bridge = True

    if has_bridge or any(time == -1 for time in discovery):
        print("IMPOSSIBLE")
        return

    output = []
    for edge in orientation:
        if edge is None:
            print("IMPOSSIBLE")
            return
        output.append(f"{edge[0] + 1} {edge[1] + 1}")
    print("\n".join(output))


if __name__ == "__main__":
    solve()
```

Tree edges point down the DFS tree and back edges point toward ancestors. A
low-link bridge test rejects exactly the graphs where one cut cannot be crossed
both ways. Robbins' theorem then proves the produced orientation is strongly
connected.

**Complexity:** `O(n + m)` time and `O(n + m)` space.
