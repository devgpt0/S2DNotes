# 134. New Year Tree — Codeforces 620E

**Source:** [Codeforces 620E - New Year Tree](https://codeforces.com/problemset/problem/620/E)  
**Difficulty:** 2300

## 1. Problem in plain words

A tree rooted at vertex `1` has one color per vertex. Operation `1 v c` recolors every vertex in `v`'s subtree to color `c`. Operation `2 v` asks how many distinct colors occur in that subtree.

The functions below use zero-based vertices and represent operations as `(1, vertex, color)` or `(2, vertex)`.

## 2. First principles

A preorder Euler tour makes each subtree a contiguous interval. Because source colors are at most `60`, a set of colors fits in one integer bit mask: color `c` is bit `c - 1`, union is bitwise OR, and the number of colors is `bit_count()`.

The flattened task is range assignment plus range OR. A lazy segment tree supports both in logarithmic time.

## 3. Cases that define correctness

- Recoloring a leaf changes one Euler position.
- Recoloring the root replaces the entire tree's color set.
- A later partial recoloring must first expose any pending ancestor assignment.
- Recoloring to an already present color remains an assignment, not a union.

## 4. Brute force

Store rooted children and visit the entire requested subtree for every operation.

```python
def new_year_tree_brute_force(
    colors: list[int], edges: list[tuple[int, int]], operations: list[tuple[int, ...]]
) -> list[int]:
    size = len(colors)
    if size == 0 or len(edges) != size - 1:
        raise ValueError("edges must describe a nonempty tree")

    graph = [[] for _ in range(size)]
    for first, second in edges:
        graph[first].append(second)
        graph[second].append(first)
    children = [[] for _ in range(size)]
    parent = [-1] * size
    parent[0] = 0
    stack = [0]
    while stack:
        vertex = stack.pop()
        for neighbor in graph[vertex]:
            if parent[neighbor] == -1:
                parent[neighbor] = vertex
                children[vertex].append(neighbor)
                stack.append(neighbor)
    if any(value == -1 for value in parent):
        raise ValueError("the graph must be connected")

    current = colors.copy()
    answers: list[int] = []
    for operation in operations:
        if len(operation) not in (2, 3):
            raise ValueError("invalid operation")
        kind, vertex = operation[:2]
        if not 0 <= vertex < size:
            raise ValueError("vertex is outside the tree")
        vertices: list[int] = []
        stack = [vertex]
        while stack:
            node = stack.pop()
            vertices.append(node)
            stack.extend(children[node])
        if kind == 1 and len(operation) == 3:
            color = operation[2]
            if not 1 <= color <= 60:
                raise ValueError("color must be between 1 and 60")
            for node in vertices:
                current[node] = color
        elif kind == 2 and len(operation) == 2:
            answers.append(len({current[node] for node in vertices}))
        else:
            raise ValueError("invalid operation")
    return answers
```

Worst-case time is `O(nm)` and auxiliary space is `O(n)`.

## 5. Better approach: Euler array scanning

Flatten once. Recolor or inspect the corresponding interval directly, avoiding a fresh tree traversal but still touching every vertex in the subtree.

```python
def new_year_tree_euler_scan(
    colors: list[int], edges: list[tuple[int, int]], operations: list[tuple[int, ...]]
) -> list[int]:
    size = len(colors)
    if size == 0 or len(edges) != size - 1:
        raise ValueError("edges must describe a nonempty tree")

    graph = [[] for _ in range(size)]
    for first, second in edges:
        graph[first].append(second)
        graph[second].append(first)
    start = [0] * size
    end = [0] * size
    tour: list[int] = []
    stack = [(0, -1, False)]
    while stack:
        vertex, parent, leaving = stack.pop()
        if leaving:
            end[vertex] = len(tour) - 1
            continue
        start[vertex] = len(tour)
        tour.append(vertex)
        stack.append((vertex, parent, True))
        for neighbor in reversed(graph[vertex]):
            if neighbor != parent:
                stack.append((neighbor, vertex, False))
    if len(tour) != size:
        raise ValueError("the graph must be connected")

    flattened = [colors[vertex] for vertex in tour]
    answers: list[int] = []
    for operation in operations:
        if len(operation) not in (2, 3):
            raise ValueError("invalid operation")
        kind, vertex = operation[:2]
        if not 0 <= vertex < size:
            raise ValueError("vertex is outside the tree")
        if kind == 1 and len(operation) == 3:
            color = operation[2]
            if not 1 <= color <= 60:
                raise ValueError("color must be between 1 and 60")
            for position in range(start[vertex], end[vertex] + 1):
                flattened[position] = color
        elif kind == 2 and len(operation) == 2:
            answers.append(len(set(flattened[start[vertex] : end[vertex] + 1])))
        else:
            raise ValueError("invalid operation")
    return answers
```

Preprocessing is `O(n)`; an operation costs `O(subtree size)` and space is `O(n)`.

## 6. Expert solution: lazy bit-mask segment tree

Store the OR of color masks in each segment. A full-range recoloring replaces the node mask and records that assignment lazily.

```python
def new_year_tree(
    colors: list[int], edges: list[tuple[int, int]], operations: list[tuple[int, ...]]
) -> list[int]:
    size = len(colors)
    if size == 0 or len(edges) != size - 1:
        raise ValueError("edges must describe a nonempty tree")
    if any(not 1 <= color <= 60 for color in colors):
        raise ValueError("colors must be between 1 and 60")

    graph = [[] for _ in range(size)]
    for first, second in edges:
        graph[first].append(second)
        graph[second].append(first)
    start = [0] * size
    end = [0] * size
    tour: list[int] = []
    stack = [(0, -1, False)]
    while stack:
        vertex, parent, leaving = stack.pop()
        if leaving:
            end[vertex] = len(tour) - 1
            continue
        start[vertex] = len(tour)
        tour.append(vertex)
        stack.append((vertex, parent, True))
        for neighbor in reversed(graph[vertex]):
            if neighbor != parent:
                stack.append((neighbor, vertex, False))
    if len(tour) != size:
        raise ValueError("the graph must be connected")

    tree = [0] * (4 * size)
    lazy = [0] * (4 * size)

    def build(node: int, left: int, right: int) -> None:
        if left == right:
            tree[node] = 1 << (colors[tour[left]] - 1)
            return
        middle = (left + right) // 2
        build(node * 2, left, middle)
        build(node * 2 + 1, middle + 1, right)
        tree[node] = tree[node * 2] | tree[node * 2 + 1]

    def apply(node: int, mask: int) -> None:
        tree[node] = mask
        lazy[node] = mask

    def push(node: int) -> None:
        mask = lazy[node]
        if mask:
            apply(node * 2, mask)
            apply(node * 2 + 1, mask)
            lazy[node] = 0

    def assign(
        node: int,
        left: int,
        right: int,
        query_left: int,
        query_right: int,
        mask: int,
    ) -> None:
        if query_left <= left and right <= query_right:
            apply(node, mask)
            return
        push(node)
        middle = (left + right) // 2
        if query_left <= middle:
            assign(node * 2, left, middle, query_left, query_right, mask)
        if middle < query_right:
            assign(node * 2 + 1, middle + 1, right, query_left, query_right, mask)
        tree[node] = tree[node * 2] | tree[node * 2 + 1]

    def query(
        node: int, left: int, right: int, query_left: int, query_right: int
    ) -> int:
        if query_left <= left and right <= query_right:
            return tree[node]
        push(node)
        middle = (left + right) // 2
        result = 0
        if query_left <= middle:
            result |= query(node * 2, left, middle, query_left, query_right)
        if middle < query_right:
            result |= query(node * 2 + 1, middle + 1, right, query_left, query_right)
        return result

    build(1, 0, size - 1)
    answers: list[int] = []
    for operation in operations:
        if len(operation) not in (2, 3):
            raise ValueError("invalid operation")
        kind, vertex = operation[:2]
        if not 0 <= vertex < size:
            raise ValueError("vertex is outside the tree")
        if kind == 1 and len(operation) == 3:
            color = operation[2]
            if not 1 <= color <= 60:
                raise ValueError("color must be between 1 and 60")
            assign(1, 0, size - 1, start[vertex], end[vertex], 1 << (color - 1))
        elif kind == 2 and len(operation) == 2:
            answers.append(
                query(1, 0, size - 1, start[vertex], end[vertex]).bit_count()
            )
        else:
            raise ValueError("invalid operation")
    return answers
```

## 7. Why the expert solution is correct

Euler intervals equal subtrees. A node mask is exactly the union of colors in its segment; assignment replaces every represented color with one bit, and pushing preserves that assignment when a child is inspected. Thus query OR is exactly the subtree's color set, whose bit count is the requested answer.

Time is `O((n + m) log n)` and space is `O(n)`.
