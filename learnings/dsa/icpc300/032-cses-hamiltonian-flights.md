# ICPC300 032: CSES - Hamiltonian Flights

**Source:** [CSES - Hamiltonian Flights](https://cses.fi/problemset/task/1690/)  
**Pattern:** subset dynamic programming

## Exact contract

Input gives a directed graph with `2 <= n <= 20` cities and `m` flights.
Count routes from city `1` to city `n` that visit every city exactly once.
Parallel flights are distinct choices. Output the count modulo `1_000_000_007`.

## First principles

Once a route has visited a set of cities and currently ends at `v`, its earlier
order matters only through the number of ways to reach that state. This gives
the state `(visited_mask, v)`.

City `1` must be present from the beginning. City `n` cannot be visited before
the final step, because leaving it would violate the required endpoint. Store
states only for cities `1..n-1`, then append one final flight to city `n`.

## Cases that decide correctness

- A city is visited once even when the graph has self-loops; self-loops never
  belong to a Hamiltonian route.
- Parallel flights multiply the number of routes and must not be deduplicated.
- City `n` is excluded from all partial masks.
- For `n = 2`, the answer is exactly the number of flights `1 -> 2`.
- Apply the modulus at every state.

## Brute force: permute all intermediate cities

```python
from collections import Counter
from itertools import permutations


def count_hamiltonian_flights_brute(
    vertex_count: int,
    edges: list[tuple[int, int]],
) -> int:
    multiplicity = Counter(edges)
    answer = 0
    for middle in permutations(range(1, vertex_count - 1)):
        route = (0, *middle, vertex_count - 1)
        ways = 1
        for start, end in zip(route, route[1:]):
            ways *= multiplicity[start, end]
        answer += ways
    return answer % 1_000_000_007
```

**Complexity:** `O((n-2)! n)` time and `O(m)` space.

## Better: memoize the endpoint-and-mask recurrence

```python
from collections import Counter
from functools import cache


def count_hamiltonian_flights_memo(
    vertex_count: int,
    edges: list[tuple[int, int]],
) -> int:
    modulus = 1_000_000_007
    edge_count = Counter(edges)

    @cache
    def routes(mask: int, end: int) -> int:
        if mask == 1:
            return int(end == 0)
        without_end = mask ^ (1 << end)
        return (
            sum(
                routes(without_end, previous) * edge_count[previous, end]
                for previous in range(vertex_count - 1)
                if without_end & (1 << previous)
            )
            % modulus
        )

    internal_mask = (1 << (vertex_count - 1)) - 1
    return (
        sum(
            routes(internal_mask, previous) * edge_count[previous, vertex_count - 1]
            for previous in range(vertex_count - 1)
        )
        % modulus
    )
```

Memoization reduces factorial repetition to `O(n^2 2^n)` work, but Python
dictionary entries for millions of states consume too much memory near
`n = 20`.

## Expert solution: packed iterative subset DP

```python
from array import array
import sys


MODULUS = 1_000_000_007


def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    vertex_count, edge_count = data[0:2]
    internal_count = vertex_count - 1
    multiplicity = [[0] * vertex_count for _ in range(vertex_count)]
    offset = 2
    for _ in range(edge_count):
        start, end = data[offset] - 1, data[offset + 1] - 1
        offset += 2
        if start != end:
            multiplicity[start][end] += 1

    incoming: list[list[tuple[int, int]]] = [[] for _ in range(internal_count)]
    for end in range(1, internal_count):
        incoming[end] = [
            (start, multiplicity[start][end])
            for start in range(internal_count)
            if multiplicity[start][end]
        ]

    mask_count = 1 << internal_count
    ways = array("I", [0]) * (mask_count * internal_count)
    ways[internal_count] = 1

    for mask in range(1, mask_count, 2):
        base_index = mask * internal_count
        for end in range(1, internal_count):
            end_bit = 1 << end
            if mask & end_bit == 0:
                continue
            previous_mask = mask ^ end_bit
            previous_base = previous_mask * internal_count
            total = 0
            for previous, count in incoming[end]:
                if previous_mask & (1 << previous):
                    total += ways[previous_base + previous] * count
            ways[base_index + end] = total % MODULUS

    full_mask = mask_count - 1
    full_base = full_mask * internal_count
    answer = (
        sum(
            ways[full_base + previous] * multiplicity[previous][vertex_count - 1]
            for previous in range(internal_count)
        )
        % MODULUS
    )
    print(answer)


if __name__ == "__main__":
    solve()
```

The recurrence removes the final internal city from the mask, so every state
counts each city exactly once. A packed unsigned-integer array avoids Python
object overhead while every stored residue remains below `2^32`.

**Complexity:** `O(2^n (n + m))` worst-case recurrence work and `O(n 2^n)`
packed memory.

