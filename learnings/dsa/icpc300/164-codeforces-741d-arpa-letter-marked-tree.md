# ICPC300 164: Codeforces 741D - Arpa's letter-marked tree

**Source:** [Codeforces 741D](https://codeforces.com/problemset/problem/741/D)  
**Pattern:** small-to-large parity-mask maps on a tree

## Exact contract

The rooted tree has root `1`. Every edge to vertices `2..n` is given by its
parent and a letter from `a` through `v`. For each vertex `v`, output the
maximum path length in edges among paths lying completely inside `v`'s subtree
whose edge letters can be permuted into a palindrome.

## First principles

Let `mask[x]` be the xor of letter bits on the root-to-`x` path. The parity mask
on a path between `x` and `y` is `mask[x] xor mask[y]`. Its letters can form a
palindrome exactly when this result has zero or one set bit.

Process children bottom-up. A map stores, for every prefix mask in the current
subtree, the greatest node depth. Paths inside one child are already solved.
When merging another child, query equal masks and all 22 one-bit variants in
the accumulated map; these cross paths have the current vertex as LCA. Retain
the largest map so each entry moves only logarithmically often.

## Cases that decide correctness

- A zero-bit xor is valid, as is any xor with exactly one bit.
- Path length is the sum of endpoint depths minus twice their LCA depth.
- The zero-length path at a vertex is always valid.
- Combine different child subtrees only after preserving their internal
  answers.
- Store the maximum depth per mask because deeper endpoints produce longer
  cross paths.

## Brute force: inspect every endpoint pair per subtree

```python
from itertools import combinations_with_replacement


def arpa_tree_brute(
    parents: list[int],
    letters: str,
) -> list[int]:
    vertex_count = len(parents) + 1
    parent = [0] * vertex_count
    depth = [0] * vertex_count
    prefix_mask = [0] * vertex_count
    children = [[] for _ in range(vertex_count)]
    for vertex, (raw_parent, letter) in enumerate(
        zip(parents, letters, strict=True), start=1
    ):
        parent[vertex] = raw_parent - 1
        children[parent[vertex]].append(vertex)
        depth[vertex] = depth[parent[vertex]] + 1
        prefix_mask[vertex] = prefix_mask[parent[vertex]] ^ (
            1 << (ord(letter) - ord("a"))
        )

    subtree_nodes: list[list[int]] = [[] for _ in range(vertex_count)]
    answer = [0] * vertex_count
    for vertex in range(vertex_count - 1, -1, -1):
        subtree_nodes[vertex].append(vertex)
        for child in children[vertex]:
            subtree_nodes[vertex].extend(subtree_nodes[child])
        for first, second in combinations_with_replacement(subtree_nodes[vertex], 2):
            if (prefix_mask[first] ^ prefix_mask[second]).bit_count() > 1:
                continue
            left = first
            right = second
            while depth[left] > depth[right]:
                left = parent[left]
            while depth[right] > depth[left]:
                right = parent[right]
            while left != right:
                left = parent[left]
                right = parent[right]
            length = depth[first] + depth[second] - 2 * depth[left]
            answer[vertex] = max(answer[vertex], length)
    return answer
```

Repeated subtree pair enumeration is cubic on long or highly branching trees.

## Better insight: parity masks replace string permutations

Prefix xor reduces a path check to 23 hash lookups, but rebuilding a mask map
independently for every subtree still repeats entries quadratically. A genuine
asymptotic improvement requires reusing a child's map, which is exactly the
small-to-large expert construction below.

## Expert solution: merge maximum-depth mask maps

```python
import sys


def solve() -> None:
    input_stream = sys.stdin.buffer
    vertex_count = int(input_stream.readline())
    children = [[] for _ in range(vertex_count)]
    depth = [0] * vertex_count
    prefix_mask = [0] * vertex_count
    for vertex in range(1, vertex_count):
        raw_parent, raw_letter = input_stream.readline().split()
        parent = int(raw_parent) - 1
        letter = raw_letter[0]
        children[parent].append(vertex)
        depth[vertex] = depth[parent] + 1
        prefix_mask[vertex] = prefix_mask[parent] ^ (1 << (letter - ord("a")))

    mask_maps: list[dict[int, int] | None] = [None] * vertex_count
    answer = [0] * vertex_count

    for vertex in range(vertex_count - 1, -1, -1):
        heavy_child = max(
            children[vertex],
            key=lambda child: len(mask_maps[child] or {}),
            default=-1,
        )
        best = max((answer[child] for child in children[vertex]), default=0)

        if heavy_child == -1:
            depths_by_mask: dict[int, int] = {}
        else:
            heavy_map = mask_maps[heavy_child]
            if heavy_map is None:
                raise RuntimeError("child mask map was not built")
            depths_by_mask = heavy_map

        vertex_mask = prefix_mask[vertex]
        candidate_depth = depths_by_mask.get(vertex_mask, -(10**9))
        for bit in range(22):
            candidate_depth = max(
                candidate_depth,
                depths_by_mask.get(vertex_mask ^ (1 << bit), -(10**9)),
            )
        best = max(best, candidate_depth - depth[vertex])
        depths_by_mask[vertex_mask] = max(
            depths_by_mask.get(vertex_mask, -1), depth[vertex]
        )

        for child in children[vertex]:
            if child == heavy_child:
                continue
            child_map = mask_maps[child]
            if child_map is None:
                raise RuntimeError("child mask map was not built")
            for mask, endpoint_depth in child_map.items():
                other_depth = depths_by_mask.get(mask, -(10**9))
                for bit in range(22):
                    other_depth = max(
                        other_depth,
                        depths_by_mask.get(mask ^ (1 << bit), -(10**9)),
                    )
                best = max(
                    best,
                    endpoint_depth + other_depth - 2 * depth[vertex],
                )
            for mask, endpoint_depth in child_map.items():
                depths_by_mask[mask] = max(depths_by_mask.get(mask, -1), endpoint_depth)

        answer[vertex] = best
        for child in children[vertex]:
            mask_maps[child] = None
        mask_maps[vertex] = depths_by_mask

    print(" ".join(map(str, answer)))


if __name__ == "__main__":
    solve()
```

Child answers cover paths staying inside one child. Every newly tested pair
uses endpoints from different accumulated parts, hence has LCA at the current
vertex and the computed length is exact.

**Complexity:** `O(22 n log n)` expected time and `O(n)` live map entries.
