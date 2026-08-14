# ICPC300 014: CSES - New Roads Queries

**Source:** [CSES - New Roads Queries](https://cses.fi/problemset/task/2101/)  
**Pattern:** disjoint-set union reconstruction forest plus LCA  
**Goal:** Roads are added in the given order. For each pair of cities, report
the first day on which a route connects them, or `-1` if that never happens.

## 1. Problem in plain words

The graph only gains edges, so connectivity is monotone: once two cities are
connected, they stay connected. A query asks for the first true point in that
history.

If day 1 adds `0-1`, day 2 adds `2-3`, and day 3 adds `1-2`, then cities `0`
and `3` first become connected on day `3`. A city is connected to itself before
any road, so query `(2, 2)` has answer `0`.

## 2. First principles

Disjoint-set union (DSU) maintains connected components while roads arrive.
Whenever a road joins two previously separate components on day `d`, create a
new tree node labelled `d` and make the two old component trees its children.

This is a **DSU reconstruction forest**:

- original cities are leaves labelled `0`;
- each successful merge is an internal node labelled with its day;
- the lowest common ancestor (LCA) of two connected city leaves is precisely
  the merge that first put them in one component.

Failed union operations create no node because they change no connectivity.

## 3. Cases that decide correctness

| Case | Required result |
| --- | --- |
| Query `(a, a)` | `0`. |
| Cities never connected | `-1`. |
| A road inside one component | It changes no answer. |
| Parallel repeated road | Only its first useful merge matters. |
| Several final components | Build a forest, not one assumed tree. |

## 4. Brute force: replay all days for each query

Reset a DSU for every query, add roads in order, and stop at the first day the
two requested cities share a representative.

```python
def earliest_connections_brute_force(
    city_count: int,
    roads: list[tuple[int, int]],
    queries: list[tuple[int, int]],
) -> list[int]:
    answers: list[int] = []

    for first, second in queries:
        if first == second:
            answers.append(0)
            continue

        parent = list(range(city_count))

        def find(city: int) -> int:
            while parent[city] != city:
                parent[city] = parent[parent[city]]
                city = parent[city]
            return city

        answer = -1
        for day, (left, right) in enumerate(roads, start=1):
            left_root = find(left)
            right_root = find(right)
            if left_root != right_root:
                parent[right_root] = left_root
            if find(first) == find(second):
                answer = day
                break
        answers.append(answer)

    return answers
```

**Complexity:** `O(q(n + m alpha(n)))` time and `O(n)` extra memory.

## 5. Better: parallel binary search

Connectivity is monotone in the day. Binary-search every query simultaneously.
In one round, bucket queries by their middle day, replay the roads once, and
test all queries scheduled for each day.

```python
def earliest_connections_parallel_binary_search(
    city_count: int,
    roads: list[tuple[int, int]],
    queries: list[tuple[int, int]],
) -> list[int]:
    road_count = len(roads)
    low = [0 if first == second else 1 for first, second in queries]
    high = [0 if first == second else road_count + 1 for first, second in queries]

    while True:
        buckets: list[list[int]] = [[] for _ in range(road_count + 1)]
        active = False
        for query_index in range(len(queries)):
            if low[query_index] < high[query_index]:
                active = True
                middle = (low[query_index] + high[query_index]) // 2
                buckets[middle].append(query_index)
        if not active:
            break

        parent = list(range(city_count))
        size = [1] * city_count

        def find(city: int) -> int:
            while parent[city] != city:
                parent[city] = parent[parent[city]]
                city = parent[city]
            return city

        def union(first: int, second: int) -> None:
            first_root = find(first)
            second_root = find(second)
            if first_root == second_root:
                return
            if size[first_root] < size[second_root]:
                first_root, second_root = second_root, first_root
            parent[second_root] = first_root
            size[first_root] += size[second_root]

        for day, (first, second) in enumerate(roads, start=1):
            union(first, second)
            for query_index in buckets[day]:
                left, right = queries[query_index]
                if find(left) == find(right):
                    high[query_index] = day
                else:
                    low[query_index] = day + 1

    return [-1 if answer == road_count + 1 else answer for answer in low]
```

**Why it is better:** each binary-search round shares one road replay across
all queries.

**Complexity:** `O((n + m + q) log m alpha(n))` time and `O(n + m + q)` memory.

## 6. Expert solution: reconstruction forest and LCA

Build history once. The forest has at most `2n - 1` nodes because only a union
of two different components creates an internal node. Binary lifting then
answers each LCA in `O(log n)`.

```python
def earliest_connections(
    city_count: int,
    roads: list[tuple[int, int]],
    queries: list[tuple[int, int]],
) -> list[int]:
    if city_count < 1:
        raise ValueError("at least one city is required")

    dsu_parent = list(range(city_count))
    dsu_size = [1] * city_count
    component_tree_root = list(range(city_count))
    merge_day = [0] * city_count
    children: list[list[int]] = [[] for _ in range(city_count)]

    def find(city: int) -> int:
        while dsu_parent[city] != city:
            dsu_parent[city] = dsu_parent[dsu_parent[city]]
            city = dsu_parent[city]
        return city

    for day, (first, second) in enumerate(roads, start=1):
        if not 0 <= first < city_count or not 0 <= second < city_count:
            raise ValueError("road endpoint is outside the graph")
        first_root = find(first)
        second_root = find(second)
        if first_root == second_root:
            continue

        tree_node = len(merge_day)
        merge_day.append(day)
        children.append(
            [component_tree_root[first_root], component_tree_root[second_root]]
        )

        if dsu_size[first_root] < dsu_size[second_root]:
            first_root, second_root = second_root, first_root
        dsu_parent[second_root] = first_root
        dsu_size[first_root] += dsu_size[second_root]
        component_tree_root[first_root] = tree_node

    node_count = len(merge_day)
    parent = list(range(node_count))
    depth = [0] * node_count

    forest_roots = [
        component_tree_root[city] for city in range(city_count) if find(city) == city
    ]
    for root in forest_roots:
        stack = [root]
        while stack:
            node = stack.pop()
            for child in children[node]:
                parent[child] = node
                depth[child] = depth[node] + 1
                stack.append(child)

    level_count = max(1, node_count.bit_length())
    ancestors = [parent]
    for _ in range(1, level_count):
        previous = ancestors[-1]
        ancestors.append([previous[previous[node]] for node in range(node_count)])

    def lift(node: int, distance: int) -> int:
        bit = 0
        while distance:
            if distance & 1:
                node = ancestors[bit][node]
            distance >>= 1
            bit += 1
        return node

    def lowest_common_ancestor(first: int, second: int) -> int:
        if depth[first] < depth[second]:
            first, second = second, first
        first = lift(first, depth[first] - depth[second])
        if first == second:
            return first
        for level in range(level_count - 1, -1, -1):
            if ancestors[level][first] != ancestors[level][second]:
                first = ancestors[level][first]
                second = ancestors[level][second]
        return parent[first]

    answers: list[int] = []
    for first, second in queries:
        if not 0 <= first < city_count or not 0 <= second < city_count:
            raise ValueError("query endpoint is outside the graph")
        if find(first) != find(second):
            answers.append(-1)
        else:
            answers.append(merge_day[lowest_common_ancestor(first, second)])
    return answers
```

### Why the expert code is correct

- A reconstruction node is created exactly when two components first merge.
- Its subtree contains exactly the cities in the newly formed component.
- The LCA of two leaves is the earliest reconstruction node containing both,
  so its label is their first connection day.
- Leaves in different final DSU components never become connected.

**Complexity:** `O((n + m) log n + q log n)` time and `O(n log n)` memory.

## 7. What to remember

For monotone DSU history queries, store each successful merge as a tree node.
The time two objects first became related is then an LCA label.
