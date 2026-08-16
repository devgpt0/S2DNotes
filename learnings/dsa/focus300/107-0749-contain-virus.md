# Focus300 107: LeetCode 749 - Contain Virus

**Source:** [LeetCode 749](https://leetcode.com/problems/contain-virus/)  
**Difficulty:** Hard  
**Pattern:** component simulation with distinct frontiers

## Exact contract

Given a rectangular binary grid, each `1` is infected and each `0` is
uninfected. Every day, quarantine the connected infected region that threatens
the most distinct uninfected cells, building one wall for every infected-to-
uninfected edge on its boundary. All other regions then infect their adjacent
uninfected cells. Return the total walls built. The source guarantees no tie
between regions selected for quarantine.

## First principles

One region needs two different boundary measurements. Its frontier is a set of
distinct zero cells and decides which region is quarantined. Its wall count is
the number of edges leading to zeros and may count one zero more than once.
Conflating those quantities changes both the choice and the answer.


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

- Connectivity uses four directions, never diagonals.
- A shared threatened zero appears once in a frontier but may need several walls.
- Quarantined cells never spread again.
- Every non-quarantined region spreads simultaneously after the wall is built.
- Stop when no active region can reach an uninfected cell.

## Brute force: rediscover a component from every infected cell

```python
def contain_virus_brute(is_infected: list[list[int]]) -> int:
    if (
        not is_infected
        or not is_infected[0]
        or any(len(row) != len(is_infected[0]) for row in is_infected)
        or any(cell not in {0, 1} for row in is_infected for cell in row)
    ):
        raise ValueError("grid must be non-empty, rectangular, and binary")

    grid = [row[:] for row in is_infected]
    rows = len(grid)
    columns = len(grid[0])
    directions = ((1, 0), (-1, 0), (0, 1), (0, -1))
    total_walls = 0

    while True:
        candidates: list[tuple[set[tuple[int, int]], set[tuple[int, int]], int]] = []
        for start_row in range(rows):
            for start_column in range(columns):
                if grid[start_row][start_column] != 1:
                    continue
                region: set[tuple[int, int]] = {(start_row, start_column)}
                frontier: set[tuple[int, int]] = set()
                walls = 0
                stack = [(start_row, start_column)]
                while stack:
                    row, column = stack.pop()
                    for row_change, column_change in directions:
                        next_row = row + row_change
                        next_column = column + column_change
                        if not (0 <= next_row < rows and 0 <= next_column < columns):
                            continue
                        if grid[next_row][next_column] == 0:
                            frontier.add((next_row, next_column))
                            walls += 1
                        elif (
                            grid[next_row][next_column] == 1
                            and (next_row, next_column) not in region
                        ):
                            region.add((next_row, next_column))
                            stack.append((next_row, next_column))
                candidates.append((region, frontier, walls))

        if not candidates:
            return total_walls
        region, frontier, walls = max(
            candidates,
            key=lambda candidate: len(candidate[1]),
        )
        if not frontier:
            return total_walls
        total_walls += walls
        for row, column in region:
            grid[row][column] = 2
        spread = {
            (next_row, next_column)
            for row in range(rows)
            for column in range(columns)
            if grid[row][column] == 1
            for row_change, column_change in directions
            for next_row, next_column in [(row + row_change, column + column_change)]
            if 0 <= next_row < rows
            and 0 <= next_column < columns
            and grid[next_row][next_column] == 0
        }
        for row, column in spread:
            grid[row][column] = 1
```

Starting a full search at every infected cell repeats the same component work
many times and can cost a cubic factor per simulated day.

## Better transition: discover each active region once

A global `seen` set partitions active cells into components in one grid scan.
Store each component, its frontier set, and its boundary-edge count; those three
objects are exactly the information needed for quarantine and spread.

## Expert solution: component-frontier simulation

```python
def contain_virus(is_infected: list[list[int]]) -> int:
    if (
        not is_infected
        or not is_infected[0]
        or any(len(row) != len(is_infected[0]) for row in is_infected)
        or any(cell not in {0, 1} for row in is_infected for cell in row)
    ):
        raise ValueError("grid must be non-empty, rectangular, and binary")

    grid = [row[:] for row in is_infected]
    rows = len(grid)
    columns = len(grid[0])
    directions = ((1, 0), (-1, 0), (0, 1), (0, -1))
    total_walls = 0

    while True:
        seen: set[tuple[int, int]] = set()
        regions: list[set[tuple[int, int]]] = []
        frontiers: list[set[tuple[int, int]]] = []
        wall_counts: list[int] = []

        for start_row in range(rows):
            for start_column in range(columns):
                start = (start_row, start_column)
                if grid[start_row][start_column] != 1 or start in seen:
                    continue
                seen.add(start)
                region = {start}
                frontier: set[tuple[int, int]] = set()
                walls = 0
                stack = [start]
                while stack:
                    row, column = stack.pop()
                    for row_change, column_change in directions:
                        next_row = row + row_change
                        next_column = column + column_change
                        if not (0 <= next_row < rows and 0 <= next_column < columns):
                            continue
                        neighbor = (next_row, next_column)
                        if grid[next_row][next_column] == 0:
                            frontier.add(neighbor)
                            walls += 1
                        elif grid[next_row][next_column] == 1 and neighbor not in seen:
                            seen.add(neighbor)
                            region.add(neighbor)
                            stack.append(neighbor)
                regions.append(region)
                frontiers.append(frontier)
                wall_counts.append(walls)

        if not regions:
            return total_walls
        quarantine = max(range(len(regions)), key=lambda index: len(frontiers[index]))
        if not frontiers[quarantine]:
            return total_walls
        total_walls += wall_counts[quarantine]

        for index, region in enumerate(regions):
            if index == quarantine:
                for row, column in region:
                    grid[row][column] = 2
            else:
                for row, column in frontiers[index]:
                    grid[row][column] = 1
```

Each day discovers every active infected cell and boundary edge once. Marking
the quarantined region before the next discovery prevents it from spreading.

**Complexity:** `O((mn)^2)` worst-case time over at most `mn` days and
`O(mn)` auxiliary space.
