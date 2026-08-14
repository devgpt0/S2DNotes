# ICPC300 213: Codeforces 652E - Pursuit For Artifacts

**Source:** [Codeforces 652E](https://codeforces.com/problemset/problem/652/E)  
**Pattern:** bridge-tree path with component metadata

## Exact contract

An undirected graph has a binary flag on every edge. Given vertices `a` and
`b`, determine whether an edge-simple route from `a` to `b` can use at least
one flagged edge. Print `YES` or `NO`.

## First principles

Delete every bridge. Each remaining 2-edge-connected component can route
between its boundary vertices while including any internal edge, so record
whether it contains a flagged non-bridge edge.

Contracting components turns bridges into a forest. The component path from
`a` to `b` is unique. A valid route exists exactly when that path contains a
flagged bridge or visits a component containing a flagged internal edge.

## Cases that decide correctness

- Parallel edges require edge IDs when detecting bridges.
- A flagged bridge matters only if it lies on the `a`-to-`b` component path.
- A flagged edge inside a visited component can be included by an internal
  detour.
- If `a` and `b` share a component, only its internal flag matters.
- Unvisited branches of the bridge tree cannot help.

## Brute force: enumerate edge-simple routes

```python
def pursuit_brute(
    vertex_count: int,
    edges: list[tuple[int, int, int]],
    source: int,
    target: int,
) -> bool:
    graph: list[list[tuple[int, int, int]]] = [[] for _ in range(vertex_count)]
    for edge_index, (first, second, flagged) in enumerate(edges):
        graph[first].append((second, flagged, edge_index))
        graph[second].append((first, flagged, edge_index))

    def search(vertex: int, used_edges: int, used_artifact: int) -> bool:
        if vertex == target and used_artifact:
            return True
        for neighbor, flagged, edge_index in graph[vertex]:
            if used_edges >> edge_index & 1:
                continue
            if search(
                neighbor,
                used_edges | (1 << edge_index),
                used_artifact | flagged,
            ):
                return True
        return False

    return search(source, 0, 0)
```

This is exponential in the number of edges and is only a small-case oracle.

## Better insight: bridges are the only irreversible choices

Inside a component, non-bridge edges lie on cycles and can be incorporated
without changing which bridge is used next. Contract those flexible regions.

## Expert solution: Tarjan bridges and component contraction

```python
import sys
from collections import deque


def solve() -> None:
    sys.setrecursionlimit(1_000_000)
    input_stream = sys.stdin.buffer
    vertex_count, edge_count = map(int, input_stream.readline().split())
    edges = []
    graph: list[list[tuple[int, int]]] = [[] for _ in range(vertex_count)]
    for edge_index in range(edge_count):
        first, second, flagged = map(int, input_stream.readline().split())
        first -= 1
        second -= 1
        edges.append((first, second, flagged))
        graph[first].append((second, edge_index))
        graph[second].append((first, edge_index))
    source, target = map(lambda value: int(value) - 1, input_stream.readline().split())

    entry = [-1] * vertex_count
    low = [0] * vertex_count
    is_bridge = [False] * edge_count
    timer = 0

    def find_bridges(vertex: int, parent_edge: int) -> None:
        nonlocal timer
        entry[vertex] = timer
        low[vertex] = timer
        timer += 1
        for neighbor, edge_index in graph[vertex]:
            if edge_index == parent_edge:
                continue
            if entry[neighbor] != -1:
                low[vertex] = min(low[vertex], entry[neighbor])
                continue
            find_bridges(neighbor, edge_index)
            low[vertex] = min(low[vertex], low[neighbor])
            if low[neighbor] > entry[vertex]:
                is_bridge[edge_index] = True

    for vertex in range(vertex_count):
        if entry[vertex] == -1:
            find_bridges(vertex, -1)

    component = [-1] * vertex_count
    component_count = 0
    for start in range(vertex_count):
        if component[start] != -1:
            continue
        component[start] = component_count
        stack = [start]
        while stack:
            vertex = stack.pop()
            for neighbor, edge_index in graph[vertex]:
                if not is_bridge[edge_index] and component[neighbor] == -1:
                    component[neighbor] = component_count
                    stack.append(neighbor)
        component_count += 1

    has_artifact = [False] * component_count
    tree: list[list[tuple[int, int]]] = [[] for _ in range(component_count)]
    for edge_index, (first, second, flagged) in enumerate(edges):
        first_component = component[first]
        second_component = component[second]
        if first_component == second_component:
            has_artifact[first_component] |= bool(flagged)
        elif is_bridge[edge_index]:
            tree[first_component].append((second_component, flagged))
            tree[second_component].append((first_component, flagged))

    start_component = component[source]
    target_component = component[target]
    queue = deque([(start_component, has_artifact[start_component])])
    visited = [False] * component_count
    visited[start_component] = True
    while queue:
        current, used = queue.popleft()
        if current == target_component:
            print("YES" if used else "NO")
            return
        for neighbor, flagged in tree[current]:
            if not visited[neighbor]:
                visited[neighbor] = True
                queue.append(
                    (neighbor, used or bool(flagged) or has_artifact[neighbor])
                )
    print("NO")


if __name__ == "__main__":
    solve()
```

Every flagged opportunity that can lie on a valid route appears either inside
a visited component or on its unique bridge-tree path.

**Complexity:** `O(n+m)` time and space.
