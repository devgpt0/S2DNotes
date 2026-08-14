# ICPC300 275: Codeforces 1292C - Xenon's Attack on the Gangs

**Source:** [Codeforces 1292C](https://codeforces.com/problemset/problem/1292/C)  
**Difficulty:** 2300  
**Pattern:** all-pairs tree interval DP

## Exact contract

Label the `n-1` tree edges with every integer from `0` through `n-2` exactly
once. For each unordered vertex pair, take the MEX of labels on its path.
Maximize the sum of these path MEX values.

## First principles

For endpoints `u,v`, remove the first path edge at each end. Let `side(u,v)` be
the size of the component containing `u` after its first edge toward `v` is
cut. Giving the next smallest label inside the current endpoint path raises
the MEX of exactly `side(u,v)*side(v,u)` vertex pairs.

After that contribution, shrink either endpoint one edge toward the other.
Therefore

`dp[u][v] = side(u,v)*side(v,u) + max(dp[next(u,v)][v], dp[u][next(v,u)])`.

Process pairs by increasing distance.

## Cases that decide correctness

- Edge labels form a permutation beginning at zero.
- A one-vertex tree has answer zero.
- Both endpoint-shrink choices must be considered.
- Directed component size depends on which side of an edge is requested.
- Pair DP is symmetric, but its two next hops are different.

## Brute force: enumerate every edge-label permutation

```python
from itertools import permutations


def xenon_attack_brute(
    vertex_count: int,
    edges: list[tuple[int, int]],
) -> int:
    graph: list[list[tuple[int, int]]] = [[] for _ in range(vertex_count)]
    for edge_index, (first, second) in enumerate(edges):
        graph[first].append((second, edge_index))
        graph[second].append((first, edge_index))

    paths: list[list[int]] = []
    for source in range(vertex_count):
        parent = [(-1, -1)] * vertex_count
        parent[source] = (source, -1)
        order = [source]
        for vertex in order:
            for neighbor, edge_index in graph[vertex]:
                if parent[neighbor][0] == -1:
                    parent[neighbor] = (vertex, edge_index)
                    order.append(neighbor)
        for target in range(source + 1, vertex_count):
            path: list[int] = []
            vertex = target
            while vertex != source:
                previous, edge_index = parent[vertex]
                path.append(edge_index)
                vertex = previous
            paths.append(path)

    answer = 0
    for labels in permutations(range(vertex_count - 1)):
        total = 0
        for path in paths:
            used = {labels[edge_index] for edge_index in path}
            mex = 0
            while mex in used:
                mex += 1
            total += mex
        answer = max(answer, total)
    return answer
```

This is factorial in the number of edges.

## Better insight: only the current path endpoints matter

Labels smaller than the current MEX form one connected path. Its next edge can
extend from either endpoint, which produces the two-state recurrence above.

## Expert solution: component-side products over all endpoint pairs

```python
import sys


def solve() -> None:
    input_stream = sys.stdin.buffer
    vertex_count = int(input_stream.readline())
    graph: list[list[int]] = [[] for _ in range(vertex_count)]
    edges: list[tuple[int, int]] = []
    for _ in range(vertex_count - 1):
        first, second = map(int, input_stream.readline().split())
        first -= 1
        second -= 1
        graph[first].append(second)
        graph[second].append(first)
        edges.append((first, second))

    parent = [-1] * vertex_count
    parent[0] = 0
    order = [0]
    for vertex in order:
        for neighbor in graph[vertex]:
            if parent[neighbor] == -1:
                parent[neighbor] = vertex
                order.append(neighbor)
    subtree_size = [1] * vertex_count
    for vertex in reversed(order[1:]):
        subtree_size[parent[vertex]] += subtree_size[vertex]

    directed_side: list[dict[int, int]] = [{} for _ in range(vertex_count)]
    for first, second in edges:
        if parent[second] == first:
            directed_side[first][second] = vertex_count - subtree_size[second]
            directed_side[second][first] = subtree_size[second]
        else:
            directed_side[second][first] = vertex_count - subtree_size[first]
            directed_side[first][second] = subtree_size[first]

    next_hop = [[0] * vertex_count for _ in range(vertex_count)]
    distance = [[0] * vertex_count for _ in range(vertex_count)]
    for source in range(vertex_count):
        next_hop[source][source] = source
        for first_step in graph[source]:
            stack = [(first_step, source)]
            next_hop[source][first_step] = first_step
            distance[source][first_step] = 1
            while stack:
                vertex, previous = stack.pop()
                for neighbor in graph[vertex]:
                    if neighbor == previous:
                        continue
                    next_hop[source][neighbor] = first_step
                    distance[source][neighbor] = distance[source][vertex] + 1
                    stack.append((neighbor, vertex))

    pairs = sorted(
        (distance[first][second], first, second)
        for first in range(vertex_count)
        for second in range(first + 1, vertex_count)
    )
    dynamic = [[0] * vertex_count for _ in range(vertex_count)]
    answer = 0
    for _, first, second in pairs:
        first_next = next_hop[first][second]
        second_next = next_hop[second][first]
        contribution = (
            directed_side[first][first_next] * directed_side[second][second_next]
        )
        value = contribution + max(
            dynamic[first_next][second],
            dynamic[first][second_next],
        )
        dynamic[first][second] = value
        dynamic[second][first] = value
        answer = max(answer, value)
    print(answer)


if __name__ == "__main__":
    solve()
```

Increasing path distance guarantees both smaller DP states are already known;
the side product counts exactly the pairs improved by the next label.

**Complexity:** `O(n^2 log n)` time and `O(n^2)` space.
