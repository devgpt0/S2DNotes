# ICPC300 188: Codeforces 960F - Pathwalks

**Source:** [Codeforces 960F](https://codeforces.com/problemset/problem/960/F)  
**Pattern:** per-vertex Fenwick maxima over edge weights

## Exact contract

Directed weighted edges are numbered in input order. Find the greatest length
of a sequence of edges with strictly increasing indices and strictly increasing
weights such that each edge's destination is the next edge's source.

## First principles

Process edges in input order, which enforces increasing indices. For edge
`u -> v` of weight `w`, its best sequence length is

`1 + best sequence ending at u with final weight < w`.

Each vertex needs prefix-maximum queries by weight and point maximum updates.
Compress all weights incident to that vertex and use a Fenwick maximum tree.

## Cases that decide correctness

- Equal weights cannot follow one another.
- Input order matters independently of weight order.
- Parallel edges and self-loops are valid.
- A single edge forms a sequence of length one.
- Updates take a maximum because several paths can end at the same state.

## Brute force: compare every earlier edge

```python
def pathwalks_brute(
    edges: list[tuple[int, int, int]],
) -> int:
    best = [1] * len(edges)
    for current, (source, _, weight) in enumerate(edges):
        for previous in range(current):
            _, destination, previous_weight = edges[previous]
            if destination == source and previous_weight < weight:
                best[current] = max(best[current], best[previous] + 1)
    return max(best, default=0)
```

This is quadratic in the number of edges.

## Better insight: group prior paths by ending vertex

Only paths ending at the current source matter. Their final weights need a
dynamic prefix maximum, which is exactly a Fenwick maximum query after offline
weight compression.

## Expert solution: one compressed maximum tree per vertex

```python
import sys
from array import array
from bisect import bisect_left


def solve() -> None:
    input_stream = sys.stdin.buffer
    vertex_count, edge_count = map(int, input_stream.readline().split())
    edges = []
    coordinates: list[list[int]] = [[] for _ in range(vertex_count)]
    for _ in range(edge_count):
        source, destination, weight = map(int, input_stream.readline().split())
        source -= 1
        destination -= 1
        edges.append((source, destination, weight))
        coordinates[source].append(weight)
        coordinates[destination].append(weight)

    for vertex in range(vertex_count):
        coordinates[vertex] = sorted(set(coordinates[vertex]))
    fenwick = [array("i", [0]) * (len(values) + 1) for values in coordinates]

    def prefix_maximum(tree: array, position: int) -> int:
        answer = 0
        while position:
            answer = max(answer, tree[position])
            position -= position & -position
        return answer

    def update(tree: array, position: int, value: int) -> None:
        while position < len(tree):
            tree[position] = max(tree[position], value)
            position += position & -position

    answer = 0
    for source, destination, weight in edges:
        smaller_count = bisect_left(coordinates[source], weight)
        candidate = prefix_maximum(fenwick[source], smaller_count) + 1
        destination_index = bisect_left(coordinates[destination], weight) + 1
        update(fenwick[destination], destination_index, candidate)
        answer = max(answer, candidate)
    print(answer)


if __name__ == "__main__":
    solve()
```

Before an edge is processed, every Fenwick value comes from an earlier edge.
The strict prefix excludes equal weights, so both required orderings hold.

**Complexity:** `O(m log m)` time and `O(n+m)` space.
