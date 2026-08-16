# Focus300 124: LeetCode 815 - Bus Routes

**Source:** [LeetCode 815](https://leetcode.com/problems/bus-routes/)  
**Difficulty:** Hard  
**Pattern:** BFS over an implicit stop-route bipartite graph

## Exact contract

Each route repeats forever through its listed stops. Starting at `source`, one
bus ride may move between any two stops on one route. Return the minimum number
of buses needed to reach `target`, or `-1` when impossible. Walking between
different stop identifiers is not allowed.

## First principles

Stops and routes form a bipartite graph: boarding crosses from a stop to a
route and riding crosses from that route to any of its stops. BFS layers count
boarded routes, which is exactly the objective. Once a route is boarded at its
minimum layer, scanning it again cannot improve any result.


## Classroom board: visit each region or node once

```text
mark what is already seen, expand to neighbors, and stop when the region
is fully explored.
```



## Step-by-step transformation

1. Choose a start state such as a cell, node, or partial path.
2. Mark the state as visited or temporarily commit the choice.
3. Expand to valid neighbors or next choices while the invariant still holds.
4. Undo the temporary choice when the branch finishes, then return the collected answer.

These problems transform the input into output by exploring one branch at a time and backtracking whenever a branch can no longer produce a valid solution.


## Diagram: search and undo

```text

            start state
                |
                v
            choose one path
                |
                v
            explore neighbors
                |
                v
            undo and try next path
                |
                v
            answer
```

These notes use search, visit markers, and backtracking to turn one starting state into the final valid path or count.

## Cases that decide correctness

- `source == target` requires zero buses even if no route contains the stop.
- Multiple routes may share several transfer stops.
- Repeatedly expanding the same route causes avoidable quadratic work.
- A stop may be reachable while the target remains disconnected.
- Stop identifiers are sparse and must not index a dense array.

## Brute force: scan every route from each reached stop

```python
from collections import deque


def minimum_buses_brute(
    routes: list[list[int]],
    source: int,
    target: int,
) -> int:
    if type(routes) is not list or not 1 <= len(routes) <= 500:
        raise ValueError("routes must contain between 1 and 500 routes")
    if any(type(route) is not list or not route for route in routes):
        raise ValueError("every route must be a nonempty list")
    if sum(map(len, routes)) > 100_000:
        raise ValueError("total route entries must not exceed 100,000")
    if any(
        type(stop) is not int or not 0 <= stop <= 1_000_000
        for route in routes
        for stop in route
    ):
        raise ValueError("stops must be integers in the source range")
    if any(len(route) != len(set(route)) for route in routes):
        raise ValueError("stops within each route must be distinct")
    if (
        type(source) is not int
        or type(target) is not int
        or not 0 <= source <= 1_000_000
        or not 0 <= target <= 1_000_000
    ):
        raise ValueError("source and target must be valid stop identifiers")
    if source == target:
        return 0

    queue = deque([(source, 0)])
    visited_stops = {source}
    boarded_routes: set[int] = set()
    while queue:
        stop, buses = queue.popleft()
        for route_index, route in enumerate(routes):
            if route_index in boarded_routes or stop not in route:
                continue
            boarded_routes.add(route_index)
            if target in route:
                return buses + 1
            for next_stop in route:
                if next_stop not in visited_stops:
                    visited_stops.add(next_stop)
                    queue.append((next_stop, buses + 1))
    return -1
```

Route membership scans make this much slower than the graph size suggests.

## Better insight: index the reverse relation from stops to routes

Building `stop -> routes` exposes only routes that can actually be boarded at a
reached stop. Marking routes once makes every route entry expand at most once.

## Expert solution: indexed BFS by buses boarded

```python
from collections import defaultdict, deque


def minimum_buses(routes: list[list[int]], source: int, target: int) -> int:
    if type(routes) is not list or not 1 <= len(routes) <= 500:
        raise ValueError("routes must contain between 1 and 500 routes")
    if any(type(route) is not list or not route for route in routes):
        raise ValueError("every route must be a nonempty list")
    if sum(map(len, routes)) > 100_000:
        raise ValueError("total route entries must not exceed 100,000")
    if any(
        type(stop) is not int or not 0 <= stop <= 1_000_000
        for route in routes
        for stop in route
    ):
        raise ValueError("stops must be integers in the source range")
    if any(len(route) != len(set(route)) for route in routes):
        raise ValueError("stops within each route must be distinct")
    if (
        type(source) is not int
        or type(target) is not int
        or not 0 <= source <= 1_000_000
        or not 0 <= target <= 1_000_000
    ):
        raise ValueError("source and target must be valid stop identifiers")
    if source == target:
        return 0

    routes_by_stop: dict[int, list[int]] = defaultdict(list)
    for route_index, route in enumerate(routes):
        for stop in route:
            routes_by_stop[stop].append(route_index)

    queue = deque([(source, 0)])
    visited_stops = {source}
    boarded_routes: set[int] = set()
    while queue:
        stop, buses = queue.popleft()
        for route_index in routes_by_stop[stop]:
            if route_index in boarded_routes:
                continue
            boarded_routes.add(route_index)
            for next_stop in routes[route_index]:
                if next_stop == target:
                    return buses + 1
                if next_stop not in visited_stops:
                    visited_stops.add(next_stop)
                    queue.append((next_stop, buses + 1))
    return -1
```

BFS first reaches every stop with the fewest buses, and every route is expanded
only at that minimum boarding count.

**Complexity:** `O(S)` time and space for `S` total route-stop entries.
