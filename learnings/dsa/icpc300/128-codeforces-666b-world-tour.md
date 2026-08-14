# ICPC300 128: Codeforces 666B - World Tour

**Source:** [Codeforces 666B](https://codeforces.com/problemset/problem/666/B)  
**Pattern:** all-pairs BFS with constant-size endpoint candidates

## Exact contract

Given a directed unweighted graph, output four distinct vertices `a b c d`
maximizing

`dist(a,b) + dist(b,c) + dist(c,d)`,

where every distance is the directed shortest-path length. The source
guarantees that a valid quadruple exists.

## First principles

Run BFS from every vertex to obtain all directed distances. For fixed middle
vertices `(b,c)`, only the best predecessor `a` reaching `b` and successor `d`
reachable from `c` matter, subject to distinctness.

Keep the three farthest predecessors of every `b` and three farthest
successors of every `c`. A candidate endpoint can be forbidden by at most two
already chosen vertices, so among the top three at least one is as good as the
endpoint used by an optimal valid quadruple.

## Cases that decide correctness

- Distances are directed; `dist(u,v)` and `dist(v,u)` differ.
- All four vertices must be distinct even if the three routes overlap.
- Unreachable endpoint pairs are excluded.
- Keep three candidates, not just one: the best one may equal another middle
  or endpoint vertex.
- Any maximizing quadruple is accepted.

## Brute force: search quadruples and rerun BFS

```python
from collections import deque
from itertools import permutations


def world_tour_brute(
    vertex_count: int,
    edges: list[tuple[int, int]],
) -> tuple[int, tuple[int, int, int, int]]:
    graph = [[] for _ in range(vertex_count)]
    for start, target in edges:
        graph[start - 1].append(target - 1)

    def distance(start: int, target: int) -> int:
        distances = [-1] * vertex_count
        distances[start] = 0
        queue = deque([start])
        while queue:
            vertex = queue.popleft()
            if vertex == target:
                return distances[vertex]
            for neighbor in graph[vertex]:
                if distances[neighbor] == -1:
                    distances[neighbor] = distances[vertex] + 1
                    queue.append(neighbor)
        return -1

    best_score = -1
    best_vertices: tuple[int, int, int, int] = (0, 0, 0, 0)
    for vertices in permutations(range(vertex_count), 4):
        first, second, third, fourth = vertices
        parts = (
            distance(first, second),
            distance(second, third),
            distance(third, fourth),
        )
        if min(parts) >= 0 and sum(parts) > best_score:
            best_score = sum(parts)
            best_vertices = vertices
    return best_score, (
        best_vertices[0] + 1,
        best_vertices[1] + 1,
        best_vertices[2] + 1,
        best_vertices[3] + 1,
    )
```

Repeated BFS makes this far worse than `O(n^4)`.

## Better: precompute distances, still inspect all quadruples

```python
from collections import deque
from itertools import permutations


def world_tour_all_quadruples(
    vertex_count: int,
    edges: list[tuple[int, int]],
) -> tuple[int, tuple[int, int, int, int]]:
    graph = [[] for _ in range(vertex_count)]
    for start, target in edges:
        graph[start - 1].append(target - 1)

    distances = []
    for start in range(vertex_count):
        current = [-1] * vertex_count
        current[start] = 0
        queue = deque([start])
        while queue:
            vertex = queue.popleft()
            for neighbor in graph[vertex]:
                if current[neighbor] == -1:
                    current[neighbor] = current[vertex] + 1
                    queue.append(neighbor)
        distances.append(current)

    best_score = -1
    best_vertices: tuple[int, int, int, int] = (0, 0, 0, 0)
    for first, second, third, fourth in permutations(range(vertex_count), 4):
        parts = (
            distances[first][second],
            distances[second][third],
            distances[third][fourth],
        )
        if min(parts) >= 0 and sum(parts) > best_score:
            best_score = sum(parts)
            best_vertices = (first, second, third, fourth)
    return best_score, (
        best_vertices[0] + 1,
        best_vertices[1] + 1,
        best_vertices[2] + 1,
        best_vertices[3] + 1,
    )
```

All-pairs BFS removes repeated path searches, but quadruple enumeration is
still `O(n^4)`.

## Expert solution: top-three endpoints per middle vertex

```python
import sys
from collections import deque


def solve() -> None:
    input_stream = sys.stdin.buffer
    vertex_count, edge_count = map(int, input_stream.readline().split())
    graph = [[] for _ in range(vertex_count)]
    for _ in range(edge_count):
        start, target = map(int, input_stream.readline().split())
        graph[start - 1].append(target - 1)

    distances = []
    for start in range(vertex_count):
        current = [-1] * vertex_count
        current[start] = 0
        queue = deque([start])
        while queue:
            vertex = queue.popleft()
            for neighbor in graph[vertex]:
                if current[neighbor] == -1:
                    current[neighbor] = current[vertex] + 1
                    queue.append(neighbor)
        distances.append(current)

    best_incoming: list[list[tuple[int, int]]] = []
    best_outgoing: list[list[tuple[int, int]]] = []
    for vertex in range(vertex_count):
        incoming = sorted(
            (
                (distances[start][vertex], start)
                for start in range(vertex_count)
                if start != vertex and distances[start][vertex] >= 0
            ),
            reverse=True,
        )[:3]
        outgoing = sorted(
            (
                (distances[vertex][target], target)
                for target in range(vertex_count)
                if target != vertex and distances[vertex][target] >= 0
            ),
            reverse=True,
        )[:3]
        best_incoming.append(incoming)
        best_outgoing.append(outgoing)

    best_score = -1
    best_vertices = (0, 0, 0, 0)
    for second in range(vertex_count):
        for third in range(vertex_count):
            middle_distance = distances[second][third]
            if second == third or middle_distance < 0:
                continue
            for first_distance, first in best_incoming[second]:
                for last_distance, fourth in best_outgoing[third]:
                    if len({first, second, third, fourth}) < 4:
                        continue
                    score = first_distance + middle_distance + last_distance
                    if score > best_score:
                        best_score = score
                        best_vertices = (first, second, third, fourth)

    print(" ".join(str(vertex + 1) for vertex in best_vertices))


if __name__ == "__main__":
    solve()
```

For each middle pair, at most two candidates in either endpoint list can
conflict with the other chosen vertices. Therefore truncating to three cannot
discard every endpoint of an optimal valid solution.

**Complexity:** `O(n(n+m) + n^2)` time and `O(n^2)` space.
