# Focus300 115: LeetCode 778 - Swim in Rising Water

**Source:** [LeetCode 778](https://leetcode.com/problems/swim-in-rising-water/)  
**Difficulty:** Hard  
**Pattern:** minimax shortest path

## Exact contract

An `n x n` grid is a permutation of elevations `0..n^2-1`, with `1 <= n <=
50`. At time `t`, cells of elevation at most `t` are traversable through four
directions. Return the earliest time at which the top-left cell can reach the
bottom-right cell.

## First principles

A path becomes usable when the water reaches its highest cell. The problem is
therefore to minimize the maximum elevation along a path, not to minimize its
length or sum. Dijkstra's algorithm still applies when path extension uses
`max(current_cost, next_elevation)` because that cost never decreases.


## Classroom board: see the repeated work once

```text
brute force tries every choice.
the optimized solution keeps only the state that must survive to the
next step.
```



## Step-by-step transformation

1. Read the input and identify the smallest state that still determines the answer.
2. Process one element, node, or row at a time while preserving that state.
3. Discard work that can no longer change the result.
4. Convert the surviving state into the output the problem requests.

The examples and code below show this transformation on the specific problem instance.


## Diagram: input to output

```text

        input
            |
            v
        core invariant
            |
            v
        process one step at a time
            |
            v
        output
```

The note shows the main idea, the repeated work, and the small state that turns the input into the output.

## Cases that decide correctness

- The answer is at least the elevation of both endpoints.
- A longer path can become available earlier than a geometrically short path.
- A `1 x 1` grid returns its only elevation, zero under the source contract.
- Each cell needs its best known minimax cost, not merely a visited flag at
  insertion time.
- Duplicate or out-of-range elevations violate the source permutation.

## Brute force: raise the water one level at a time

```python
from collections import deque


def earliest_swim_time_brute(grid: list[list[int]]) -> int:
    if (
        type(grid) is not list
        or not grid
        or len(grid) > 50
        or any(type(row) is not list or len(row) != len(grid) for row in grid)
    ):
        raise TypeError("grid must be a nonempty square list with side at most 50")
    if any(type(value) is not int for row in grid for value in row):
        raise TypeError("every elevation must be an integer")
    elevations = [value for row in grid for value in row]
    if set(elevations) != set(range(len(elevations))):
        raise ValueError("elevations must be a permutation of 0..n^2-1")

    side = len(grid)
    for water in range(max(grid[0][0], grid[-1][-1]), side * side):
        queue = deque([(0, 0)])
        seen = {(0, 0)}
        while queue:
            row, column = queue.popleft()
            if (row, column) == (side - 1, side - 1):
                return water
            for row_step, column_step in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                next_row = row + row_step
                next_column = column + column_step
                if (
                    0 <= next_row < side
                    and 0 <= next_column < side
                    and (next_row, next_column) not in seen
                    and grid[next_row][next_column] <= water
                ):
                    seen.add((next_row, next_column))
                    queue.append((next_row, next_column))
    raise RuntimeError("the maximum water level must connect the grid")
```

Up to `n^2` water levels each scan `n^2` cells, taking `O(n^4)` time and
`O(n^2)` space.

## Better approach: binary-search a reachability threshold

Reachability is monotone in the water level, so binary search plus BFS takes
`O(n^2 log n)` time. Dijkstra avoids repeating whole-grid reachability scans
and discovers the minimum threshold directly.

## Expert solution: Dijkstra under maximum-edge composition

```python
from heapq import heappop, heappush


def earliest_swim_time(grid: list[list[int]]) -> int:
    if (
        type(grid) is not list
        or not grid
        or len(grid) > 50
        or any(type(row) is not list or len(row) != len(grid) for row in grid)
    ):
        raise TypeError("grid must be a nonempty square list with side at most 50")
    if any(type(value) is not int for row in grid for value in row):
        raise TypeError("every elevation must be an integer")
    elevations = [value for row in grid for value in row]
    if set(elevations) != set(range(len(elevations))):
        raise ValueError("elevations must be a permutation of 0..n^2-1")

    side = len(grid)
    infinity = side * side
    best = [[infinity] * side for _ in range(side)]
    best[0][0] = grid[0][0]
    heap = [(grid[0][0], 0, 0)]
    while heap:
        water, row, column = heappop(heap)
        if water != best[row][column]:
            continue
        if (row, column) == (side - 1, side - 1):
            return water
        for row_step, column_step in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            next_row = row + row_step
            next_column = column + column_step
            if 0 <= next_row < side and 0 <= next_column < side:
                next_water = max(water, grid[next_row][next_column])
                if next_water < best[next_row][next_column]:
                    best[next_row][next_column] = next_water
                    heappush(heap, (next_water, next_row, next_column))
    raise RuntimeError("a valid grid must contain a path")
```

When a cell leaves the heap at its best cost, no later path can lower its
maximum elevation. The first finalized destination cost is the earliest water
level that supports any complete path.

**Complexity:** `O(n^2 log n)` time and `O(n^2)` space.
