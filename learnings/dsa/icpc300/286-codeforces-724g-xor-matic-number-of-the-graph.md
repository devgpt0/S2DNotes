# ICPC300 286: Codeforces 724G - Xor-matic Number of the Graph

**Source:** [Codeforces 724G - Xor-matic Number of the Graph](https://codeforces.com/problemset/problem/724/G)  
**Rating:** 2500  
**Pattern:** component XOR potentials and a linear basis  
**Goal:** For every unordered connected vertex pair, sum all distinct XOR
values achievable along routes between the pair. Return the total modulo
`1_000_000_007`. Vertices are zero-based.

## 1. First principles

Choose an XOR distance `distance[v]` from a component root. Every route XOR
between `u` and `v` is

```text
distance[u] XOR distance[v] XOR cycle_value
```

where `cycle_value` belongs to the linear span of all cycle XORs. For any bit,
that span either never changes the bit or makes it one in exactly half of its
values.

## 2. Cases that decide correctness

- Only pairs inside the same connected component contribute.
- Parallel edges and zero-weight edges are valid.
- A component with no independent cycle has a span containing only zero.
- Variable span bits are balanced across its `2^rank` values.
- Pairs are unordered and use distinct vertices.

## 3. Brute force: enumerate every cycle-span value

```python
MODULO = 1_000_000_007


def xor_matic_sum_brute(vertex_count: int, edges: list[tuple[int, int, int]]) -> int:
    if vertex_count <= 0 or any(
        not 0 <= first < vertex_count or not 0 <= second < vertex_count or weight < 0
        for first, second, weight in edges
    ):
        raise ValueError("invalid graph")

    adjacency: list[list[tuple[int, int]]] = [[] for _ in range(vertex_count)]
    for first, second, weight in edges:
        adjacency[first].append((second, weight))
        adjacency[second].append((first, weight))

    seen = [False] * vertex_count
    distance = [0] * vertex_count
    answer = 0
    for root in range(vertex_count):
        if seen[root]:
            continue
        seen[root] = True
        stack = [root]
        vertices: list[int] = []
        cycles: list[int] = []
        while stack:
            vertex = stack.pop()
            vertices.append(vertex)
            for neighbor, weight in adjacency[vertex]:
                if not seen[neighbor]:
                    seen[neighbor] = True
                    distance[neighbor] = distance[vertex] ^ weight
                    stack.append(neighbor)
                else:
                    cycles.append(distance[vertex] ^ distance[neighbor] ^ weight)

        basis: list[int] = []
        for value in cycles:
            for vector in basis:
                value = min(value, value ^ vector)
            if value:
                basis.append(value)
                basis.sort(reverse=True)
        span = [0]
        for vector in basis:
            span += [value ^ vector for value in span]
        for first_index, first in enumerate(vertices):
            for second in vertices[first_index + 1 :]:
                base = distance[first] ^ distance[second]
                answer += sum(base ^ value for value in span)
    return answer % MODULO
```

**Complexity:** Exponential in the component cycle rank.

## 4. Better transition: count each bit instead of each span value

Insert cycle XORs into a binary linear basis. If any basis vector contains a
bit, the corresponding linear functional is nonzero and exactly half the span
sets that bit. Otherwise, the bit is fixed and depends only on the two vertex
potentials.

## 5. Expert solution: per-component basis and bit contributions

```python
MODULO = 1_000_000_007


def xor_matic_sum(vertex_count: int, edges: list[tuple[int, int, int]]) -> int:
    if vertex_count <= 0 or any(
        not 0 <= first < vertex_count or not 0 <= second < vertex_count or weight < 0
        for first, second, weight in edges
    ):
        raise ValueError("invalid graph")

    maximum_weight = max((weight for _, _, weight in edges), default=0)
    bit_count = max(1, maximum_weight.bit_length())
    adjacency: list[list[tuple[int, int]]] = [[] for _ in range(vertex_count)]
    for first, second, weight in edges:
        adjacency[first].append((second, weight))
        adjacency[second].append((first, weight))

    seen = [False] * vertex_count
    distance = [0] * vertex_count
    answer = 0
    for root in range(vertex_count):
        if seen[root]:
            continue
        basis = [0] * bit_count
        vertices: list[int] = []

        def insert(value: int) -> None:
            for bit in range(bit_count - 1, -1, -1):
                if value >> bit & 1 == 0:
                    continue
                if basis[bit]:
                    value ^= basis[bit]
                else:
                    basis[bit] = value
                    return

        seen[root] = True
        stack = [root]
        while stack:
            vertex = stack.pop()
            vertices.append(vertex)
            for neighbor, weight in adjacency[vertex]:
                if not seen[neighbor]:
                    seen[neighbor] = True
                    distance[neighbor] = distance[vertex] ^ weight
                    stack.append(neighbor)
                else:
                    insert(distance[vertex] ^ distance[neighbor] ^ weight)

        rank = sum(vector != 0 for vector in basis)
        span_size = pow(2, rank, MODULO)
        changing_bits = 0
        for vector in basis:
            changing_bits |= vector
        size = len(vertices)
        pair_count = size * (size - 1) // 2
        for bit in range(bit_count):
            bit_value = (1 << bit) % MODULO
            if changing_bits >> bit & 1:
                contribution = pair_count * pow(2, rank - 1, MODULO)
            else:
                ones = sum(distance[vertex] >> bit & 1 for vertex in vertices)
                contribution = ones * (size - ones) * span_size
            answer = (answer + contribution * bit_value) % MODULO
    return answer
```

### Why the expert code is correct

Root potentials reduce every route XOR to a fixed pair value plus the cycle
span. A nonzero bit projection maps exactly half of a vector space to one; a
zero projection leaves the pair's potential bit unchanged for every span
value. The two formulas count those cases for every unordered pair, and
components are independent.

**Complexity:** `O((n + m) B + nB)` time and `O(n + m + B)` auxiliary space,
where `B` is the weight bit length.

## 6. What to remember

```text
route XORs -> one root potential plus cycle combinations
cycle combinations -> binary linear basis
sum all values -> count each bit as fixed or balanced
```
