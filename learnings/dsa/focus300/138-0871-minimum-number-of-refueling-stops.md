# Focus300 138: LeetCode 871 - Minimum Number of Refueling Stops

**Source:** [LeetCode 871](https://leetcode.com/problems/minimum-number-of-refueling-stops/)  
**Difficulty:** Hard  
**Pattern:** greedy retroactive choice with a max-heap

## Exact contract

A car starts at position zero with `start_fuel`, consumes one fuel per mile,
and may take all fuel at strictly increasing stations `[position, fuel]` before
positive `target`. Return the minimum stops needed to reach target, or `-1`.

## First principles

Whenever current fuel cannot reach the target, a stop at some already reachable
station is required. Choosing the largest available fuel extends reach at least
as far as any other single choice, never uses more stops, and leaves every
smaller station available for later.


## Classroom board: keep only the useful unfinished work

```text
a stack stores the part of the state that can still matter after the next step.
```



## Step-by-step transformation

1. Load the current candidates into a stack, queue, heap, or window.
2. Push or pop the structure while the current element keeps the invariant true.
3. Drop stale candidates and keep only the ones that can still affect the answer.
4. Read the final top, window score, or popped order as the output.

These problems transform the input by keeping just the active frontier of candidates instead of rescanning the whole array every time.


## Diagram: active frontier only

```text

            scan left to right
                |
                v
            keep active candidates
                |
                v
            pop stale work
                |
                v
            current best answer
```

These notes keep only the active frontier of useful candidates instead of rescanning the whole input.

## Cases that decide correctness

- If starting fuel reaches target, return zero.
- Only stations at or before current reach can be selected.
- A station may be used at most once.
- Running out of reachable stations before target means `-1`.
- Station order is by position, not fuel amount.

## Brute force: test every station subset

```python
def minimum_refuel_stops_brute(
    target: int, start_fuel: int, stations: list[list[int]]
) -> int:
    if type(target) is not int or type(start_fuel) is not int:
        raise TypeError("target and start_fuel must be integers")
    if target <= 0 or start_fuel < 0:
        raise ValueError("target must be positive and start_fuel non-negative")
    if type(stations) is not list or any(
        type(station) is not list
        or len(station) != 2
        or any(type(value) is not int for value in station)
        for station in stations
    ):
        raise TypeError("stations must be [position, fuel] integer lists")
    if any(
        not 0 < position < target or fuel <= 0 for position, fuel in stations
    ) or any(
        stations[index][0] >= stations[index + 1][0]
        for index in range(len(stations) - 1)
    ):
        raise ValueError(
            "stations must have increasing valid positions and positive fuel"
        )

    answer = len(stations) + 1
    for mask in range(1 << len(stations)):
        fuel = start_fuel
        previous = 0
        feasible = True
        for index, (position, station_fuel) in enumerate(stations):
            fuel -= position - previous
            if fuel < 0:
                feasible = False
                break
            if mask & (1 << index):
                fuel += station_fuel
            previous = position
        if feasible and fuel >= target - previous:
            answer = min(answer, mask.bit_count())
    return -1 if answer > len(stations) else answer
```

This examines `2^n` subsets and simulates `O(n)` travel for each.

## Better approach: DP by number of stops

Let `reach[j]` be the farthest distance reachable after exactly `j` stops.
Updating it backward for every station takes `O(n^2)` time and `O(n)` space.

## Expert solution: take the largest reachable fuel only when needed

```python
from heapq import heappop, heappush


def minimum_refuel_stops(
    target: int, start_fuel: int, stations: list[list[int]]
) -> int:
    if type(target) is not int or type(start_fuel) is not int:
        raise TypeError("target and start_fuel must be integers")
    if target <= 0 or start_fuel < 0:
        raise ValueError("target must be positive and start_fuel non-negative")
    if type(stations) is not list or any(
        type(station) is not list
        or len(station) != 2
        or any(type(value) is not int for value in station)
        for station in stations
    ):
        raise TypeError("stations must be [position, fuel] integer lists")
    if any(
        not 0 < position < target or fuel <= 0 for position, fuel in stations
    ) or any(
        stations[index][0] >= stations[index + 1][0]
        for index in range(len(stations) - 1)
    ):
        raise ValueError(
            "stations must have increasing valid positions and positive fuel"
        )

    reachable_fuel: list[int] = []
    reach = start_fuel
    station_index = 0
    stops = 0
    while reach < target:
        while station_index < len(stations) and stations[station_index][0] <= reach:
            heappush(reachable_fuel, -stations[station_index][1])
            station_index += 1
        if not reachable_fuel:
            return -1
        reach -= heappop(reachable_fuel)
        stops += 1
    return stops
```

The heap delays committing to a station until a stop is forced. The largest
available fuel maximizes reach for the current stop count, which is the greedy
exchange invariant.

**Complexity:** `O(n log n)` time and `O(n)` space.
