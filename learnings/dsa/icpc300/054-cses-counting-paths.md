# ICPC300 054: CSES - Counting Paths

**Source:** [CSES - Counting Paths](https://cses.fi/problemset/task/1136/)  
**Pattern:** lowest common ancestor + tree difference array  
**Goal:** For every vertex, count how many requested tree paths contain it.

Vertices and path endpoints are zero-based.

## 1. First principles

Updating every vertex on every path is too slow. Mark only endpoints and the
lowest common ancestor (LCA), then accumulate marks from children to parents.

For a vertex-inclusive path from `u` to `v`, with `w = lca(u, v)`:

```text
delta[u] += 1
delta[v] += 1
delta[w] -= 1
delta[parent[w]] -= 1   if w is not the root
```

After postorder accumulation, exactly the vertices on the path retain one
unit. Binary lifting finds each LCA in `O(log n)`.

## 2. Cases that decide correctness

| Case | Required behavior |
| --- | --- |
| `u == v` | Increment that one vertex once. |
| LCA equals one endpoint | Include the endpoint/LCA exactly once. |
| LCA is the root | Do not subtract from a nonexistent parent. |
| Repeated path | Add another identical contribution. |
| Chain tree | Counts must include every vertex between endpoints. |

## 3. Brute force: search each path

Find the unique path for every request and increment its vertices.

```python
def counting_paths_brute(
    graph: list[list[int]], paths: list[tuple[int, int]]
) -> list[int]:
    if not graph:
        raise ValueError("graph must not be empty")

    counts = [0] * len(graph)
    for first, second in paths:
        parent = [-2] * len(graph)
        parent[first] = -1
        stack = [first]
        while stack:
            node = stack.pop()
            if node == second:
                break
            for neighbor in graph[node]:
                if parent[neighbor] == -2:
                    parent[neighbor] = node
                    stack.append(neighbor)

        if parent[second] == -2:
            raise ValueError("graph must be connected")
        node = second
        while node != -1:
            counts[node] += 1
            if node == first:
                break
            node = parent[node]
    return counts
```

**Complexity:** `O(qn)` time and `O(n)` extra space.

## 4. Better: root once and climb parents

Precompute each vertex's parent and depth. Lift the deeper endpoint, then lift
both endpoints until they meet.

```python
def counting_paths_parent_climb(
    graph: list[list[int]], paths: list[tuple[int, int]]
) -> list[int]:
    if not graph:
        raise ValueError("graph must not be empty")

    parent = [-2] * len(graph)
    depth = [0] * len(graph)
    parent[0] = -1
    stack = [0]
    while stack:
        node = stack.pop()
        for neighbor in graph[node]:
            if parent[neighbor] != -2:
                continue
            parent[neighbor] = node
            depth[neighbor] = depth[node] + 1
            stack.append(neighbor)
    if any(ancestor == -2 for ancestor in parent):
        raise ValueError("graph must be connected")

    counts = [0] * len(graph)
    for first, second in paths:
        while depth[first] > depth[second]:
            counts[first] += 1
            first = parent[first]
        while depth[second] > depth[first]:
            counts[second] += 1
            second = parent[second]
        while first != second:
            counts[first] += 1
            counts[second] += 1
            first = parent[first]
            second = parent[second]
        counts[first] += 1
    return counts
```

**Complexity:** `O(n + q * height)` time and `O(n)` space. A chain still has
linear-height paths.

## 5. Expert solution: LCA and tree differences

Binary lifting answers LCAs. One reverse traversal then pushes every subtree's
net difference into its parent.

```python
def counting_paths_lca_difference(
    graph: list[list[int]], paths: list[tuple[int, int]]
) -> list[int]:
    if not graph:
        raise ValueError("graph must not be empty")

    vertex_count = len(graph)
    parent = [-2] * vertex_count
    depth = [0] * vertex_count
    order: list[int] = []
    parent[0] = -1
    stack = [0]
    while stack:
        node = stack.pop()
        order.append(node)
        for neighbor in graph[node]:
            if neighbor == parent[node]:
                continue
            if parent[neighbor] != -2:
                raise ValueError("graph must be a tree")
            parent[neighbor] = node
            depth[neighbor] = depth[node] + 1
            stack.append(neighbor)
    if len(order) != vertex_count:
        raise ValueError("graph must be connected")

    level_count = max(1, vertex_count.bit_length())
    ancestor = [[0] * vertex_count for _ in range(level_count)]
    ancestor[0] = [0 if value == -1 else value for value in parent]
    for level in range(1, level_count):
        previous = ancestor[level - 1]
        ancestor[level] = [previous[previous[node]] for node in range(vertex_count)]

    def lowest_common_ancestor(first: int, second: int) -> int:
        if depth[first] < depth[second]:
            first, second = second, first
        difference = depth[first] - depth[second]
        for level in range(level_count):
            if difference & (1 << level):
                first = ancestor[level][first]
        if first == second:
            return first
        for level in range(level_count - 1, -1, -1):
            if ancestor[level][first] != ancestor[level][second]:
                first = ancestor[level][first]
                second = ancestor[level][second]
        return ancestor[0][first]

    difference = [0] * vertex_count
    for first, second in paths:
        shared_ancestor = lowest_common_ancestor(first, second)
        difference[first] += 1
        difference[second] += 1
        difference[shared_ancestor] -= 1
        ancestor_parent = parent[shared_ancestor]
        if ancestor_parent != -1:
            difference[ancestor_parent] -= 1

    for node in reversed(order):
        if parent[node] != -1:
            difference[parent[node]] += difference[node]
    return difference
```

### Why the expert code is correct

- Endpoint additions start one upward contribution on each side of the path.
- The subtraction at the LCA leaves one copy there; subtracting at its parent
  stops that copy from moving above the path.
- Postorder accumulation sends each contribution through exactly the vertices
  between its endpoint and the LCA.

**Complexity:** `O(n log n + q log n)` time and `O(n log n)` space.

## 6. What to remember

```text
vertex path difference:
    +1 at both endpoints
    -1 at LCA
    -1 at parent(LCA)
then accumulate child -> parent
```
