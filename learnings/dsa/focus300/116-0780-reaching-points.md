# Focus300 116: LeetCode 780 - Reaching Points

**Source:** [LeetCode 780](https://leetcode.com/problems/reaching-points/)  
**Difficulty:** Hard  
**Pattern:** reverse Euclidean reduction

## Exact contract

Starting from positive integers `(sx, sy)`, a move changes `(x, y)` to either
`(x + y, y)` or `(x, x + y)`. Return whether target `(tx, ty)` is reachable.
All four coordinates are between 1 and `1_000_000_000`.

## First principles

Forward search branches, but a target with unequal coordinates has only one
possible predecessor: subtract the smaller coordinate from the larger. Many
identical reverse subtractions can be batched with modulo. Once one target
coordinate equals its source coordinate, only repeated additions of that fixed
coordinate remain possible.


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

- The source point reaches itself with zero moves.
- Coordinates never decrease in forward moves, so an exceeded target is dead.
- Reverse subtraction always affects the larger target coordinate.
- Modulo batching must stop before reducing a coordinate below its source.
- When one coordinate matches, divisibility decides the remaining straight
  sequence of moves.

## Brute force: breadth-first forward search

```python
from collections import deque


def reaching_points_brute(
    source_x: int,
    source_y: int,
    target_x: int,
    target_y: int,
) -> bool:
    coordinates = (source_x, source_y, target_x, target_y)
    if any(type(value) is not int for value in coordinates):
        raise TypeError("all coordinates must be integers")
    if any(not 1 <= value <= 1_000_000_000 for value in coordinates):
        raise ValueError("all coordinates must be between 1 and 1000000000")

    queue = deque([(source_x, source_y)])
    seen = {(source_x, source_y)}
    while queue:
        x_value, y_value = queue.popleft()
        if (x_value, y_value) == (target_x, target_y):
            return True
        candidates = (
            (x_value + y_value, y_value),
            (x_value, x_value + y_value),
        )
        for candidate in candidates:
            if (
                candidate[0] <= target_x
                and candidate[1] <= target_y
                and candidate not in seen
            ):
                seen.add(candidate)
                queue.append(candidate)
    return False
```

The number of bounded forward states can be proportional to `tx * ty`.

## Better approach: reverse one subtraction at a time

```python
def reaching_points_subtraction(
    source_x: int,
    source_y: int,
    target_x: int,
    target_y: int,
) -> bool:
    coordinates = (source_x, source_y, target_x, target_y)
    if any(type(value) is not int for value in coordinates):
        raise TypeError("all coordinates must be integers")
    if any(not 1 <= value <= 1_000_000_000 for value in coordinates):
        raise ValueError("all coordinates must be between 1 and 1000000000")

    while target_x > source_x and target_y > source_y:
        if target_x > target_y:
            target_x -= target_y
        else:
            target_y -= target_x
    if target_x == source_x:
        return target_y >= source_y and (target_y - source_y) % source_x == 0
    if target_y == source_y:
        return target_x >= source_x and (target_x - source_x) % source_y == 0
    return False
```

This removes branching and constant storage, but a highly unbalanced target
can require linearly many subtractions.

## Expert solution: batch forced subtractions with modulo

```python
def reaching_points(
    source_x: int,
    source_y: int,
    target_x: int,
    target_y: int,
) -> bool:
    coordinates = (source_x, source_y, target_x, target_y)
    if any(type(value) is not int for value in coordinates):
        raise TypeError("all coordinates must be integers")
    if any(not 1 <= value <= 1_000_000_000 for value in coordinates):
        raise ValueError("all coordinates must be between 1 and 1000000000")

    while target_x > source_x and target_y > source_y:
        if target_x > target_y:
            target_x %= target_y
        else:
            target_y %= target_x
    if target_x == source_x:
        return target_y >= source_y and (target_y - source_y) % source_x == 0
    if target_y == source_y:
        return target_x >= source_x and (target_x - source_x) % source_y == 0
    return False
```

Modulo performs every forced subtraction of the smaller coordinate in one
step. The tail tests preserve the source boundary rather than reducing past it.

**Complexity:** `O(log(max(tx, ty)))` time and `O(1)` space.
