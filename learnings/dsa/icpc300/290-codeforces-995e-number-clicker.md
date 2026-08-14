# ICPC300 290: Codeforces 995E - Number Clicker

**Source:** [Codeforces 995E - Number Clicker](https://codeforces.com/problemset/problem/995/E)  
**Rating:** 2500  
**Pattern:** bidirectional breadth-first search on modular operations  
**Goal:** For prime `modulus`, find a shortest value path from `start` to
`target`. One move adds one, subtracts one, or replaces a nonzero value by its
modular inverse; every result is reduced modulo `modulus`.

## 1. First principles

Values are graph vertices. Addition and subtraction are reverse edges, while
modular inversion is its own reverse. The graph is therefore undirected and
unweighted, so BFS is exact. Searching from both endpoints reduces the explored
depth from `distance` to about half that distance.

## 2. Cases that decide correctness

- `start == target` needs a one-vertex path.
- Addition and subtraction wrap modulo `modulus`.
- Zero has no modular-inverse edge.
- The source guarantees a prime modulus; the code validates that promise.
- Parent maps on the target side point toward the target.

## 3. Brute force: BFS over the full residue graph

```python
from collections import deque
from math import isqrt


def number_click_path_brute(start: int, target: int, modulus: int) -> list[int]:
    if modulus < 2 or any(
        modulus % divisor == 0 for divisor in range(2, isqrt(modulus) + 1)
    ):
        raise ValueError("modulus must be prime")
    if not 0 <= start < modulus or not 0 <= target < modulus:
        raise ValueError("values must be residues")

    parents: dict[int, int | None] = {start: None}
    queue = deque([start])
    while target not in parents:
        value = queue.popleft()
        neighbors = {(value + 1) % modulus, (value - 1) % modulus}
        if value:
            neighbors.add(pow(value, modulus - 2, modulus))
        for neighbor in neighbors:
            if neighbor not in parents:
                parents[neighbor] = value
                queue.append(neighbor)

    path: list[int] = []
    current: int | None = target
    while current is not None:
        path.append(current)
        current = parents[current]
    return path[::-1]
```

**Complexity:** `O(modulus)` time and space in the worst case.

## 4. Better transition: search from both ends

Maintain one BFS frontier and parent map per endpoint. Expand a complete layer,
then test which newly reached vertices already belong to the opposite search.
The first intersecting layer gives a shortest connection in an undirected
unweighted graph.

## 5. Expert solution: bidirectional BFS with reconstruction

```python
from math import isqrt


def number_click_path(start: int, target: int, modulus: int) -> list[int]:
    if modulus < 2 or any(
        modulus % divisor == 0 for divisor in range(2, isqrt(modulus) + 1)
    ):
        raise ValueError("modulus must be prime")
    if not 0 <= start < modulus or not 0 <= target < modulus:
        raise ValueError("values must be residues")
    if start == target:
        return [start]

    def neighbors(value: int) -> set[int]:
        result = {(value + 1) % modulus, (value - 1) % modulus}
        if value:
            result.add(pow(value, modulus - 2, modulus))
        return result

    def expand(
        frontier: set[int],
        own_parents: dict[int, int | None],
        own_distances: dict[int, int],
        other_distances: dict[int, int],
    ) -> tuple[set[int], int | None]:
        next_frontier: set[int] = set()
        meeting: int | None = None
        best_distance = modulus + 1
        for value in frontier:
            for neighbor in neighbors(value):
                if neighbor in own_parents:
                    continue
                own_parents[neighbor] = value
                own_distances[neighbor] = own_distances[value] + 1
                next_frontier.add(neighbor)
                if (
                    neighbor in other_distances
                    and own_distances[neighbor] + other_distances[neighbor]
                    < best_distance
                ):
                    best_distance = own_distances[neighbor] + other_distances[neighbor]
                    meeting = neighbor
        return next_frontier, meeting

    forward_parents: dict[int, int | None] = {start: None}
    backward_parents: dict[int, int | None] = {target: None}
    forward_distances = {start: 0}
    backward_distances = {target: 0}
    forward_frontier = {start}
    backward_frontier = {target}
    meeting: int | None = None
    while meeting is None:
        forward_frontier, meeting = expand(
            forward_frontier,
            forward_parents,
            forward_distances,
            backward_distances,
        )
        if meeting is not None:
            break
        backward_frontier, meeting = expand(
            backward_frontier,
            backward_parents,
            backward_distances,
            forward_distances,
        )

    left: list[int] = []
    current: int | None = meeting
    while current is not None:
        left.append(current)
        current = forward_parents[current]
    left.reverse()

    right: list[int] = []
    current = backward_parents[meeting]
    while current is not None:
        right.append(current)
        current = backward_parents[current]
    return left + right
```

### Why the expert code is correct

Each side performs ordinary BFS one full distance layer at a time. Because
every operation is reversible, the first layer intersection joins shortest
prefix and suffix paths; any shorter route would have intersected an earlier
pair of explored layers. Forward parents lead to `start`, backward parents lead
to `target`, so joining their chains reconstructs a legal shortest path.

**Complexity:** `O(3^(distance/2))` expected explored states and space, capped
by `O(modulus)`.

## 6. What to remember

```text
reversible modular operations -> undirected unweighted graph
shortest path -> BFS
small branching but unknown diameter -> search from both endpoints
```
