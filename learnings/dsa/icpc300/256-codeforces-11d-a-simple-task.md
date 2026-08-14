# ICPC300 256: Codeforces 11D - A Simple Task

**Source:** [Codeforces 11D - A Simple Task](https://codeforces.com/problemset/problem/11/D)  
**Rating:** 2200  
**Pattern:** smallest-vertex anchored subset path DP  
**Goal:** Count distinct simple cycles in a simple undirected graph. Rotations
and the two traversal directions describe the same cycle.

## 1. First principles

Give every cycle its smallest vertex `start`. Count simple paths that begin at
`start`, use only vertices at least `start`, and close back to `start` after at
least three vertices.

Let `dp[mask][last]` count such paths visiting exactly `mask`. Restricting every
extension to vertices larger than the smallest bit makes the anchor unique.
Each undirected cycle is still counted in its two directions, so divide by two.

## 2. Cases that decide correctness

- Cycles need at least three distinct vertices.
- The graph has no self-loops or parallel edges.
- Every cycle has exactly one smallest vertex.
- A path cannot revisit a masked vertex.
- Clockwise and counterclockwise traversals are the only remaining duplication.

## 3. Brute force: enumerate anchored cycle orders

```python
from itertools import permutations


def simple_cycle_count_brute(vertex_count: int, edges: list[tuple[int, int]]) -> int:
    if vertex_count <= 0:
        raise ValueError("vertex_count must be positive")
    adjacency = [[False] * vertex_count for _ in range(vertex_count)]
    for first, second in edges:
        if (
            not 0 <= first < vertex_count
            or not 0 <= second < vertex_count
            or first == second
            or adjacency[first][second]
        ):
            raise ValueError("graph must be simple")
        adjacency[first][second] = adjacency[second][first] = True

    directed_count = 0
    for start in range(vertex_count):
        larger = list(range(start + 1, vertex_count))
        for length in range(2, len(larger) + 1):
            for middle in permutations(larger, length):
                order = (start, *middle)
                if (
                    all(
                        adjacency[order[index]][order[index + 1]]
                        for index in range(len(order) - 1)
                    )
                    and adjacency[order[-1]][start]
                ):
                    directed_count += 1
    return directed_count // 2
```

**Complexity:** `O(n! * n)` time and `O(n^2)` space.

## 4. Better transition: remember a visited set and one endpoint

Once the smallest vertex is fixed, a partial path's future depends only on its
visited mask and last vertex. The mask also prevents repeated vertices, turning
factorial order enumeration into `O(n^2 2^n)` state transitions.

## 5. Expert solution: global anchored bitmask DP

```python
def simple_cycle_count(vertex_count: int, edges: list[tuple[int, int]]) -> int:
    if vertex_count <= 0:
        raise ValueError("vertex_count must be positive")
    adjacency = [[False] * vertex_count for _ in range(vertex_count)]
    neighbors = [[] for _ in range(vertex_count)]
    for first, second in edges:
        if (
            not 0 <= first < vertex_count
            or not 0 <= second < vertex_count
            or first == second
            or adjacency[first][second]
        ):
            raise ValueError("graph must be simple")
        adjacency[first][second] = adjacency[second][first] = True
        neighbors[first].append(second)
        neighbors[second].append(first)

    mask_count = 1 << vertex_count
    dp = [[0] * vertex_count for _ in range(mask_count)]
    for vertex in range(vertex_count):
        dp[1 << vertex][vertex] = 1

    directed_count = 0
    for mask in range(1, mask_count):
        start_bit = mask & -mask
        start = start_bit.bit_length() - 1
        for last in range(start, vertex_count):
            paths = dp[mask][last]
            if paths == 0:
                continue
            if mask.bit_count() >= 3 and adjacency[last][start]:
                directed_count += paths
            for neighbor in neighbors[last]:
                if neighbor > start and mask >> neighbor & 1 == 0:
                    dp[mask | (1 << neighbor)][neighbor] += paths
    return directed_count // 2
```

### Why the expert code is correct

Every DP path starts at the smallest vertex in its mask and never introduces a
smaller one, so each directed cycle traversal has one unique state sequence.
Closing after at least three visited vertices counts every simple cycle in both
directions and no other walk. Division by two therefore leaves each undirected
cycle exactly once.

**Complexity:** `O(n^2 2^n)` time and `O(n 2^n)` space.

## 6. What to remember

```text
cycle rotation duplicate -> anchor its minimum vertex
simple path state -> visited mask plus endpoint
undirected direction duplicate -> divide by two
```
