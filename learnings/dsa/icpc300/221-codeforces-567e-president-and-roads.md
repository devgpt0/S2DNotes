# ICPC300 221: Codeforces 567E - President and Roads

**Source:** [Codeforces 567E - President and Roads](https://codeforces.com/problemset/problem/567/E)  
**Rating:** 2300  
**Pattern:** two Dijkstra runs plus shortest-path DAG counting  
**Goal:** Classify every directed positive-weight edge as `YES` if every
shortest source-to-target path uses it, `CAN x` if decreasing its weight by the
minimum positive `x` can make every shortest path use it, or `NO`.

## 1. First principles

Let `from_source[u]` and `to_target[v]` be shortest distances. An edge
`u -> v` lies on some current shortest path exactly when

```text
from_source[u] + weight + to_target[v] = shortest
```

Count paths through the resulting distance-increasing DAG with two moduli. The
edge is mandatory when its prefix-count times suffix-count equals the total
shortest-path count under both moduli.

Otherwise make its through-path strictly shorter than the old optimum. Its
largest valid new weight is

```text
shortest - from_source[u] - to_target[v] - 1
```

## 2. Cases that decide correctness

- Edge weights must remain positive after a decrease.
- An edge on some but not all shortest paths is usually `CAN 1`.
- A weight-one non-mandatory edge cannot be decreased.
- Unreachable edge endpoints cannot be made useful by changing only that edge.
- The source must initially reach the target.

## 3. Brute force: enumerate simple paths and every decrease

```python
def classify_roads_brute(
    vertex_count: int,
    edges: list[tuple[int, int, int]],
    source: int,
    target: int,
) -> list[str]:
    if (
        vertex_count <= 0
        or not 0 <= source < vertex_count
        or not 0 <= target < vertex_count
    ):
        raise ValueError("invalid vertices")
    graph = [[] for _ in range(vertex_count)]
    for index, (first, second, weight) in enumerate(edges):
        if (
            not 0 <= first < vertex_count
            or not 0 <= second < vertex_count
            or first == second
            or weight <= 0
        ):
            raise ValueError("invalid edge")
        graph[first].append((second, weight, index))

    paths: list[tuple[int, int]] = []

    def enumerate_paths(node: int, visited: int, weight: int, used: int) -> None:
        if node == target:
            paths.append((weight, used))
            return
        for neighbor, edge_weight, edge_index in graph[node]:
            if visited >> neighbor & 1:
                continue
            enumerate_paths(
                neighbor,
                visited | (1 << neighbor),
                weight + edge_weight,
                used | (1 << edge_index),
            )

    enumerate_paths(source, 1 << source, 0, 0)
    if not paths:
        raise ValueError("target must be reachable")
    shortest = min(weight for weight, _ in paths)
    shortest_masks = [used for weight, used in paths if weight == shortest]

    answers: list[str] = []
    for edge_index, (_, _, weight) in enumerate(edges):
        if all(mask >> edge_index & 1 for mask in shortest_masks):
            answers.append("YES")
            continue
        answer = "NO"
        for decrease in range(1, weight):
            changed_shortest = min(
                path_weight - (decrease if used >> edge_index & 1 else 0)
                for path_weight, used in paths
            )
            changed_shortest_masks = [
                used
                for path_weight, used in paths
                if path_weight - (decrease if used >> edge_index & 1 else 0)
                == changed_shortest
            ]
            if all(used >> edge_index & 1 for used in changed_shortest_masks):
                answer = f"CAN {decrease}"
                break
        answers.append(answer)
    return answers
```

**Complexity:** Exponential in `V`, with up to `weight` trials per edge.

## 4. Better transition: reason on the shortest-path DAG

Positive weights orient every shortest-path edge toward a larger source
distance, so path counts have a topological order. Distances also reveal the
exact one-edge decrease needed without rerunning Dijkstra.

## 5. Expert solution: distance DAG counts under two moduli

```python
from heapq import heappop, heappush


def classify_roads(
    vertex_count: int,
    edges: list[tuple[int, int, int]],
    source: int,
    target: int,
) -> list[str]:
    if (
        vertex_count <= 0
        or not 0 <= source < vertex_count
        or not 0 <= target < vertex_count
    ):
        raise ValueError("invalid vertices")
    graph = [[] for _ in range(vertex_count)]
    reverse = [[] for _ in range(vertex_count)]
    for index, (first, second, weight) in enumerate(edges):
        if (
            not 0 <= first < vertex_count
            or not 0 <= second < vertex_count
            or first == second
            or weight <= 0
        ):
            raise ValueError("invalid edge")
        graph[first].append((second, weight, index))
        reverse[second].append((first, weight, index))

    infinity = 10**30

    def dijkstra(start: int, adjacency: list[list[tuple[int, int, int]]]) -> list[int]:
        distance = [infinity] * vertex_count
        distance[start] = 0
        heap = [(0, start)]
        while heap:
            current_distance, node = heappop(heap)
            if current_distance != distance[node]:
                continue
            for neighbor, weight, _ in adjacency[node]:
                candidate = current_distance + weight
                if candidate < distance[neighbor]:
                    distance[neighbor] = candidate
                    heappush(heap, (candidate, neighbor))
        return distance

    from_source = dijkstra(source, graph)
    to_target = dijkstra(target, reverse)
    shortest = from_source[target]
    if shortest == infinity:
        raise ValueError("target must be reachable")

    moduli = (1_000_000_007, 1_000_000_009)
    from_count = [[0] * vertex_count for _ in moduli]
    to_count = [[0] * vertex_count for _ in moduli]
    for counts in from_count:
        counts[source] = 1
    order = sorted(range(vertex_count), key=from_source.__getitem__)
    for node in order:
        for neighbor, weight, _ in graph[node]:
            if from_source[node] + weight + to_target[neighbor] != shortest:
                continue
            for index, modulus in enumerate(moduli):
                from_count[index][neighbor] = (
                    from_count[index][neighbor] + from_count[index][node]
                ) % modulus
    for counts in to_count:
        counts[target] = 1
    for node in reversed(order):
        for neighbor, weight, _ in graph[node]:
            if from_source[node] + weight + to_target[neighbor] != shortest:
                continue
            for index, modulus in enumerate(moduli):
                to_count[index][node] = (
                    to_count[index][node] + to_count[index][neighbor]
                ) % modulus

    answers: list[str] = []
    for first, second, weight in edges:
        on_shortest = from_source[first] + weight + to_target[second] == shortest
        mandatory = on_shortest and all(
            from_count[index][first] * to_count[index][second] % modulus
            == from_count[index][target]
            for index, modulus in enumerate(moduli)
        )
        if mandatory:
            answers.append("YES")
            continue
        new_weight = shortest - from_source[first] - to_target[second] - 1
        if 1 <= new_weight < weight:
            answers.append(f"CAN {weight - new_weight}")
        else:
            answers.append("NO")
    return answers
```

### Why the expert code is correct

The distance equality identifies exactly the shortest-path DAG. Prefix and
suffix counts multiply to the number of shortest paths using one edge, so
equality with the total under two independent moduli identifies mandatory
edges with negligible collision risk. For every other edge, the stated new
weight makes one through-path exactly one shorter than the old optimum and is
the smallest possible decrease that can do so.

**Complexity:** `O((V+E) log V)` time and `O(V+E)` space.

## 6. What to remember

```text
two distance arrays -> shortest path through each edge
mandatory edge -> all shortest DAG paths pass through it
make edge useful -> lower its through-path to shortest - 1
```
