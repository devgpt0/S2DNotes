# ICPC300 297: Codeforces 1399E2 - Weights Division (hard version)

**Source:** [Codeforces 1399E2 - Weights Division (hard version)](https://codeforces.com/problemset/problem/1399/E2)  
**Rating:** 2200  
**Pattern:** marginal halving gains and two cost classes  
**Goal:** Root a weighted tree at vertex `0`. Its score is the sum of every
root-to-leaf path length. One operation replaces an edge weight by its floor
half and costs the edge's class, `1` or `2`. Reach `score_limit` with minimum
cost.

## 1. First principles

An edge used by `leaves` root-to-leaf paths contributes `weight * leaves`.
One halving reduces the score by
`(weight - weight // 2) * leaves`; further halvings yield an independent
decreasing gain sequence.

For either cost class, taking its largest gains first is optimal. Build prefix
sums for both classes, enumerate how many class-2 operations are used, and
binary-search the required number of class-1 operations.

## 2. Cases that decide correctness

- An edge above many leaves has proportionally larger gain.
- Repeated halvings stop when the weight reaches zero.
- An already small enough score costs zero.
- Class-2 operations cost two, not one operation count.
- The input edges must form a tree.

## 3. Brute force: shortest path over all weight states

```python
from heapq import heappop, heappush


WeightedEdge = tuple[int, int, int, int]


def minimum_weight_division_cost_brute(
    vertex_count: int,
    edges: list[WeightedEdge],
    score_limit: int,
) -> int:
    if type(vertex_count) is not int or vertex_count <= 0:
        raise ValueError("vertex_count must be positive")
    if type(score_limit) is not int or score_limit < 0:
        raise ValueError("score_limit must be nonnegative")
    if len(edges) != vertex_count - 1:
        raise ValueError("edges must describe a tree")
    graph: list[list[tuple[int, int]]] = [[] for _ in range(vertex_count)]
    weights = []
    classes = []
    for edge_index, (first, second, weight, cost_class) in enumerate(edges):
        if (
            type(first) is not int
            or type(second) is not int
            or not 0 <= first < vertex_count
            or not 0 <= second < vertex_count
            or first == second
            or type(weight) is not int
            or weight < 0
            or cost_class not in (1, 2)
        ):
            raise ValueError("invalid weighted edge")
        graph[first].append((second, edge_index))
        graph[second].append((first, edge_index))
        weights.append(weight)
        classes.append(cost_class)

    parent = [-2] * vertex_count
    parent[0] = -1
    parent_edge = [-1] * vertex_count
    order = [0]
    for vertex in order:
        for neighbor, edge_index in graph[vertex]:
            if neighbor == parent[vertex]:
                continue
            if parent[neighbor] != -2:
                raise ValueError("edges must describe a tree")
            parent[neighbor] = vertex
            parent_edge[neighbor] = edge_index
            order.append(neighbor)
    if len(order) != vertex_count:
        raise ValueError("tree must be connected")

    leaf_count = [0] * vertex_count
    for vertex in reversed(order):
        children = [
            neighbor for neighbor, _ in graph[vertex] if parent[neighbor] == vertex
        ]
        leaf_count[vertex] = (
            sum(leaf_count[child] for child in children) if children else 1
        )
    edge_leaves = [0] * len(edges)
    for vertex in range(1, vertex_count):
        edge_leaves[parent_edge[vertex]] = leaf_count[vertex]

    start = tuple(weights)
    queue = [(0, start)]
    best = {start: 0}
    while queue:
        cost, state = heappop(queue)
        if best[state] != cost:
            continue
        score = sum(state[index] * edge_leaves[index] for index in range(len(edges)))
        if score <= score_limit:
            return cost
        for edge_index, weight in enumerate(state):
            if weight == 0:
                continue
            changed = list(state)
            changed[edge_index] //= 2
            next_state = tuple(changed)
            next_cost = cost + classes[edge_index]
            if next_cost < best.get(next_state, 10**100):
                best[next_state] = next_cost
                heappush(queue, (next_cost, next_state))
    raise RuntimeError("zero weights always satisfy a nonnegative limit")
```

**Complexity:** exponential in the edge weights' halving state space.

## 4. Better approach: knapsack over all marginal gains

Every gain may be treated as an item of cost one or two, but a general
knapsack wastes the fact that gains within each cost class should be selected
in descending order.

## 5. Expert solution: two sorted gain-prefix arrays

```python
from bisect import bisect_left


WeightedEdge = tuple[int, int, int, int]


def minimum_weight_division_cost(
    vertex_count: int,
    edges: list[WeightedEdge],
    score_limit: int,
) -> int:
    if type(vertex_count) is not int or vertex_count <= 0:
        raise ValueError("vertex_count must be positive")
    if type(score_limit) is not int or score_limit < 0:
        raise ValueError("score_limit must be nonnegative")
    if len(edges) != vertex_count - 1:
        raise ValueError("edges must describe a tree")
    graph: list[list[tuple[int, int]]] = [[] for _ in range(vertex_count)]
    weights = []
    classes = []
    for edge_index, (first, second, weight, cost_class) in enumerate(edges):
        if (
            type(first) is not int
            or type(second) is not int
            or not 0 <= first < vertex_count
            or not 0 <= second < vertex_count
            or first == second
            or type(weight) is not int
            or weight < 0
            or cost_class not in (1, 2)
        ):
            raise ValueError("invalid weighted edge")
        graph[first].append((second, edge_index))
        graph[second].append((first, edge_index))
        weights.append(weight)
        classes.append(cost_class)

    parent = [-2] * vertex_count
    parent[0] = -1
    parent_edge = [-1] * vertex_count
    order = [0]
    for vertex in order:
        for neighbor, edge_index in graph[vertex]:
            if neighbor == parent[vertex]:
                continue
            if parent[neighbor] != -2:
                raise ValueError("edges must describe a tree")
            parent[neighbor] = vertex
            parent_edge[neighbor] = edge_index
            order.append(neighbor)
    if len(order) != vertex_count:
        raise ValueError("tree must be connected")

    leaf_count = [0] * vertex_count
    child_count = [0] * vertex_count
    for vertex in range(1, vertex_count):
        child_count[parent[vertex]] += 1
    for vertex in reversed(order):
        if child_count[vertex] == 0:
            leaf_count[vertex] = 1
        elif vertex != 0 or vertex_count > 1:
            leaf_count[vertex] = sum(
                leaf_count[neighbor]
                for neighbor, _ in graph[vertex]
                if parent[neighbor] == vertex
            )

    gains = {1: [], 2: []}
    total = 0
    for vertex in range(1, vertex_count):
        edge_index = parent_edge[vertex]
        weight = weights[edge_index]
        leaves = leaf_count[vertex]
        total += weight * leaves
        while weight:
            gains[classes[edge_index]].append((weight - weight // 2) * leaves)
            weight //= 2
    required = max(0, total - score_limit)
    if required == 0:
        return 0

    prefixes: dict[int, list[int]] = {}
    for cost_class in (1, 2):
        prefix = [0]
        for gain in sorted(gains[cost_class], reverse=True):
            prefix.append(prefix[-1] + gain)
        prefixes[cost_class] = prefix

    answer = 10**100
    for class_two_count, class_two_gain in enumerate(prefixes[2]):
        remaining = max(0, required - class_two_gain)
        class_one_count = bisect_left(prefixes[1], remaining)
        if class_one_count < len(prefixes[1]):
            answer = min(answer, 2 * class_two_count + class_one_count)
    return answer
```

### Why the expert code is correct

Leaf counts convert the path objective into independent edge contributions.
Within one cost class, exchanging a selected smaller gain for an unselected
larger gain never hurts, so optimal choices are prefixes of sorted gains.
Enumerating one prefix and binary-searching the other covers every optimum.

**Complexity:** `O(n log W log(n log W))` time and `O(n log W)` space.

## 6. What to remember

```text
edge contribution -> weight times leaves below it
one halving -> independent marginal reduction
two operation costs -> enumerate one sorted prefix, search the other
```
