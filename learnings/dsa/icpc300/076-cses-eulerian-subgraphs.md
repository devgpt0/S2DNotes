# ICPC300 076: CSES - Eulerian Subgraphs

**Source:** [CSES - Eulerian Subgraphs](https://cses.fi/problemset/task/2078/)  
**Pattern:** cycle-space dimension over GF(2)

## Exact contract

Input gives an undirected graph with `1 <= n <= 100000` vertices and
`0 <= m <= 200000` edges. Count edge subsets in which every vertex has even
degree. Output the count modulo `1_000_000_007`. The empty edge subset counts.

## First principles

Choosing edges is a binary vector. Every vertex contributes one parity equation
over GF(2). In a connected component with `v` vertices, exactly `v-1` incidence
equations are independent. With `e` edges, that component therefore has
`e-v+1` free choices.

Across `c` connected components, the total cycle-space dimension is
`m-n+c`, so the answer is `2^(m-n+c)`.

## Cases that decide correctness

- Isolated vertices count as connected components and add no constraint rank.
- A forest has dimension zero and only the empty Eulerian subgraph.
- Each independent cycle doubles the answer.
- Component counting includes every vertex, not only endpoints appearing in
  an edge.

## Brute force: test all edge subsets

```python
def count_eulerian_subgraphs_brute(
    vertex_count: int,
    edges: list[tuple[int, int]],
) -> int:
    answer = 0
    for mask in range(1 << len(edges)):
        parity = [0] * vertex_count
        for edge_id, (left, right) in enumerate(edges):
            if mask & (1 << edge_id):
                parity[left] ^= 1
                parity[right] ^= 1
        answer += not any(parity)
    return answer
```

**Complexity:** `O(2^m(n+m))` time and `O(n)` space.

## Better for small graphs: Gaussian elimination over GF(2)

```python
def count_eulerian_subgraphs_gaussian(
    vertex_count: int,
    edges: list[tuple[int, int]],
) -> int:
    equations = [0] * vertex_count
    for edge_id, (left, right) in enumerate(edges):
        equations[left] ^= 1 << edge_id
        equations[right] ^= 1 << edge_id

    rank = 0
    for column in range(len(edges)):
        pivot = next(
            (
                row
                for row in range(rank, vertex_count)
                if equations[row] & (1 << column)
            ),
            None,
        )
        if pivot is None:
            continue
        equations[rank], equations[pivot] = equations[pivot], equations[rank]
        for row in range(vertex_count):
            if row != rank and equations[row] & (1 << column):
                equations[row] ^= equations[rank]
        rank += 1
    return pow(2, len(edges) - rank, 1_000_000_007)
```

This derives the nullity directly but can take cubic bit-matrix work.

## Expert solution: DSU component count

```python
import sys


MODULUS = 1_000_000_007


class DisjointSet:
    def __init__(self, size: int) -> None:
        self.parent = list(range(size))
        self.component_size = [1] * size
        self.components = size

    def find(self, vertex: int) -> int:
        while vertex != self.parent[vertex]:
            self.parent[vertex] = self.parent[self.parent[vertex]]
            vertex = self.parent[vertex]
        return vertex

    def union(self, left: int, right: int) -> None:
        left_root = self.find(left)
        right_root = self.find(right)
        if left_root == right_root:
            return
        if self.component_size[left_root] < self.component_size[right_root]:
            left_root, right_root = right_root, left_root
        self.parent[right_root] = left_root
        self.component_size[left_root] += self.component_size[right_root]
        self.components -= 1


def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    vertex_count, edge_count = data[0:2]
    disjoint_set = DisjointSet(vertex_count)
    offset = 2
    for _ in range(edge_count):
        left, right = data[offset] - 1, data[offset + 1] - 1
        offset += 2
        disjoint_set.union(left, right)

    dimension = edge_count - vertex_count + disjoint_set.components
    print(pow(2, dimension, MODULUS))


if __name__ == "__main__":
    solve()
```

DSU supplies `c`. The incidence rank identity then gives the exact number of
free binary edge choices without constructing any parity matrix.

**Complexity:** `O((n+m) alpha(n))` time and `O(n)` space.

