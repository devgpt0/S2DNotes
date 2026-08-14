# ICPC300 005: CSES - Path Queries II

**Source:** [CSES - Path Queries II](https://cses.fi/problemset/task/2134/)  
**Pattern:** heavy-light decomposition + segment tree  
**Goal:** Support vertex-value assignments and maximum queries on tree paths.

The implementations use zero-based vertices. An operation is
`(1, vertex, value)` or `(2, first, second)`.

## 1. First principles

A segment tree needs contiguous array ranges, but a tree path is not normally
contiguous. Heavy-light decomposition chooses one **heavy child** per vertex:
the child with the largest subtree.

Following a light edge at least halves the remaining subtree size. Therefore
any root path crosses at most `O(log n)` light edges, and any path splits into
at most `O(log n)` contiguous heavy-chain ranges.

```text
tree path u -> v
    chain suffix from u
    zero or more whole chain pieces
    chain prefix to v

maximum(path) = maximum of those segment-tree ranges
```

## 2. Cases that decide correctness

| Case | Required behavior |
| --- | --- |
| `u == v` | Return that vertex's current value. |
| Negative values | Do not initialize the answer to zero. |
| Update the LCA | A later path query must see the new value. |
| Vertices on one heavy chain | Use one inclusive segment-tree range. |
| Vertices on different chains | Always lift the deeper chain head. |

## 3. Brute force: find the path for every query

Search from one endpoint, reconstruct the unique tree path, and scan its
values. This is a dependable oracle.

```python
def path_queries_brute(
    graph: list[list[int]],
    values: list[int],
    operations: list[tuple[int, ...]],
) -> list[int]:
    if not graph or len(graph) != len(values):
        raise ValueError("graph and values must have the same nonzero size")

    current_values = values.copy()
    answers: list[int] = []

    for operation in operations:
        operation_type = operation[0]
        if operation_type == 1:
            _, vertex, value = operation
            current_values[vertex] = value
        elif operation_type == 2:
            _, first, second = operation
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

            path_maximum = current_values[second]
            node = second
            while node != first:
                node = parent[node]
                path_maximum = max(path_maximum, current_values[node])
            answers.append(path_maximum)
        else:
            raise ValueError(f"unknown operation type: {operation_type}")

    return answers
```

**Complexity:** `O(n)` per path query, `O(1)` per update, and `O(n)` extra
space.

## 4. Better: root once and climb parents

Precompute `parent` and `depth`. For a query, lift the deeper endpoint until
both endpoints meet. Updates remain direct assignments.

```python
def path_queries_parent_climb(
    graph: list[list[int]],
    values: list[int],
    operations: list[tuple[int, ...]],
) -> list[int]:
    if not graph or len(graph) != len(values):
        raise ValueError("graph and values must have the same nonzero size")

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

    current_values = values.copy()
    answers: list[int] = []

    for operation in operations:
        operation_type = operation[0]
        if operation_type == 1:
            _, vertex, value = operation
            current_values[vertex] = value
            continue
        if operation_type != 2:
            raise ValueError(f"unknown operation type: {operation_type}")

        _, first, second = operation
        path_maximum = max(current_values[first], current_values[second])

        while depth[first] > depth[second]:
            path_maximum = max(path_maximum, current_values[first])
            first = parent[first]
        while depth[second] > depth[first]:
            path_maximum = max(path_maximum, current_values[second])
            second = parent[second]
        while first != second:
            path_maximum = max(
                path_maximum, current_values[first], current_values[second]
            )
            first = parent[first]
            second = parent[second]

        answers.append(max(path_maximum, current_values[first]))

    return answers
```

**Complexity:** `O(n)` preprocessing, `O(height)` per path query, `O(1)` per
update. A chain still gives `O(n)` queries.

## 5. Expert solution: heavy-light decomposition

Number each heavy chain contiguously. A segment tree over that order handles
point assignments and chain-range maxima.

```python
def path_queries_heavy_light(
    graph: list[list[int]],
    values: list[int],
    operations: list[tuple[int, ...]],
) -> list[int]:
    vertex_count = len(graph)
    if vertex_count == 0 or vertex_count != len(values):
        raise ValueError("graph and values must have the same nonzero size")

    parent = [-2] * vertex_count
    depth = [0] * vertex_count
    traversal_order: list[int] = []
    parent[0] = -1
    stack = [0]

    while stack:
        node = stack.pop()
        traversal_order.append(node)
        for neighbor in graph[node]:
            if neighbor == parent[node]:
                continue
            if parent[neighbor] != -2:
                raise ValueError("graph must be a tree")
            parent[neighbor] = node
            depth[neighbor] = depth[node] + 1
            stack.append(neighbor)

    if len(traversal_order) != vertex_count:
        raise ValueError("graph must be connected")

    subtree_size = [1] * vertex_count
    heavy_child = [-1] * vertex_count
    for node in reversed(traversal_order):
        largest_child_size = 0
        for neighbor in graph[node]:
            if parent[neighbor] != node:
                continue
            subtree_size[node] += subtree_size[neighbor]
            if subtree_size[neighbor] > largest_child_size:
                largest_child_size = subtree_size[neighbor]
                heavy_child[node] = neighbor

    chain_head = [0] * vertex_count
    position = [0] * vertex_count
    next_position = 0
    pending_chains = [(0, 0)]

    while pending_chains:
        node, head = pending_chains.pop()
        while node != -1:
            chain_head[node] = head
            position[node] = next_position
            next_position += 1

            for neighbor in graph[node]:
                if parent[neighbor] == node and neighbor != heavy_child[node]:
                    pending_chains.append((neighbor, neighbor))
            node = heavy_child[node]

    tree_size = 1
    while tree_size < vertex_count:
        tree_size *= 2
    negative_infinity = -(1 << 63)
    segment_tree = [negative_infinity] * (2 * tree_size)

    for node, value in enumerate(values):
        segment_tree[tree_size + position[node]] = value
    for index in range(tree_size - 1, 0, -1):
        segment_tree[index] = max(segment_tree[2 * index], segment_tree[2 * index + 1])

    def assign(vertex: int, value: int) -> None:
        index = tree_size + position[vertex]
        segment_tree[index] = value
        index //= 2
        while index > 0:
            segment_tree[index] = max(
                segment_tree[2 * index], segment_tree[2 * index + 1]
            )
            index //= 2

    def range_maximum(left: int, right: int) -> int:
        left += tree_size
        right += tree_size
        result = negative_infinity
        while left <= right:
            if left % 2 == 1:
                result = max(result, segment_tree[left])
                left += 1
            if right % 2 == 0:
                result = max(result, segment_tree[right])
                right -= 1
            left //= 2
            right //= 2
        return result

    def path_maximum(first: int, second: int) -> int:
        result = negative_infinity
        while chain_head[first] != chain_head[second]:
            if depth[chain_head[first]] < depth[chain_head[second]]:
                first, second = second, first
            result = max(
                result,
                range_maximum(position[chain_head[first]], position[first]),
            )
            first = parent[chain_head[first]]

        if depth[first] > depth[second]:
            first, second = second, first
        return max(result, range_maximum(position[first], position[second]))

    answers: list[int] = []
    for operation in operations:
        operation_type = operation[0]
        if operation_type == 1:
            _, vertex, value = operation
            assign(vertex, value)
        elif operation_type == 2:
            _, first, second = operation
            answers.append(path_maximum(first, second))
        else:
            raise ValueError(f"unknown operation type: {operation_type}")

    return answers
```

### Why the expert code is correct

- Each vertex belongs to exactly one heavy chain, and each chain occupies one
  contiguous position range.
- Lifting the deeper chain head removes a disjoint path segment; eventually
  both endpoints share a chain.
- Those queried segments are disjoint and cover the path exactly, so their
  maximum is the path maximum.

**Complexity:** `O(n)` decomposition, `O(log n)` per update, and
`O(log^2 n)` per path query. Memory is `O(n)`.

## 6. What to remember

```text
heavy edges make chains contiguous
every light edge at least halves subtree size
tree path -> O(log n) chain ranges -> segment-tree maximum
```
