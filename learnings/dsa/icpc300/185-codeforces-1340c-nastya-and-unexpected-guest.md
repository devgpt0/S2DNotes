# ICPC300 185: Codeforces 1340C - Nastya and Unexpected Guest

**Source:** [Codeforces 1340C](https://codeforces.com/problemset/problem/1340/C)  
**Pattern:** 0-1 BFS over safe-point and green-time states

## Exact contract

Nastya travels on a line from `0` to `n`. She may move one unit per second in
either direction during each green period of length `g`. If green expires
before she finishes, she must be at one of the given safe points and wait the
whole red period of length `r` before moving again. Find the minimum arrival
time, or `-1` if arrival is impossible.

## First principles

A state is `(safe_point, used_green_time)`. Between safe points, only adjacent
ones in sorted order matter: skipping an intermediate point is equivalent to
passing it without stopping.

A move that keeps used time below `g` costs no completed light cycle. A move
that reaches exactly `g` at a safe point forces one red wait and resets used
time to zero. Therefore transitions cost either zero or one completed cycle,
which is a 0-1 BFS graph.

## Cases that decide correctness

- The destination need not be a safe point.
- No red wait is paid after reaching the destination, even exactly at time
  `g`.
- Reversing direction can be necessary.
- Arriving at a non-destination point exactly when green ends is legal only if
  it is safe.
- A gap longer than `g` cannot be crossed in one green period.

## Brute force: Dijkstra on the full state graph

```python
from heapq import heappop, heappush


def unexpected_guest_brute(
    destination: int,
    safe_points: list[int],
    green: int,
    red: int,
) -> int:
    points = sorted(safe_points)
    start = points.index(0)
    infinity = 10**30
    distance = [[infinity] * (green + 1) for _ in points]
    distance[start][0] = 0
    queue = [(0, start, 0)]
    answer = infinity

    while queue:
        elapsed, point_index, used = heappop(queue)
        if elapsed != distance[point_index][used]:
            continue
        remaining = destination - points[point_index]
        if remaining >= 0 and used + remaining <= green:
            answer = min(answer, elapsed + remaining)
        for neighbor in (point_index - 1, point_index + 1):
            if not 0 <= neighbor < len(points):
                continue
            travel = abs(points[neighbor] - points[point_index])
            new_used = used + travel
            if new_used > green:
                continue
            extra = travel
            if new_used == green:
                new_used = 0
                extra += red
            candidate = elapsed + extra
            if candidate < distance[neighbor][new_used]:
                distance[neighbor][new_used] = candidate
                heappush(queue, (candidate, neighbor, new_used))
    return -1 if answer == infinity else answer
```

This keeps actual elapsed times and pays a heap logarithm per state transition.

## Better insight: separate completed cycles from used green time

For a fixed state, elapsed time is
`cycles * (g+r) + used_green_time`. Minimizing elapsed time therefore means
minimizing `cycles`, and each transition changes it by only zero or one.

## Expert solution: cycle-count 0-1 BFS

```python
import sys
from array import array
from collections import deque


def solve() -> None:
    input_stream = sys.stdin.buffer
    destination, safe_count = map(int, input_stream.readline().split())
    points = sorted(map(int, input_stream.readline().split()))
    green, red = map(int, input_stream.readline().split())

    width = green + 1
    infinity = 2**31 - 1
    cycle_count = array("i", [infinity]) * (safe_count * width)
    start = points.index(0) * width
    cycle_count[start] = 0
    queue = deque([start])
    answer = 10**30

    while queue:
        state = queue.popleft()
        point_index, used = divmod(state, width)
        cycles = cycle_count[state]
        remaining = destination - points[point_index]
        if remaining >= 0 and used + remaining <= green:
            answer = min(
                answer,
                cycles * (green + red) + used + remaining,
            )

        for neighbor in (point_index - 1, point_index + 1):
            if not 0 <= neighbor < safe_count:
                continue
            new_used = used + abs(points[neighbor] - points[point_index])
            if new_used > green:
                continue
            new_cycles = cycles
            if new_used == green:
                new_used = 0
                new_cycles += 1
            next_state = neighbor * width + new_used
            if new_cycles >= cycle_count[next_state]:
                continue
            cycle_count[next_state] = new_cycles
            if new_cycles == cycles:
                queue.appendleft(next_state)
            else:
                queue.append(next_state)

    print(-1 if answer == 10**30 else answer)


if __name__ == "__main__":
    solve()
```

The deque computes the fewest completed green-red cycles for every reachable
state. The final direct walk correctly omits a red wait after arrival.

**Complexity:** `O(mg)` time and compact `O(mg)` integer storage.
