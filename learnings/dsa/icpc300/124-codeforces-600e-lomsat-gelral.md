# ICPC300 124: Codeforces 600E - Lomsat gelral

**Source:** [Codeforces 600E](https://codeforces.com/problemset/problem/600/E)  
**Pattern:** small-to-large subtree frequency merging

## Exact contract

A tree rooted at vertex `1` has one positive color number on every vertex. For
each vertex `v`, consider its rooted subtree. Among the colors with maximum
frequency in that subtree, output the sum of their color numbers.

## First principles

The answer needs an entire frequency map, not only the best color: maps from
different child subtrees must be combined. Always retain the largest child map
and insert every entry from smaller maps into it. Whenever a color's merged
frequency exceeds the current maximum, replace the sum; when it ties, add the
color.

An entry moved from a smaller map enters a map at least twice as large. Hence
each color entry moves only `O(log n)` times over the whole tree.

## Cases that decide correctness

- The subtree is defined by root `1`, not by an arbitrary local orientation.
- Several colors can tie for maximum frequency; sum each color once.
- Color numbers need not be dense, so dictionary keys are appropriate.
- A leaf's answer is its own color.
- Preserve each child's finished answer before its map is reused by an
  ancestor.

## Brute force: recount every subtree independently

```python
from collections import Counter


def lomsat_recount(colors: list[int], edges: list[tuple[int, int]]) -> list[int]:
    vertex_count = len(colors)
    graph = [[] for _ in range(vertex_count)]
    for first, second in edges:
        graph[first - 1].append(second - 1)
        graph[second - 1].append(first - 1)

    parent = [-1] * vertex_count
    parent[0] = 0
    order = [0]
    for vertex in order:
        for neighbor in graph[vertex]:
            if parent[neighbor] == -1:
                parent[neighbor] = vertex
                order.append(neighbor)

    answers = []
    for root in range(vertex_count):
        frequencies: Counter[int] = Counter()
        stack = [root]
        while stack:
            vertex = stack.pop()
            frequencies[colors[vertex]] += 1
            stack.extend(
                neighbor for neighbor in graph[vertex] if parent[neighbor] == vertex
            )
        maximum = max(frequencies.values())
        answers.append(
            sum(color for color, count in frequencies.items() if count == maximum)
        )
    return answers
```

Long chains make the total work quadratic.

## Better: Mo's algorithm on Euler subtree intervals

```python
from math import isqrt


def lomsat_mo(colors: list[int], edges: list[tuple[int, int]]) -> list[int]:
    vertex_count = len(colors)
    graph = [[] for _ in range(vertex_count)]
    for first, second in edges:
        graph[first - 1].append(second - 1)
        graph[second - 1].append(first - 1)

    parent = [-1] * vertex_count
    parent[0] = 0
    children = [[] for _ in range(vertex_count)]
    order = [0]
    for vertex in order:
        for neighbor in graph[vertex]:
            if parent[neighbor] == -1:
                parent[neighbor] = vertex
                children[vertex].append(neighbor)
                order.append(neighbor)

    entry = [0] * vertex_count
    exit_time = [0] * vertex_count
    euler = []
    stack = [(0, False)]
    while stack:
        vertex, exiting = stack.pop()
        if exiting:
            exit_time[vertex] = len(euler)
            continue
        entry[vertex] = len(euler)
        euler.append(vertex)
        stack.append((vertex, True))
        for child in reversed(children[vertex]):
            stack.append((child, False))

    block_size = isqrt(vertex_count) + 1
    queries = [(entry[v], exit_time[v], v) for v in range(vertex_count)]
    queries.sort(
        key=lambda query: (
            query[0] // block_size,
            query[1] if (query[0] // block_size) % 2 == 0 else -query[1],
        )
    )

    frequencies: dict[int, int] = {}
    sum_at_frequency = [0] * (vertex_count + 1)
    maximum_frequency = 0
    current_left = 0
    current_right = 0
    answers = [0] * vertex_count

    def add(position: int) -> None:
        nonlocal maximum_frequency
        color = colors[euler[position]]
        old_frequency = frequencies.get(color, 0)
        if old_frequency:
            sum_at_frequency[old_frequency] -= color
        new_frequency = old_frequency + 1
        frequencies[color] = new_frequency
        sum_at_frequency[new_frequency] += color
        maximum_frequency = max(maximum_frequency, new_frequency)

    def remove(position: int) -> None:
        nonlocal maximum_frequency
        color = colors[euler[position]]
        old_frequency = frequencies[color]
        sum_at_frequency[old_frequency] -= color
        new_frequency = old_frequency - 1
        frequencies[color] = new_frequency
        if new_frequency:
            sum_at_frequency[new_frequency] += color
        while maximum_frequency and not sum_at_frequency[maximum_frequency]:
            maximum_frequency -= 1

    for query_left, query_right, vertex in queries:
        while current_left > query_left:
            current_left -= 1
            add(current_left)
        while current_right < query_right:
            add(current_right)
            current_right += 1
        while current_left < query_left:
            remove(current_left)
            current_left += 1
        while current_right > query_right:
            current_right -= 1
            remove(current_right)
        answers[vertex] = sum_at_frequency[maximum_frequency]
    return answers
```

Every subtree is one Euler interval, so Mo's ordering reduces pointer movement
to about `O(n sqrt n)` while maintaining exact frequency sums.

## Expert solution: retain the largest child map

```python
import sys


def solve() -> None:
    input_stream = sys.stdin.buffer
    vertex_count = int(input_stream.readline())
    colors = list(map(int, input_stream.readline().split()))
    graph = [[] for _ in range(vertex_count)]
    for _ in range(vertex_count - 1):
        first, second = map(int, input_stream.readline().split())
        graph[first - 1].append(second - 1)
        graph[second - 1].append(first - 1)

    parent = [-1] * vertex_count
    parent[0] = 0
    children = [[] for _ in range(vertex_count)]
    order = [0]
    for vertex in order:
        for neighbor in graph[vertex]:
            if parent[neighbor] == -1:
                parent[neighbor] = vertex
                children[vertex].append(neighbor)
                order.append(neighbor)

    frequency_maps: list[dict[int, int] | None] = [None] * vertex_count
    maximum_frequency = [0] * vertex_count
    maximum_sum = [0] * vertex_count

    for vertex in reversed(order):
        heavy_child = max(
            children[vertex],
            key=lambda child: len(frequency_maps[child]),
            default=-1,
        )
        if heavy_child == -1:
            frequencies: dict[int, int] = {}
            best_frequency = 0
            best_sum = 0
        else:
            heavy_map = frequency_maps[heavy_child]
            if heavy_map is None:
                raise RuntimeError("child map was not built")
            frequencies = heavy_map
            best_frequency = maximum_frequency[heavy_child]
            best_sum = maximum_sum[heavy_child]

        for child in children[vertex]:
            if child == heavy_child:
                continue
            child_map = frequency_maps[child]
            if child_map is None:
                raise RuntimeError("child map was not built")
            for color, count in child_map.items():
                new_count = frequencies.get(color, 0) + count
                frequencies[color] = new_count
                if new_count > best_frequency:
                    best_frequency = new_count
                    best_sum = color
                elif new_count == best_frequency:
                    best_sum += color

        color = colors[vertex]
        new_count = frequencies.get(color, 0) + 1
        frequencies[color] = new_count
        if new_count > best_frequency:
            best_frequency = new_count
            best_sum = color
        elif new_count == best_frequency:
            best_sum += color

        frequency_maps[vertex] = frequencies
        maximum_frequency[vertex] = best_frequency
        maximum_sum[vertex] = best_sum
        for child in children[vertex]:
            frequency_maps[child] = None

    print(" ".join(map(str, maximum_sum)))


if __name__ == "__main__":
    solve()
```

At each vertex the retained dictionary becomes the exact multiset of its
subtree, and `best_frequency/best_sum` are updated on every changed key. The
doubling argument bounds all dictionary-entry moves.

**Complexity:** `O(n log n)` expected time and `O(n)` stored entries.
