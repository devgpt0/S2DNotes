# ICPC300 154: Codeforces 160D - Edges in MST

**Source:** [Codeforces 160D - Edges in MST](https://codeforces.com/problemset/problem/160/D)  
**Rating:** 2300  
**Pattern:** Kruskal weight groups plus bridges in a contracted multigraph  
**Goal:** Classify every weighted undirected edge as `none`, `at least one`, or
`any` according to whether it belongs to no minimum spanning tree, some but not
all minimum spanning trees, or every minimum spanning tree.

## 1. First principles

Before Kruskal processes weight `w`, DSU components contain exactly the
connections achievable with lighter edges. An edge inside one component is
already redundant and belongs to no MST.

Contract those components and inspect all weight-`w` edges together. Such an
edge is mandatory exactly when it is a bridge of this temporary multigraph;
otherwise equal-weight alternatives can replace it.

## 2. Cases that decide correctness

- All equal-weight edges must be classified before any of them are unioned.
- Parallel temporary edges prevent either copy from being a bridge.
- An edge whose endpoints already share a lighter path is `none`.
- A bridge in a weight group is `any`, not merely `at least one`.
- The source graph must be connected.

## 3. Brute force: enumerate every spanning tree

```python
from itertools import combinations


def classify_mst_edges_brute(
    vertex_count: int, edges: list[tuple[int, int, int]]
) -> list[str]:
    if vertex_count <= 0:
        raise ValueError("vertex_count must be positive")
    for first, second, _ in edges:
        if (
            not 0 <= first < vertex_count
            or not 0 <= second < vertex_count
            or first == second
        ):
            raise ValueError("invalid edge")

    best_weight: int | None = None
    best_masks: list[int] = []
    for chosen in combinations(range(len(edges)), vertex_count - 1):
        parent = list(range(vertex_count))

        def find(node: int) -> int:
            while parent[node] != node:
                node = parent[node]
            return node

        weight = 0
        mask = 0
        valid = True
        for edge_index in chosen:
            first, second, edge_weight = edges[edge_index]
            first_root = find(first)
            second_root = find(second)
            if first_root == second_root:
                valid = False
                break
            parent[second_root] = first_root
            weight += edge_weight
            mask |= 1 << edge_index
        if not valid or any(find(node) != find(0) for node in range(vertex_count)):
            continue
        if best_weight is None or weight < best_weight:
            best_weight = weight
            best_masks = [mask]
        elif weight == best_weight:
            best_masks.append(mask)

    if best_weight is None:
        raise ValueError("graph must be connected")
    answers: list[str] = []
    for edge_index in range(len(edges)):
        occurrences = sum(bool(mask & (1 << edge_index)) for mask in best_masks)
        if occurrences == 0:
            answers.append("none")
        elif occurrences == len(best_masks):
            answers.append("any")
        else:
            answers.append("at least one")
    return answers
```

**Complexity:** `O(C(E,V-1) * V)` time and exponential stored MST masks.

## 4. Better: force and ban each edge

```python
def classify_mst_edges_repeated_kruskal(
    vertex_count: int, edges: list[tuple[int, int, int]]
) -> list[str]:
    if vertex_count <= 0:
        raise ValueError("vertex_count must be positive")
    for first, second, _ in edges:
        if (
            not 0 <= first < vertex_count
            or not 0 <= second < vertex_count
            or first == second
        ):
            raise ValueError("invalid edge")
    order = sorted(range(len(edges)), key=lambda index: edges[index][2])

    def mst_weight(forced: int | None, banned: int | None) -> int | None:
        parent = list(range(vertex_count))
        sizes = [1] * vertex_count

        def find(node: int) -> int:
            while parent[node] != node:
                parent[node] = parent[parent[node]]
                node = parent[node]
            return node

        def union(first: int, second: int) -> bool:
            first_root = find(first)
            second_root = find(second)
            if first_root == second_root:
                return False
            if sizes[first_root] < sizes[second_root]:
                first_root, second_root = second_root, first_root
            parent[second_root] = first_root
            sizes[first_root] += sizes[second_root]
            return True

        total = 0
        used = 0
        if forced is not None:
            first, second, weight = edges[forced]
            if not union(first, second):
                return None
            total += weight
            used += 1
        for edge_index in order:
            if edge_index == forced or edge_index == banned:
                continue
            first, second, weight = edges[edge_index]
            if union(first, second):
                total += weight
                used += 1
        return total if used == vertex_count - 1 else None

    baseline = mst_weight(None, None)
    if baseline is None:
        raise ValueError("graph must be connected")
    answers: list[str] = []
    for edge_index in range(len(edges)):
        if mst_weight(edge_index, None) != baseline:
            answers.append("none")
        elif mst_weight(None, edge_index) != baseline:
            answers.append("any")
        else:
            answers.append("at least one")
    return answers
```

**Complexity:** `O(E^2 alpha(V) + E log E)` time and `O(V+E)` space.

## 5. Expert solution: bridges inside Kruskal groups

```python
import sys


def classify_mst_edges_grouped(
    vertex_count: int, edges: list[tuple[int, int, int]]
) -> list[str]:
    if vertex_count <= 0:
        raise ValueError("vertex_count must be positive")
    for first, second, _ in edges:
        if (
            not 0 <= first < vertex_count
            or not 0 <= second < vertex_count
            or first == second
        ):
            raise ValueError("invalid edge")

    sys.setrecursionlimit(max(1_000, 2 * len(edges) + 10))
    parent = list(range(vertex_count))
    sizes = [1] * vertex_count

    def find(node: int) -> int:
        while parent[node] != node:
            parent[node] = parent[parent[node]]
            node = parent[node]
        return node

    def union(first: int, second: int) -> None:
        first_root = find(first)
        second_root = find(second)
        if first_root == second_root:
            return
        if sizes[first_root] < sizes[second_root]:
            first_root, second_root = second_root, first_root
        parent[second_root] = first_root
        sizes[first_root] += sizes[second_root]

    order = sorted(range(len(edges)), key=lambda index: edges[index][2])
    answers = ["none"] * len(edges)
    group_start = 0
    while group_start < len(order):
        group_end = group_start
        weight = edges[order[group_start]][2]
        while group_end < len(order) and edges[order[group_end]][2] == weight:
            group_end += 1

        temporary: dict[int, list[tuple[int, int]]] = {}
        candidates: list[int] = []
        for position in range(group_start, group_end):
            edge_index = order[position]
            first, second, _ = edges[edge_index]
            first_root = find(first)
            second_root = find(second)
            if first_root == second_root:
                continue
            answers[edge_index] = "at least one"
            candidates.append(edge_index)
            temporary.setdefault(first_root, []).append((second_root, edge_index))
            temporary.setdefault(second_root, []).append((first_root, edge_index))

        entered: dict[int, int] = {}
        low: dict[int, int] = {}
        timer = 0

        def find_bridges(node: int, parent_edge: int) -> None:
            nonlocal timer
            entered[node] = timer
            low[node] = timer
            timer += 1
            for neighbor, edge_index in temporary[node]:
                if edge_index == parent_edge:
                    continue
                if neighbor not in entered:
                    find_bridges(neighbor, edge_index)
                    low[node] = min(low[node], low[neighbor])
                    if low[neighbor] > entered[node]:
                        answers[edge_index] = "any"
                else:
                    low[node] = min(low[node], entered[neighbor])

        for node in temporary:
            if node not in entered:
                find_bridges(node, -1)
        for edge_index in candidates:
            first, second, _ = edges[edge_index]
            union(first, second)
        group_start = group_end

    root = find(0)
    if any(find(node) != root for node in range(vertex_count)):
        raise ValueError("graph must be connected")
    return answers
```

### Why the expert code is correct

Kruskal's cut property eliminates edges internal to lighter-weight components.
Among the remaining equal-weight edges, every spanning forest is interchangeable
except for bridges: removing a temporary bridge disconnects a cut that no other
edge of that weight crosses. Thus temporary bridges are in every MST, other
candidates are in some MST, and eliminated edges are in none.

**Complexity:** `O(E log E + E alpha(V))` time and `O(V+E)` space.

## 6. What to remember

```text
lighter edges -> contract with DSU
equal-weight choices -> temporary multigraph
mandatory equal-weight edge -> bridge after contraction
```
