# 171. Blood Cousins Return — Codeforces 246E

**Source:** [Codeforces 246E - Blood Cousins Return](https://codeforces.com/problemset/problem/246/E)  
**Difficulty:** 2300

## 1. Problem in plain words

A rooted forest assigns a name to every vertex. Query `(v, k)` asks for the number of distinct names among descendants of `v` exactly `k` edges below it. For `k = 0`, only `v` is considered.

The functions use zero-based vertices and parent `-1` for a root.

## 2. First principles

A forest preorder makes every subtree a contiguous Euler interval. Group vertices by absolute depth; then a query becomes a distinct-value query on one contiguous slice of one depth group.

For each depth independently, sort queries by right endpoint. A Fenwick tree keeps `1` only at the latest position of every name, so its range sum equals the number of distinct names.

## 3. Cases that define correctness

- Several roots form independent Euler intervals.
- If the requested depth is below every descendant, the answer is zero.
- Equal text names at different vertices are one distinct name.
- `k` is relative to `v`, but depth groups are absolute.

## 4. Brute force

Traverse the subtree and collect names at the target depth.

```python
def blood_cousin_counts_brute_force(
    parents: list[int], names: list[str], queries: list[tuple[int, int]]
) -> list[int]:
    size = len(parents)
    if (
        size == 0
        or len(names) != size
        or any(type(name) is not str or not name for name in names)
    ):
        raise ValueError("invalid forest")

    children = [[] for _ in range(size)]
    roots: list[int] = []
    for vertex, parent in enumerate(parents):
        if type(parent) is int and parent == -1:
            roots.append(vertex)
        elif type(parent) is int and 0 <= parent < size and parent != vertex:
            children[parent].append(vertex)
        else:
            raise ValueError("invalid parent")
    if not roots:
        raise ValueError("forest must have a root")

    depth = [0] * size
    visited = 0
    for root in roots:
        stack = [root]
        while stack:
            vertex = stack.pop()
            visited += 1
            for child in children[vertex]:
                depth[child] = depth[vertex] + 1
                stack.append(child)
    if visited != size:
        raise ValueError("parents must form a forest")

    answers: list[int] = []
    for root, distance in queries:
        if not 0 <= root < size or distance < 0:
            raise ValueError("invalid query")
        target_depth = depth[root] + distance
        found: set[str] = set()
        stack = [root]
        while stack:
            vertex = stack.pop()
            if depth[vertex] == target_depth:
                found.add(names[vertex])
            elif depth[vertex] < target_depth:
                stack.extend(children[vertex])
        answers.append(len(found))
    return answers
```

Worst-case time is `O(nq)` and space is `O(n)`.

## 5. Better approach: Euler depth-group scanning

Flatten the forest and store Euler positions by depth. Binary searches isolate the subtree slice; build a set from that slice.

```python
from bisect import bisect_left, bisect_right


def blood_cousin_counts_depth_scan(
    parents: list[int], names: list[str], queries: list[tuple[int, int]]
) -> list[int]:
    size = len(parents)
    if (
        size == 0
        or len(names) != size
        or any(type(name) is not str or not name for name in names)
    ):
        raise ValueError("invalid forest")

    children = [[] for _ in range(size)]
    roots: list[int] = []
    for vertex, parent in enumerate(parents):
        if type(parent) is int and parent == -1:
            roots.append(vertex)
        elif type(parent) is int and 0 <= parent < size and parent != vertex:
            children[parent].append(vertex)
        else:
            raise ValueError("invalid parent")
    if not roots:
        raise ValueError("forest must have a root")

    depth = [0] * size
    start = [0] * size
    end = [0] * size
    tour: list[int] = []
    for root in roots:
        stack = [(root, False)]
        while stack:
            vertex, leaving = stack.pop()
            if leaving:
                end[vertex] = len(tour) - 1
                continue
            start[vertex] = len(tour)
            tour.append(vertex)
            stack.append((vertex, True))
            for child in reversed(children[vertex]):
                depth[child] = depth[vertex] + 1
                stack.append((child, False))
    if len(tour) != size:
        raise ValueError("parents must form a forest")

    maximum_depth = max(depth)
    positions = [[] for _ in range(maximum_depth + 1)]
    depth_names = [[] for _ in range(maximum_depth + 1)]
    for position, vertex in enumerate(tour):
        positions[depth[vertex]].append(position)
        depth_names[depth[vertex]].append(names[vertex])

    answers: list[int] = []
    for vertex, distance in queries:
        if not 0 <= vertex < size or distance < 0:
            raise ValueError("invalid query")
        level = depth[vertex] + distance
        if level > maximum_depth:
            answers.append(0)
            continue
        left = bisect_left(positions[level], start[vertex])
        right = bisect_right(positions[level], end[vertex])
        answers.append(len(set(depth_names[level][left:right])))
    return answers
```

Preprocessing is `O(n)`; query time is linear in the selected depth slice.

## 6. Expert solution: offline distinct queries per depth

Convert every query to local indices in one depth array. Sweep that array by right endpoint, toggling each name's previous and current latest positions in a Fenwick tree.

```python
from bisect import bisect_left, bisect_right


def blood_cousin_counts(
    parents: list[int], names: list[str], queries: list[tuple[int, int]]
) -> list[int]:
    size = len(parents)
    if (
        size == 0
        or len(names) != size
        or any(type(name) is not str or not name for name in names)
    ):
        raise ValueError("invalid forest")

    children = [[] for _ in range(size)]
    roots: list[int] = []
    for vertex, parent in enumerate(parents):
        if type(parent) is int and parent == -1:
            roots.append(vertex)
        elif type(parent) is int and 0 <= parent < size and parent != vertex:
            children[parent].append(vertex)
        else:
            raise ValueError("invalid parent")
    if not roots:
        raise ValueError("forest must have a root")

    depth = [0] * size
    start = [0] * size
    end = [0] * size
    tour: list[int] = []
    for root in roots:
        stack = [(root, False)]
        while stack:
            vertex, leaving = stack.pop()
            if leaving:
                end[vertex] = len(tour) - 1
                continue
            start[vertex] = len(tour)
            tour.append(vertex)
            stack.append((vertex, True))
            for child in reversed(children[vertex]):
                depth[child] = depth[vertex] + 1
                stack.append((child, False))
    if len(tour) != size:
        raise ValueError("parents must form a forest")

    maximum_depth = max(depth)
    positions = [[] for _ in range(maximum_depth + 1)]
    depth_names = [[] for _ in range(maximum_depth + 1)]
    for position, vertex in enumerate(tour):
        level = depth[vertex]
        positions[level].append(position)
        depth_names[level].append(names[vertex])

    grouped_queries: list[list[tuple[int, int, int]]] = [
        [] for _ in range(maximum_depth + 1)
    ]
    answers = [0] * len(queries)
    for query_index, (vertex, distance) in enumerate(queries):
        if not 0 <= vertex < size or distance < 0:
            raise ValueError("invalid query")
        level = depth[vertex] + distance
        if level > maximum_depth:
            continue
        left = bisect_left(positions[level], start[vertex])
        right = bisect_right(positions[level], end[vertex]) - 1
        if left <= right:
            grouped_queries[level].append((right, left, query_index))

    for level, level_queries in enumerate(grouped_queries):
        if not level_queries:
            continue
        level_queries.sort()
        count = len(depth_names[level])
        fenwick = [0] * (count + 1)

        def add(position: int, delta: int) -> None:
            index = position + 1
            while index <= count:
                fenwick[index] += delta
                index += index & -index

        def prefix(position: int) -> int:
            result = 0
            index = position + 1
            while index > 0:
                result += fenwick[index]
                index -= index & -index
            return result

        last: dict[str, int] = {}
        processed = -1
        for right, left, query_index in level_queries:
            while processed < right:
                processed += 1
                name = depth_names[level][processed]
                previous = last.get(name)
                if previous is not None:
                    add(previous, -1)
                add(processed, 1)
                last[name] = processed
            answers[query_index] = prefix(right) - (prefix(left - 1) if left else 0)
    return answers
```

## 7. Why the expert solution is correct

Euler and depth intersection selects exactly the requested descendants. During a depth sweep, the Fenwick tree contains one marker at the latest occurrence of every name seen so far. A marker lies in the query range exactly when that name appears there, so the range sum counts distinct names.

Time is `O((n + q) log n)` and space is `O(n + q)`.
