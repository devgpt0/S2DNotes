# ICPC300 112: CSES - Monster Game I

**Source:** [CSES - Monster Game I](https://cses.fi/problemset/task/2084/)  
**Pattern:** monotone convex hull trick  
**Goal:** Compute
`dp[i] = min(dp[j] + slope[j] * query[i])`, including an initial line with
intercept `0`.

`query_points[i]` is the source value `s[i]`, `line_slopes[i]` is `f[i]`, and
`initial_slope` is `x`. Monster Game I guarantees nondecreasing query points
and nonincreasing inserted slopes.

## 1. First principles

Each previous state is a line:

```text
y = line_slopes[j] * x + dp[j]
```

The next DP value is the minimum line value at `query_points[i]`. Monotone
slopes make obsolete lines removable from the back; monotone queries make the
best line removable from the front.

## 2. Cases that decide correctness

- The initial line participates in the first query.
- Equal slopes keep only the smaller intercept.
- Large products require integer arithmetic.
- A line is removed only when its intersection order is obsolete.
- The answer is the final DP value, not the minimum over all states.

## 3. Brute force: scan every prior state

```python
def monster_game_i_brute(
    query_points: list[int], line_slopes: list[int], initial_slope: int
) -> int:
    if not query_points or len(query_points) != len(line_slopes):
        raise ValueError("query_points and line_slopes need equal nonzero length")

    dynamic = [0] * len(query_points)
    for index, point in enumerate(query_points):
        best = initial_slope * point
        for previous in range(index):
            best = min(
                best,
                dynamic[previous] + line_slopes[previous] * point,
            )
        dynamic[index] = best
    return dynamic[-1]
```

**Complexity:** `O(n^2)` time and `O(n)` space.

## 4. Better: Li Chao tree

A Li Chao tree supports arbitrary insertion/query order over the known query
coordinates.

```python
def monster_game_i_li_chao(
    query_points: list[int], line_slopes: list[int], initial_slope: int
) -> int:
    if not query_points or len(query_points) != len(line_slopes):
        raise ValueError("query_points and line_slopes need equal nonzero length")

    coordinates = sorted(set(query_points))
    lines: list[tuple[int, int] | None] = [None] * (4 * len(coordinates))

    def value(line: tuple[int, int], point: int) -> int:
        return line[0] * point + line[1]

    def add_line(node: int, low: int, high: int, new_line: tuple[int, int]) -> None:
        current = lines[node]
        if current is None:
            lines[node] = new_line
            return

        middle = (low + high) // 2
        if value(new_line, coordinates[middle]) < value(current, coordinates[middle]):
            current, new_line = new_line, current
            lines[node] = current
        if low == high:
            return
        if value(new_line, coordinates[low]) < value(current, coordinates[low]):
            add_line(2 * node, low, middle, new_line)
        elif value(new_line, coordinates[high]) < value(current, coordinates[high]):
            add_line(2 * node + 1, middle + 1, high, new_line)

    def query(node: int, low: int, high: int, index: int) -> int:
        line = lines[node]
        best = value(line, coordinates[index]) if line is not None else 10**40
        if low == high:
            return best
        middle = (low + high) // 2
        if index <= middle:
            return min(best, query(2 * node, low, middle, index))
        return min(best, query(2 * node + 1, middle + 1, high, index))

    coordinate_index = {point: index for index, point in enumerate(coordinates)}
    add_line(1, 0, len(coordinates) - 1, (initial_slope, 0))
    answer = 0
    for point, slope in zip(query_points, line_slopes, strict=True):
        answer = query(1, 0, len(coordinates) - 1, coordinate_index[point])
        add_line(1, 0, len(coordinates) - 1, (slope, answer))
    return answer
```

**Complexity:** `O(n log n)` time and `O(n)` space.

## 5. Expert solution: monotone line deque

Cross multiplication compares intersection order without floating point.

```python
from collections import deque


def monster_game_i_monotone_hull(
    query_points: list[int], line_slopes: list[int], initial_slope: int
) -> int:
    if not query_points or len(query_points) != len(line_slopes):
        raise ValueError("query_points and line_slopes need equal nonzero length")
    if any(
        query_points[index] > query_points[index + 1]
        for index in range(len(query_points) - 1)
    ):
        raise ValueError("query points must be nondecreasing")
    inserted_slopes = [initial_slope, *line_slopes]
    if any(
        inserted_slopes[index] < inserted_slopes[index + 1]
        for index in range(len(inserted_slopes) - 1)
    ):
        raise ValueError("inserted slopes must be nonincreasing")

    lines: deque[tuple[int, int]] = deque()

    def evaluate(line: tuple[int, int], point: int) -> int:
        return line[0] * point + line[1]

    def redundant(
        first: tuple[int, int],
        second: tuple[int, int],
        third: tuple[int, int],
    ) -> bool:
        return (second[1] - first[1]) * (second[0] - third[0]) >= (
            third[1] - second[1]
        ) * (first[0] - second[0])

    def add_line(slope: int, intercept: int) -> None:
        while lines and lines[-1][0] == slope:
            if lines[-1][1] <= intercept:
                return
            lines.pop()
        new_line = (slope, intercept)
        while len(lines) >= 2 and redundant(lines[-2], lines[-1], new_line):
            lines.pop()
        lines.append(new_line)

    add_line(initial_slope, 0)
    answer = 0
    for point, slope in zip(query_points, line_slopes, strict=True):
        while len(lines) >= 2 and evaluate(lines[0], point) >= evaluate(
            lines[1], point
        ):
            lines.popleft()
        answer = evaluate(lines[0], point)
        add_line(slope, answer)
    return answer
```

### Why the expert code is correct

Back removal preserves only lines that are optimal on some future interval.
Because queries never decrease, once the second line beats the first, the
first can never become optimal again.

**Complexity:** `O(n)` time and `O(n)` space; each line enters and leaves the
deque once.

## 6. What to remember

```text
DP transition min(dp[j] + m[j] * x[i]) -> minimum line query
monotone slopes -> prune hull from back
monotone x -> advance best line from front
```
