# 132. Tree and Queries — Codeforces 375D

**Source:** [Codeforces 375D - Tree and Queries](https://codeforces.com/problemset/problem/375/D)  
**Difficulty:** 2300

## 1. Problem in plain words

A tree rooted at vertex `1` has a color on every vertex. For each query `(vertex, k)`, count how many different colors occur at least `k` times in that vertex's subtree.

The functions below use zero-based vertices; subtract one from source input vertices.

## 2. First principles

A preorder Euler tour writes every subtree into one contiguous array interval. The query then becomes: in one array interval, how many values have frequency at least `k`? Mo's algorithm orders intervals so that a maintained window changes by few single-position moves.

Knowing each color's frequency is not enough: a query ranges over frequencies. Also maintain `frequency_count[f]`, the number of colors occurring exactly `f` times, plus square-root bucket sums over that array.

## 3. Cases that define correctness

- A leaf's interval contains one vertex.
- If `k` exceeds the subtree size, the answer is zero.
- Many vertices may share one color.
- Repeated queries must retain their original output order.

## 4. Brute force

Traverse the requested subtree and count its colors independently for every query.

```python
from collections import Counter


def tree_queries_brute_force(
    colors: list[int], edges: list[tuple[int, int]], queries: list[tuple[int, int]]
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
            if parent[neighbor] != -1:
                continue
            parent[neighbor] = vertex
            children[vertex].append(neighbor)
            stack.append(neighbor)
    if any(value == -1 for value in parent):
        raise ValueError("the graph must be connected")

    answers: list[int] = []
    for root, threshold in queries:
        if not 0 <= root < size or threshold <= 0:
            raise ValueError("invalid query")
        counts: Counter[int] = Counter()
        stack = [root]
        while stack:
            vertex = stack.pop()
            counts[colors[vertex]] += 1
            stack.extend(children[vertex])
        answers.append(sum(count >= threshold for count in counts.values()))
    return answers
```

Worst-case time is `O(nq)` and auxiliary space is `O(n)`.

## 5. Better approach: flatten each subtree

Build one preorder tour. Every query can scan `tour[tin[v] : tout[v] + 1]` instead of walking tree edges, which removes repeated traversal logic but still takes linear time in the subtree size.

```python
from collections import Counter


def tree_queries_euler_scan(
    colors: list[int], edges: list[tuple[int, int]], queries: list[tuple[int, int]]
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

    answers: list[int] = []
    for vertex, threshold in queries:
        if not 0 <= vertex < size or threshold <= 0:
            raise ValueError("invalid query")
        counts = Counter(
            colors[tour[index]] for index in range(start[vertex], end[vertex] + 1)
        )
        answers.append(sum(count >= threshold for count in counts.values()))
    return answers
```

Preprocessing is `O(n)`; query time is `O(subtree size)` and space is `O(n)`.

## 6. Expert solution: Euler tour plus Mo's algorithm

Compress colors, sort subtree intervals in Mo order, and move one shared window. Exact-frequency buckets answer “at least `k`” in `O(sqrt(n))` time.

```python
from math import isqrt


def tree_queries(
    colors: list[int], edges: list[tuple[int, int]], queries: list[tuple[int, int]]
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

    color_index = {color: index for index, color in enumerate(sorted(set(colors)))}
    flattened = [color_index[colors[vertex]] for vertex in tour]
    interval_block = isqrt(size) + 1
    ordered: list[tuple[int, int, int, int]] = []
    for index, (vertex, threshold) in enumerate(queries):
        if not 0 <= vertex < size or threshold <= 0:
            raise ValueError("invalid query")
        ordered.append((start[vertex], end[vertex], threshold, index))
    ordered.sort(
        key=lambda item: (
            item[0] // interval_block,
            item[1] if item[0] // interval_block % 2 == 0 else -item[1],
        )
    )

    color_frequency = [0] * len(color_index)
    exact_frequency = [0] * (size + 1)
    frequency_block = isqrt(size) + 1
    bucket_count = (size + frequency_block) // frequency_block
    frequency_buckets = [0] * bucket_count

    def change(position: int, delta: int) -> None:
        color = flattened[position]
        old_frequency = color_frequency[color]
        if old_frequency:
            exact_frequency[old_frequency] -= 1
            frequency_buckets[old_frequency // frequency_block] -= 1
        new_frequency = old_frequency + delta
        color_frequency[color] = new_frequency
        if new_frequency:
            exact_frequency[new_frequency] += 1
            frequency_buckets[new_frequency // frequency_block] += 1

    def at_least(threshold: int) -> int:
        if threshold > size:
            return 0
        block = threshold // frequency_block
        boundary = min(size + 1, (block + 1) * frequency_block)
        answer = sum(exact_frequency[threshold:boundary])
        for later_block in range(block + 1, bucket_count):
            answer += frequency_buckets[later_block]
        return answer

    answers = [0] * len(queries)
    current_left = 0
    current_right = -1
    for left, right, threshold, query_index in ordered:
        while current_left > left:
            current_left -= 1
            change(current_left, 1)
        while current_right < right:
            current_right += 1
            change(current_right, 1)
        while current_left < left:
            change(current_left, -1)
            current_left += 1
        while current_right > right:
            change(current_right, -1)
            current_right -= 1
        answers[query_index] = at_least(threshold)

    return answers
```

## 7. Why the expert solution is correct

The Euler interval of a vertex contains exactly its subtree. Mo's pointer moves keep `color_frequency` equal to the frequencies in the current interval. Every change transfers one color between the correct exact-frequency buckets, so summing buckets from `k` upward counts exactly the colors occurring at least `k` times. Restoring original query indices restores source order.

The standard Mo bound is `O((n + q) sqrt(n))` window moves; frequency queries add `O(q sqrt(n))`. Space is `O(n + q)`.
