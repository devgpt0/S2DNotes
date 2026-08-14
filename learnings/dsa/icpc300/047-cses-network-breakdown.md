# ICPC300 047: CSES - Network Breakdown

**Source:** [CSES - Network Breakdown](https://cses.fi/problemset/task/1677/)  
**Pattern:** offline deletions processed as reverse additions  
**Goal:** Roads are removed in the given order. After every removal, output the
number of connected components in the undirected city network.

## 1. Problem in plain words

Disjoint-set union (DSU) efficiently adds an edge, but it cannot split a
component when an edge is deleted. The deletion order is known in advance, so
run time backwards: the final graph is the starting point, and each reversed
deletion becomes an addition.

The functions below identify an undirected road by its endpoint pair. This
matches the source guarantee that roads and removed roads are distinct.

## 2. First principles

Remove all scheduled roads conceptually and build a DSU from the roads that
remain. Let its component count be the answer after every forward deletion has
happened.

Process removed roads from last to first:

1. record the current component count as the answer after that forward removal;
2. add the road back for the next reverse step;
3. decrease the count only if the road joins two different DSU roots.

Reversing the recorded answers restores forward query order.

## 3. Cases that decide correctness

| Case | Required behavior |
| --- | --- |
| Removed road is a bridge at that time | Component count increases by one. |
| Removed road lies on a cycle | Component count stays unchanged. |
| All roads are removed | Start reverse processing from isolated cities. |
| Network is initially disconnected | Count every initial component. |
| Reversed road joins an already connected pair | Do not decrement the count. |

## 4. Brute force: rebuild connectivity after every removal

```python
Road = tuple[int, int]


def network_components_brute_force(
    city_count: int, roads: list[Road], removals: list[Road]
) -> list[int]:
    def normalize(road: Road) -> Road:
        first, second = road
        return (first, second) if first < second else (second, first)

    active = {normalize(road) for road in roads}
    if len(active) != len(roads):
        raise ValueError("roads must be distinct")

    answers: list[int] = []
    for removal in removals:
        road = normalize(removal)
        if road not in active:
            raise ValueError("each removal must name an active road")
        active.remove(road)

        graph: list[list[int]] = [[] for _ in range(city_count)]
        for first, second in active:
            graph[first].append(second)
            graph[second].append(first)

        seen = [False] * city_count
        components = 0
        for start in range(city_count):
            if seen[start]:
                continue
            components += 1
            seen[start] = True
            stack = [start]
            while stack:
                city = stack.pop()
                for neighbor in graph[city]:
                    if not seen[neighbor]:
                        seen[neighbor] = True
                        stack.append(neighbor)
        answers.append(components)

    return answers
```

**Complexity:** `O(k(n + m))` time and `O(n + m)` memory for `k` removals.

## 5. Better approach: why ordinary online DSU cannot delete

Path compression deliberately forgets the internal merge history of a
component. Removing one old road may split that component in a way DSU cannot
recover. Rebuilding after each removal is the direct fallback; maintaining a
fully dynamic connectivity structure would be much more complex than this
source requires.

Because all deletions are known before processing, reversing time is the
simple genuine improvement. There is no useful intermediate DSU deletion
operation to implement.

## 6. Expert solution: start after all removals and add roads back

```python
Road = tuple[int, int]


def network_components_after_removals(
    city_count: int, roads: list[Road], removals: list[Road]
) -> list[int]:
    if city_count < 1:
        raise ValueError("at least one city is required")

    def normalize(road: Road) -> Road:
        first, second = road
        if not 0 <= first < city_count or not 0 <= second < city_count:
            raise ValueError("road endpoint is outside the graph")
        if first == second:
            raise ValueError("roads must join different cities")
        return (first, second) if first < second else (second, first)

    normalized_roads = [normalize(road) for road in roads]
    road_set = set(normalized_roads)
    if len(road_set) != len(normalized_roads):
        raise ValueError("roads must be distinct")

    normalized_removals = [normalize(road) for road in removals]
    removed_set = set(normalized_removals)
    if len(removed_set) != len(normalized_removals):
        raise ValueError("a road cannot be removed twice")
    if not removed_set <= road_set:
        raise ValueError("every removed road must exist")

    parent = list(range(city_count))
    size = [1] * city_count
    component_count = city_count

    def find(city: int) -> int:
        while parent[city] != city:
            parent[city] = parent[parent[city]]
            city = parent[city]
        return city

    def union(first: int, second: int) -> bool:
        first_root = find(first)
        second_root = find(second)
        if first_root == second_root:
            return False
        if size[first_root] < size[second_root]:
            first_root, second_root = second_root, first_root
        parent[second_root] = first_root
        size[first_root] += size[second_root]
        return True

    for first, second in normalized_roads:
        if (first, second) not in removed_set and union(first, second):
            component_count -= 1

    answers = [0] * len(normalized_removals)
    for index in range(len(normalized_removals) - 1, -1, -1):
        answers[index] = component_count
        first, second = normalized_removals[index]
        if union(first, second):
            component_count -= 1

    return answers
```

### Why the expert code is correct

- Before reverse processing, DSU represents exactly the graph after all
  forward removals.
- At reverse index `i`, the current graph is exactly the graph immediately
  after forward removal `i`, so its component count is the requested answer.
- Adding removal `i` back creates exactly the graph needed for reverse index
  `i-1`.
- DSU decreases the component count precisely when that addition merges two
  previously separate components.

**Complexity:** `O((n + m + k) alpha(n))` time and `O(n + m + k)` memory.

## 7. What to remember

If updates are deletions but all are known offline, ask whether reversing time
turns them into additions that DSU can handle.
