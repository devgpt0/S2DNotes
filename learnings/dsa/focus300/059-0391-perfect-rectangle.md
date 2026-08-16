# Focus300 059: LeetCode 391 - Perfect Rectangle

**Source:** [LeetCode 391 - Perfect Rectangle](https://leetcode.com/problems/perfect-rectangle/)  
**Difficulty:** Hard  
**Pattern:** total area plus corner parity  

## Exact contract

Return whether nonempty axis-aligned integer-coordinate rectangles cover one
bounding rectangle exactly: no positive-area overlap and no gap.

## First principles

In a perfect cover, small rectangle areas sum to the bounding area. Every
interior corner appears an even number of times and cancels under parity;
exactly the four bounding corners remain odd. Both conditions together exclude
gaps and overlaps.


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

- Duplicate rectangles create overlap.
- A gap and overlap can preserve total area, so area alone is insufficient.
- Rectangles may share complete boundaries.
- Every rectangle must have positive width and height.
- Exactly four specific outer corners must remain after parity toggling.

## Brute force: mark every unit cell

```python
Rectangle = tuple[int, int, int, int]


def is_perfect_rectangle_brute(rectangles: list[Rectangle]) -> bool:
    if not rectangles:
        raise ValueError("rectangles must be nonempty")
    covered: set[tuple[int, int]] = set()
    minimum_x = minimum_y = 10**100
    maximum_x = maximum_y = -(10**100)
    for left, bottom, right, top in rectangles:
        if (
            any(type(value) is not int for value in (left, bottom, right, top))
            or left >= right
            or bottom >= top
        ):
            raise ValueError("invalid rectangle")
        minimum_x = min(minimum_x, left)
        minimum_y = min(minimum_y, bottom)
        maximum_x = max(maximum_x, right)
        maximum_y = max(maximum_y, top)
        for x_coordinate in range(left, right):
            for y_coordinate in range(bottom, top):
                cell = (x_coordinate, y_coordinate)
                if cell in covered:
                    return False
                covered.add(cell)
    expected = {
        (x_coordinate, y_coordinate)
        for x_coordinate in range(minimum_x, maximum_x)
        for y_coordinate in range(minimum_y, maximum_y)
    }
    return covered == expected
```

**Complexity:** `O(bounding area)` time and space.

## Better approach: sweep vertical events

A line sweep can verify that active y-intervals exactly partition the bounding
height between consecutive x-events. It costs `O(n log n)` but needs a dynamic
interval structure.

## Expert solution: area equality and corner toggling

```python
Rectangle = tuple[int, int, int, int]


def is_perfect_rectangle(rectangles: list[Rectangle]) -> bool:
    if not rectangles:
        raise ValueError("rectangles must be nonempty")
    minimum_x = minimum_y = 10**100
    maximum_x = maximum_y = -(10**100)
    total_area = 0
    odd_corners: set[tuple[int, int]] = set()
    for left, bottom, right, top in rectangles:
        if (
            any(type(value) is not int for value in (left, bottom, right, top))
            or left >= right
            or bottom >= top
        ):
            raise ValueError("invalid rectangle")
        minimum_x = min(minimum_x, left)
        minimum_y = min(minimum_y, bottom)
        maximum_x = max(maximum_x, right)
        maximum_y = max(maximum_y, top)
        total_area += (right - left) * (top - bottom)
        for corner in (
            (left, bottom),
            (left, top),
            (right, bottom),
            (right, top),
        ):
            if corner in odd_corners:
                odd_corners.remove(corner)
            else:
                odd_corners.add(corner)

    bounding_area = (maximum_x - minimum_x) * (maximum_y - minimum_y)
    bounding_corners = {
        (minimum_x, minimum_y),
        (minimum_x, maximum_y),
        (maximum_x, minimum_y),
        (maximum_x, maximum_y),
    }
    return total_area == bounding_area and odd_corners == bounding_corners
```

Interior boundary vertices have even incidence in an exact tiling, leaving
only the four outer corners. Equal area prevents any uncancelled combination of
overlap and gap from satisfying that boundary parity.

**Complexity:** `O(n)` expected time and `O(n)` space.

