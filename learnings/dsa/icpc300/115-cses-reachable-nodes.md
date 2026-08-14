# ICPC300 115: CSES - Reachable Nodes

**Source:** [CSES - Reachable Nodes](https://cses.fi/problemset/task/2138/)  
**Pattern:** DAG transitive closure with bitsets  
**Goal:** For every vertex in a directed acyclic graph, count the vertices
reachable from it, including itself.

## 1. First principles

In reverse topological order, every successor's reachable set is already final:

```text
reachable[u] = {u} union reachable[v] for every edge u -> v
```

Represent a set as a bit vector. Union becomes bitwise OR, and population count
gives the answer.

## 2. Cases that decide correctness

- Every vertex reaches itself.
- Duplicate edges do not duplicate reachable vertices.
- A sink's answer is `1`.
- Shared descendants must be counted once.
- Any directed cycle violates the source contract.

## 3. Brute force: DFS from every vertex

```python
def reachable_nodes_brute(vertex_count: int, edges: list[tuple[int, int]]) -> list[int]:
    if vertex_count <= 0:
        raise ValueError("vertex_count must be positive")

    graph = [[] for _ in range(vertex_count)]
    for first, second in edges:
        graph[first].append(second)

    answers: list[int] = []
    for start in range(vertex_count):
        seen = {start}
        stack = [start]
        while stack:
            node = stack.pop()
            for neighbor in graph[node]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)
        answers.append(len(seen))
    return answers
```

**Complexity:** `O(V(V+E))` time and `O(V+E)` space.

## 4. Better: reverse-topological Python sets

```python
from collections import deque


def reachable_nodes_sets(vertex_count: int, edges: list[tuple[int, int]]) -> list[int]:
    if vertex_count <= 0:
        raise ValueError("vertex_count must be positive")

    graph = [[] for _ in range(vertex_count)]
    indegree = [0] * vertex_count
    for first, second in edges:
        graph[first].append(second)
        indegree[second] += 1

    queue = deque(vertex for vertex in range(vertex_count) if indegree[vertex] == 0)
    order: list[int] = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)
    if len(order) != vertex_count:
        raise ValueError("graph must be acyclic")

    reachable = [{vertex} for vertex in range(vertex_count)]
    for node in reversed(order):
        for neighbor in graph[node]:
            reachable[node].update(reachable[neighbor])
    return [len(vertices) for vertices in reachable]
```

**Complexity:** up to `O(V(V+E))` set work and `O(V^2)` stored entries.

## 5. Expert solution: integer bitsets

Python integers store dense bits in machine words, making each set union one
optimized big-integer OR.

```python
from collections import deque


def reachable_nodes_bitsets(
    vertex_count: int, edges: list[tuple[int, int]]
) -> list[int]:
    if vertex_count <= 0:
        raise ValueError("vertex_count must be positive")

    graph = [[] for _ in range(vertex_count)]
    indegree = [0] * vertex_count
    for first, second in edges:
        graph[first].append(second)
        indegree[second] += 1

    queue = deque(vertex for vertex in range(vertex_count) if indegree[vertex] == 0)
    order: list[int] = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)
    if len(order) != vertex_count:
        raise ValueError("graph must be acyclic")

    reachable = [1 << vertex for vertex in range(vertex_count)]
    for node in reversed(order):
        for neighbor in graph[node]:
            reachable[node] |= reachable[neighbor]
    return [vertices.bit_count() for vertices in reachable]
```

### Why the expert code is correct

Reverse topological order finalizes every successor first. OR combines exactly
the successor closures plus the vertex's own bit; idempotence removes all
duplicate paths automatically.

**Complexity:** `O((V+E) * V / word_size)` bit work and `O(V^2 / word_size)`
space.

## 6. What to remember

```text
DAG closure -> reverse topological unions
dense vertex sets -> bit vectors
union/count -> bitwise OR / population count
```
