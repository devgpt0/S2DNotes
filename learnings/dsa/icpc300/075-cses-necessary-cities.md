# ICPC300 075: CSES - Necessary Cities

**Source:** [CSES - Necessary Cities](https://cses.fi/problemset/task/2077/)  
**Pattern:** articulation points with low-link values

## Exact contract

Input gives a connected undirected graph with `2 <= n <= 100000` cities and
`1 <= m <= 200000` roads. Output the number of cities whose removal disconnects
the remaining graph, then their one-based indices in any order.

## First principles

For a non-root DFS vertex `u`, removing `u` disconnects a child subtree `v`
exactly when that subtree has no back edge above `u`, expressed by
`low[v] >= tin[u]`. The DFS root has no ancestor; it is an articulation point
exactly when it has at least two DFS-tree children.

## Cases that decide correctness

- The root uses the child-count rule, not the ordinary low-link rule.
- The articulation comparison is `>=`; the bridge comparison was strictly `>`.
- Multiple qualifying children still add their parent only once.
- Parallel edges require tracking the exact parent edge id.
- Iterative DFS avoids call-stack failure on a long chain.

## Brute force: remove every city

```python
def necessary_cities_brute(
    vertex_count: int,
    edges: list[tuple[int, int]],
) -> list[int]:
    necessary = []
    for removed in range(vertex_count):
        start = next(
            (vertex for vertex in range(vertex_count) if vertex != removed), -1
        )
        if start == -1:
            continue
        graph = [[] for _ in range(vertex_count)]
        for left, right in edges:
            if left != removed and right != removed:
                graph[left].append(right)
                graph[right].append(left)
        seen = {start}
        stack = [start]
        while stack:
            node = stack.pop()
            for neighbor in graph[node]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)
        if len(seen) != vertex_count - 1:
            necessary.append(removed)
    return necessary
```

**Complexity:** `O(n(n+m))` time and `O(n+m)` space.

## Better: recursive Tarjan DFS

```python
def necessary_cities_recursive(
    vertex_count: int,
    edges: list[tuple[int, int]],
) -> list[int]:
    graph: list[list[tuple[int, int]]] = [[] for _ in range(vertex_count)]
    for edge_id, (left, right) in enumerate(edges):
        graph[left].append((right, edge_id))
        graph[right].append((left, edge_id))
    discovery = [-1] * vertex_count
    low = [0] * vertex_count
    articulation = [False] * vertex_count
    timer = 0

    def dfs(node: int, parent_edge: int) -> None:
        nonlocal timer
        discovery[node] = timer
        low[node] = timer
        timer += 1
        children = 0
        for neighbor, edge_id in graph[node]:
            if edge_id == parent_edge:
                continue
            if discovery[neighbor] == -1:
                children += 1
                dfs(neighbor, edge_id)
                low[node] = min(low[node], low[neighbor])
                if parent_edge != -1 and low[neighbor] >= discovery[node]:
                    articulation[node] = True
            else:
                low[node] = min(low[node], discovery[neighbor])
        if parent_edge == -1 and children > 1:
            articulation[node] = True

    dfs(0, -1)
    return [vertex for vertex, needed in enumerate(articulation) if needed]
```

This is linear, but recursive depth can reach `n`.

## Expert solution: iterative articulation DFS

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
    children = [0] * vertex_count
    next_edge = [0] * vertex_count
    articulation = [False] * vertex_count
    discovery[0] = 0
    low[0] = 0
    timer = 1
    stack = [0]

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
                children[node] += 1
                discovery[neighbor] = timer
                low[neighbor] = timer
                timer += 1
                stack.append(neighbor)
            else:
                low[node] = min(low[node], discovery[neighbor])
            continue

        stack.pop()
        previous = parent[node]
        if previous != -1:
            low[previous] = min(low[previous], low[node])
            if parent[previous] != -1 and low[node] >= discovery[previous]:
                articulation[previous] = True

    articulation[0] = children[0] > 1
    answer = [vertex + 1 for vertex, needed in enumerate(articulation) if needed]
    print(len(answer))
    print(*answer)


if __name__ == "__main__":
    solve()
```

On child finalization, its complete low value is available. The non-root and
root rules exactly characterize whether deleting the parent separates DFS
subtrees.

**Complexity:** `O(n+m)` time and `O(n+m)` space.

