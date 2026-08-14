# 140. Watching Fireworks is Fun — Codeforces 372C

**Source:** [Codeforces 372C - Watching Fireworks is Fun](https://codeforces.com/problemset/problem/372/C)  
**Difficulty:** 2200

## 1. Problem in plain words

Cities lie at integer positions `1..n`. Firework `(a, b, t)` gives happiness `b - |a - x|` when watched from city `x` at time `t`. Between two event times, you can move at most `d` cities per time unit. Choose a city for every firework to maximize total happiness.

## 2. First principles

Let `previous[x]` be the best total ending at city `x` after the preceding event. If the time difference permits radius `r`, then

`current[x] = b - |a-x| + max(previous[y])` over `|x-y| <= r`.

For consecutive `x`, this predecessor interval slides by one. A monotone deque supplies all its maxima in linear time per event.

## 3. Cases that define correctness

- The starting city is free, so all positions begin with value zero.
- Cap movement radius at `n - 1`; larger movement reaches every city.
- Event rewards can make the optimal total negative.
- Source events arrive in strictly increasing time order.

## 4. Brute force

For every event and destination city, scan every reachable previous city.

```python
def maximum_firework_happiness_brute_force(
    city_count: int, speed: int, events: list[tuple[int, int, int]]
) -> int:
    if city_count <= 0 or speed < 0 or not events:
        raise ValueError("invalid city count, speed, or event list")
    if any(not 1 <= position <= city_count for position, _, _ in events):
        raise ValueError("event position is outside the cities")
    if any(
        events[index][2] >= events[index + 1][2] for index in range(len(events) - 1)
    ):
        raise ValueError("event times must be strictly increasing")

    previous = [0] * city_count
    previous_time = events[0][2]
    for position, reward, time in events:
        radius = min(city_count - 1, speed * (time - previous_time))
        current = [0] * city_count
        for city in range(city_count):
            left = max(0, city - radius)
            right = min(city_count, city + radius + 1)
            current[city] = (
                max(previous[left:right]) + reward - abs(position - (city + 1))
            )
        previous = current
        previous_time = time
    return max(previous)
```

Time is `O(mn²)` and space is `O(n)`.

## 5. Better approach: range-maximum segment tree

Build an iterative maximum segment tree over the preceding DP layer. Each destination makes one range-maximum query.

```python
def maximum_firework_happiness_segment_tree(
    city_count: int, speed: int, events: list[tuple[int, int, int]]
) -> int:
    if city_count <= 0 or speed < 0 or not events:
        raise ValueError("invalid city count, speed, or event list")
    if any(not 1 <= position <= city_count for position, _, _ in events):
        raise ValueError("event position is outside the cities")
    if any(
        events[index][2] >= events[index + 1][2] for index in range(len(events) - 1)
    ):
        raise ValueError("event times must be strictly increasing")

    previous = [0] * city_count
    previous_time = events[0][2]
    for position, reward, time in events:
        tree = [-(10**40)] * (2 * city_count)
        tree[city_count:] = previous
        for node in range(city_count - 1, 0, -1):
            tree[node] = max(tree[node * 2], tree[node * 2 + 1])

        def range_maximum(left: int, right: int) -> int:
            left += city_count
            right += city_count
            answer = -(10**40)
            while left < right:
                if left & 1:
                    answer = max(answer, tree[left])
                    left += 1
                if right & 1:
                    right -= 1
                    answer = max(answer, tree[right])
                left //= 2
                right //= 2
            return answer

        radius = min(city_count - 1, speed * (time - previous_time))
        current = [0] * city_count
        for city in range(city_count):
            left = max(0, city - radius)
            right = min(city_count, city + radius + 1)
            current[city] = (
                range_maximum(left, right) + reward - abs(position - (city + 1))
            )
        previous = current
        previous_time = time
    return max(previous)
```

Time is `O(mn log n)` and space is `O(n)`.

## 6. Expert solution: sliding-window maxima

For each event, sweep destination cities left to right. Keep reachable previous cities in decreasing DP-value order and evict indices that leave the movement window.

```python
from collections import deque


def maximum_firework_happiness(
    city_count: int, speed: int, events: list[tuple[int, int, int]]
) -> int:
    if city_count <= 0 or speed < 0 or not events:
        raise ValueError("invalid city count, speed, or event list")
    if any(not 1 <= position <= city_count for position, _, _ in events):
        raise ValueError("event position is outside the cities")
    if any(
        events[index][2] >= events[index + 1][2] for index in range(len(events) - 1)
    ):
        raise ValueError("event times must be strictly increasing")

    previous = [0] * city_count
    previous_time = events[0][2]
    for position, reward, time in events:
        radius = min(city_count - 1, speed * (time - previous_time))
        candidates: deque[int] = deque()
        right = -1
        current = [0] * city_count

        for city in range(city_count):
            window_right = min(city_count - 1, city + radius)
            while right < window_right:
                right += 1
                while candidates and previous[candidates[-1]] <= previous[right]:
                    candidates.pop()
                candidates.append(right)
            window_left = city - radius
            while candidates and candidates[0] < window_left:
                candidates.popleft()
            current[city] = (
                previous[candidates[0]] + reward - abs(position - (city + 1))
            )

        previous = current
        previous_time = time
    return max(previous)
```

## 7. Why the expert solution is correct

The DP recurrence considers exactly the cities reachable between consecutive event times. During the sweep, the deque contains precisely that sliding predecessor window, and decreasing values make its front the maximum. Removing a dominated back entry is safe because the newer entry is at least as good and remains in every future window at least as long.

Each city enters and leaves the deque once per event, giving `O(mn)` time and `O(n)` space.
