# ICPC300 298: Codeforces 1551F - Equidistant Vertices

**Source:** [Codeforces 1551F - Equidistant Vertices](https://codeforces.com/problemset/problem/1551/F)  
**Rating:** 2300  
**Pattern:** choose equal-depth vertices from distinct center branches  
**Goal:** Count size-`chosen_count` vertex sets in a tree for which every pair
of chosen vertices has the same distance, modulo `1_000_000_007`.

## 1. First principles

For at least three equidistant tree vertices, their paths meet at one vertex
center. Every chosen vertex has the same depth from that center and lies in a
different incident branch.

For each center and depth, count eligible vertices in every branch. The
`chosen_count`-th elementary symmetric sum of those branch counts chooses one
vertex from each of distinct branches.

## 2. Cases that decide correctness

- One chosen vertex gives `n` singleton sets.
- Every pair of vertices is equidistant internally, so `k = 2` gives `C(n, 2)`.
- For `k >= 3`, an edge midpoint cannot be the common center.
- Chosen vertices may not share the same first branch from the center.
- The input must be a tree.

## 3. Brute force: test every vertex subset

```python
from collections import deque
from itertools import combinations


MODULO = 1_000_000_007


def equidistant_vertex_sets_brute(
    vertex_count: int,
    edges: list[tuple[int, int]],
    chosen_count: int,
) -> int:
    if (
        type(vertex_count) is not int
        or vertex_count <= 0
        or type(chosen_count) is not int
        or not 1 <= chosen_count <= vertex_count
        or len(edges) != vertex_count - 1
    ):
        raise ValueError("invalid tree size or chosen_count")
    graph = [[] for _ in range(vertex_count)]
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

    distances = []
    for start in range(vertex_count):
        distance = [-1] * vertex_count
        distance[start] = 0
        queue = deque([start])
        while queue:
            vertex = queue.popleft()
            for neighbor in graph[vertex]:
                if distance[neighbor] == -1:
                    distance[neighbor] = distance[vertex] + 1
                    queue.append(neighbor)
        if -1 in distance:
            raise ValueError("tree must be connected")
        distances.append(distance)

    answer = 0
    for chosen in combinations(range(vertex_count), chosen_count):
        pair_distances = {
            distances[first][second] for first, second in combinations(chosen, 2)
        }
        answer += len(pair_distances) <= 1
    return answer % MODULO
```

**Complexity:** `O(n^2 + C(n, k) k^2)` time and `O(n^2)` space.

## 4. Better approach: enumerate a center and explicit branch choices

After fixing a center and depth, recursively choose distinct branches and one
vertex from each. The elementary-symmetric DP aggregates all such choices in
`O(degree * k)` instead of enumerating them.

## 5. Expert solution: branch-depth counts and symmetric-sum DP

```python
MODULO = 1_000_000_007


def equidistant_vertex_sets(
    vertex_count: int,
    edges: list[tuple[int, int]],
    chosen_count: int,
) -> int:
    if (
        type(vertex_count) is not int
        or vertex_count <= 0
        or type(chosen_count) is not int
        or not 1 <= chosen_count <= vertex_count
        or len(edges) != vertex_count - 1
    ):
        raise ValueError("invalid tree size or chosen_count")
    graph = [[] for _ in range(vertex_count)]
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
    reached = {0}
    stack = [(0, -1)]
    while stack:
        vertex, parent = stack.pop()
        for neighbor in graph[vertex]:
            if neighbor == parent:
                continue
            if neighbor in reached:
                raise ValueError("edges must describe a tree")
            reached.add(neighbor)
            stack.append((neighbor, vertex))
    if len(reached) != vertex_count:
        raise ValueError("tree must be connected")

    if chosen_count == 1:
        return vertex_count
    if chosen_count == 2:
        return vertex_count * (vertex_count - 1) // 2 % MODULO

    answer = 0
    for center in range(vertex_count):
        branch_counts = []
        for neighbor in graph[center]:
            counts = [0] * vertex_count
            stack = [(neighbor, center, 1)]
            while stack:
                vertex, parent, depth = stack.pop()
                counts[depth] += 1
                for next_vertex in graph[vertex]:
                    if next_vertex != parent:
                        stack.append((next_vertex, vertex, depth + 1))
            branch_counts.append(counts)

        for depth in range(1, vertex_count):
            dp = [0] * (chosen_count + 1)
            dp[0] = 1
            for counts in branch_counts:
                available = counts[depth]
                for chosen in range(chosen_count, 0, -1):
                    dp[chosen] += dp[chosen - 1] * available
                    dp[chosen] %= MODULO
            answer = (answer + dp[chosen_count]) % MODULO
    return answer
```

### Why the expert code is correct

Every set of at least three pairwise-equidistant tree vertices has one unique
vertex center, one common depth, and distinct center branches. The outer loops
select that unique center and depth; the symmetric-sum DP counts exactly one
choice from each selected branch, so every valid set is counted once.

**Complexity:** `O(n^3 k)` time in a direct worst-case bound and `O(n^2 + k)`
working space.

## 6. What to remember

```text
three or more equidistant tree vertices -> unique vertex center
same radius -> one depth layer
different first edges -> elementary symmetric sum of branch counts
```
