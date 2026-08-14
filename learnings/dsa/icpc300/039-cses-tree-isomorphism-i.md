# ICPC300 039: CSES - Tree Isomorphism I

**Source:** [CSES - Tree Isomorphism I](https://cses.fi/problemset/task/1700/)  
**Pattern:** rooted AHU canonical forms

## Exact contract

Input gives `t` test cases. Each test gives `n`, then the `n - 1` edges of a
first tree and the `n - 1` edges of a second tree. Both trees are rooted at
vertex `1`. For each test, output `YES` if a bijection exists that maps root to
root and preserves every edge; otherwise output `NO`. Across tests, the total
number of vertices is at most `100000`.

## First principles

A rooted tree is determined recursively by the multiset of its rooted child
subtrees. Leaves all have the same empty signature. An internal vertex's
signature is the sorted tuple of its children's signature ids.

Intern each distinct tuple as one integer. Two roots receive the same integer
exactly when their entire rooted trees are isomorphic. The two trees must share
the same interning table; independently assigned integers are not comparable.

## Cases that decide correctness

- Vertex labels have no meaning except that vertex `1` is the root.
- Child order is irrelevant, so child identifiers must be sorted.
- A one-vertex tree has the empty child tuple in both inputs.
- Repeated identical child subtrees remain repeated entries in the tuple.
- Build parent/order arrays iteratively to avoid recursion failure on a chain.

## Brute force: test every root-fixing bijection

```python
from itertools import permutations


def rooted_trees_isomorphic_brute(
    vertex_count: int,
    first_edges: list[tuple[int, int]],
    second_edges: list[tuple[int, int]],
) -> bool:
    second_edge_set = {frozenset(edge) for edge in second_edges}
    for tail_permutation in permutations(range(1, vertex_count)):
        mapping = (0, *tail_permutation)
        if all(
            frozenset((mapping[left], mapping[right])) in second_edge_set
            for left, right in first_edges
        ):
            return True
    return False
```

**Complexity:** `O((n-1)! n)` time and `O(n)` space.

## Better: explicit parenthesized canonical strings

```python
def rooted_tree_code(graph: list[list[int]], root: int = 0) -> str:
    def encode(node: int, parent: int) -> str:
        child_codes = [encode(child, node) for child in graph[node] if child != parent]
        child_codes.sort()
        return "(" + "".join(child_codes) + ")"

    return encode(root, -1)
```

This is the classic AHU proof in executable form. On a chain, repeatedly
building nested strings can copy `O(n^2)` characters and recursion can be too
deep.

## Expert solution: iterative integer interning

```python
import sys


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
        first_id = rooted_identifier(first_tree, 0, identifiers)
        second_id = rooted_identifier(second_tree, 0, identifiers)
        answers.append("YES" if first_id == second_id else "NO")

    print("\n".join(answers))


if __name__ == "__main__":
    solve()
```

Bottom-up induction proves equal identifiers exactly at isomorphic rooted
subtrees: leaves share the empty tuple, and parents match exactly when their
sorted multisets of already-correct child identifiers match.

**Complexity:** `O(n log n)` worst-case time from sorting child identifiers and
`O(n)` space per test; total `n` is the sum across both input trees.

