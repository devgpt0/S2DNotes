# ICPC300 204: Codeforces 845G - Shortest Path Problem?

**Source:** [Codeforces 845G - Shortest Path Problem?](https://codeforces.com/problemset/problem/845/G)  
**Difficulty:** 2300  
**Pattern:** XOR distances plus a linear basis of cycle values

## Exact contract

In a connected undirected weighted graph, a walk's cost is the XOR of its edge
weights. Find the minimum achievable XOR cost from vertex `0` to vertex
`n-1`.

## First principles

Choose any DFS-tree walk and let `distance[v]` be its XOR from the source. A
non-tree edge `(u,v,w)` creates cycle XOR
`distance[u] ^ distance[v] ^ w`. Every source-to-target walk XOR is the tree
value `distance[target]` XOR some combination of cycle values.

Gaussian elimination over bits stores the span of all cycle XORs. Greedily XOR
a basis vector when it decreases the target value.

## Cases that decide correctness

- Zero-weight edges and zero-valued cycles are valid.
- Parallel edges can create a useful two-edge cycle.
- The graph must be connected under the source contract.
- Undirected adjacency sees each cycle twice; duplicate insertion is harmless.
- Numeric minimization processes basis pivots from high bit to low bit.

## Brute force: BFS over `(vertex, xor)` states

```python
from collections import deque


def minimum_xor_walk_brute(size: int, edges: list[tuple[int, int, int]]) -> int:
    if type(size) is not int or size < 1:
        raise ValueError("size must be positive")
    maximum_weight = 0
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
        maximum_weight = max(maximum_weight, weight)
        graph[first].append((second, weight))
        graph[second].append((first, weight))

    bit_count = maximum_weight.bit_length()
    if bit_count > 16:
        raise ValueError("brute force supports at most 16 weight bits")
    xor_limit = 1 << bit_count
    seen = [bytearray(xor_limit) for _ in range(size)]
    seen[0][0] = 1
    queue = deque([(0, 0)])
    while queue:
        vertex, value = queue.popleft()
        for neighbor, weight in graph[vertex]:
            changed = value ^ weight
            if not seen[neighbor][changed]:
                seen[neighbor][changed] = 1
                queue.append((neighbor, changed))
    if any(not any(vertex_states) for vertex_states in seen):
        raise ValueError("graph must be connected")
    for value, reachable in enumerate(seen[-1]):
        if reachable:
            return value
    raise RuntimeError("connected target has no XOR state")
```

The state count is `O(n 2^B)` for `B` weight bits.

## Better approach: enumerate cycle combinations

Compute one XOR distance and collect every cycle XOR. Trying all subsets of
those cycle values is correct but exponential in the number of independent
cycles; Gaussian elimination compresses them to at most `B` generators.

## Expert solution: XOR Gaussian basis

```python
def minimum_xor_walk(size: int, edges: list[tuple[int, int, int]]) -> int:
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
            or weight < 0
        ):
            raise ValueError("invalid edge")
        graph[first].append((second, weight))
        graph[second].append((first, weight))

    distance: list[int | None] = [None] * size
    distance[0] = 0
    stack = [0]
    basis: dict[int, int] = {}

    def insert(value: int) -> None:
        while value:
            bit = value.bit_length() - 1
            if bit in basis:
                value ^= basis[bit]
            else:
                basis[bit] = value
                return

    while stack:
        vertex = stack.pop()
        vertex_distance = distance[vertex]
        if vertex_distance is None:
            raise RuntimeError("visited vertex lacks a distance")
        for neighbor, weight in graph[vertex]:
            neighbor_distance = distance[neighbor]
            if neighbor_distance is None:
                distance[neighbor] = vertex_distance ^ weight
                stack.append(neighbor)
            else:
                insert(vertex_distance ^ neighbor_distance ^ weight)

    if any(value is None for value in distance):
        raise ValueError("graph must be connected")
    target = distance[-1]
    if target is None:
        raise RuntimeError("validated target lacks a distance")
    for bit in sorted(basis, reverse=True):
        target = min(target, target ^ basis[bit])
    return target
```

The DFS value plus the cycle space describes every feasible walk XOR. Basis
insertion preserves exactly that span, and high-to-low minimization chooses the
smallest member of its affine coset.

**Complexity:** `O((n+m)B)` time and `O(n+m+B)` space.
