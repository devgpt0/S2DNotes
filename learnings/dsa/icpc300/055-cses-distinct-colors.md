# ICPC300 055: CSES - Distinct Colors

**Source:** [CSES - Distinct Colors](https://cses.fi/problemset/task/1139/)  
**Pattern:** Euler tour + offline distinct-range queries  
**Goal:** For every rooted-tree vertex, count the distinct colors in its
subtree.

The tree is rooted at vertex `0`.

## 1. First principles

A depth-first preorder places every subtree in one contiguous interval:

```text
subtree(node) = euler[tin[node] : tout[node] + 1]
```

The problem becomes one distinct-value query per interval. Sweep interval
right endpoints. Keep a Fenwick marker only at the latest processed occurrence
of each color; the marker sum over a subtree interval is its distinct count.

## 2. Cases that decide correctness

| Case | Required behavior |
| --- | --- |
| Leaf | Return `1`. |
| Every color equal | Every subtree returns `1`. |
| Every color different | Return the subtree size. |
| Same color inside and before a subtree interval | Count it only if an occurrence lies inside. |
| Root | Its interval contains every vertex. |

## 3. Brute force: collect every subtree separately

Root the tree once, then traverse each vertex's descendants into a set.

```python
def distinct_colors_brute(graph: list[list[int]], colors: list[int]) -> list[int]:
    if not graph or len(graph) != len(colors):
        raise ValueError("graph and colors must have the same nonzero size")

    parent = [-2] * len(graph)
    parent[0] = -1
    order: list[int] = []
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
            stack.append(neighbor)
    if len(order) != len(graph):
        raise ValueError("graph must be connected")

    answers = [0] * len(graph)
    for root in range(len(graph)):
        subtree_colors: set[int] = set()
        stack = [root]
        while stack:
            node = stack.pop()
            subtree_colors.add(colors[node])
            for neighbor in graph[node]:
                if parent[neighbor] == node:
                    stack.append(neighbor)
        answers[root] = len(subtree_colors)
    return answers
```

**Complexity:** `O(n^2)` time and `O(n)` temporary space.

## 4. Better: merge smaller color sets into larger sets

Process vertices in postorder. Always merge the smaller set into the larger
one, so any stored color moves only when its destination size at least doubles.

```python
def distinct_colors_small_to_large(
    graph: list[list[int]], colors: list[int]
) -> list[int]:
    if not graph or len(graph) != len(colors):
        raise ValueError("graph and colors must have the same nonzero size")

    parent = [-2] * len(graph)
    parent[0] = -1
    order: list[int] = []
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
            stack.append(neighbor)
    if len(order) != len(graph):
        raise ValueError("graph must be connected")

    color_sets: list[set[int]] = [set() for _ in graph]
    answers = [0] * len(graph)
    for node in reversed(order):
        merged = {colors[node]}
        for neighbor in graph[node]:
            if parent[neighbor] != node:
                continue
            child_colors = color_sets[neighbor]
            if len(merged) < len(child_colors):
                merged, child_colors = child_colors, merged
            merged.update(child_colors)
        color_sets[node] = merged
        answers[node] = len(merged)
    return answers
```

**Complexity:** `O(n log n)` expected time and `O(n)` stored colors.

## 5. Expert solution: Euler tour and Fenwick sweep

Flatten the tree, convert each subtree to an interval, and answer all intervals
in increasing right-endpoint order.

```python
def distinct_colors_fenwick(graph: list[list[int]], colors: list[int]) -> list[int]:
    if not graph or len(graph) != len(colors):
        raise ValueError("graph and colors must have the same nonzero size")

    vertex_count = len(graph)
    parent = [-2] * vertex_count
    entry = [0] * vertex_count
    order: list[int] = []
    parent[0] = -1
    stack = [0]
    while stack:
        node = stack.pop()
        entry[node] = len(order)
        order.append(node)
        for neighbor in graph[node]:
            if neighbor == parent[node]:
                continue
            if parent[neighbor] != -2:
                raise ValueError("graph must be a tree")
            parent[neighbor] = node
            stack.append(neighbor)
    if len(order) != vertex_count:
        raise ValueError("graph must be connected")

    subtree_size = [1] * vertex_count
    for node in reversed(order):
        if parent[node] != -1:
            subtree_size[parent[node]] += subtree_size[node]
    exit_position = [
        entry[node] + subtree_size[node] - 1 for node in range(vertex_count)
    ]
    euler_colors = [colors[node] for node in order]

    tree = [0] * (vertex_count + 1)

    def add(index: int, difference: int) -> None:
        index += 1
        while index < len(tree):
            tree[index] += difference
            index += index & -index

    def prefix_sum(end: int) -> int:
        total = 0
        while end > 0:
            total += tree[end]
            end -= end & -end
        return total

    answers = [0] * vertex_count
    last_position: dict[int, int] = {}
    current_right = -1
    for node in sorted(range(vertex_count), key=exit_position.__getitem__):
        right = exit_position[node]
        while current_right < right:
            current_right += 1
            color = euler_colors[current_right]
            previous = last_position.get(color)
            if previous is not None:
                add(previous, -1)
            add(current_right, 1)
            last_position[color] = current_right
        answers[node] = prefix_sum(right + 1) - prefix_sum(entry[node])
    return answers
```

### Why the expert code is correct

- DFS preorder makes every subtree exactly one interval.
- At each processed right endpoint, one marker exists at the latest occurrence
  of every color in the prefix.
- A color appears in a subtree interval exactly when its latest occurrence up
  to that interval's right endpoint is not before the interval's left endpoint.

**Complexity:** `O(n log n)` time and `O(n)` space.

## 6. What to remember

```text
subtree -> Euler interval
distinct interval query -> keep one latest-occurrence marker per color
Fenwick interval sum -> distinct subtree colors
```
