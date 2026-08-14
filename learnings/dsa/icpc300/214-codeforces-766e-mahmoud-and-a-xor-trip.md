# ICPC300 214: Codeforces 766E - Mahmoud and a xor trip

**Source:** [Codeforces 766E](https://codeforces.com/problemset/problem/766/E)  
**Pattern:** per-bit parity DP on tree paths

## Exact contract

Each tree vertex has a nonnegative value. For every unordered vertex pair,
including a vertex paired with itself, take the XOR of all values on their
inclusive path. Output the sum of these path XORs.

## First principles

Handle each bit independently. At vertex `v`, maintain counts of subtree
endpoints whose path XOR from `v` has parity zero or one for this bit.

When merging a child, pairs crossing into already merged endpoints have LCA
`v`. Their path parity is
`parity(v..x) xor parity(v..y) xor bit(value[v])`, because `v` was included in
both rootward parities but belongs once on the final path.

## Cases that decide correctness

- Single-vertex paths contribute the vertex value.
- Paths and endpoint pairs are unordered.
- The LCA value must not be canceled twice.
- A set bit at the parent complements every child endpoint parity.
- Wide integers are required for the total sum.

## Brute force: recover every tree path

```python
from collections import deque


def xor_trip_brute(values: list[int], edges: list[tuple[int, int]]) -> int:
    size = len(values)
    graph = [[] for _ in range(size)]
    for first, second in edges:
        graph[first].append(second)
        graph[second].append(first)
    answer = 0
    for source in range(size):
        parent = [-1] * size
        path_xor = [0] * size
        parent[source] = source
        path_xor[source] = values[source]
        queue = deque([source])
        while queue:
            vertex = queue.popleft()
            for neighbor in graph[vertex]:
                if parent[neighbor] == -1:
                    parent[neighbor] = vertex
                    path_xor[neighbor] = path_xor[vertex] ^ values[neighbor]
                    queue.append(neighbor)
        answer += sum(path_xor[target] for target in range(source, size))
    return answer
```

This performs a traversal from every endpoint.

## Better insight: count odd parities instead of XOR values

For one bit, only whether a path contains an odd number of set vertices
matters. Tree DP counts all such pairs at their unique LCA.

## Expert solution: merge zero/one endpoint counts

```python
import sys


def solve() -> None:
    input_stream = sys.stdin.buffer
    size = int(input_stream.readline())
    values = list(map(int, input_stream.readline().split()))
    graph = [[] for _ in range(size)]
    for _ in range(size - 1):
        first, second = map(int, input_stream.readline().split())
        first -= 1
        second -= 1
        graph[first].append(second)
        graph[second].append(first)

    parent = [-1] * size
    parent[0] = 0
    children = [[] for _ in range(size)]
    order = [0]
    for vertex in order:
        for neighbor in graph[vertex]:
            if parent[neighbor] == -1:
                parent[neighbor] = vertex
                children[vertex].append(neighbor)
                order.append(neighbor)

    answer = 0
    bit_count = max(1, max(values).bit_length())
    for bit in range(bit_count):
        zero_count = [0] * size
        one_count = [0] * size
        odd_paths = 0
        for vertex in reversed(order):
            vertex_bit = values[vertex] >> bit & 1
            accumulated_zero = int(vertex_bit == 0)
            accumulated_one = int(vertex_bit == 1)
            odd_paths += vertex_bit
            for child in children[vertex]:
                child_one = one_count[child]
                child_zero = zero_count[child]
                if vertex_bit:
                    child_zero, child_one = child_one, child_zero
                    odd_paths += (
                        accumulated_zero * child_zero + accumulated_one * child_one
                    )
                else:
                    odd_paths += (
                        accumulated_zero * child_one + accumulated_one * child_zero
                    )
                accumulated_zero += child_zero
                accumulated_one += child_one
            zero_count[vertex] = accumulated_zero
            one_count[vertex] = accumulated_one
        answer += odd_paths << bit
    print(answer)


if __name__ == "__main__":
    solve()
```

Every nontrivial pair is counted exactly when its child groups meet at the LCA;
singletons are added separately.

**Complexity:** `O(nB)` time and `O(n)` space for `B` value bits.
