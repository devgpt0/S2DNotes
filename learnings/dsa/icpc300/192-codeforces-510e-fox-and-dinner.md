# ICPC300 192: Codeforces 510E - Fox And Dinner

**Source:** [Codeforces 510E - Fox And Dinner](https://codeforces.com/problemset/problem/510/E)  
**Rating:** 2200  
**Pattern:** bipartite degree-constrained flow followed by cycle extraction  
**Goal:** Seat every person in circular tables so each adjacent pair's values
sum to a prime, or report that no arrangement exists. Returned indices are
zero-based.

## 1. First principles

Every value is at least two. A prime sum must therefore contain one even and
one odd value: same-parity sums are even and greater than two. Each person
needs exactly two compatible neighbors.

Build a bipartite flow network:

```text
source -> each even vertex       capacity 2
compatible even -> odd pair      capacity 1
each odd vertex -> sink          capacity 2
```

A flow of `n` selects degree two at every vertex. The selected undirected graph
is then a disjoint union of cycles, exactly the required tables.

## 2. Cases that decide correctness

- The counts of even and odd values must be equal.
- Every selected person needs degree exactly two, not merely positive degree.
- Compatibility depends on the sum being prime.
- Several disjoint cycles are valid.
- A feasible selected graph cannot contain a path because every degree is two.

## 3. Brute force: enumerate compatible edge subsets

```python
from itertools import combinations


def prime_sum_tables_brute(values: list[int]) -> list[list[int]] | None:
    if not values or any(value < 2 for value in values):
        raise ValueError("values must be integers of at least two")
    even = [index for index, value in enumerate(values) if value % 2 == 0]
    odd = [index for index, value in enumerate(values) if value % 2 == 1]
    if len(even) != len(odd):
        return None

    limit = 2 * max(values)
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for prime in range(2, int(limit**0.5) + 1):
        if is_prime[prime]:
            for multiple in range(prime * prime, limit + 1, prime):
                is_prime[multiple] = False

    compatible = [
        (first, second)
        for first in even
        for second in odd
        if is_prime[values[first] + values[second]]
    ]
    for chosen in combinations(compatible, len(values)):
        degree = [0] * len(values)
        adjacency = [[] for _ in values]
        for first, second in chosen:
            degree[first] += 1
            degree[second] += 1
            adjacency[first].append(second)
            adjacency[second].append(first)
        if any(current != 2 for current in degree):
            continue

        tables: list[list[int]] = []
        visited = [False] * len(values)
        for start in range(len(values)):
            if visited[start]:
                continue
            table: list[int] = []
            previous = -1
            current = start
            while not visited[current]:
                visited[current] = True
                table.append(current)
                first, second = adjacency[current]
                next_vertex = first if first != previous else second
                previous, current = current, next_vertex
            if current != start:
                raise RuntimeError("degree-two component was not a cycle")
            tables.append(table)
        return tables
    return None
```

**Complexity:** `O(C(E,n) * (n+E))` time and `O(n+E)` space.

## 4. Better transition: degree two is a flow demand

The parity split makes the compatibility graph bipartite. Unit capacities on
compatibility edges prevent duplicate neighbors, while capacity two at every
person enforces exactly the two seats required by a circle.

## 5. Expert solution: max flow and cycle extraction

```python
from collections import deque


def prime_sum_tables(values: list[int]) -> list[list[int]] | None:
    if not values or any(value < 2 for value in values):
        raise ValueError("values must be integers of at least two")
    even = [index for index, value in enumerate(values) if value % 2 == 0]
    odd = [index for index, value in enumerate(values) if value % 2 == 1]
    if len(even) != len(odd):
        return None

    limit = 2 * max(values)
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for prime in range(2, int(limit**0.5) + 1):
        if is_prime[prime]:
            for multiple in range(prime * prime, limit + 1, prime):
                is_prime[multiple] = False

    vertex_count = len(values) + 2
    source = len(values)
    sink = source + 1
    adjacency = [[] for _ in range(vertex_count)]
    capacity = [[0] * vertex_count for _ in range(vertex_count)]

    def add_edge(first: int, second: int, edge_capacity: int) -> None:
        adjacency[first].append(second)
        adjacency[second].append(first)
        capacity[first][second] = edge_capacity

    for vertex in even:
        add_edge(source, vertex, 2)
    for vertex in odd:
        add_edge(vertex, sink, 2)
    compatible: list[tuple[int, int]] = []
    for first in even:
        for second in odd:
            if is_prime[values[first] + values[second]]:
                add_edge(first, second, 1)
                compatible.append((first, second))

    flow = 0
    while True:
        level = [-1] * vertex_count
        level[source] = 0
        queue = deque([source])
        while queue:
            node = queue.popleft()
            for neighbor in adjacency[node]:
                if capacity[node][neighbor] > 0 and level[neighbor] == -1:
                    level[neighbor] = level[node] + 1
                    queue.append(neighbor)
        if level[sink] == -1:
            break

        next_edge = [0] * vertex_count

        def send(node: int, pushed: int) -> int:
            if node == sink:
                return pushed
            while next_edge[node] < len(adjacency[node]):
                neighbor = adjacency[node][next_edge[node]]
                if capacity[node][neighbor] > 0 and level[neighbor] == level[node] + 1:
                    sent = send(
                        neighbor,
                        min(pushed, capacity[node][neighbor]),
                    )
                    if sent:
                        capacity[node][neighbor] -= sent
                        capacity[neighbor][node] += sent
                        return sent
                next_edge[node] += 1
            return 0

        while sent := send(source, len(values) - flow):
            flow += sent
    if flow != len(values):
        return None

    selected = [[] for _ in values]
    for first, second in compatible:
        if capacity[first][second] == 0:
            selected[first].append(second)
            selected[second].append(first)
    if any(len(neighbors) != 2 for neighbors in selected):
        raise RuntimeError("flow did not satisfy every degree")

    tables: list[list[int]] = []
    visited = [False] * len(values)
    for start in range(len(values)):
        if visited[start]:
            continue
        table: list[int] = []
        previous = -1
        current = start
        while not visited[current]:
            visited[current] = True
            table.append(current)
            first, second = selected[current]
            next_vertex = first if first != previous else second
            previous, current = current, next_vertex
        if current != start:
            raise RuntimeError("degree-two component was not a cycle")
        tables.append(table)
    return tables
```

### Why the expert code is correct

Integral max flow selects compatible edges with value zero or one. Flow `n`
saturates every capacity-two person edge, so every person has exactly two
selected compatible neighbors. A finite undirected graph in which every vertex
has degree two consists only of disjoint cycles, which the final walk extracts.

**Complexity:** Dinic runs in `O(V^2 E)` here; extraction is `O(V+E)`, and the
capacity matrix uses `O(V^2)` space.

## 6. What to remember

```text
prime sums for values >= 2 -> even-odd compatibility
circular seating -> degree exactly two
bipartite degree demands -> integral max flow
```
