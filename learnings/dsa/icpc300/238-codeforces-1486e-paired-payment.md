# ICPC300 238: Codeforces 1486E - Paired Payment

**Source:** [Codeforces 1486E - Paired Payment](https://codeforces.com/problemset/problem/1486/E)  
**Difficulty:** 2200  
**Pattern:** Dijkstra on pending-edge states

## Exact contract

In an undirected graph with edge weights in `[1,50]`, path edges are paid in
consecutive pairs. A pair with weights `first,second` costs
`(first+second)^2`. Return the minimum cost from vertex `0` to every vertex
using an even number of edges, or `-1` when unreachable.

## First principles

Expand each vertex into states `(vertex,pending)`. At a pair boundary,
traversing weight `w` stores `pending=w` at zero cost. Traversing the next edge
adds `(pending+w)^2` and returns to the boundary state. All expanded edges are
nonnegative, so Dijkstra applies.

## Cases that decide correctness

- A one-edge route is not a payable complete path.
- Vertex `0` has answer zero.
- Different first-edge weights at one vertex are distinct states.
- Returning through the same undirected edge is legal.
- Only pending-zero states produce final answers.

## Brute force: repeated relaxation on expanded states

```python
def paired_payment_brute(size: int, edges: list[tuple[int, int, int]]) -> list[int]:
    if type(size) is not int or size < 1:
        raise ValueError("size must be positive")
    graph = [[] for _ in range(size)]
    for first, second, weight in edges:
        if (
            type(first) is not int
            or type(second) is not int
            or type(weight) is not int
            or not 0 <= first < size
            or not 0 <= second < size
            or first == second
            or not 1 <= weight <= 50
        ):
            raise ValueError("invalid edge")
        graph[first].append((second, weight))
        graph[second].append((first, weight))

    infinity = 10**30
    distance = [[infinity] * 51 for _ in range(size)]
    distance[0][0] = 0
    state_count = size * 51
    for _ in range(state_count - 1):
        changed = False
        for vertex in range(size):
            for pending in range(51):
                current = distance[vertex][pending]
                if current == infinity:
                    continue
                for neighbor, weight in graph[vertex]:
                    next_pending = weight if pending == 0 else 0
                    added = 0 if pending == 0 else (pending + weight) ** 2
                    if current + added < distance[neighbor][next_pending]:
                        distance[neighbor][next_pending] = current + added
                        changed = True
        if not changed:
            break
    return [value if value < infinity else -1 for value in (row[0] for row in distance)]
```

Bellman-Ford-style relaxation is polynomial but far too slow on all 51 states.

## Better approach: no separate intermediate

The expanded graph is the necessary state model. Replacing repeated relaxation
with a nonnegative shortest-path priority queue is the direct scalable step.

## Expert solution: two-phase state Dijkstra

```python
from heapq import heappop, heappush


def paired_payment(size: int, edges: list[tuple[int, int, int]]) -> list[int]:
    if type(size) is not int or size < 1:
        raise ValueError("size must be positive")
    graph = [[] for _ in range(size)]
    for first, second, weight in edges:
        if (
            type(first) is not int
            or type(second) is not int
            or type(weight) is not int
            or not 0 <= first < size
            or not 0 <= second < size
            or first == second
            or not 1 <= weight <= 50
        ):
            raise ValueError("invalid edge")
        graph[first].append((second, weight))
        graph[second].append((first, weight))

    infinity = 10**30
    distance = [[infinity] * 51 for _ in range(size)]
    distance[0][0] = 0
    heap = [(0, 0, 0)]
    while heap:
        current, vertex, pending = heappop(heap)
        if current != distance[vertex][pending]:
            continue
        for neighbor, weight in graph[vertex]:
            if pending == 0:
                next_pending = weight
                candidate = current
            else:
                next_pending = 0
                candidate = current + (pending + weight) ** 2
            if candidate < distance[neighbor][next_pending]:
                distance[neighbor][next_pending] = candidate
                heappush(heap, (candidate, neighbor, next_pending))
    return [value if value < infinity else -1 for value in (row[0] for row in distance)]
```

Each expanded path records exactly the unmatched first edge, so completing a
pair charges its exact cost once. Dijkstra therefore minimizes every payable
even-edge route.

**Complexity:** `O((nW+mW) log(nW))` time and `O(nW+m)` space for `W=51`.
