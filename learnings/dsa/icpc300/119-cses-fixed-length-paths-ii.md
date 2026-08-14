# ICPC300 119: CSES - Fixed-Length Paths II

**Source:** [CSES - Fixed-Length Paths II](https://cses.fi/problemset/task/2081/)  
**Pattern:** centroid decomposition with depth frequencies  
**Goal:** Count unordered pairs of distinct tree vertices whose path length is
between `minimum_distance` and `maximum_distance`, inclusive.

## 1. First principles

At a centroid, every path counted now must either use the centroid or connect
two different components left after removing it. If their depths from the
centroid are `a` and `b`, the path length is `a + b`.

Count all depth pairs around the centroid, subtract pairs lying in the same
neighbor component, then recurse. Every vertex pair is counted at the first
centroid that separates its endpoints.

## 2. Cases that decide correctness

- Pairs are unordered and a vertex is never paired with itself.
- Both distance bounds are inclusive.
- `minimum_distance = 0` still contributes no self-pairs.
- Bounds above the tree diameter simply contribute nothing extra.
- The input must contain exactly one connected, acyclic tree.

## 3. Brute force: traverse from every start vertex

```python
from collections import deque


def fixed_length_paths_brute(
    vertex_count: int,
    edges: list[tuple[int, int]],
    minimum_distance: int,
    maximum_distance: int,
) -> int:
    if vertex_count <= 0:
        raise ValueError("vertex_count must be positive")
    if not 0 <= minimum_distance <= maximum_distance:
        raise ValueError("invalid distance interval")
    if len(edges) != vertex_count - 1:
        raise ValueError("a tree must have vertex_count - 1 edges")
    graph = [[] for _ in range(vertex_count)]
    for first, second in edges:
        if not 0 <= first < vertex_count or not 0 <= second < vertex_count:
            raise ValueError("edge endpoint out of range")
        graph[first].append(second)
        graph[second].append(first)

    answer = 0
    for start in range(vertex_count):
        distance = [-1] * vertex_count
        distance[start] = 0
        queue = deque([start])
        while queue:
            node = queue.popleft()
            for neighbor in graph[node]:
                if distance[neighbor] == -1:
                    distance[neighbor] = distance[node] + 1
                    queue.append(neighbor)
        if any(value == -1 for value in distance):
            raise ValueError("edges must form a connected tree")
        answer += sum(
            minimum_distance <= distance[end] <= maximum_distance
            for end in range(start + 1, vertex_count)
        )
    return answer
```

**Complexity:** `O(V^2)` time and `O(V+E)` space.

## 4. Better: merge bounded depth distributions

```python
import sys


def fixed_length_paths_tree_dp(
    vertex_count: int,
    edges: list[tuple[int, int]],
    minimum_distance: int,
    maximum_distance: int,
) -> int:
    if vertex_count <= 0:
        raise ValueError("vertex_count must be positive")
    if not 0 <= minimum_distance <= maximum_distance:
        raise ValueError("invalid distance interval")
    if len(edges) != vertex_count - 1:
        raise ValueError("a tree must have vertex_count - 1 edges")
    graph = [[] for _ in range(vertex_count)]
    for first, second in edges:
        if not 0 <= first < vertex_count or not 0 <= second < vertex_count:
            raise ValueError("edge endpoint out of range")
        graph[first].append(second)
        graph[second].append(first)

    sys.setrecursionlimit(max(1_000, 2 * vertex_count + 10))
    limit = min(maximum_distance, vertex_count - 1)
    visited = [False] * vertex_count
    answer = 0

    def visit(node: int, parent: int) -> list[int]:
        nonlocal answer
        if visited[node]:
            raise ValueError("edges must form an acyclic tree")
        visited[node] = True
        counts = [1]
        for neighbor in graph[node]:
            if neighbor == parent:
                continue
            child_counts = visit(neighbor, node)
            prefix = [0]
            for count in child_counts:
                prefix.append(prefix[-1] + count)
            for first_depth, first_count in enumerate(counts):
                low = max(0, minimum_distance - first_depth - 1)
                high = min(
                    len(child_counts) - 1,
                    limit - first_depth - 1,
                )
                if low <= high:
                    answer += first_count * (prefix[high + 1] - prefix[low])
            needed = min(limit + 1, len(child_counts) + 1)
            if len(counts) < needed:
                counts.extend([0] * (needed - len(counts)))
            for depth, count in enumerate(child_counts):
                if depth + 1 > limit:
                    break
                counts[depth + 1] += count
        return counts

    visit(0, -1)
    if not all(visited):
        raise ValueError("edges must form a connected tree")
    return answer
```

**Complexity:** `O(V * maximum_distance)` time and up to
`O(V * maximum_distance)` space.

## 5. Expert solution: centroid decomposition

```python
import sys


def fixed_length_paths_centroid(
    vertex_count: int,
    edges: list[tuple[int, int]],
    minimum_distance: int,
    maximum_distance: int,
) -> int:
    if vertex_count <= 0:
        raise ValueError("vertex_count must be positive")
    if not 0 <= minimum_distance <= maximum_distance:
        raise ValueError("invalid distance interval")
    if len(edges) != vertex_count - 1:
        raise ValueError("a tree must have vertex_count - 1 edges")
    graph = [[] for _ in range(vertex_count)]
    for first, second in edges:
        if not 0 <= first < vertex_count or not 0 <= second < vertex_count:
            raise ValueError("edge endpoint out of range")
        graph[first].append(second)
        graph[second].append(first)

    seen = {0}
    stack = [0]
    while stack:
        node = stack.pop()
        for neighbor in graph[node]:
            if neighbor not in seen:
                seen.add(neighbor)
                stack.append(neighbor)
    if len(seen) != vertex_count:
        raise ValueError("edges must form a connected tree")

    sys.setrecursionlimit(max(1_000, 2 * vertex_count + 10))
    removed = [False] * vertex_count
    subtree_size = [0] * vertex_count
    answer = 0

    def calculate_sizes(node: int, parent: int) -> int:
        subtree_size[node] = 1
        for neighbor in graph[node]:
            if neighbor != parent and not removed[neighbor]:
                subtree_size[node] += calculate_sizes(neighbor, node)
        return subtree_size[node]

    def find_centroid(node: int, parent: int, total: int) -> int:
        for neighbor in graph[node]:
            if (
                neighbor != parent
                and not removed[neighbor]
                and subtree_size[neighbor] > total // 2
            ):
                return find_centroid(neighbor, node, total)
        return node

    def collect_depths(node: int, parent: int, depth: int, counts: list[int]) -> None:
        if depth > maximum_distance:
            return
        if len(counts) <= depth:
            counts.extend([0] * (depth + 1 - len(counts)))
        counts[depth] += 1
        for neighbor in graph[node]:
            if neighbor != parent and not removed[neighbor]:
                collect_depths(neighbor, node, depth + 1, counts)

    def count_at_most(counts: list[int], limit: int) -> int:
        if limit < 0:
            return 0
        prefix: list[int] = []
        running = 0
        for count in counts:
            running += count
            prefix.append(running)
        ordered_pairs = 0
        self_pairs = 0
        for depth, count in enumerate(counts):
            maximum_other = min(len(counts) - 1, limit - depth)
            if maximum_other >= 0:
                ordered_pairs += count * prefix[maximum_other]
            if 2 * depth <= limit:
                self_pairs += count
        return (ordered_pairs - self_pairs) // 2

    def count_in_range(counts: list[int]) -> int:
        return count_at_most(counts, maximum_distance) - count_at_most(
            counts, minimum_distance - 1
        )

    def decompose(entry: int) -> None:
        nonlocal answer
        total = calculate_sizes(entry, -1)
        centroid = find_centroid(entry, -1, total)
        all_counts = [1]
        for neighbor in graph[centroid]:
            if removed[neighbor]:
                continue
            child_counts: list[int] = []
            collect_depths(neighbor, centroid, 1, child_counts)
            answer -= count_in_range(child_counts)
            if len(all_counts) < len(child_counts):
                all_counts.extend([0] * (len(child_counts) - len(all_counts)))
            for depth, count in enumerate(child_counts):
                all_counts[depth] += count
        answer += count_in_range(all_counts)
        removed[centroid] = True
        for neighbor in graph[centroid]:
            if not removed[neighbor]:
                decompose(neighbor)

    decompose(0)
    return answer
```

### Why the expert code is correct

The all-depth count includes exactly the pairs whose endpoints surround the
centroid, plus pairs from the same remaining component. Subtracting each
child's internal depth pairs leaves exactly the paths separated by this
centroid. Recursion handles every subtracted pair later, at one unique first
separating centroid.

**Complexity:** `O(V log V)` time and `O(V)` space.

## 6. What to remember

```text
path through a centroid -> sum of endpoint depths
same child component -> subtract now and count recursively
each centroid level touches every remaining vertex once
```
