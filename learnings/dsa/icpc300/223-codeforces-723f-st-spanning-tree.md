# ICPC300 223: Codeforces 723F - st-Spanning Tree

**Source:** [Codeforces 723F - st-Spanning Tree](https://codeforces.com/problemset/problem/723/F)  
**Rating:** 2300  
**Pattern:** DSU component forest with constrained special attachments  
**Goal:** Build a spanning tree whose degrees at special vertices `s` and `t`
do not exceed their limits, or return `None`.

## 1. First principles

Remove `s` and `t`. Connect every remaining component internally with a forest.
Each component must then attach through an edge to `s`, to `t`, or to either.

Components with only one option consume that degree limit immediately. To
connect the `s` and `t` sides, either attach one flexible component to both, or
use the direct edge `(s, t)` when no flexible component exists. Every other
flexible component consumes one remaining slot on either side.

## 2. Cases that decide correctness

- A component adjacent to neither special vertex makes a tree impossible.
- Mandatory one-sided components are assigned before flexible components.
- One flexible component attached to both specials connects the two sides.
- Without a flexible component, a direct `s-t` edge is required.
- Parallel input edges are allowed but a tree uses at most one useful copy.

## 3. Brute force: enumerate every edge subset of tree size

```python
from itertools import combinations


def constrained_spanning_tree_brute(
    vertex_count: int,
    edges: list[tuple[int, int]],
    source: int,
    target: int,
    source_limit: int,
    target_limit: int,
) -> list[tuple[int, int]] | None:
    if (
        vertex_count <= 1
        or source == target
        or not 0 <= source < vertex_count
        or not 0 <= target < vertex_count
        or source_limit < 0
        or target_limit < 0
    ):
        raise ValueError("invalid vertices or limits")
    for first, second in edges:
        if (
            not 0 <= first < vertex_count
            or not 0 <= second < vertex_count
            or first == second
        ):
            raise ValueError("invalid edge")

    for chosen_indices in combinations(range(len(edges)), vertex_count - 1):
        parent = list(range(vertex_count))

        def find(node: int) -> int:
            while parent[node] != node:
                node = parent[node]
            return node

        chosen: list[tuple[int, int]] = []
        source_degree = 0
        target_degree = 0
        valid = True
        for edge_index in chosen_indices:
            first, second = edges[edge_index]
            first_root = find(first)
            second_root = find(second)
            if first_root == second_root:
                valid = False
                break
            parent[second_root] = first_root
            chosen.append((first, second))
            source_degree += first == source or second == source
            target_degree += first == target or second == target
        if (
            valid
            and source_degree <= source_limit
            and target_degree <= target_limit
            and all(find(vertex) == find(0) for vertex in range(vertex_count))
        ):
            return chosen
    return None
```

**Complexity:** `O(C(E,V-1) * V)` time and `O(V)` space.

## 4. Better transition: collapse the unrestricted vertices

Inside components that exclude the two constrained vertices, any spanning
forest is safe. After DSU contraction, the only remaining decisions are which
special vertex attaches each component and how the two special sides connect.

## 5. Expert solution: component attachment greedy

```python
def constrained_spanning_tree(
    vertex_count: int,
    edges: list[tuple[int, int]],
    source: int,
    target: int,
    source_limit: int,
    target_limit: int,
) -> list[tuple[int, int]] | None:
    if (
        vertex_count <= 1
        or source == target
        or not 0 <= source < vertex_count
        or not 0 <= target < vertex_count
        or source_limit < 0
        or target_limit < 0
    ):
        raise ValueError("invalid vertices or limits")
    for first, second in edges:
        if (
            not 0 <= first < vertex_count
            or not 0 <= second < vertex_count
            or first == second
        ):
            raise ValueError("invalid edge")

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

    answer: list[tuple[int, int]] = []
    for first, second in edges:
        if source in (first, second) or target in (first, second):
            continue
        if union(first, second):
            answer.append((first, second))

    components = {
        find(vertex) for vertex in range(vertex_count) if vertex not in (source, target)
    }
    source_edge: dict[int, tuple[int, int]] = {}
    target_edge: dict[int, tuple[int, int]] = {}
    direct_edge: tuple[int, int] | None = None
    for first, second in edges:
        if {first, second} == {source, target}:
            direct_edge = (first, second)
        elif first == source and second not in (source, target):
            source_edge[find(second)] = (first, second)
        elif second == source and first not in (source, target):
            source_edge[find(first)] = (first, second)
        elif first == target and second not in (source, target):
            target_edge[find(second)] = (first, second)
        elif second == target and first not in (source, target):
            target_edge[find(first)] = (first, second)

    remaining_source = source_limit
    remaining_target = target_limit
    flexible: list[int] = []
    for component in sorted(components):
        has_source = component in source_edge
        has_target = component in target_edge
        if not has_source and not has_target:
            return None
        if has_source and has_target:
            flexible.append(component)
        elif has_source:
            answer.append(source_edge[component])
            remaining_source -= 1
        else:
            answer.append(target_edge[component])
            remaining_target -= 1
    if remaining_source < 0 or remaining_target < 0:
        return None

    if flexible:
        bridge = flexible.pop()
        if remaining_source == 0 or remaining_target == 0:
            return None
        answer.append(source_edge[bridge])
        answer.append(target_edge[bridge])
        remaining_source -= 1
        remaining_target -= 1
    else:
        if direct_edge is None or remaining_source == 0 or remaining_target == 0:
            return None
        answer.append(direct_edge)
        remaining_source -= 1
        remaining_target -= 1

    for component in flexible:
        if remaining_source > 0:
            answer.append(source_edge[component])
            remaining_source -= 1
        elif remaining_target > 0:
            answer.append(target_edge[component])
            remaining_target -= 1
        else:
            return None
    if len(answer) != vertex_count - 1:
        raise RuntimeError("constructed edge count is not a tree")
    return answer
```

### Why the expert code is correct

The DSU forest connects each non-special component with no special degree cost.
Every component then needs exactly one attachment, except one flexible bridge
component needs two to connect `s` and `t`; without such a component the direct
edge supplies that connection. Mandatory choices are unavoidable, and all
remaining components are interchangeable between available limits, so the
greedy succeeds exactly when a feasible tree exists.

**Complexity:** `O((V+E) alpha(V))` time and `O(V+E)` space.

## 6. What to remember

```text
remove constrained vertices -> ordinary DSU components
one-sided component -> mandatory degree use
connect s and t -> one flexible component twice, or direct edge
```
