# Focus300 114: LeetCode 773 - Sliding Puzzle

**Source:** [LeetCode 773](https://leetcode.com/problems/sliding-puzzle/)  
**Difficulty:** Hard  
**Pattern:** shortest path over permutation states

## Exact contract

Given a `2 x 3` board containing each value `0..5` exactly once, one move swaps
`0` with a horizontally or vertically adjacent tile. Return the minimum moves
to reach `[[1, 2, 3], [4, 5, 0]]`, or `-1` if the target is unreachable.

## First principles

Every board arrangement is a graph vertex, and every legal blank swap is an
unweighted edge. Therefore breadth-first search discovers states in exact
move-count order. Encoding the board as a six-value tuple makes states
immutable and hashable.


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

- The solved board returns zero without generating neighbors.
- The blank's legal destinations depend only on its flattened index.
- Some permutations have the wrong parity and are unreachable.
- Revisited states must be suppressed to keep the finite graph small.
- The input must contain each value `0..5` exactly once.

## Brute force: search the entire reachable state graph

```python
from collections import deque


def sliding_puzzle_moves_brute(board: list[list[int]]) -> int:
    if (
        type(board) is not list
        or len(board) != 2
        or any(type(row) is not list or len(row) != 3 for row in board)
    ):
        raise TypeError("board must be a 2 x 3 list of integer lists")
    if any(type(value) is not int for row in board for value in row):
        raise TypeError("every board value must be an integer")
    flattened = [value for row in board for value in row]
    if set(flattened) != set(range(6)):
        raise ValueError("board must contain every value from 0 through 5 once")

    target = (1, 2, 3, 4, 5, 0)
    neighbors = ((1, 3), (0, 2, 4), (1, 5), (0, 4), (1, 3, 5), (2, 4))
    start = tuple(flattened)
    queue = deque([(start, 0)])
    seen = {start}
    while queue:
        state, moves = queue.popleft()
        if state == target:
            return moves
        blank = state.index(0)
        for destination in neighbors[blank]:
            next_state = list(state)
            next_state[blank], next_state[destination] = (
                next_state[destination],
                next_state[blank],
            )
            encoded = tuple(next_state)
            if encoded not in seen:
                seen.add(encoded)
                queue.append((encoded, moves + 1))
    return -1
```

This exhaustive BFS visits at most `6! = 720` states and uses `O(6!)` space.

## Better approach: guide search with Manhattan distance

A* can prioritize `moves + Manhattan distance`; the distance is admissible
because each move changes one tile by one grid step. For this fixed tiny state
space, bidirectional BFS is simpler and has no priority-queue bookkeeping.

## Expert solution: bidirectional breadth-first search

```python
def sliding_puzzle_moves(board: list[list[int]]) -> int:
    if (
        type(board) is not list
        or len(board) != 2
        or any(type(row) is not list or len(row) != 3 for row in board)
    ):
        raise TypeError("board must be a 2 x 3 list of integer lists")
    if any(type(value) is not int for row in board for value in row):
        raise TypeError("every board value must be an integer")
    flattened = [value for row in board for value in row]
    if set(flattened) != set(range(6)):
        raise ValueError("board must contain every value from 0 through 5 once")

    target = (1, 2, 3, 4, 5, 0)
    start = tuple(flattened)
    if start == target:
        return 0

    neighbors = ((1, 3), (0, 2, 4), (1, 5), (0, 4), (1, 3, 5), (2, 4))
    frontier = {start}
    opposite_frontier = {target}
    distance = {start: 0}
    opposite_distance = {target: 0}

    while frontier and opposite_frontier:
        if len(frontier) > len(opposite_frontier):
            frontier, opposite_frontier = opposite_frontier, frontier
            distance, opposite_distance = opposite_distance, distance

        next_frontier: set[tuple[int, ...]] = set()
        for state in frontier:
            blank = state.index(0)
            for destination in neighbors[blank]:
                next_state = list(state)
                next_state[blank], next_state[destination] = (
                    next_state[destination],
                    next_state[blank],
                )
                encoded = tuple(next_state)
                if encoded in opposite_distance:
                    return distance[state] + 1 + opposite_distance[encoded]
                if encoded not in distance:
                    distance[encoded] = distance[state] + 1
                    next_frontier.add(encoded)
        frontier = next_frontier
    return -1
```

Both searches expand complete distance layers. Their first meeting therefore
joins two shortest partial paths into a globally shortest solution.

**Complexity:** `O(6!)` worst-case time and space, with roughly half the search
depth explored from each side.
