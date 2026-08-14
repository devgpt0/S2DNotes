# ICPC300 040: CSES - Tree Isomorphism II

**Source:** [CSES - Tree Isomorphism II](https://cses.fi/problemset/task/1701/)  
**Pattern:** tree centroids plus rooted AHU canonical forms

## Exact contract

Input gives `t` test cases. Each test gives `n`, then two unrooted trees with
`n - 1` edges each. For every test, output `YES` if some vertex bijection
preserves adjacency, otherwise `NO`. Across tests, the total number of vertices
is at most `100000`.

## First principles

Every tree has one centroid or two adjacent centroids. An isomorphism must map
the centroid set of one tree to the centroid set of the other because removing
a centroid is characterized by leaving no component larger than `n/2`.

Root each tree at each of its at most two centroids. The unrooted trees are
isomorphic exactly when one rooted canonical identifier from the first tree
equals one from the second. Rooted identifiers use sorted child-subtree
multisets, as in Tree Isomorphism I.

## Cases that decide correctness

- A one-vertex tree has one centroid and no edges.
- An even-length path has two centroids; both possible root mappings must be
  considered.
- Labels and adjacency-list order are irrelevant.
- Both trees must use the same signature interning table.
- Centroid peeling stops when one or two vertices remain.

## Brute force: test all vertex bijections

```python
from itertools import permutations


def trees_isomorphic_brute(
    vertex_count: int,
    first_edges: list[tuple[int, int]],
    second_edges: list[tuple[int, int]],
) -> bool:
    second_edge_set = {frozenset(edge) for edge in second_edges}
    for mapping in permutations(range(vertex_count)):
        if all(
            frozenset((mapping[left], mapping[right])) in second_edge_set
            for left, right in first_edges
        ):
            return True
    return False
```

**Complexity:** `O(n! n)` time and `O(n)` space.

## Better: centroid roots with parenthesized codes

```python
def tree_centroids(graph: list[list[int]]) -> list[int]:
    if len(graph) <= 2:
        return list(range(len(graph)))
    degree = [len(neighbors) for neighbors in graph]
    leaves = [vertex for vertex, value in enumerate(degree) if value <= 1]
    remaining = len(graph)
    while remaining > 2:
        remaining -= len(leaves)
        next_leaves = []
        for leaf in leaves:
            for neighbor in graph[leaf]:
                degree[neighbor] -= 1
                if degree[neighbor] == 1:
                    next_leaves.append(neighbor)
        leaves = next_leaves
    return leaves


def unrooted_tree_codes(graph: list[list[int]]) -> set[str]:
    def encode(node: int, parent: int) -> str:
        children = sorted(
            encode(neighbor, node) for neighbor in graph[node] if neighbor != parent
        )
        return "(" + "".join(children) + ")"

    return {encode(centroid, -1) for centroid in tree_centroids(graph)}
```

Comparing the two code sets is correct and convenient for moderate trees, but
recursive nested strings can require quadratic copying on a chain.

## Expert solution: centroid-rooted integer signatures

```python
import sys


def find_centroids(graph: list[list[int]]) -> list[int]:
    vertex_count = len(graph)
    if vertex_count <= 2:
        return list(range(vertex_count))
    degree = [len(neighbors) for neighbors in graph]
    leaves = [vertex for vertex, value in enumerate(degree) if value <= 1]
    remaining = vertex_count

    while remaining > 2:
        remaining -= len(leaves)
        next_leaves = []
        for leaf in leaves:
            for neighbor in graph[leaf]:
                degree[neighbor] -= 1
                if degree[neighbor] == 1:
                    next_leaves.append(neighbor)
        leaves = next_leaves
    return leaves


def rooted_identifier(
    graph: list[list[int]],
    root: int,
    identifiers: dict[tuple[int, ...], int],
) -> int:
    parent = [-1] * len(graph)
    order = [root]
    for node in order:
        for neighbor in graph[node]:
            if neighbor != parent[node]:
                parent[neighbor] = node
                order.append(neighbor)

    node_identifier = [0] * len(graph)
    for node in reversed(order):
        signature = tuple(
            sorted(
                node_identifier[neighbor]
                for neighbor in graph[node]
                if neighbor != parent[node]
            )
        )
        identifier = identifiers.get(signature)
        if identifier is None:
            identifier = len(identifiers) + 1
            identifiers[signature] = identifier
        node_identifier[node] = identifier
    return node_identifier[root]


def read_tree(
    data: list[int], offset: int, vertex_count: int
) -> tuple[list[list[int]], int]:
    graph = [[] for _ in range(vertex_count)]
    for _ in range(vertex_count - 1):
        left, right = data[offset] - 1, data[offset + 1] - 1
        offset += 2
        graph[left].append(right)
        graph[right].append(left)
    return graph, offset


def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    test_count = data[0]
    offset = 1
    answers = []

    for _ in range(test_count):
        vertex_count = data[offset]
        offset += 1
        first_tree, offset = read_tree(data, offset, vertex_count)
        second_tree, offset = read_tree(data, offset, vertex_count)
        identifiers: dict[tuple[int, ...], int] = {}
        first_ids = {
            rooted_identifier(first_tree, root, identifiers)
            for root in find_centroids(first_tree)
        }
        second_ids = {
            rooted_identifier(second_tree, root, identifiers)
            for root in find_centroids(second_tree)
        }
        answers.append("YES" if first_ids & second_ids else "NO")

    print("\n".join(answers))


if __name__ == "__main__":
    solve()
```

Centroids are invariant under isomorphism. For every possible invariant root,
the shared integer signatures are exact rooted canonical forms, so a common id
is both necessary and sufficient for unrooted isomorphism.

**Complexity:** `O(n log n)` worst-case time and `O(n)` space per test.

