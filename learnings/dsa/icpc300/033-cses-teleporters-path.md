# ICPC300 033: CSES - Teleporters Path

**Source:** [CSES - Teleporters Path](https://cses.fi/problemset/task/1693/)  
**Pattern:** directed Euler trail with fixed endpoints

## Exact contract

Input gives a directed graph with `2 <= n <= 100000` rooms and
`1 <= m <= 200000` one-way teleporters. Find a route that starts in room `1`,
ends in room `n`, and uses every teleporter exactly once. Parallel edges are
distinct teleporters. Output the room sequence, or `IMPOSSIBLE` if no route
exists.

## First principles

Using every edge once is an Euler trail. Every intermediate room must be
entered as many times as it is left. The start needs one extra outgoing edge,
and the end one extra incoming edge.

Hierholzer's algorithm follows unused edges until stuck, then adds the stuck
vertex to the answer. Any unused detour encountered on the current stack is
spliced in automatically. The produced list is therefore reversed.

## Cases that decide correctness

- Require `out(1) = in(1) + 1` and `in(n) = out(n) + 1`.
- Every other room needs equal indegree and outdegree.
- Degree conditions alone do not guarantee relevant connectivity; requiring
  exactly `m + 1` output vertices proves every edge was reached.
- Parallel edges must be popped separately.
- The final route must still be checked to start at `1` and end at `n`.

## Brute force: backtrack over unused edge identities

```python
def teleporters_path_brute(
    vertex_count: int,
    edges: list[tuple[int, int]],
) -> list[int] | None:
    graph: list[list[tuple[int, int]]] = [[] for _ in range(vertex_count)]
    for edge_id, (start, end) in enumerate(edges):
        graph[start].append((end, edge_id))
    used = [False] * len(edges)
    route = [0]

    def search(node: int, used_count: int) -> bool:
        if used_count == len(edges):
            return node == vertex_count - 1
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

**Complexity:** `O(m!)` time in the worst case and `O(n + m)` space.

## Better for tiny edge counts: subset-state search

```python
from collections import deque


def teleporters_path_subset_dp(
    vertex_count: int,
    edges: list[tuple[int, int]],
) -> list[int] | None:
    graph: list[list[tuple[int, int]]] = [[] for _ in range(vertex_count)]
    for edge_id, (start, end) in enumerate(edges):
        graph[start].append((end, edge_id))

    start_state: tuple[int, int] = (0, 0)
    parent: dict[tuple[int, int], tuple[tuple[int, int], int]] = {}
    queue: deque[tuple[int, int]] = deque([start_state])
    seen: set[tuple[int, int]] = {start_state}
    full_mask = (1 << len(edges)) - 1
    final_state: tuple[int, int] | None = None

    while queue:
        mask, node = queue.popleft()
        if mask == full_mask and node == vertex_count - 1:
            final_state = (mask, node)
            break
        for neighbor, edge_id in graph[node]:
            edge_bit = 1 << edge_id
            if mask & edge_bit:
                continue
            next_state = (mask | edge_bit, neighbor)
            if next_state not in seen:
                seen.add(next_state)
                parent[next_state] = ((mask, node), neighbor)
                queue.append(next_state)

    if final_state is None:
        return None
    route = [vertex_count - 1]
    state = final_state
    while state != start_state:
        state, _ = parent[state]
        route.append(state[1])
    route.reverse()
    return route
```

Memoizing `(used_edges, room)` removes repeated suffix searches, but still
uses `O(n 2^m)` states.

## Expert solution: iterative Hierholzer traversal

```python
import sys


def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    vertex_count, edge_count = data[0:2]
    graph: list[list[int]] = [[] for _ in range(vertex_count)]
    indegree = [0] * vertex_count
    outdegree = [0] * vertex_count
    offset = 2

    for _ in range(edge_count):
        start, end = data[offset] - 1, data[offset + 1] - 1
        offset += 2
        graph[start].append(end)
        outdegree[start] += 1
        indegree[end] += 1

    valid_degrees = outdegree[0] == indegree[0] + 1
    valid_degrees &= indegree[-1] == outdegree[-1] + 1
    valid_degrees &= all(
        indegree[vertex] == outdegree[vertex] for vertex in range(1, vertex_count - 1)
    )
    if not valid_degrees:
        print("IMPOSSIBLE")
        return

    stack = [0]
    reversed_route: list[int] = []
    while stack:
        node = stack[-1]
        if graph[node]:
            stack.append(graph[node].pop())
        else:
            reversed_route.append(stack.pop())

    route = reversed_route[::-1]
    if len(route) != edge_count + 1 or route[0] != 0 or route[-1] != vertex_count - 1:
        print("IMPOSSIBLE")
        return
    print(" ".join(str(vertex + 1) for vertex in route))


if __name__ == "__main__":
    solve()
```

Each edge is removed once. A vertex enters the answer only after all its
reachable unused outgoing edges have been spliced into the trail. Degree and
length checks make that trail use every teleporter with the required endpoints.

**Complexity:** `O(n + m)` time and `O(n + m)` space.
