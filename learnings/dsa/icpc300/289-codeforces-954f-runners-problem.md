# ICPC300 289: Codeforces 954F - Runner's Problem

**Source:** [Codeforces 954F - Runner's Problem](https://codeforces.com/problemset/problem/954/F)  
**Rating:** 2400  
**Pattern:** obstacle sweep with 3x3 matrix exponentiation  
**Goal:** A runner starts in the middle row at column one of a three-row track
and must finish in the middle row at column `length`. Each next column may use
the same or an adjacent row. Count paths avoiding inclusive blocked intervals,
modulo `1_000_000_007`. Rows are zero-based in the code.

## 1. First principles

For a fixed set of open rows, advancing one column is a constant `3 x 3`
transition. Obstacle endpoints divide the huge track into constant-mask runs,
so a run of `k` destination columns applies the same matrix to the `k`th power.

## 2. Cases that decide correctness

- The start and finish are both the middle row.
- A move changes the row by at most one.
- A blocked destination row receives no paths.
- Intervals may overlap, so endpoint events use counts rather than XOR toggles.
- Column one is the initial state, not a transition from a virtual column.

## 3. Brute force: process every column

```python
MODULO = 1_000_000_007


def runner_path_count_brute(length: int, obstacles: list[tuple[int, int, int]]) -> int:
    if length <= 0 or any(
        not 0 <= row < 3 or not 1 <= left <= right <= length
        for row, left, right in obstacles
    ):
        raise ValueError("invalid track")

    blocked = [[False] * (length + 1) for _ in range(3)]
    for row, left, right in obstacles:
        for column in range(left, right + 1):
            blocked[row][column] = True
    ways = [0, int(not blocked[1][1]), 0]
    for column in range(2, length + 1):
        ways = [
            0
            if blocked[row][column]
            else sum(
                ways[previous] for previous in range(3) if abs(row - previous) <= 1
            )
            % MODULO
            for row in range(3)
        ]
    return ways[1]
```

**Complexity:** `O(length + total blocked interval length)` time and space.

## 4. Better transition: exponentiate each constant obstacle run

Create `+1` and `-1` events for every blocked interval. Between consecutive
event columns, the open-row mask is fixed. Build its destination-filtered move
matrix and exponentiate it for the number of destination columns in that run.

## 5. Expert solution: sweep endpoints and power matrices

```python
MODULO = 1_000_000_007


def runner_path_count(length: int, obstacles: list[tuple[int, int, int]]) -> int:
    if length <= 0 or any(
        not 0 <= row < 3 or not 1 <= left <= right <= length
        for row, left, right in obstacles
    ):
        raise ValueError("invalid track")

    events: dict[int, list[int]] = {1: [0, 0, 0], length + 1: [0, 0, 0]}
    for row, left, right in obstacles:
        events.setdefault(left, [0, 0, 0])[row] += 1
        events.setdefault(right + 1, [0, 0, 0])[row] -= 1

    def multiply(first: list[list[int]], second: list[list[int]]) -> list[list[int]]:
        return [
            [
                sum(first[row][middle] * second[middle][column] for middle in range(3))
                % MODULO
                for column in range(3)
            ]
            for row in range(3)
        ]

    def apply_power(
        vector: list[int], matrix: list[list[int]], exponent: int
    ) -> list[int]:
        while exponent:
            if exponent & 1:
                vector = [
                    sum(matrix[row][column] * vector[column] for column in range(3))
                    % MODULO
                    for row in range(3)
                ]
            matrix = multiply(matrix, matrix)
            exponent >>= 1
        return vector

    positions = sorted(events)
    blocked_counts = [0, 0, 0]
    ways = [0, 1, 0]
    for event_index, position in enumerate(positions[:-1]):
        for row in range(3):
            blocked_counts[row] += events[position][row]
        if position == 1 and blocked_counts[1] > 0:
            ways[1] = 0

        next_position = positions[event_index + 1]
        destination_count = max(0, next_position - max(position, 2))
        transition = [
            [
                int(blocked_counts[row] == 0 and abs(row - previous) <= 1)
                for previous in range(3)
            ]
            for row in range(3)
        ]
        ways = apply_power(ways, transition, destination_count)
    return ways[1]
```

### Why the expert code is correct

The vector before each run describes paths at the preceding processed column.
Its transition admits exactly the legal neighboring moves into open destination
rows. Endpoint counts construct the correct blocked mask for every maximal
constant run, and powering applies that transition once per destination column.
Thus the sweep is identical to the column DP without visiting empty columns.

**Complexity:** `O(n log length)` time and `O(n)` space for `n` obstacles.

## 6. What to remember

```text
huge coordinate range -> sweep only change points
constant local movement -> small transition matrix
long unchanged run -> matrix exponentiation
```
