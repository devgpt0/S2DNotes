# ICPC300 272: Codeforces 1039C - Network Safety

**Source:** [Codeforces 1039C](https://codeforces.com/problemset/problem/1039/C)  
**Difficulty:** 2500  
**Pattern:** group edges by endpoint XOR and rebuild sparse DSUs

## Exact contract

Each graph vertex has a `k`-bit label. For every mask `x`, keep only edges
whose endpoint labels have XOR `x`. If that graph has `c_x` connected
components, contribute `2^c_x`. Return the sum over all `2^k` masks modulo
`1_000_000_007`.

## First principles

An edge belongs to exactly one mask: `label[u] XOR label[v]`. Most masks have
no edges and therefore have `n` singleton components.

For a mask that occurs, start with `n` components and decrement once for every
successful DSU union among its edges. Only incident vertices need explicit DSU
entries; all others remain isolated.

## Cases that decide correctness

- Masks with no edges dominate when `k` is large.
- Repeated or cycle edges do not reduce the component count twice.
- A vertex isolated for one mask may be incident for another.
- Each mask needs fresh DSU state.
- The number of masks is `2^k`, while powers in the answer are modulo the prime.

## Brute force: rebuild the graph for every mask

```python
MODULUS = 1_000_000_007


def network_safety_brute(
    labels: list[int],
    edges: list[tuple[int, int]],
    bit_count: int,
) -> int:
    answer = 0
    for mask in range(1 << bit_count):
        parent = list(range(len(labels)))

        def find(vertex: int) -> int:
            while vertex != parent[vertex]:
                vertex = parent[vertex]
            return vertex

        components = len(labels)
        for first, second in edges:
            if labels[first] ^ labels[second] != mask:
                continue
            first_root = find(first)
            second_root = find(second)
            if first_root != second_root:
                parent[second_root] = first_root
                components -= 1
        answer += pow(2, components, MODULUS)
    return answer % MODULUS
```

This takes `O(2^k(n+m))` time.

## Better insight: only XOR values present on edges need work

Group every edge once. Every missing group has the same contribution `2^n`,
so all missing masks are handled by one multiplication.

## Expert solution: one local DSU per present XOR group

```python
from collections import defaultdict
import sys


MODULUS = 1_000_000_007


def solve() -> None:
    input_stream = sys.stdin.buffer
    vertex_count, edge_count, bit_count = map(int, input_stream.readline().split())
    labels = list(map(int, input_stream.readline().split()))
    groups: dict[int, list[tuple[int, int]]] = defaultdict(list)
    for _ in range(edge_count):
        first, second = map(int, input_stream.readline().split())
        first -= 1
        second -= 1
        groups[labels[first] ^ labels[second]].append((first, second))

    empty_contribution = pow(2, vertex_count, MODULUS)
    answer = ((1 << bit_count) - len(groups)) * empty_contribution

    for edges in groups.values():
        parent: dict[int, int] = {}
        size: dict[int, int] = {}

        def find(vertex: int) -> int:
            parent.setdefault(vertex, vertex)
            size.setdefault(vertex, 1)
            root = vertex
            while root != parent[root]:
                root = parent[root]
            while vertex != root:
                next_vertex = parent[vertex]
                parent[vertex] = root
                vertex = next_vertex
            return root

        components = vertex_count
        for first, second in edges:
            first_root = find(first)
            second_root = find(second)
            if first_root == second_root:
                continue
            if size[first_root] < size[second_root]:
                first_root, second_root = second_root, first_root
            parent[second_root] = first_root
            size[first_root] += size[second_root]
            components -= 1
        answer += pow(2, components, MODULUS)

    print(answer % MODULUS)


if __name__ == "__main__":
    solve()
```

Every edge is processed in its unique XOR group, while all absent groups are
accounted for exactly once.

**Complexity:** `O(m alpha(n)+2^0)` explicit edge work and `O(m)` space; the
`2^k` masks are counted arithmetically, not iterated.
