# ICPC300 042: CSES - Investigation

**Source:** [CSES - Investigation](https://cses.fi/problemset/task/1202/)  
**Pattern:** Dijkstra with shortest-path statistics  
**Goal:** From city `1` to city `n`, output the minimum price, the number of
minimum-price routes modulo `1_000_000_007`, and the minimum and maximum flight
counts among those routes.

## 1. Problem in plain words

Each directed flight has a positive price. Four values describe the cheapest
routes:

1. their common minimum total price;
2. how many such routes exist;
3. the fewest flights used by one;
4. the most flights used by one.

Parallel flights are distinct choices. A route's flight count is the number of
edges, not the number of cities.

## 2. First principles

For every city `v`, maintain statistics over routes whose cost equals
`distance[v]`:

- `route_count[v]` sums their counts;
- `minimum_flights[v]` takes their minimum edge count;
- `maximum_flights[v]` takes their maximum edge count.

Relaxing edge `u -> v` of price `w` has two cases:

- smaller candidate cost: replace all four values at `v`;
- equal candidate cost: merge count, minimum, and maximum.

Prices are positive. Therefore every predecessor on a shortest route has
strictly smaller distance and is finalized before its destination in Dijkstra.

## 3. Cases that decide correctness

| Case | Required behavior |
| --- | --- |
| Parallel equal-price flights | Count both routes. |
| Equal price with different edge counts | Merge count, minimum, and maximum. |
| A more expensive route with fewer edges | Ignore it completely. |
| Stale heap entry | Skip it without merging again. |
| Route counts exceed the modulus | Reduce only the count, never the distance. |

## 4. Brute force: enumerate simple routes

Positive prices imply a cheapest route never repeats a city: deleting its
positive-cost cycle would make it cheaper. This makes simple-path DFS a correct
tiny oracle.

```python
MODULO = 1_000_000_007


def investigate_routes_brute_force(
    city_count: int, flights: list[tuple[int, int, int]]
) -> tuple[int, int, int, int]:
    graph: list[list[tuple[int, int]]] = [[] for _ in range(city_count)]
    for start, end, price in flights:
        if price <= 0:
            raise ValueError("flight prices must be positive")
        graph[start].append((end, price))

    target = city_count - 1
    seen = [False] * city_count
    seen[0] = True
    best_price: int | None = None
    route_count = 0
    minimum_flights = city_count
    maximum_flights = 0

    def search(city: int, price: int, used_flights: int) -> None:
        nonlocal best_price, route_count, minimum_flights, maximum_flights
        if best_price is not None and price > best_price:
            return
        if city == target:
            if best_price is None or price < best_price:
                best_price = price
                route_count = 1
                minimum_flights = used_flights
                maximum_flights = used_flights
            elif price == best_price:
                route_count = (route_count + 1) % MODULO
                minimum_flights = min(minimum_flights, used_flights)
                maximum_flights = max(maximum_flights, used_flights)
            return

        for neighbor, edge_price in graph[city]:
            if seen[neighbor]:
                continue
            seen[neighbor] = True
            search(neighbor, price + edge_price, used_flights + 1)
            seen[neighbor] = False

    search(0, 0, 0)
    if best_price is None:
        raise ValueError("the destination is unreachable")
    return best_price, route_count, minimum_flights, maximum_flights
```

**Complexity:** `O(number of simple routes * n)` time and `O(n + m)` memory.

## 5. Better: Bellman-Ford distances, then shortest-DAG DP

First compute distances in `O(nm)`. Because every price is positive, an edge
on a shortest route goes from a smaller distance to a larger one. Sorting
cities by distance gives a valid order for the three remaining statistics.

```python
MODULO = 1_000_000_007


def investigate_routes_bellman_ford(
    city_count: int, flights: list[tuple[int, int, int]]
) -> tuple[int, int, int, int]:
    infinity = 10**100
    distance = [infinity] * city_count
    distance[0] = 0

    for _ in range(city_count - 1):
        changed = False
        for start, end, price in flights:
            if price <= 0:
                raise ValueError("flight prices must be positive")
            candidate = distance[start] + price
            if candidate < distance[end]:
                distance[end] = candidate
                changed = True
        if not changed:
            break

    if distance[-1] == infinity:
        raise ValueError("the destination is unreachable")

    graph: list[list[tuple[int, int]]] = [[] for _ in range(city_count)]
    for start, end, price in flights:
        graph[start].append((end, price))

    route_count = [0] * city_count
    minimum_flights = [city_count + 1] * city_count
    maximum_flights = [-1] * city_count
    route_count[0] = 1
    minimum_flights[0] = 0
    maximum_flights[0] = 0

    for city in sorted(range(city_count), key=distance.__getitem__):
        for neighbor, price in graph[city]:
            if distance[city] + price != distance[neighbor]:
                continue
            route_count[neighbor] = (route_count[neighbor] + route_count[city]) % MODULO
            minimum_flights[neighbor] = min(
                minimum_flights[neighbor], minimum_flights[city] + 1
            )
            maximum_flights[neighbor] = max(
                maximum_flights[neighbor], maximum_flights[city] + 1
            )

    return (
        distance[-1],
        route_count[-1],
        minimum_flights[-1],
        maximum_flights[-1],
    )
```

**Complexity:** `O(nm + n log n)` time and `O(n + m)` memory.

## 6. Expert solution: merge all statistics during Dijkstra

```python
from heapq import heappop, heappush

MODULO = 1_000_000_007


def investigate_routes(
    city_count: int, flights: list[tuple[int, int, int]]
) -> tuple[int, int, int, int]:
    if city_count < 2:
        raise ValueError("source and destination must be different cities")

    graph: list[list[tuple[int, int]]] = [[] for _ in range(city_count)]
    for start, end, price in flights:
        if not 0 <= start < city_count or not 0 <= end < city_count:
            raise ValueError("flight endpoint is outside the graph")
        if price <= 0:
            raise ValueError("flight prices must be positive")
        graph[start].append((end, price))

    infinity = 10**100
    distance = [infinity] * city_count
    route_count = [0] * city_count
    minimum_flights = [city_count + 1] * city_count
    maximum_flights = [-1] * city_count

    distance[0] = 0
    route_count[0] = 1
    minimum_flights[0] = 0
    maximum_flights[0] = 0
    heap = [(0, 0)]

    while heap:
        current_distance, city = heappop(heap)
        if current_distance != distance[city]:
            continue

        for neighbor, price in graph[city]:
            candidate = current_distance + price
            if candidate < distance[neighbor]:
                distance[neighbor] = candidate
                route_count[neighbor] = route_count[city]
                minimum_flights[neighbor] = minimum_flights[city] + 1
                maximum_flights[neighbor] = maximum_flights[city] + 1
                heappush(heap, (candidate, neighbor))
            elif candidate == distance[neighbor]:
                route_count[neighbor] = (
                    route_count[neighbor] + route_count[city]
                ) % MODULO
                minimum_flights[neighbor] = min(
                    minimum_flights[neighbor], minimum_flights[city] + 1
                )
                maximum_flights[neighbor] = max(
                    maximum_flights[neighbor], maximum_flights[city] + 1
                )

    if distance[-1] == infinity:
        raise ValueError("the destination is unreachable")
    return (
        distance[-1],
        route_count[-1],
        minimum_flights[-1],
        maximum_flights[-1],
    )
```

### Why the expert code is correct

- Dijkstra finalizes cities in nondecreasing shortest distance.
- Positive edge prices make every shortest-route predecessor strictly earlier,
  so all of its statistics are complete before they are propagated.
- A smaller relaxation replaces the known route family; an equal relaxation
  merges exactly another family of minimum-price routes.
- The three merge operations are respectively sum, minimum, and maximum, which
  match the four requested source values.

**Complexity:** `O((n + m) log n)` time and `O(n + m)` memory.

## 7. What to remember

When shortest paths need metadata, define how metadata behaves on a strictly
better relaxation and on an equal relaxation before coding Dijkstra.
