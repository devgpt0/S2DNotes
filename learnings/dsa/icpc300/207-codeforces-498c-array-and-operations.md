# ICPC300 207: Codeforces 498C - Array and Operations

**Source:** [Codeforces 498C - Array and Operations](https://codeforces.com/problemset/problem/498/C)  
**Difficulty:** 2300  
**Pattern:** independent prime-exponent flows on a bipartite index graph

## Exact contract

Array values are positive integers. Every allowed pair joins an odd one-based
index to an even one-based index. One operation chooses an allowed pair and a
prime dividing both current values, then divides both values by that prime.
Return the maximum number of operations.

## First principles

Prime factors never interact, so optimize each prime independently. For one
prime, index `i` owns `exponent_i` divisible units. Send units from odd indices
to even indices through allowed pairs:

- source to odd index capacity = its exponent;
- allowed pair capacity = infinity;
- even index to sink capacity = its exponent.

One unit of flow is exactly one legal division operation.

## Cases that decide correctness

- Repeated exponents create multiple capacity units.
- A pair's input order does not matter; orient it odd-to-even.
- Duplicate allowed pairs do not change the maximum.
- Prime `p` flow cannot consume exponent units of another prime.
- Values equal to one contribute no prime nodes.

## Brute force: recurse over current array states

```python
from functools import cache
from math import gcd


def array_operations_brute(
    values: list[int], allowed_pairs: list[tuple[int, int]]
) -> int:
    if not values or any(type(value) is not int or value < 1 for value in values):
        raise ValueError("values must be positive integers")
    normalized: list[tuple[int, int]] = []
    for first, second in allowed_pairs:
        if (
            type(first) is not int
            or type(second) is not int
            or not 0 <= first < len(values)
            or not 0 <= second < len(values)
            or first == second
            or (first - second) % 2 == 0
        ):
            raise ValueError("pairs must join opposite index parities")
        normalized.append((first, second))

    @cache
    def search(state: tuple[int, ...]) -> int:
        best = 0
        for first, second in normalized:
            common = gcd(state[first], state[second])
            prime = 2
            while prime * prime <= common:
                if common % prime == 0:
                    changed = list(state)
                    changed[first] //= prime
                    changed[second] //= prime
                    best = max(best, 1 + search(tuple(changed)))
                while common % prime == 0:
                    common //= prime
                prime += 1
            if common > 1:
                changed = list(state)
                changed[first] //= common
                changed[second] //= common
                best = max(best, 1 + search(tuple(changed)))
        return best

    return search(tuple(values))
```

The number of exponent-distribution states is exponential.

## Better approach: no separate intermediate

Expanding each prime exponent into individual unit vertices reduces the problem
to bipartite matching, but that is the same capacity network with more nodes.
Capacitated max flow is its direct compact form.

## Expert solution: one Dinic flow per distinct prime

```python
from collections import deque


def maximum_array_operations(
    values: list[int], allowed_pairs: list[tuple[int, int]]
) -> int:
    if not values or any(type(value) is not int or value < 1 for value in values):
        raise ValueError("values must be positive integers")
    normalized: list[tuple[int, int]] = []
    for first, second in allowed_pairs:
        if (
            type(first) is not int
            or type(second) is not int
            or not 0 <= first < len(values)
            or not 0 <= second < len(values)
            or first == second
            or (first - second) % 2 == 0
        ):
            raise ValueError("pairs must join opposite index parities")
        if first % 2 == 1:
            first, second = second, first
        normalized.append((first, second))

    primes: set[int] = set()
    for original in values:
        value = original
        divisor = 2
        while divisor * divisor <= value:
            if value % divisor == 0:
                primes.add(divisor)
                while value % divisor == 0:
                    value //= divisor
            divisor += 1
        if value > 1:
            primes.add(value)

    size = len(values)
    source = size
    sink = size + 1
    answer = 0

    for prime in primes:
        exponents = [0] * size
        for index, original in enumerate(values):
            value = original
            while value % prime == 0:
                exponents[index] += 1
                value //= prime

        graph: list[list[list[int]]] = [[] for _ in range(size + 2)]

        def add_edge(first: int, second: int, capacity: int) -> None:
            forward = [second, len(graph[second]), capacity]
            backward = [first, len(graph[first]), 0]
            graph[first].append(forward)
            graph[second].append(backward)

        total_units = sum(exponents)
        for vertex, exponent in enumerate(exponents):
            if vertex % 2 == 0:
                add_edge(source, vertex, exponent)
            else:
                add_edge(vertex, sink, exponent)
        for first, second in normalized:
            add_edge(first, second, total_units)

        while True:
            level = [-1] * (size + 2)
            level[source] = 0
            queue = deque([source])
            while queue:
                vertex = queue.popleft()
                for neighbor, _, capacity in graph[vertex]:
                    if capacity and level[neighbor] == -1:
                        level[neighbor] = level[vertex] + 1
                        queue.append(neighbor)
            if level[sink] == -1:
                break

            edge_index = [0] * (size + 2)

            def send(vertex: int, flow: int) -> int:
                if vertex == sink:
                    return flow
                while edge_index[vertex] < len(graph[vertex]):
                    index = edge_index[vertex]
                    neighbor, reverse, capacity = graph[vertex][index]
                    if capacity and level[neighbor] == level[vertex] + 1:
                        pushed = send(neighbor, min(flow, capacity))
                        if pushed:
                            graph[vertex][index][2] -= pushed
                            graph[neighbor][reverse][2] += pushed
                            return pushed
                    edge_index[vertex] += 1
                return 0

            while True:
                pushed = send(source, total_units)
                if not pushed:
                    break
                answer += pushed
    return answer
```

Flow conservation pairs one odd exponent unit with one even exponent unit
along an allowed operation edge. Max-flow integrality produces legal discrete
operations, and summing independent prime networks is globally optimal.

**Complexity:** one bipartite max flow per distinct input prime; space is
`O(n+m)` per flow network.
