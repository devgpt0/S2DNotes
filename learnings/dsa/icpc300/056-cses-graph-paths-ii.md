# ICPC300 056: CSES - Graph Paths II

**Source:** [CSES - Graph Paths II](https://cses.fi/problemset/task/1724/)  
**Pattern:** min-plus matrix exponentiation  
**Goal:** Find the minimum cost of a directed walk from vertex `0` to vertex
`n - 1` using exactly `k` edges, or `-1` if none exists.

Edges are zero-based `(source, destination, weight)` triples.

## 1. First principles

Ordinary matrix multiplication combines path counts with multiplication and
addition. Shortest paths instead combine alternatives with `min` and
concatenate walks with `+`:

```text
(A x B)[i][j] = min over m of A[i][m] + B[m][j]
```

This is **min-plus multiplication**. If matrix `M` stores cheapest one-edge
walks, then `M^k` in this algebra stores cheapest walks of exactly `k` edges.
Binary exponentiation handles a huge `k`.

## 2. Cases that decide correctness

| Case | Required behavior |
| --- | --- |
| Parallel edges | Keep the cheaper one-edge cost. |
| A cheaper path uses fewer than `k` edges | Reject it; the edge count must be exact. |
| Cycles | They may be required to reach exactly `k` edges. |
| No valid walk | Return `-1`. |
| `k = 0` | Cost is `0` only when source equals sink. |

## 3. Brute force: enumerate every length-`k` walk

```python
def graph_paths_ii_brute(
    vertex_count: int,
    edges: list[tuple[int, int, int]],
    required_edges: int,
) -> int:
    if vertex_count <= 0 or required_edges < 0:
        raise ValueError("vertex_count and required_edges must be nonnegative")

    graph: list[list[tuple[int, int]]] = [[] for _ in range(vertex_count)]
    for first, second, weight in edges:
        graph[first].append((second, weight))

    def search(node: int, remaining_edges: int) -> int | None:
        if remaining_edges == 0:
            return 0 if node == vertex_count - 1 else None

        best: int | None = None
        for neighbor, weight in graph[node]:
            suffix = search(neighbor, remaining_edges - 1)
            if suffix is None:
                continue
            candidate = weight + suffix
            best = candidate if best is None else min(best, candidate)
        return best

    answer = search(0, required_edges)
    return -1 if answer is None else answer
```

**Complexity:** `O(out_degree^k)` time and `O(k)` recursion space.

## 4. Better: dynamic programming by edge count

After `step` rounds, `distance[v]` is the cheapest walk from the source to `v`
using exactly `step` edges.

```python
def graph_paths_ii_dynamic_programming(
    vertex_count: int,
    edges: list[tuple[int, int, int]],
    required_edges: int,
) -> int:
    if vertex_count <= 0 or required_edges < 0:
        raise ValueError("vertex_count and required_edges must be nonnegative")

    distance: list[int | None] = [None] * vertex_count
    distance[0] = 0
    for _ in range(required_edges):
        next_distance: list[int | None] = [None] * vertex_count
        for first, second, weight in edges:
            first_distance = distance[first]
            if first_distance is None:
                continue
            candidate = first_distance + weight
            known_distance = next_distance[second]
            if known_distance is None:
                next_distance[second] = candidate
            else:
                next_distance[second] = min(known_distance, candidate)
        distance = next_distance

    answer = distance[-1]
    return -1 if answer is None else answer
```

**Complexity:** `O(kE)` time and `O(V)` space. This is effective only when
`k` is small.

## 5. Expert solution: min-plus exponentiation

Use `None` as infinity so no numeric sentinel can collide with a valid large
cost.

```python
Matrix = list[list[int | None]]


def graph_paths_ii_min_plus(
    vertex_count: int,
    edges: list[tuple[int, int, int]],
    required_edges: int,
) -> int:
    if vertex_count <= 0 or required_edges < 0:
        raise ValueError("vertex_count and required_edges must be nonnegative")

    def multiply(left: Matrix, right: Matrix) -> Matrix:
        result: Matrix = [[None] * vertex_count for _ in range(vertex_count)]
        for first in range(vertex_count):
            for middle in range(vertex_count):
                left_cost = left[first][middle]
                if left_cost is None:
                    continue
                for second in range(vertex_count):
                    right_cost = right[middle][second]
                    if right_cost is None:
                        continue
                    candidate = left_cost + right_cost
                    current = result[first][second]
                    if current is None or candidate < current:
                        result[first][second] = candidate
        return result

    power: Matrix = [[None] * vertex_count for _ in range(vertex_count)]
    for first, second, weight in edges:
        current = power[first][second]
        if current is None or weight < current:
            power[first][second] = weight

    result: Matrix = [[None] * vertex_count for _ in range(vertex_count)]
    for vertex in range(vertex_count):
        result[vertex][vertex] = 0

    exponent = required_edges
    while exponent > 0:
        if exponent & 1:
            result = multiply(result, power)
        exponent //= 2
        if exponent > 0:
            power = multiply(power, power)

    answer = result[0][-1]
    return -1 if answer is None else answer
```

### Why the expert code is correct

- The base matrix represents exactly one edge, including the cheapest parallel
  edge.
- Min-plus multiplication concatenates exact-length walks and minimizes over
  their joining vertex.
- Binary exponentiation combines powers whose edge counts sum to exactly the
  set bits of `k`.

**Complexity:** `O(V^3 log k)` time and `O(V^2)` space.

## 6. What to remember

```text
ordinary matrix: multiply then add
shortest-walk matrix: add costs then take minimum
min-plus M^k = cheapest walks using exactly k edges
```
