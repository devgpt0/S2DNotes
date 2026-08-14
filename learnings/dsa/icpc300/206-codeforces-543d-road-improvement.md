# ICPC300 206: Codeforces 543D - Road Improvement

**Source:** [Codeforces 543D - Road Improvement](https://codeforces.com/problemset/problem/543/D)  
**Difficulty:** 2300  
**Pattern:** multiplicative reroot DP without modular division

## Exact contract

For every vertex of a tree, count connected nonempty vertex subsets containing
that vertex. Return all counts modulo `1_000_000_007`.

## First principles

Root the tree. For a vertex `v`, each child side independently contributes
either nothing or one connected subset containing that child. Thus

`down[v] = product(down[child] + 1)`.

Rerooting adds one analogous parent-side choice. For child `c`, that choice is
formed from the parent's outside choice and every sibling factor. Prefix and
suffix products compute it without dividing modulo a prime.

## Cases that decide correctness

- The singleton containing only `v` chooses nothing from every side.
- Every selected neighbor side must include that neighbor to stay connected.
- Modulo factors can be zero, so modular division is unsafe.
- A leaf has `down = 1`.
- Iterative rooting handles path-shaped trees.

## Brute force: enumerate all vertex subsets

```python
MODULO = 1_000_000_007


def road_improvement_brute(size: int, edges: list[tuple[int, int]]) -> list[int]:
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

    answers = [0] * size
    for mask in range(1, 1 << size):
        start = (mask & -mask).bit_length() - 1
        seen = 1 << start
        stack = [start]
        while stack:
            vertex = stack.pop()
            for neighbor in graph[vertex]:
                bit = 1 << neighbor
                if mask & bit and not seen & bit:
                    seen |= bit
                    stack.append(neighbor)
        if seen == mask:
            for vertex in range(size):
                if mask >> vertex & 1:
                    answers[vertex] += 1
    if sum(answer > 0 for answer in answers) != size:
        raise ValueError("graph must be connected")
    return [answer % MODULO for answer in answers]
```

This takes `O(2^n(n+m))` time.

## Better approach: reroot from every vertex

Running the `down` recurrence with each vertex as root gives its answer in
`O(n)` time, for `O(n^2)` total. The expert pass reuses all directed-side
products between roots.

## Expert solution: prefix/suffix reroot products

```python
MODULO = 1_000_000_007


def road_improvement(size: int, edges: list[tuple[int, int]]) -> list[int]:
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
    order = [0]
    for vertex in order:
        for neighbor in graph[vertex]:
            if neighbor == parent[vertex]:
                continue
            if parent[neighbor] != -2:
                raise ValueError("graph must be a tree")
            parent[neighbor] = vertex
            order.append(neighbor)
    if len(order) != size:
        raise ValueError("graph must be connected")

    children = [[] for _ in range(size)]
    for vertex in range(1, size):
        children[parent[vertex]].append(vertex)

    down = [1] * size
    for vertex in reversed(order):
        for child in children[vertex]:
            down[vertex] = down[vertex] * (down[child] + 1) % MODULO

    outside = [0] * size
    answers = [0] * size
    for vertex in order:
        answers[vertex] = down[vertex] * (outside[vertex] + 1) % MODULO
        child_count = len(children[vertex])
        prefix = [1] * (child_count + 1)
        suffix = [1] * (child_count + 1)
        for index, child in enumerate(children[vertex]):
            prefix[index + 1] = prefix[index] * (down[child] + 1) % MODULO
        for index in range(child_count - 1, -1, -1):
            child = children[vertex][index]
            suffix[index] = suffix[index + 1] * (down[child] + 1) % MODULO
        for index, child in enumerate(children[vertex]):
            sibling_product = prefix[index] * suffix[index + 1] % MODULO
            outside[child] = (outside[vertex] + 1) * sibling_product % MODULO
    return answers
```

`down[v]` enumerates all connected choices below `v`. `outside[v]` enumerates
connected choices through its parent, and prefix/suffix products include every
sibling side exactly once. Their independent optional choices give the answer.

**Complexity:** `O(n)` time and `O(n)` space.
