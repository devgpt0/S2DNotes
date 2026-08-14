# ICPC300 235: Codeforces 1253F - Cheap Robot

**Source:** [Codeforces 1253F - Cheap Robot](https://codeforces.com/problemset/problem/1253/F)  
**Difficulty:** 2300  
**Pattern:** multi-source distances, bottleneck MST, and binary lifting

## Exact contract

In a connected weighted undirected graph, vertices `0..special_count-1` are
charging cities. For each query, return the minimum battery capacity needed to
travel between its vertices while charging optimally.

## First principles

Multi-source Dijkstra gives `nearest[v]`, the distance to a closest charger.
Crossing edge `(u,v,w)` between charger regions needs capacity
`nearest[u] + w + nearest[v]`. The query becomes a minimax path problem on
these transformed edge weights.

Every minimax path value equals the maximum edge on the path in a minimum
spanning tree. Binary lifting answers those path maxima.

## Cases that decide correctness

- All chargers start Dijkstra at distance zero.
- Parallel edges keep their independent transformed weights.
- A query from a vertex to itself needs zero.
- Kruskal may choose any edge among equal weights.
- Path aggregation uses maximum, not sum.

## Brute force: minimax Floyd-Warshall

```python
from heapq import heappop, heappush


def cheap_robot_brute(
    size: int,
    edges: list[tuple[int, int, int]],
    special_count: int,
    queries: list[tuple[int, int]],
) -> list[int]:
    if type(size) is not int or size < 1 or not 1 <= special_count <= size:
        raise ValueError("invalid size or special count")
    graph = [[] for _ in range(size)]
    for first, second, weight in edges:
        if (
            type(first) is not int
            or type(second) is not int
            or type(weight) is not int
            or not 0 <= first < size
            or not 0 <= second < size
            or first == second
            or weight < 0
        ):
            raise ValueError("invalid edge")
        graph[first].append((second, weight))
        graph[second].append((first, weight))

    infinity = 10**30
    nearest = [infinity] * size
    heap: list[tuple[int, int]] = []
    for vertex in range(special_count):
        nearest[vertex] = 0
        heappush(heap, (0, vertex))
    while heap:
        distance, vertex = heappop(heap)
        if distance != nearest[vertex]:
            continue
        for neighbor, weight in graph[vertex]:
            candidate = distance + weight
            if candidate < nearest[neighbor]:
                nearest[neighbor] = candidate
                heappush(heap, (candidate, neighbor))
    if any(distance == infinity for distance in nearest):
        raise ValueError("graph must be connected")

    bottleneck = [[infinity] * size for _ in range(size)]
    for vertex in range(size):
        bottleneck[vertex][vertex] = 0
    for first, second, weight in edges:
        transformed = nearest[first] + weight + nearest[second]
        bottleneck[first][second] = min(bottleneck[first][second], transformed)
        bottleneck[second][first] = min(bottleneck[second][first], transformed)
    for middle in range(size):
        for first in range(size):
            for second in range(size):
                bottleneck[first][second] = min(
                    bottleneck[first][second],
                    max(bottleneck[first][middle], bottleneck[middle][second]),
                )

    answers = []
    for first, second in queries:
        if (
            type(first) is not int
            or type(second) is not int
            or not 0 <= first < size
            or not 0 <= second < size
        ):
            raise ValueError("invalid query")
        answers.append(bottleneck[first][second])
    return answers
```

This takes `O(n^3)` time.

## Better approach: one minimax Dijkstra per query

Relaxing a path by `max(current, edge)` answers one query in
`O((n+m) log n)`. The MST preserves all pairwise bottleneck answers at once.

## Expert solution: transformed Kruskal tree paths

```python
from heapq import heappop, heappush


def cheap_robot(
    size: int,
    edges: list[tuple[int, int, int]],
    special_count: int,
    queries: list[tuple[int, int]],
) -> list[int]:
    if type(size) is not int or size < 1 or not 1 <= special_count <= size:
        raise ValueError("invalid size or special count")
    graph = [[] for _ in range(size)]
    for first, second, weight in edges:
        if (
            type(first) is not int
            or type(second) is not int
            or type(weight) is not int
            or not 0 <= first < size
            or not 0 <= second < size
            or first == second
            or weight < 0
        ):
            raise ValueError("invalid edge")
        graph[first].append((second, weight))
        graph[second].append((first, weight))

    infinity = 10**30
    nearest = [infinity] * size
    heap: list[tuple[int, int]] = []
    for vertex in range(special_count):
        nearest[vertex] = 0
        heappush(heap, (0, vertex))
    while heap:
        distance, vertex = heappop(heap)
        if distance != nearest[vertex]:
            continue
        for neighbor, weight in graph[vertex]:
            candidate = distance + weight
            if candidate < nearest[neighbor]:
                nearest[neighbor] = candidate
                heappush(heap, (candidate, neighbor))
    if any(distance == infinity for distance in nearest):
        raise ValueError("graph must be connected")

    transformed_edges = sorted(
        (nearest[first] + weight + nearest[second], first, second)
        for first, second, weight in edges
    )
    representative = list(range(size))
    component_size = [1] * size

    def find(vertex: int) -> int:
        while representative[vertex] != vertex:
            representative[vertex] = representative[representative[vertex]]
            vertex = representative[vertex]
        return vertex

    tree = [[] for _ in range(size)]
    for weight, first, second in transformed_edges:
        first_root = find(first)
        second_root = find(second)
        if first_root == second_root:
            continue
        if component_size[first_root] < component_size[second_root]:
            first_root, second_root = second_root, first_root
        representative[second_root] = first_root
        component_size[first_root] += component_size[second_root]
        tree[first].append((second, weight))
        tree[second].append((first, weight))

    levels = size.bit_length()
    ancestor = [[0] * size for _ in range(levels)]
    maximum = [[0] * size for _ in range(levels)]
    depth = [-1] * size
    depth[0] = 0
    stack = [0]
    while stack:
        vertex = stack.pop()
        for neighbor, weight in tree[vertex]:
            if depth[neighbor] != -1:
                continue
            depth[neighbor] = depth[vertex] + 1
            ancestor[0][neighbor] = vertex
            maximum[0][neighbor] = weight
            stack.append(neighbor)
    if any(value == -1 for value in depth):
        raise RuntimeError("Kruskal failed to span a connected graph")

    for level in range(1, levels):
        for vertex in range(size):
            middle = ancestor[level - 1][vertex]
            ancestor[level][vertex] = ancestor[level - 1][middle]
            maximum[level][vertex] = max(
                maximum[level - 1][vertex], maximum[level - 1][middle]
            )

    answers: list[int] = []
    for first, second in queries:
        if (
            type(first) is not int
            or type(second) is not int
            or not 0 <= first < size
            or not 0 <= second < size
        ):
            raise ValueError("invalid query")
        answer = 0
        if depth[first] < depth[second]:
            first, second = second, first
        difference = depth[first] - depth[second]
        for level in range(levels):
            if difference >> level & 1:
                answer = max(answer, maximum[level][first])
                first = ancestor[level][first]
        if first != second:
            for level in range(levels - 1, -1, -1):
                if ancestor[level][first] != ancestor[level][second]:
                    answer = max(answer, maximum[level][first], maximum[level][second])
                    first = ancestor[level][first]
                    second = ancestor[level][second]
            answer = max(answer, maximum[0][first], maximum[0][second])
        answers.append(answer)
    return answers
```

The transformed graph encodes the charger detours needed at each crossing.
Kruskal preserves minimum bottleneck paths, and binary lifting returns each MST
path maximum.

**Complexity:** `O((n+m+q) log n)` time and `O(n log n+m)` space.
