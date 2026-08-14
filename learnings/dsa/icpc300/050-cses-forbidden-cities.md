# ICPC300 050: CSES - Forbidden Cities

**Source:** [CSES - Forbidden Cities](https://cses.fi/problemset/task/1705/)  
**Pattern:** DFS low-link values and binary lifting  
**Goal:** For each `(a, b, c)`, decide whether an undirected route from `a` to
`b` exists without visiting forbidden city `c`.

## 1. Problem in plain words

Removing a non-articulation city does not separate any other pair in its
connected component. Removing an articulation city may detach one or more DFS
child subtrees.

The query endpoints themselves cannot be used when forbidden: if `a == c` or
`b == c`, the answer is immediately false.

## 2. First principles

Run an undirected DFS. For each vertex `v`:

- `tin[v]` is its discovery time;
- `low[v]` is the smallest discovery time reachable from `v`'s DFS subtree
  using tree edges and at most one back edge.

For a direct DFS child `child` of forbidden city `c`:

- if `low[child] >= tin[c]`, that child's subtree is separated when `c` is
  removed;
- otherwise, a back edge connects the subtree to an ancestor of `c`, so it
  remains in the same "rest of graph" region.

For any descendant `x` of `c`, binary lifting finds the direct child of `c` on
the path to `x`. Classify both query endpoints by their separated child, or by
one common rest-region marker. They remain connected exactly when the markers
match.

## 3. Cases that decide correctness

| Case | Required behavior |
| --- | --- |
| Forbidden city equals an endpoint | `False`. |
| Forbidden city is not an articulation point | Other connected endpoints stay connected. |
| Endpoints lie in the same separated child subtree | `True`. |
| Endpoints lie in different separated child subtrees | `False`. |
| A child subtree has a back edge above the forbidden city | It belongs to the rest region. |
| Forbidden city is a DFS root | Each root child is a separate region. |

## 4. Brute force: DFS while skipping the forbidden city

```python
Query = tuple[int, int, int]


def routes_without_forbidden_brute_force(
    city_count: int,
    roads: list[tuple[int, int]],
    queries: list[Query],
) -> list[bool]:
    graph: list[list[int]] = [[] for _ in range(city_count)]
    for first, second in roads:
        graph[first].append(second)
        graph[second].append(first)

    answers: list[bool] = []
    for start, target, forbidden in queries:
        if start == forbidden or target == forbidden:
            answers.append(False)
            continue

        seen = [False] * city_count
        seen[forbidden] = True
        seen[start] = True
        stack = [start]
        while stack:
            city = stack.pop()
            for neighbor in graph[city]:
                if not seen[neighbor]:
                    seen[neighbor] = True
                    stack.append(neighbor)
        answers.append(seen[target])
    return answers
```

**Complexity:** `O(q(n + m))` time and `O(n + m)` memory.

## 5. Better when forbidden cities repeat: cache deletion components

For each distinct forbidden city appearing in queries, label every connected
component of the graph after removing it once. Queries with that forbidden city
then compare two labels in constant time.

```python
Query = tuple[int, int, int]


def routes_without_forbidden_cached(
    city_count: int,
    roads: list[tuple[int, int]],
    queries: list[Query],
) -> list[bool]:
    graph: list[list[int]] = [[] for _ in range(city_count)]
    for first, second in roads:
        graph[first].append(second)
        graph[second].append(first)

    cache: dict[int, list[int]] = {}
    answers: list[bool] = []
    for start, target, forbidden in queries:
        if start == forbidden or target == forbidden:
            answers.append(False)
            continue

        if forbidden not in cache:
            component = [-1] * city_count
            component[forbidden] = -2
            component_id = 0
            for root in range(city_count):
                if component[root] != -1:
                    continue
                component[root] = component_id
                stack = [root]
                while stack:
                    city = stack.pop()
                    for neighbor in graph[city]:
                        if component[neighbor] == -1:
                            component[neighbor] = component_id
                            stack.append(neighbor)
                component_id += 1
            cache[forbidden] = component

        labels = cache[forbidden]
        answers.append(labels[start] == labels[target])
    return answers
```

**Complexity:** `O(s(n + m) + q)` time and `O(sn + m)` memory for `s` distinct
forbidden cities.

## 6. Expert solution: low links classify deletion regions

The iterative DFS skips only the exact parent edge ID, so parallel roads are
handled correctly. Entry/exit intervals test ancestry, and lifting moves a
descendant to the direct child below the forbidden city.

```python
Query = tuple[int, int, int]


def routes_without_forbidden(
    city_count: int,
    roads: list[tuple[int, int]],
    queries: list[Query],
) -> list[bool]:
    if city_count < 1:
        raise ValueError("at least one city is required")

    graph: list[list[tuple[int, int]]] = [[] for _ in range(city_count)]
    for edge_id, (first, second) in enumerate(roads):
        if not 0 <= first < city_count or not 0 <= second < city_count:
            raise ValueError("road endpoint is outside the graph")
        if first == second:
            raise ValueError("roads must join different cities")
        graph[first].append((second, edge_id))
        graph[second].append((first, edge_id))

    entry = [-1] * city_count
    exit_time = [-1] * city_count
    low = [-1] * city_count
    parent = [-1] * city_count
    parent_edge = [-1] * city_count
    depth = [0] * city_count
    component = [-1] * city_count
    timer = 0
    component_id = 0

    for root in range(city_count):
        if entry[root] != -1:
            continue
        parent[root] = root
        component[root] = component_id
        entry[root] = timer
        low[root] = timer
        timer += 1
        stack = [(root, 0)]

        while stack:
            city, edge_index = stack[-1]
            if edge_index < len(graph[city]):
                neighbor, edge_id = graph[city][edge_index]
                stack[-1] = (city, edge_index + 1)
                if edge_id == parent_edge[city]:
                    continue
                if entry[neighbor] == -1:
                    parent[neighbor] = city
                    parent_edge[neighbor] = edge_id
                    depth[neighbor] = depth[city] + 1
                    component[neighbor] = component_id
                    entry[neighbor] = timer
                    low[neighbor] = timer
                    timer += 1
                    stack.append((neighbor, 0))
                else:
                    low[city] = min(low[city], entry[neighbor])
            else:
                exit_time[city] = timer - 1
                stack.pop()
                if city != root:
                    low[parent[city]] = min(low[parent[city]], low[city])

        component_id += 1

    level_count = max(1, city_count.bit_length())
    ancestors = [parent.copy()]
    for _ in range(1, level_count):
        previous = ancestors[-1]
        ancestors.append([previous[previous[city]] for city in range(city_count)])

    def is_ancestor(ancestor: int, city: int) -> bool:
        return (
            component[ancestor] == component[city]
            and entry[ancestor] <= entry[city] <= exit_time[ancestor]
        )

    def lift(city: int, steps: int) -> int:
        bit = 0
        while steps:
            if steps & 1:
                city = ancestors[bit][city]
            steps >>= 1
            bit += 1
        return city

    def deletion_region(city: int, forbidden: int) -> int:
        if not is_ancestor(forbidden, city):
            return -1
        child = lift(city, depth[city] - depth[forbidden] - 1)
        return child if low[child] >= entry[forbidden] else -1

    answers: list[bool] = []
    for start, target, forbidden in queries:
        if any(not 0 <= city < city_count for city in (start, target, forbidden)):
            raise ValueError("query city is outside the graph")
        if start == forbidden or target == forbidden:
            answers.append(False)
        elif component[start] != component[target]:
            answers.append(False)
        elif component[forbidden] != component[start]:
            answers.append(True)
        else:
            answers.append(
                deletion_region(start, forbidden) == deletion_region(target, forbidden)
            )
    return answers
```

### Why the expert code is correct

- DFS intervals identify exactly which query vertices lie below the forbidden
  city and lifting identifies their unique direct child branch.
- `low[child] >= entry[forbidden]` is exactly the condition that branch has no
  route to the forbidden city's ancestors without using the forbidden city.
- All nonseparating child branches and vertices outside the forbidden subtree
  connect through the common rest region.
- Two allowed endpoints remain connected precisely when their region labels
  are equal; root children work because each satisfies the separating condition.

**Complexity:** `O((n + m) + n log n + q log n)` time and `O(n log n + m)`
memory.

## 7. What to remember

Removing an articulation vertex partitions its DFS child subtrees according to
the condition `low[child] >= tin[parent]`. Binary lifting maps any query vertex
to the child branch whose condition matters.
