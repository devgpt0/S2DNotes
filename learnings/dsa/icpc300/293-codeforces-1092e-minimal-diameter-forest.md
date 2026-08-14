# ICPC300 293: Codeforces 1092E - Minimal Diameter Forest

**Source:** [Codeforces 1092E - Minimal Diameter Forest](https://codeforces.com/problemset/problem/1092/E)  
**Rating:** 2200  
**Pattern:** component diameters and a star of tree centers  
**Goal:** Add edges to a forest until it becomes one tree. Minimize its
diameter and return both that diameter and the added edges.

## 1. First principles

Connecting a component through a vertex with eccentricity `r` can expose a
path of length at least `r`, so its center is always optimal and its cost is the
component radius.

Choose the center of a maximum-radius component as a hub and join every other
component center to it. Any tree connecting three components must pay either
two radii plus one edge or three radii plus two edges; the center star attains
those lower bounds.

## 2. Cases that decide correctness

- An already connected tree needs no added edge.
- An isolated vertex has diameter and radius zero.
- Either middle vertex of an odd-length diameter path is a valid center.
- The input must be acyclic.
- Added edges connect different original components.

## 3. Brute force: enumerate cross-component edge sets

```python
from collections import deque
from itertools import combinations


def minimum_forest_diameter_brute(
    vertex_count: int,
    edges: list[tuple[int, int]],
) -> int:
    if type(vertex_count) is not int or vertex_count <= 0:
        raise ValueError("vertex_count must be positive")
    graph = [[] for _ in range(vertex_count)]
    parent = list(range(vertex_count))

    def find(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for first, second in edges:
        if (
            type(first) is not int
            or type(second) is not int
            or not 0 <= first < vertex_count
            or not 0 <= second < vertex_count
            or first == second
        ):
            raise ValueError("invalid edge")
        first_root = find(first)
        second_root = find(second)
        if first_root == second_root:
            raise ValueError("edges must form a forest")
        parent[first_root] = second_root
        graph[first].append(second)
        graph[second].append(first)

    component = [find(vertex) for vertex in range(vertex_count)]
    component_count = len(set(component))
    candidates = [
        (first, second)
        for first in range(vertex_count)
        for second in range(first + 1, vertex_count)
        if component[first] != component[second]
    ]

    def diameter(extra: tuple[tuple[int, int], ...]) -> int | None:
        augmented = [neighbors.copy() for neighbors in graph]
        for first, second in extra:
            augmented[first].append(second)
            augmented[second].append(first)
        best = 0
        for start in range(vertex_count):
            distance = [-1] * vertex_count
            distance[start] = 0
            queue = deque([start])
            while queue:
                vertex = queue.popleft()
                for neighbor in augmented[vertex]:
                    if distance[neighbor] == -1:
                        distance[neighbor] = distance[vertex] + 1
                        queue.append(neighbor)
            if -1 in distance:
                return None
            best = max(best, max(distance))
        return best

    answer = vertex_count
    for extra in combinations(candidates, component_count - 1):
        candidate = diameter(extra)
        if candidate is not None:
            answer = min(answer, candidate)
    return answer
```

**Complexity:** exponential in the number of possible cross-component edges.

## 4. Better approach: try every attachment vertex

Computing each vertex's eccentricity identifies all component centers, after
which the same star construction works. Diameter paths find those centers in
linear rather than quadratic time per component.

## 5. Expert solution: connect all component centers to one hub

```python
from collections import deque


def connect_forest_minimum_diameter(
    vertex_count: int,
    edges: list[tuple[int, int]],
) -> tuple[int, list[tuple[int, int]]]:
    if type(vertex_count) is not int or vertex_count <= 0:
        raise ValueError("vertex_count must be positive")
    graph = [[] for _ in range(vertex_count)]
    parent = list(range(vertex_count))

    def find(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for first, second in edges:
        if (
            type(first) is not int
            or type(second) is not int
            or not 0 <= first < vertex_count
            or not 0 <= second < vertex_count
            or first == second
        ):
            raise ValueError("invalid edge")
        first_root = find(first)
        second_root = find(second)
        if first_root == second_root:
            raise ValueError("edges must form a forest")
        parent[first_root] = second_root
        graph[first].append(second)
        graph[second].append(first)

    def farthest(start: int) -> tuple[int, list[int], list[int]]:
        distance = [-1] * vertex_count
        previous = [-1] * vertex_count
        distance[start] = 0
        queue = deque([start])
        while queue:
            vertex = queue.popleft()
            for neighbor in graph[vertex]:
                if distance[neighbor] == -1:
                    distance[neighbor] = distance[vertex] + 1
                    previous[neighbor] = vertex
                    queue.append(neighbor)
        endpoint = max(
            (vertex for vertex, value in enumerate(distance) if value != -1),
            key=distance.__getitem__,
        )
        return endpoint, distance, previous

    components: dict[int, list[int]] = {}
    for vertex in range(vertex_count):
        components.setdefault(find(vertex), []).append(vertex)

    center_data = []
    for vertices in components.values():
        endpoint, _, _ = farthest(vertices[0])
        other_endpoint, distance, previous = farthest(endpoint)
        path = []
        vertex = other_endpoint
        while vertex != -1:
            path.append(vertex)
            if vertex == endpoint:
                break
            vertex = previous[vertex]
        diameter = distance[other_endpoint]
        center_data.append(((diameter + 1) // 2, path[len(path) // 2]))

    center_data.sort(reverse=True)
    hub = center_data[0][1]
    added = [(hub, center) for _, center in center_data[1:]]
    for first, second in added:
        graph[first].append(second)
        graph[second].append(first)

    endpoint, _, _ = farthest(0)
    other_endpoint, distance, _ = farthest(endpoint)
    return distance[other_endpoint], added
```

### Why the expert code is correct

Each diameter path yields a minimum-eccentricity attachment point. Joining all
centers to the largest-radius center realizes the unavoidable longest paths
among one, two, or three original components. The final two BFS traversals
measure the constructed tree's exact diameter.

**Complexity:** `O(n + m + c log c)` time and `O(n + m)` space for `c`
components.

## 6. What to remember

```text
best component attachment -> a diameter center
connect many components -> star around the largest radius
tree diameter -> two BFS traversals
```
