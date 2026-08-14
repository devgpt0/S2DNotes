# ICPC300 074: CSES - Necessary Roads

**Source:** [CSES - Necessary Roads](https://cses.fi/problemset/task/2076/)  
**Pattern:** bridge detection with low-link values

## Exact contract

Input gives a connected undirected graph with `2 <= n <= 100000` vertices and
`1 <= m <= 200000` roads. Output the number of roads whose removal disconnects
the graph, followed by those roads in any order.

## First principles

For a DFS-tree edge `parent -> child`, `low[child]` is the earliest discovery
time reachable from the child's subtree using tree edges and at most one back
edge. The edge is a bridge exactly when `low[child] > tin[parent]`: then no
route from that subtree reaches the parent side without this edge.

## Cases that decide correctness

- Parallel roads prevent either copy from being a bridge; skip only the exact
  parent edge id.
- Back edges update `low` with the neighbor's discovery time.
- Bridge endpoints may be output in either direction.
- An iterative DFS avoids Python recursion failure on a chain of `100000`
  vertices.

## Brute force: remove every road and test connectivity

```python
def necessary_roads_brute(
    vertex_count: int,
    edges: list[tuple[int, int]],
) -> list[tuple[int, int]]:
    bridges = []
    for removed_edge, edge in enumerate(edges):
        graph = [[] for _ in range(vertex_count)]
        for edge_id, (left, right) in enumerate(edges):
            if edge_id != removed_edge:
                graph[left].append(right)
                graph[right].append(left)
        seen = {0}
        stack = [0]
        while stack:
            node = stack.pop()
            for neighbor in graph[node]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)
        if len(seen) != vertex_count:
            bridges.append(edge)
    return bridges
```

**Complexity:** `O(m(n+m))` time and `O(n+m)` space.

## Better: recursive Tarjan DFS

```python
def necessary_roads_recursive(
    vertex_count: int,
    edges: list[tuple[int, int]],
) -> list[tuple[int, int]]:
    graph: list[list[tuple[int, int]]] = [[] for _ in range(vertex_count)]
    for edge_id, (left, right) in enumerate(edges):
        graph[left].append((right, edge_id))
        graph[right].append((left, edge_id))
    discovery = [-1] * vertex_count
    low = [0] * vertex_count
    bridges = []
    timer = 0

    def dfs(node: int, parent_edge: int) -> None:
        nonlocal timer
        discovery[node] = timer
        low[node] = timer
        timer += 1
        for neighbor, edge_id in graph[node]:
            if edge_id == parent_edge:
                continue
            if discovery[neighbor] == -1:
                dfs(neighbor, edge_id)
                low[node] = min(low[node], low[neighbor])
                if low[neighbor] > discovery[node]:
                    bridges.append((node, neighbor))
            else:
                low[node] = min(low[node], discovery[neighbor])

    dfs(0, -1)
    return bridges
```

This is linear but unsafe for a worst-case deep DFS in Python.

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
    discovery[0] = 0
    low[0] = 0
    timer = 1
    stack = [0]
    bridges: list[tuple[int, int]] = []

    while stack:
        node = stack[-1]
        if next_edge[node] < len(graph[node]):
            neighbor, edge_id = graph[node][next_edge[node]]
            next_edge[node] += 1
            if edge_id == parent_edge[node]:
                continue
            if discovery[neighbor] == -1:
                parent[neighbor] = node
                parent_edge[neighbor] = edge_id
                discovery[neighbor] = timer
                low[neighbor] = timer
                timer += 1
                stack.append(neighbor)
            else:
                low[node] = min(low[node], discovery[neighbor])
            continue

        stack.pop()
        if parent[node] != -1:
            previous = parent[node]
            low[previous] = min(low[previous], low[node])
            if low[node] > discovery[previous]:
                bridges.append((previous, node))

    output = [str(len(bridges))]
    output.extend(f"{left + 1} {right + 1}" for left, right in bridges)
    print("\n".join(output))


if __name__ == "__main__":
    solve()
```

Every child is finalized before its low value is merged into its parent. The
strict comparison identifies exactly the tree edges with no alternate return
path.

**Complexity:** `O(n+m)` time and `O(n+m)` space.

