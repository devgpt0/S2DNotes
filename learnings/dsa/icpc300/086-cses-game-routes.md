# ICPC300 086: CSES - Game Routes

**Source:** [CSES - Game Routes](https://cses.fi/problemset/task/1681/)  
**Pattern:** path counting on a directed acyclic graph  
**Goal:** Count directed routes from vertex `0` to vertex `n-1` modulo
`1_000_000_007`.

The source graph is acyclic. Parallel edges represent distinct route choices.

## 1. First principles

For a DAG, every route into `v` ends with one incoming edge `u -> v`:

```text
routes[v] += routes[u]
```

Process vertices in topological order so every predecessor count is final
before it is propagated.

## 2. Cases that decide correctness

- The source has one empty prefix route used to start propagation.
- An unreachable vertex contributes zero.
- Parallel edges add the predecessor count once per edge.
- A direct source-to-sink edge is one route.
- A cycle violates the finite-DAG contract and must fail.

## 3. Brute force: enumerate every route

```python
def game_routes_brute(
    vertex_count: int,
    edges: list[tuple[int, int]],
    modulo: int = 1_000_000_007,
) -> int:
    if vertex_count <= 0 or modulo <= 0:
        raise ValueError("vertex_count and modulo must be positive")

    graph: list[list[int]] = [[] for _ in range(vertex_count)]
    for first, second in edges:
        graph[first].append(second)
    visiting = [False] * vertex_count

    def count_from(node: int) -> int:
        if node == vertex_count - 1:
            return 1
        if visiting[node]:
            raise ValueError("graph must be acyclic")
        visiting[node] = True
        total = sum(count_from(neighbor) for neighbor in graph[node])
        visiting[node] = False
        return total % modulo

    return count_from(0)
```

**Complexity:** proportional to the number and lengths of all routes, which can
be exponential.

## 4. Better: memoized DAG recursion

Each vertex's suffix-route count is independent of how it was reached, so cache
it once.

```python
def game_routes_memoized(
    vertex_count: int,
    edges: list[tuple[int, int]],
    modulo: int = 1_000_000_007,
) -> int:
    if vertex_count <= 0 or modulo <= 0:
        raise ValueError("vertex_count and modulo must be positive")

    graph: list[list[int]] = [[] for _ in range(vertex_count)]
    for first, second in edges:
        graph[first].append(second)
    state = [0] * vertex_count
    cached = [0] * vertex_count

    def count_from(node: int) -> int:
        if node == vertex_count - 1:
            return 1
        if state[node] == 1:
            raise ValueError("graph must be acyclic")
        if state[node] == 2:
            return cached[node]
        state[node] = 1
        cached[node] = sum(count_from(neighbor) for neighbor in graph[node]) % modulo
        state[node] = 2
        return cached[node]

    return count_from(0)
```

**Complexity:** `O(V + E)` time and `O(V + E)` space, but recursion can reach
the full DAG depth.

## 5. Expert solution: iterative topological DP

Kahn's algorithm validates acyclicity and gives a safe processing order without
deep recursion.

```python
from collections import deque


def game_routes_topological(
    vertex_count: int,
    edges: list[tuple[int, int]],
    modulo: int = 1_000_000_007,
) -> int:
    if vertex_count <= 0 or modulo <= 0:
        raise ValueError("vertex_count and modulo must be positive")

    graph: list[list[int]] = [[] for _ in range(vertex_count)]
    indegree = [0] * vertex_count
    for first, second in edges:
        graph[first].append(second)
        indegree[second] += 1

    queue = deque(vertex for vertex in range(vertex_count) if indegree[vertex] == 0)
    topological_order: list[int] = []
    while queue:
        node = queue.popleft()
        topological_order.append(node)
        for neighbor in graph[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)
    if len(topological_order) != vertex_count:
        raise ValueError("graph must be acyclic")

    routes = [0] * vertex_count
    routes[0] = 1
    for node in topological_order:
        for neighbor in graph[node]:
            routes[neighbor] = (routes[neighbor] + routes[node]) % modulo
    return routes[-1]
```

### Why the expert code is correct

Topological order places every edge from an earlier vertex to a later one.
Thus, when a vertex propagates its count, every route ending there has already
been counted exactly once by its final edge.

**Complexity:** `O(V + E)` time and `O(V + E)` space.

## 6. What to remember

```text
DAG path count = sum of predecessor path counts
topological order finalizes predecessors first
parallel edges are distinct contributions
```
