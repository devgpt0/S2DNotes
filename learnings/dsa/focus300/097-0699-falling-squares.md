# Focus300 097: LeetCode 699 - Falling Squares

**Source:** [LeetCode 699](https://leetcode.com/problems/falling-squares/)  
**Difficulty:** Hard  
**Pattern:** coordinate compression with range maximum and range assignment

## Exact contract

Squares arrive in order as `[left, side]`. A square falls vertically over the
half-open horizontal interval `[left, left+side)` until its bottom meets the
ground or an earlier square. After every drop, return the maximum stack height.
Touching only at an edge does not count as overlap.

## First principles

A new square lands on the maximum existing height anywhere under its footprint,
then makes that entire footprint have height `base + side`. Thus each drop is a
range-maximum query followed by a range assignment.

Only input endpoints can change the height profile. Coordinate compression
turns the huge coordinates into at most `2*n-1` elementary intervals without
changing overlap relationships.

## Cases that decide correctness

- `[a, b)` and `[b, c)` do not overlap.
- A square's top is uniform across its full footprint after landing.
- Duplicate footprints stack vertically.
- The reported sequence is the global maximum after each individual drop.
- Compression must represent gaps between adjacent distinct endpoints.

## Brute force: compare each square with every earlier square

```python
def falling_squares_brute(positions: list[list[int]]) -> list[int]:
    if type(positions) is not list or not 1 <= len(positions) <= 1_000:
        raise ValueError("positions must contain between 1 and 1,000 squares")
    if any(
        type(position) is not list
        or len(position) != 2
        or type(position[0]) is not int
        or type(position[1]) is not int
        or not 1 <= position[0] <= 100_000_000
        or not 1 <= position[1] <= 1_000_000
        for position in positions
    ):
        raise ValueError("each position must contain a valid left edge and side")

    landed: list[tuple[int, int, int]] = []
    answer: list[int] = []
    global_maximum = 0
    for left, side in positions:
        right = left + side
        base = 0
        for previous_left, previous_right, previous_top in landed:
            if max(left, previous_left) < min(right, previous_right):
                base = max(base, previous_top)
        top = base + side
        landed.append((left, right, top))
        global_maximum = max(global_maximum, top)
        answer.append(global_maximum)
    return answer
```

This is `O(n^2)` time and `O(n)` space.

## Better insight: the ground is a piecewise-constant height function

Compress every left and right endpoint. A lazy segment tree stores the maximum
height of each node and an optional assignment covering its whole interval.

## Expert solution: compressed lazy segment tree

```python
class RangeMaximumAssignmentTree:
    def __init__(self, size: int) -> None:
        if size <= 0:
            raise ValueError("tree size must be positive")
        self._size = size
        self._maximum = [0] * (4 * size)
        self._assignment: list[int | None] = [None] * (4 * size)

    def _apply(self, node: int, value: int) -> None:
        self._maximum[node] = value
        self._assignment[node] = value

    def _push(self, node: int) -> None:
        value = self._assignment[node]
        if value is None:
            return
        self._apply(node * 2, value)
        self._apply(node * 2 + 1, value)
        self._assignment[node] = None

    def query(self, query_left: int, query_right: int) -> int:
        def visit(node: int, left: int, right: int) -> int:
            if query_left <= left and right <= query_right:
                return self._maximum[node]
            self._push(node)
            middle = (left + right) // 2
            result = 0
            if query_left <= middle:
                result = visit(node * 2, left, middle)
            if middle < query_right:
                result = max(result, visit(node * 2 + 1, middle + 1, right))
            return result

        return visit(1, 0, self._size - 1)

    def assign(self, query_left: int, query_right: int, value: int) -> None:
        def visit(node: int, left: int, right: int) -> None:
            if query_left <= left and right <= query_right:
                self._apply(node, value)
                return
            self._push(node)
            middle = (left + right) // 2
            if query_left <= middle:
                visit(node * 2, left, middle)
            if middle < query_right:
                visit(node * 2 + 1, middle + 1, right)
            self._maximum[node] = max(
                self._maximum[node * 2], self._maximum[node * 2 + 1]
            )

        visit(1, 0, self._size - 1)


def falling_squares(positions: list[list[int]]) -> list[int]:
    if type(positions) is not list or not 1 <= len(positions) <= 1_000:
        raise ValueError("positions must contain between 1 and 1,000 squares")
    if any(
        type(position) is not list
        or len(position) != 2
        or type(position[0]) is not int
        or type(position[1]) is not int
        or not 1 <= position[0] <= 100_000_000
        or not 1 <= position[1] <= 1_000_000
        for position in positions
    ):
        raise ValueError("each position must contain a valid left edge and side")

    coordinates = sorted(
        {coordinate for left, side in positions for coordinate in (left, left + side)}
    )
    index = {
        coordinate: compressed for compressed, coordinate in enumerate(coordinates)
    }
    tree = RangeMaximumAssignmentTree(len(coordinates) - 1)
    answer: list[int] = []
    global_maximum = 0
    for left, side in positions:
        compressed_left = index[left]
        compressed_right = index[left + side] - 1
        top = tree.query(compressed_left, compressed_right) + side
        tree.assign(compressed_left, compressed_right, top)
        global_maximum = max(global_maximum, top)
        answer.append(global_maximum)
    return answer
```

Each elementary interval in a compressed update corresponds to exactly the
same original footprint, so the tree performs the physical landing rule.

**Complexity:** `O(n log n)` time and `O(n)` space.
