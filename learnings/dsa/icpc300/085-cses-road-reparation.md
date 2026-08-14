# ICPC300 085: CSES - Road Reparation

**Source:** [CSES - Road Reparation](https://cses.fi/problemset/task/1675/)  
**Pattern:** minimum spanning tree with disjoint sets  
**Goal:** Connect every city with minimum total road cost, or return `-1` when
the graph is disconnected.

Edges are zero-based `(first, second, cost)` triples.

## 1. First principles

A spanning tree connects `n` vertices with exactly `n-1` cycle-free edges.
Kruskal processes edges by increasing cost and accepts an edge precisely when
its endpoints are currently in different components.

The cut property proves the choice: the cheapest edge crossing any component
cut can belong to a minimum spanning tree.

## 2. Cases that decide correctness

- Parallel roads require considering the cheaper useful edge first.
- A cycle edge must be skipped even when cheap.
- A disconnected graph has no spanning tree.
- Negative costs remain valid for MST algorithms.
- One city needs cost `0`.

## 3. Brute force: enumerate edge subsets

```python
from itertools import combinations


def road_reparation_brute(vertex_count: int, edges: list[tuple[int, int, int]]) -> int:
    if vertex_count <= 0:
        raise ValueError("vertex_count must be positive")

    best: int | None = None
    for selected in combinations(edges, vertex_count - 1):
        parent = list(range(vertex_count))

        def find(vertex: int) -> int:
            while parent[vertex] != vertex:
                vertex = parent[vertex]
            return vertex

        valid = True
        cost = 0
        for first, second, weight in selected:
            first_root = find(first)
            second_root = find(second)
            if first_root == second_root:
                valid = False
                break
            parent[first_root] = second_root
            cost += weight
        if valid and (best is None or cost < best):
            best = cost
    return -1 if best is None else best
```

**Complexity:** `O(choose(E, V-1) * V)` time and `O(V)` space.

## 4. Better: dense Prim scan

Grow one tree. Repeatedly scan all unused vertices for the cheapest connection
to the current tree, then relax its incident roads.

```python
def road_reparation_prim(vertex_count: int, edges: list[tuple[int, int, int]]) -> int:
    if vertex_count <= 0:
        raise ValueError("vertex_count must be positive")

    graph: list[list[tuple[int, int]]] = [[] for _ in range(vertex_count)]
    for first, second, cost in edges:
        graph[first].append((second, cost))
        graph[second].append((first, cost))

    minimum_cost: list[int | None] = [None] * vertex_count
    minimum_cost[0] = 0
    used = [False] * vertex_count
    total = 0

    for _ in range(vertex_count):
        vertex = -1
        for candidate in range(vertex_count):
            candidate_cost = minimum_cost[candidate]
            if used[candidate] or candidate_cost is None:
                continue
            if vertex == -1:
                vertex = candidate
                continue
            current_cost = minimum_cost[vertex]
            if current_cost is None:
                raise RuntimeError("selected vertex must have a finite cost")
            if candidate_cost < current_cost:
                vertex = candidate
        if vertex == -1:
            return -1

        used[vertex] = True
        selected_cost = minimum_cost[vertex]
        if selected_cost is None:
            raise RuntimeError("selected vertex must have a finite cost")
        total += selected_cost
        for neighbor, cost in graph[vertex]:
            neighbor_cost = minimum_cost[neighbor]
            if not used[neighbor] and (neighbor_cost is None or cost < neighbor_cost):
                minimum_cost[neighbor] = cost
    return total
```

**Complexity:** `O(V^2 + E)` time and `O(V + E)` space.

## 5. Expert solution: Kruskal with union by size

```python
def road_reparation_kruskal(
    vertex_count: int, edges: list[tuple[int, int, int]]
) -> int:
    if vertex_count <= 0:
        raise ValueError("vertex_count must be positive")

    parent = list(range(vertex_count))
    component_size = [1] * vertex_count

    def find(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    total = 0
    accepted = 0
    for first, second, cost in sorted(edges, key=lambda edge: edge[2]):
        first_root = find(first)
        second_root = find(second)
        if first_root == second_root:
            continue
        if component_size[first_root] < component_size[second_root]:
            first_root, second_root = second_root, first_root
        parent[second_root] = first_root
        component_size[first_root] += component_size[second_root]
        total += cost
        accepted += 1
        if accepted == vertex_count - 1:
            return total

    return 0 if vertex_count == 1 else -1
```

### Why the expert code is correct

Each accepted edge is the cheapest edge connecting two current components, so
the cut property permits it in an MST. DSU rejects exactly the cycle-forming
edges. Accepting `V-1` edges therefore yields a minimum spanning tree.

**Complexity:** `O(E log E)` time and `O(V)` auxiliary space.

## 6. What to remember

```text
sort edges by cost
different DSU components -> accept and unite
same component -> skip cycle
fewer than V-1 accepted -> impossible
```
