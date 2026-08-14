# ICPC300 034: CSES - Mail Delivery

**Source:** [CSES - Mail Delivery](https://cses.fi/problemset/task/1691/)  
**Pattern:** undirected Euler circuit

## Exact contract

Input gives an undirected multigraph with `2 <= n <= 100000` intersections and
`1 <= m <= 200000` streets. Find a route that starts at intersection `1`,
uses every street exactly once, and returns to intersection `1`. Output its
vertex sequence, or `IMPOSSIBLE` if it does not exist.

## First principles

Every time an Euler circuit enters a vertex, it must leave on another unused
edge. Thus every vertex needs even degree. All vertices incident to edges must
also lie in the component reachable from vertex `1`.

Hierholzer's algorithm follows unused streets and records a vertex only when
no unused incident street remains. This splices all cycles into one circuit
without repeatedly testing bridges.

## Cases that decide correctness

- An undirected edge appears in both adjacency lists but may be consumed only
  once; track a shared edge id.
- Parallel streets are different edge ids and are both usable.
- Even degrees are insufficient if a separate component contains streets.
- Requiring `m + 1` vertices in the constructed route detects disconnected
  unused edges.
- The first and last output vertices must both be `1`.

## Brute force: backtrack over all unused streets

```python
def mail_route_brute(
    vertex_count: int,
    edges: list[tuple[int, int]],
) -> list[int] | None:
    graph: list[list[tuple[int, int]]] = [[] for _ in range(vertex_count)]
    for edge_id, (left, right) in enumerate(edges):
        graph[left].append((right, edge_id))
        graph[right].append((left, edge_id))
    used = [False] * len(edges)
    route = [0]

    def search(node: int, used_count: int) -> bool:
        if used_count == len(edges):
            return node == 0
        for neighbor, edge_id in graph[node]:
            if used[edge_id]:
                continue
            used[edge_id] = True
            route.append(neighbor)
            if search(neighbor, used_count + 1):
                return True
            route.pop()
            used[edge_id] = False
        return False

    return route if search(0, 0) else None
```

**Complexity:** `O(m!)` time and `O(n + m)` space.

## Better: Fleury's avoid-a-bridge rule

```python
def mail_route_fleury(
    vertex_count: int,
    edges: list[tuple[int, int]],
) -> list[int] | None:
    graph: list[list[tuple[int, int]]] = [[] for _ in range(vertex_count)]
    for edge_id, (left, right) in enumerate(edges):
        graph[left].append((right, edge_id))
        graph[right].append((left, edge_id))
    if any(len(neighbors) % 2 for neighbors in graph):
        return None

    available = [True] * len(edges)

    def remains_reachable(start: int, target: int, removed_edge: int) -> bool:
        stack = [start]
        seen = {start}
        while stack:
            node = stack.pop()
            for neighbor, edge_id in graph[node]:
                if edge_id == removed_edge or not available[edge_id]:
                    continue
                if neighbor == target:
                    return True
                if neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)
        return start == target

    route = [0]
    node = 0
    for _ in edges:
        choices = [item for item in graph[node] if available[item[1]]]
        if not choices:
            return None
        chosen = choices[-1]
        if len(choices) > 1:
            for candidate in choices:
                if remains_reachable(node, candidate[0], candidate[1]):
                    chosen = candidate
                    break
        node, edge_id = chosen
        available[edge_id] = False
        route.append(node)

    return route if node == 0 else None
```

Fleury's rule is constructive, but each bridge test scans the remaining graph,
giving `O(m(n+m))` worst-case time.

## Expert solution: edge-id Hierholzer traversal

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

    if any(len(neighbors) % 2 for neighbors in graph):
        print("IMPOSSIBLE")
        return

    used = [False] * edge_count
    next_edge = [0] * vertex_count
    stack = [0]
    reversed_route: list[int] = []

    while stack:
        node = stack[-1]
        while (
            next_edge[node] < len(graph[node]) and used[graph[node][next_edge[node]][1]]
        ):
            next_edge[node] += 1

        if next_edge[node] == len(graph[node]):
            reversed_route.append(stack.pop())
            continue

        neighbor, edge_id = graph[node][next_edge[node]]
        next_edge[node] += 1
        if not used[edge_id]:
            used[edge_id] = True
            stack.append(neighbor)

    route = reversed_route[::-1]
    if len(route) != edge_count + 1 or route[0] != 0 or route[-1] != 0:
        print("IMPOSSIBLE")
        return
    print(" ".join(str(vertex + 1) for vertex in route))


if __name__ == "__main__":
    solve()
```

Each street id is marked once even though it occurs in two adjacency lists.
The reverse postorder splices every reachable cycle; the route-length check
proves that no street was stranded elsewhere.

**Complexity:** `O(n + m)` time and `O(n + m)` space.

