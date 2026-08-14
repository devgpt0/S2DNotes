# ICPC300 177: Codeforces 986A - Fair

**Source:** [Codeforces 986A - Fair](https://codeforces.com/problemset/problem/986/A)  
**Pattern:** one multi-source BFS per product type

## Exact contract

Each vertex of a connected, unweighted, undirected graph produces one of `k`
product types. For every vertex, find the sum of its distances to the nearest
producer of each of the closest `s` distinct product types.

## First principles

For one type, the distance from every vertex to its nearest producer is a
multi-source shortest-path problem: put all producers of that type in the BFS
queue at distance zero. Repeat independently for all `k` types, then select the
smallest `s` distances at each vertex.

## Cases that decide correctness

- Distance is to the nearest vertex of a type, not to every producer.
- A vertex has distance zero to its own product type.
- Choose `s` distinct types even when several distances are equal.
- Every declared type must have a producer.
- Parallel edges do not change BFS distances.

## Brute force: BFS from every vertex

```python
from collections import deque


def fair_costs_brute(
    product_types: list[int], edges: list[tuple[int, int]], type_count: int, wanted: int
) -> list[int]:
    size = len(product_types)
    if size == 0 or type(type_count) is not int or not 1 <= type_count <= size:
        raise ValueError("invalid graph or type count")
    if type(wanted) is not int or not 1 <= wanted <= type_count:
        raise ValueError("wanted must be in [1, type_count]")
    if any(
        type(value) is not int or not 1 <= value <= type_count
        for value in product_types
    ):
        raise ValueError("invalid product type")
    if set(product_types) != set(range(1, type_count + 1)):
        raise ValueError("every product type must occur")

    graph = [[] for _ in range(size)]
    for first, second in edges:
        if (
            type(first) is not int
            or type(second) is not int
            or not 0 <= first < size
            or not 0 <= second < size
            or first == second
        ):
            raise ValueError("invalid edge")
        graph[first].append(second)
        graph[second].append(first)

    answers: list[int] = []
    for start in range(size):
        distance = [-1] * size
        distance[start] = 0
        queue = deque([start])
        while queue:
            vertex = queue.popleft()
            for neighbor in graph[vertex]:
                if distance[neighbor] == -1:
                    distance[neighbor] = distance[vertex] + 1
                    queue.append(neighbor)
        if any(value == -1 for value in distance):
            raise ValueError("graph must be connected")

        nearest = [size + 1] * type_count
        for vertex, product_type in enumerate(product_types):
            type_index = product_type - 1
            nearest[type_index] = min(nearest[type_index], distance[vertex])
        answers.append(sum(sorted(nearest)[:wanted]))
    return answers
```

This takes `O(n(n+m))` time and is only a small-instance oracle.

## Better approach: no separate intermediate

Running one BFS from every producer and then taking a per-type minimum repeats
work without adding a useful invariant. Initializing one queue with all
producers of a type is the direct scalable form of that shortest-path search.

## Expert solution: multi-source BFS by type

```python
from array import array
from collections import deque
from heapq import nsmallest


def fair_costs(
    product_types: list[int], edges: list[tuple[int, int]], type_count: int, wanted: int
) -> list[int]:
    size = len(product_types)
    if size == 0 or type(type_count) is not int or not 1 <= type_count <= size:
        raise ValueError("invalid graph or type count")
    if type(wanted) is not int or not 1 <= wanted <= type_count:
        raise ValueError("wanted must be in [1, type_count]")
    if any(
        type(value) is not int or not 1 <= value <= type_count
        for value in product_types
    ):
        raise ValueError("invalid product type")
    if set(product_types) != set(range(1, type_count + 1)):
        raise ValueError("every product type must occur")

    graph = [[] for _ in range(size)]
    for first, second in edges:
        if (
            type(first) is not int
            or type(second) is not int
            or not 0 <= first < size
            or not 0 <= second < size
            or first == second
        ):
            raise ValueError("invalid edge")
        graph[first].append(second)
        graph[second].append(first)

    distances: list[array[int]] = []
    for product_type in range(1, type_count + 1):
        distance = array("i", [-1]) * size
        queue: deque[int] = deque()
        for vertex, vertex_type in enumerate(product_types):
            if vertex_type == product_type:
                distance[vertex] = 0
                queue.append(vertex)

        while queue:
            vertex = queue.popleft()
            for neighbor in graph[vertex]:
                if distance[neighbor] == -1:
                    distance[neighbor] = distance[vertex] + 1
                    queue.append(neighbor)
        if any(value == -1 for value in distance):
            raise ValueError("graph must be connected")
        distances.append(distance)

    return [
        sum(nsmallest(wanted, (distance[vertex] for distance in distances)))
        for vertex in range(size)
    ]
```

Each BFS computes the exact nearest distance for one type. Selecting the `s`
smallest independent type distances therefore gives exactly the required
minimum sum at every vertex.

**Complexity:** `O(k(n+m) + nk log s)` time and `O(nk+n+m)` space. Packed
32-bit distance arrays keep the `nk` table bounded.
