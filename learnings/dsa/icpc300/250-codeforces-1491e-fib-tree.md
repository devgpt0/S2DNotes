# ICPC300 250: Codeforces 1491E - Fib-tree

**Source:** [Codeforces 1491E](https://codeforces.com/problemset/problem/1491/E)  
**Difficulty:** 2500  
**Pattern:** recursive Fibonacci separators in a tree

## Exact contract

A one-vertex tree is a Fibonacci tree. A larger tree of Fibonacci size is a
Fibonacci tree when one edge can be removed so that its two components are
Fibonacci trees of the two preceding sizes. Given a tree, print whether it has
this recursive decomposition.

## First principles

If the current component has size `F[k]`, its next cut must create sizes
`F[k-1]` and `F[k-2]`. Root the component anywhere. Removing the parent edge
of a vertex isolates exactly its subtree, so a valid cut must appear as a
subtree of one target size.

Find such a subtree, mark its parent edge removed, and recurse on both sides.
No other sizes can satisfy the definition.

## Cases that decide correctness

- A non-Fibonacci total size is rejected immediately.
- Both `F[0]` and `F[1]` equal one; either is a base component.
- Removed edges must stay absent in every descendant recursion.
- The two recursive calls use different preceding Fibonacci indices.
- Iterative component traversal avoids recursion depth proportional to `n`.

## Brute force: try every possible recursive cut

```python
def fib_tree_brute(vertex_count: int, edges: list[tuple[int, int]]) -> bool:
    fibonacci = [1, 1]
    while fibonacci[-1] < vertex_count:
        fibonacci.append(fibonacci[-1] + fibonacci[-2])
    if fibonacci[-1] != vertex_count:
        return False
    size_index = {value: index for index, value in enumerate(fibonacci)}

    graph: list[list[tuple[int, int]]] = [[] for _ in range(vertex_count)]
    for edge_index, (first, second) in enumerate(edges):
        graph[first].append((second, edge_index))
        graph[second].append((first, edge_index))

    def decompose(vertices: frozenset[int]) -> bool:
        if len(vertices) == 1:
            return True
        index = size_index[len(vertices)]
        target_sizes = {fibonacci[index - 1], fibonacci[index - 2]}
        for blocked_edge, (first, second) in enumerate(edges):
            if first not in vertices or second not in vertices:
                continue
            first_side = {first}
            stack = [first]
            while stack:
                vertex = stack.pop()
                for neighbor, edge_index in graph[vertex]:
                    if (
                        edge_index != blocked_edge
                        and neighbor in vertices
                        and neighbor not in first_side
                    ):
                        first_side.add(neighbor)
                        stack.append(neighbor)
            if len(first_side) not in target_sizes:
                continue
            second_side = vertices.difference(first_side)
            if len(second_side) not in target_sizes:
                continue
            if decompose(frozenset(first_side)) and decompose(frozenset(second_side)):
                return True
        return False

    return decompose(frozenset(range(vertex_count)))
```

This is exponential and is useful only for tiny trees.

## Better insight: a required cut is visible as a rooted subtree

One component traversal computes every subtree size. The Fibonacci definition
restricts the cut to two target sizes, so no edge of any other size needs
consideration.

## Expert solution: find and remove one Fibonacci separator per component

```python
import sys


def solve() -> None:
    input_stream = sys.stdin.buffer
    vertex_count = int(input_stream.readline())
    graph: list[list[tuple[int, int]]] = [[] for _ in range(vertex_count)]
    for edge_index in range(vertex_count - 1):
        first, second = map(int, input_stream.readline().split())
        first -= 1
        second -= 1
        graph[first].append((second, edge_index))
        graph[second].append((first, edge_index))

    fibonacci = [1, 1]
    while fibonacci[-1] < vertex_count:
        fibonacci.append(fibonacci[-1] + fibonacci[-2])
    if fibonacci[-1] != vertex_count:
        print("NO")
        return

    removed = [False] * (vertex_count - 1)

    def decompose(start: int, index: int) -> bool:
        if index <= 1:
            return True

        parent = [-2] * vertex_count
        parent_edge = [-1] * vertex_count
        parent[start] = -1
        order = [start]
        for vertex in order:
            for neighbor, edge_index in graph[vertex]:
                if removed[edge_index] or neighbor == parent[vertex]:
                    continue
                parent[neighbor] = vertex
                parent_edge[neighbor] = edge_index
                order.append(neighbor)

        subtree_size = [1] * vertex_count
        separator = -1
        first_target = fibonacci[index - 1]
        second_target = fibonacci[index - 2]
        for vertex in reversed(order[1:]):
            size = subtree_size[vertex]
            if separator == -1 and size in (first_target, second_target):
                separator = vertex
            subtree_size[parent[vertex]] += size
        if separator == -1:
            return False

        separated_size = subtree_size[separator]
        removed[parent_edge[separator]] = True
        if separated_size == first_target:
            return decompose(separator, index - 1) and decompose(start, index - 2)
        return decompose(separator, index - 2) and decompose(start, index - 1)

    print("YES" if decompose(0, len(fibonacci) - 1) else "NO")


if __name__ == "__main__":
    solve()
```

Every accepted cut has the only two sizes allowed by the definition; the two
recursive calls therefore prove the decomposition down to singleton trees.

**Complexity:** `O(n log n)` time and `O(n)` auxiliary space.
