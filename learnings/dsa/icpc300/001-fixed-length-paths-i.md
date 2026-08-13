# ICPC300 001: Fixed-Length Paths I

**Source:** [CSES - Fixed-Length Paths I](https://cses.fi/problemset/task/2080/)  
**Pattern:** centroid decomposition  
**Goal:** Count unordered pairs of distinct tree vertices whose simple path has
exactly `k` edges.

## 1. Problem in plain words

A tree has one and only one path between two vertices. We need count every
pair `{a, b}` for which that path length is `k`. `{a, b}` and `{b, a}` are the
same pair.

For this tree and `k = 2`:

```text
0 - 1 - 2
    |
    3
```

The valid pairs are `{0, 2}`, `{0, 3}`, and `{2, 3}`. The answer is `3`.

## 2. First principles

The direct idea is honest: start at each vertex, find distances to every other
vertex, and count the vertices at distance `k`. Count only destinations with a
larger index so each unordered pair is counted once.

That repeats nearly the same tree walk `n` times. The key question is:

> Can one vertex split many paths into independent smaller problems?

A **centroid** is a vertex whose removal leaves no component with more than
half of the current vertices. Every recursive component is therefore at most
half as large. A path either:

1. stays completely inside one child component of the centroid, or
2. passes through the centroid.

Count case 2 once at this centroid. Then recurse to handle case 1. No pair can
be counted at two centroids because the first removed centroid on its path is
unique.

## 3. Cases that decide correctness

| Case | What must happen |
| --- | --- |
| `k = 0` | Return `0`: a pair needs two distinct vertices. |
| `k >= n` | Return `0`: a tree path has at most `n - 1` edges. |
| A chain | The centroid may have two large sides; pairs crossing it still count once. |
| A star | The centroid is the centre; every two leaves are a distance-two pair. |
| One child subtree | Do not count two vertices from that subtree at this centroid; its recursive call owns them. |

## 4. Brute force: run a tree search from every start

For every `start`, perform DFS and count only `end > start` at distance `k`.
This is the smallest correct oracle for random testing.

```python
def count_pairs_brute_force(graph: list[list[int]], distance_needed: int) -> int:
    vertex_count = len(graph)
    if distance_needed == 0 or distance_needed >= vertex_count:
        return 0

    answer = 0
    for start in range(vertex_count):
        distance = [-1] * vertex_count
        distance[start] = 0
        stack = [start]

        while stack:
            node = stack.pop()
            if distance[node] == distance_needed:
                if node > start:
                    answer += 1
                continue

            for neighbor in graph[node]:
                if distance[neighbor] == -1:
                    distance[neighbor] = distance[node] + 1
                    stack.append(neighbor)

    return answer
```

**Why it works:** DFS visits every vertex exactly once from `start`, so its
stored distance is the unique tree-path length. The `end > start` test removes
the mirrored duplicate.

**Complexity:** `O(n^2)` time and `O(n)` extra space. It cannot handle the
source limit near `2 * 10^5`.

## 5. Better: dynamic programming when `k` is small

Root the tree. Let `dp[u][d]` be the number of vertices in the already merged
part of `u`'s subtree at distance `d` from `u`.

When merging child `v`, a vertex already stored at distance `a` from `u` pairs
with a vertex at distance `b` from `v` exactly when:

```text
a + 1 + b = k
```

After counting those crossing pairs, move `v`'s distances one step farther
from `u` and merge them. Each pair is created at its lowest common ancestor.

```python
def count_pairs_tree_dp(graph: list[list[int]], distance_needed: int) -> int:
    vertex_count = len(graph)
    if distance_needed == 0 or distance_needed >= vertex_count:
        return 0

    answer = 0

    def dfs(node: int, parent: int) -> list[int]:
        nonlocal answer
        counts = [0] * (distance_needed + 1)
        counts[0] = 1

        for child in graph[node]:
            if child == parent:
                continue
            child_counts = dfs(child, node)

            for from_node in range(distance_needed):
                answer += counts[from_node] * child_counts[distance_needed - 1 - from_node]

            for from_child in range(distance_needed):
                counts[from_child + 1] += child_counts[from_child]

        return counts

    dfs(0, -1)
    return answer
```

**Why it is better:** no path is walked from every start. The state reuses a
child's distance counts for all pairs that meet at its parent.

**Complexity:** `O(nk)` time and `O(nk)` worst-case memory from recursive
states. This is excellent for small `k`, but `k` can be close to `n`, making it
quadratic again.

## 6. Expert solution: centroid decomposition

At centroid `c`, collect distances from `c` to every vertex in each child
component, but stop once the distance exceeds `k`; larger distances can never
help.

Let `all_distances` contain `0` for the centroid and every collected distance.
The number of pairs in it that sum to `k` includes every path passing through
`c`, **plus** pairs entirely inside one child component. Subtract the latter by
running the same sum count for each child list separately.

```text
answer at c = pairs(all_distances, k)
              - sum(pairs(distances_of_one_child, k))
```

Then remove `c` and solve each remaining component. Because each component is
at most half as big, a vertex participates in `O(log n)` centroid levels.

```python
from collections import Counter
import sys


def count_pairs_centroid(graph: list[list[int]], distance_needed: int) -> int:
    vertex_count = len(graph)
    if distance_needed == 0 or distance_needed >= vertex_count:
        return 0

    sys.setrecursionlimit(max(1_000_000, vertex_count * 3))
    removed = [False] * vertex_count
    subtree_size = [0] * vertex_count
    answer = 0

    def calculate_size(node: int, parent: int) -> int:
        subtree_size[node] = 1
        for neighbor in graph[node]:
            if neighbor != parent and not removed[neighbor]:
                subtree_size[node] += calculate_size(neighbor, node)
        return subtree_size[node]

    def find_centroid(node: int, parent: int, total_size: int) -> int:
        for neighbor in graph[node]:
            if neighbor != parent and not removed[neighbor]:
                if subtree_size[neighbor] > total_size // 2:
                    return find_centroid(neighbor, node, total_size)
        return node

    def collect_distances(node: int, parent: int, distance: int, values: list[int]) -> None:
        if distance > distance_needed:
            return
        values.append(distance)
        for neighbor in graph[node]:
            if neighbor != parent and not removed[neighbor]:
                collect_distances(neighbor, node, distance + 1, values)

    def count_sums(values: list[int]) -> int:
        frequencies = Counter(values)
        total = 0
        for distance, count in frequencies.items():
            complement = distance_needed - distance
            if complement < distance:
                continue
            if complement == distance:
                total += count * (count - 1) // 2
            else:
                total += count * frequencies[complement]
        return total

    def decompose(start: int) -> None:
        nonlocal answer
        total_size = calculate_size(start, -1)
        centroid = find_centroid(start, -1, total_size)
        removed[centroid] = True

        all_distances = [0]
        child_distance_lists: list[list[int]] = []
        for neighbor in graph[centroid]:
            if removed[neighbor]:
                continue
            distances: list[int] = []
            collect_distances(neighbor, centroid, 1, distances)
            all_distances.extend(distances)
            child_distance_lists.append(distances)

        answer += count_sums(all_distances)
        for distances in child_distance_lists:
            answer -= count_sums(distances)

        for neighbor in graph[centroid]:
            if not removed[neighbor]:
                decompose(neighbor)

    decompose(0)
    return answer
```

### Why the expert code is correct

- `count_sums(all_distances)` counts every pair whose route through this
  centroid has length `k`.
- A pair inside one child component does not use the centroid; it is the only
  overcount, and its child's subtraction removes it.
- All remaining pairs lie fully inside exactly one component after removal and
  are counted by that recursive call.
- These cases are disjoint and cover every pair.

**Complexity:** `O(n log n)` expected/practical time and `O(n)` auxiliary
memory, excluding the input graph. Each decomposition level scans all vertices
in its components, and there are at most `O(log n)` levels.

## 7. What to remember

```text
count pairs at fixed tree distance
    small k       -> tree DP, O(nk)
    large k       -> centroid decomposition, O(n log n)

At a centroid:
all child distances together
    minus distances inside each one child
    = paths that pass through the centroid exactly once
```
