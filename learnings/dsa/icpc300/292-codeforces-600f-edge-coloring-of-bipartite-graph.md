# ICPC300 292: Codeforces 600F - Edge coloring of bipartite graph

**Source:** [Codeforces 600F - Edge coloring of bipartite graph](https://codeforces.com/problemset/problem/600/F)  
**Rating:** 2300  
**Pattern:** incremental coloring with alternating-color swaps  
**Goal:** Properly color every edge of a bipartite graph with the minimum
number of colors. Incident edges must have different colors.

## 1. First principles

The minimum is at least the maximum degree `delta`. Konig's line-coloring
theorem says a bipartite graph always attains exactly `delta`.

When inserting edge `(u, v)`, choose color `a` missing at `u` and color `b`
missing at `v`. If they differ, swap `a` and `b` throughout the alternating
component containing `u`. Color `b` becomes missing at `u` and remains missing
at `v`, so the new edge can use it.

## 2. Cases that decide correctness

- Disconnected bipartite components are independent.
- An odd cycle makes the source contract invalid.
- Isolated vertices do not increase `delta`.
- Alternating-component entries must be cleared before recoloring them.
- Colors returned by the functions are one-based.

## 3. Brute force: backtrack over `delta` colors

```python
def edge_coloring_brute(
    vertex_count: int,
    edges: list[tuple[int, int]],
) -> tuple[int, list[int]]:
    if type(vertex_count) is not int or vertex_count <= 0:
        raise ValueError("vertex_count must be positive")
    graph = [[] for _ in range(vertex_count)]
    degree = [0] * vertex_count
    for edge_index, (first, second) in enumerate(edges):
        if (
            type(first) is not int
            or type(second) is not int
            or not 0 <= first < vertex_count
            or not 0 <= second < vertex_count
            or first == second
        ):
            raise ValueError("invalid edge")
        graph[first].append(second)
        graph[second].append(first)
        degree[first] += 1
        degree[second] += 1

    colors = [-1] * vertex_count
    for start in range(vertex_count):
        if colors[start] != -1:
            continue
        colors[start] = 0
        stack = [start]
        while stack:
            vertex = stack.pop()
            for neighbor in graph[vertex]:
                if colors[neighbor] == -1:
                    colors[neighbor] = colors[vertex] ^ 1
                    stack.append(neighbor)
                elif colors[neighbor] == colors[vertex]:
                    raise ValueError("graph must be bipartite")

    delta = max(degree, default=0)
    answer = [-1] * len(edges)
    used = [set() for _ in range(vertex_count)]

    def search(edge_index: int) -> bool:
        if edge_index == len(edges):
            return True
        first, second = edges[edge_index]
        for color in range(delta):
            if color in used[first] or color in used[second]:
                continue
            answer[edge_index] = color
            used[first].add(color)
            used[second].add(color)
            if search(edge_index + 1):
                return True
            used[first].remove(color)
            used[second].remove(color)
        return False

    if not search(0):
        raise RuntimeError("bipartite graph must have a delta-edge-coloring")
    return delta, [color + 1 for color in answer]
```

**Complexity:** `O(delta^m)` time and `O(n + m)` space.

## 4. Better approach: rebuild a matching for each color

Regularize the graph to a `delta`-regular bipartite multigraph and repeatedly
remove perfect matchings. This proves the theorem constructively but needs a
full matching algorithm for every color.

## 5. Expert solution: insert edges and swap two-color components

```python
def minimum_bipartite_edge_coloring(
    vertex_count: int,
    edges: list[tuple[int, int]],
) -> tuple[int, list[int]]:
    if type(vertex_count) is not int or vertex_count <= 0:
        raise ValueError("vertex_count must be positive")
    graph = [[] for _ in range(vertex_count)]
    degree = [0] * vertex_count
    for first, second in edges:
        if (
            type(first) is not int
            or type(second) is not int
            or not 0 <= first < vertex_count
            or not 0 <= second < vertex_count
            or first == second
        ):
            raise ValueError("invalid edge")
        graph[first].append(second)
        graph[second].append(first)
        degree[first] += 1
        degree[second] += 1

    sides = [-1] * vertex_count
    for start in range(vertex_count):
        if sides[start] != -1:
            continue
        sides[start] = 0
        stack = [start]
        while stack:
            vertex = stack.pop()
            for neighbor in graph[vertex]:
                if sides[neighbor] == -1:
                    sides[neighbor] = sides[vertex] ^ 1
                    stack.append(neighbor)
                elif sides[neighbor] == sides[vertex]:
                    raise ValueError("graph must be bipartite")

    delta = max(degree, default=0)
    incident = [[-1] * delta for _ in range(vertex_count)]
    edge_colors = [-1] * len(edges)
    for edge_index, (first, second) in enumerate(edges):
        missing_first = incident[first].index(-1)
        missing_second = incident[second].index(-1)
        chosen = missing_first
        if missing_first != missing_second:
            component_edges: set[int] = set()
            seen = {first}
            stack = [first]
            while stack:
                vertex = stack.pop()
                for color in (missing_first, missing_second):
                    other_edge = incident[vertex][color]
                    if other_edge == -1:
                        continue
                    component_edges.add(other_edge)
                    edge_first, edge_second = edges[other_edge]
                    neighbor = edge_second if edge_first == vertex else edge_first
                    if neighbor not in seen:
                        seen.add(neighbor)
                        stack.append(neighbor)

            for other_edge in component_edges:
                edge_first, edge_second = edges[other_edge]
                old_color = edge_colors[other_edge]
                incident[edge_first][old_color] = -1
                incident[edge_second][old_color] = -1
            for other_edge in component_edges:
                edge_first, edge_second = edges[other_edge]
                old_color = edge_colors[other_edge]
                new_color = (
                    missing_second if old_color == missing_first else missing_first
                )
                edge_colors[other_edge] = new_color
                incident[edge_first][new_color] = other_edge
                incident[edge_second][new_color] = other_edge
            chosen = missing_second

        edge_colors[edge_index] = chosen
        incident[first][chosen] = edge_index
        incident[second][chosen] = edge_index
    return delta, [color + 1 for color in edge_colors]
```

### Why the expert code is correct

Two-color components are alternating paths or cycles, so swapping their colors
preserves proper coloring. The component from `u` cannot contain `v`: its path
would start with `b`, end with `a`, and have even length, while opposite sides
of a bipartite graph have only odd-length paths. Thus `b` is free at both new
edge endpoints.

**Complexity:** `O(m(n + delta))` time and `O(n * delta + m)` space.

## 6. What to remember

```text
bipartite edge chromatic number -> maximum degree
different missing colors -> swap their alternating component
proper coloring survives every swap
```
