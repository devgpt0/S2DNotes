# ICPC300 201: Codeforces 1009F - Dominant Indices

**Source:** [Codeforces 1009F - Dominant Indices](https://codeforces.com/problemset/problem/1009/F)  
**Difficulty:** 2300  
**Pattern:** small-to-large subtree depth-frequency merging

## Exact contract

Root a tree at vertex `0`. For every vertex `v`, count subtree vertices by
their distance from `v` and return the smallest distance having maximum count.

## First principles

Absolute depth turns a relative distance into `depth[u] - depth[v]`. A subtree
answer therefore needs a frequency map from absolute depth to count. Merge
child maps into the largest child map, add the current vertex, and retain the
smallest depth on ties.

## Cases that decide correctness

- Distance zero always has at least the current vertex.
- Equal maximum frequencies choose the smaller distance.
- Only descendants in the root-at-zero orientation count.
- A one-vertex tree answers zero.
- Iterative traversal avoids recursion depth failure on a path.

## Brute force: scan every subtree

```python
def dominant_indices_brute(size: int, edges: list[tuple[int, int]]) -> list[int]:
    if type(size) is not int or size < 1 or len(edges) != size - 1:
        raise ValueError("edges must describe a nonempty tree")
    graph = [[] for _ in range(size)]
    for first, second in edges:
        if (
            type(first) is not int
            or type(second) is not int
            or not 0 <= first < size
            or not 0 <= second < size
            or first == second
        ):
            raise ValueError("invalid edge")
        graph[first].append(second)
        graph[second].append(first)

    parent = [-2] * size
    parent[0] = -1
    depth = [0] * size
    order = [0]
    for vertex in order:
        for neighbor in graph[vertex]:
            if neighbor == parent[vertex]:
                continue
            if parent[neighbor] != -2:
                raise ValueError("graph must be a tree")
            parent[neighbor] = vertex
            depth[neighbor] = depth[vertex] + 1
            order.append(neighbor)
    if len(order) != size:
        raise ValueError("graph must be connected")

    children = [[] for _ in range(size)]
    for vertex in range(1, size):
        children[parent[vertex]].append(vertex)

    answers = [0] * size
    for root in range(size):
        counts: dict[int, int] = {}
        stack = [root]
        while stack:
            vertex = stack.pop()
            distance = depth[vertex] - depth[root]
            counts[distance] = counts.get(distance, 0) + 1
            stack.extend(children[vertex])
        answers[root] = min(counts, key=lambda distance: (-counts[distance], distance))
    return answers
```

The worst-case time is `O(n^2)`.

## Better approach: no separate intermediate

Euler depth groups can count one chosen depth in a subtree quickly, but testing
every possible depth remains quadratic. Aggregating all depth frequencies while
merging subtrees is the first genuinely scalable invariant.

## Expert solution: merge smaller maps into the largest

```python
def dominant_indices(size: int, edges: list[tuple[int, int]]) -> list[int]:
    if type(size) is not int or size < 1 or len(edges) != size - 1:
        raise ValueError("edges must describe a nonempty tree")
    graph = [[] for _ in range(size)]
    for first, second in edges:
        if (
            type(first) is not int
            or type(second) is not int
            or not 0 <= first < size
            or not 0 <= second < size
            or first == second
        ):
            raise ValueError("invalid edge")
        graph[first].append(second)
        graph[second].append(first)

    parent = [-2] * size
    parent[0] = -1
    depth = [0] * size
    order = [0]
    for vertex in order:
        for neighbor in graph[vertex]:
            if neighbor == parent[vertex]:
                continue
            if parent[neighbor] != -2:
                raise ValueError("graph must be a tree")
            parent[neighbor] = vertex
            depth[neighbor] = depth[vertex] + 1
            order.append(neighbor)
    if len(order) != size:
        raise ValueError("graph must be connected")

    children = [[] for _ in range(size)]
    for vertex in range(1, size):
        children[parent[vertex]].append(vertex)

    bags: list[dict[int, int] | None] = [None] * size
    best_depth = [0] * size
    best_count = [0] * size
    answers = [0] * size

    for vertex in reversed(order):
        heavy = max(
            children[vertex], key=lambda child: len(bags[child] or {}), default=-1
        )
        if heavy == -1:
            bag: dict[int, int] = {}
            mode_depth = depth[vertex]
            mode_count = 0
        else:
            heavy_bag = bags[heavy]
            if heavy_bag is None:
                raise RuntimeError("missing child depth map")
            bag = heavy_bag
            mode_depth = best_depth[heavy]
            mode_count = best_count[heavy]

        for child in children[vertex]:
            child_bag = bags[child]
            if child_bag is None:
                raise RuntimeError("missing child depth map")
            if child != heavy:
                for absolute_depth, count in child_bag.items():
                    merged = bag.get(absolute_depth, 0) + count
                    bag[absolute_depth] = merged
                    if merged > mode_count or (
                        merged == mode_count and absolute_depth < mode_depth
                    ):
                        mode_count = merged
                        mode_depth = absolute_depth
            bags[child] = None

        own_count = bag.get(depth[vertex], 0) + 1
        bag[depth[vertex]] = own_count
        if own_count > mode_count or (
            own_count == mode_count and depth[vertex] < mode_depth
        ):
            mode_count = own_count
            mode_depth = depth[vertex]

        bags[vertex] = bag
        best_depth[vertex] = mode_depth
        best_count[vertex] = mode_count
        answers[vertex] = mode_depth - depth[vertex]

    return answers
```

Each map always represents exactly one processed subtree. A depth entry moves
only when its current map is smaller than the destination, so it moves at most
`O(log n)` times. The stored mode is updated after every changed frequency.

**Complexity:** `O(n log n)` expected time and `O(n)` live map entries.
