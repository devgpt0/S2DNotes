# ICPC300 219: Codeforces 1354E - Graph Coloring

**Source:** [Codeforces 1354E](https://codeforces.com/problemset/problem/1354/E)  
**Pattern:** bipartite components with exact-size subset DP

## Exact contract

Assign labels `1`, `2`, and `3` to exactly `n1`, `n2`, and `n3` vertices.
Every graph edge must join labels whose absolute difference is exactly one.
Print `NO` if impossible; otherwise print `YES` and one label string.

## First principles

Every valid graph is bipartite: label `2` occupies one bipartition side of each
connected component, while the other side receives labels `1` and `3`. For
each component choose which side contributes to the exact total `n2` using
subset DP.

After those choices, vertices outside label `2` form an independent set inside
each component. Any `n1` of them may be labeled `1`; the rest become `3`.

## Cases that decide correctness

- An odd cycle makes every assignment impossible.
- Isolated vertices form components with side sizes one and zero.
- The chosen side sizes must total exactly `n2`.
- Counts `n1+n2+n3` equal the vertex count.
- Labels `1` and `3` may be assigned arbitrarily only after fixing label `2`.

## Brute force: enumerate all labelings

```python
from itertools import product


def graph_coloring_brute(
    vertex_count: int,
    edges: list[tuple[int, int]],
    required: tuple[int, int, int],
) -> str | None:
    for labels in product((1, 2, 3), repeat=vertex_count):
        if tuple(labels.count(value) for value in (1, 2, 3)) != required:
            continue
        if all(abs(labels[first] - labels[second]) == 1 for first, second in edges):
            return "".join(map(str, labels))
    return None
```

This is exponential in the vertex count.

## Better insight: only the middle label needs component DP

Every edge must touch label `2`, so each connected component offers exactly
two choices: its left or right bipartition side.

## Expert solution: reconstruct bipartition choices

```python
import sys
from collections import deque


def solve() -> None:
    input_stream = sys.stdin.buffer
    vertex_count, edge_count = map(int, input_stream.readline().split())
    first_required, second_required, third_required = map(
        int, input_stream.readline().split()
    )
    graph = [[] for _ in range(vertex_count)]
    for _ in range(edge_count):
        first, second = map(int, input_stream.readline().split())
        first -= 1
        second -= 1
        graph[first].append(second)
        graph[second].append(first)

    color = [-1] * vertex_count
    components: list[tuple[list[int], list[int]]] = []
    for start in range(vertex_count):
        if color[start] != -1:
            continue
        sides = ([], [])
        color[start] = 0
        queue = deque([start])
        while queue:
            vertex = queue.popleft()
            sides[color[vertex]].append(vertex)
            for neighbor in graph[vertex]:
                if color[neighbor] == -1:
                    color[neighbor] = color[vertex] ^ 1
                    queue.append(neighbor)
                elif color[neighbor] == color[vertex]:
                    print("NO")
                    return
        components.append(sides)

    reachable = bytearray(second_required + 1)
    reachable[0] = 1
    choices: list[bytearray] = []
    for first_side, second_side in components:
        next_reachable = bytearray(second_required + 1)
        choice = bytearray(second_required + 1)
        for current_sum, possible in enumerate(reachable):
            if not possible:
                continue
            first_sum = current_sum + len(first_side)
            if first_sum <= second_required and not next_reachable[first_sum]:
                next_reachable[first_sum] = 1
                choice[first_sum] = 1
            second_sum = current_sum + len(second_side)
            if second_sum <= second_required and not next_reachable[second_sum]:
                next_reachable[second_sum] = 1
                choice[second_sum] = 2
        reachable = next_reachable
        choices.append(choice)

    if not reachable[second_required]:
        print("NO")
        return

    labels = [0] * vertex_count
    current_sum = second_required
    for component_index in range(len(components) - 1, -1, -1):
        selected_side = choices[component_index][current_sum] - 1
        for vertex in components[component_index][selected_side]:
            labels[vertex] = 2
        current_sum -= len(components[component_index][selected_side])

    remaining = [vertex for vertex, label in enumerate(labels) if label == 0]
    for vertex in remaining[:first_required]:
        labels[vertex] = 1
    for vertex in remaining[first_required:]:
        labels[vertex] = 3
    if labels.count(3) != third_required:
        raise RuntimeError("input label counts are inconsistent")
    print("YES")
    print("".join(map(str, labels)))


if __name__ == "__main__":
    solve()
```

The DP chooses one whole bipartition side per component for label `2`; all
remaining edges then connect that side to vertices labeled `1` or `3`.

**Complexity:** `O(n+m+c*n2)` time and `O(c*n2+n+m)` space for `c` components.
