# ICPC300 296: Codeforces 1209F - Koala and Notebook

**Source:** [Codeforces 1209F - Koala and Notebook](https://codeforces.com/problemset/problem/1209/F)  
**Rating:** 2300  
**Pattern:** decimal-edge expansion and lexicographic grouped BFS  
**Goal:** Edge `i` of an undirected connected graph is labeled by decimal
`i`. A path's value is the concatenation of its edge labels. Find the minimum
value from vertex `1` to every vertex and return each modulo `1_000_000_007`.

## 1. First principles

Labels have no leading zero, so numeric order is first shorter digit length,
then lexicographic order. Replace each traversal direction of every edge by a
directed chain of single decimal digits.

BFS now minimizes digit length. Within one BFS layer, process groups with equal
prefix in lexicographic order and bucket outgoing edges by digit `0..9`. The
first visit to an expanded vertex is its minimum digit string.

## 2. Cases that decide correctness

- Traversing an undirected edge in either direction appends the same label.
- Each direction needs its own intermediate chain.
- Several equal-prefix parents may reach the same vertex.
- Smaller digit buckets must mark vertices before larger buckets.
- The source graph must be connected.

## 3. Brute force: Dijkstra with complete digit strings

```python
from heapq import heappop, heappush


MODULO = 1_000_000_007


def minimum_path_numbers_brute(
    vertex_count: int,
    edges: list[tuple[int, int]],
) -> list[int]:
    if type(vertex_count) is not int or vertex_count <= 0:
        raise ValueError("vertex_count must be positive")
    graph: list[list[tuple[int, str]]] = [[] for _ in range(vertex_count)]
    for edge_number, (first, second) in enumerate(edges, start=1):
        if (
            type(first) is not int
            or type(second) is not int
            or not 0 <= first < vertex_count
            or not 0 <= second < vertex_count
            or first == second
        ):
            raise ValueError("invalid edge")
        label = str(edge_number)
        graph[first].append((second, label))
        graph[second].append((first, label))

    best: list[str | None] = [None] * vertex_count
    best[0] = ""
    queue = [(0, "", 0)]
    while queue:
        length, digits, vertex = heappop(queue)
        if best[vertex] != digits:
            continue
        for neighbor, label in graph[vertex]:
            candidate = digits + label
            known = best[neighbor]
            if known is None or (len(candidate), candidate) < (len(known), known):
                best[neighbor] = candidate
                heappush(queue, (length + len(label), candidate, neighbor))
    if any(digits is None for digits in best):
        raise ValueError("graph must be connected")
    return [0 if not digits else int(digits) % MODULO for digits in best]
```

**Complexity:** exponential-size strings may be copied; suitable only for tiny
graphs.

## 4. Better approach: expand labels and compare stored strings

Single-digit expansion makes all edges unit length, but retaining a complete
best string at every expanded node still causes quadratic copying. Equal-prefix
groups need only one modular prefix value.

## 5. Expert solution: grouped BFS in numeric-string order

```python
from collections import deque


MODULO = 1_000_000_007


def minimum_path_numbers(
    vertex_count: int,
    edges: list[tuple[int, int]],
) -> list[int]:
    if type(vertex_count) is not int or vertex_count <= 0:
        raise ValueError("vertex_count must be positive")
    expanded: list[list[tuple[int, int]]] = [[] for _ in range(vertex_count)]
    for edge_number, (first, second) in enumerate(edges, start=1):
        if (
            type(first) is not int
            or type(second) is not int
            or not 0 <= first < vertex_count
            or not 0 <= second < vertex_count
            or first == second
        ):
            raise ValueError("invalid edge")
        label = str(edge_number)
        for start, finish in ((first, second), (second, first)):
            current = start
            for offset, character in enumerate(label):
                if offset == len(label) - 1:
                    next_vertex = finish
                else:
                    next_vertex = len(expanded)
                    expanded.append([])
                expanded[current].append((int(character), next_vertex))
                current = next_vertex

    visited = [False] * len(expanded)
    value_modulo = [0] * len(expanded)
    visited[0] = True
    groups = deque([[0]])
    while groups:
        group = groups.popleft()
        prefix_modulo = value_modulo[group[0]]
        buckets = [[] for _ in range(10)]
        for vertex in group:
            for digit, neighbor in expanded[vertex]:
                if not visited[neighbor]:
                    buckets[digit].append(neighbor)
        for digit, bucket in enumerate(buckets):
            next_group = []
            for neighbor in bucket:
                if visited[neighbor]:
                    continue
                visited[neighbor] = True
                value_modulo[neighbor] = (10 * prefix_modulo + digit) % MODULO
                next_group.append(neighbor)
            if next_group:
                groups.append(next_group)

    if not all(visited[:vertex_count]):
        raise ValueError("graph must be connected")
    return value_modulo[:vertex_count]
```

### Why the expert code is correct

Expanded BFS layers are increasing digit lengths. FIFO prefix groups are
lexicographically ordered within each layer, and their digit buckets append
children in lexicographic order. Therefore the first visit is the minimum
numeric string; its modular value follows the ordinary decimal recurrence.

**Complexity:** `O(n + sum(log edge_index))` time and space over all directed
edge-label chains.

## 6. What to remember

```text
concatenated positive labels -> length then lexicographic order
multi-digit edge -> directed digit chain per traversal direction
equal prefix -> process all its outgoing digits together
```
