# ICPC300 187: Codeforces 817F - MEX Queries

**Source:** [Codeforces 817F](https://codeforces.com/problemset/problem/817/F)  
**Pattern:** compressed interval assignment and inversion

## Exact contract

Start with an empty set of positive integers. Each query supplies an inclusive
interval `[l,r]`: type `1` inserts every integer in it, type `2` removes every
integer in it, and type `3` toggles membership of every integer in it. After
each query, print the set's smallest missing positive integer.

## First principles

Membership changes only at operation boundaries. Compress `1`, every `l`,
every `r+1`, and one sentinel beyond the greatest `r+1`. Each leaf represents
a half-open coordinate interval on which membership is constant.

Store the covered physical length, not merely the number of compressed leaves.
A node is full exactly when its covered length equals its coordinate length.
Lazy tags support assignment to zero, assignment to one, and inversion.

## Cases that decide correctness

- MEX is over positive integers, so coordinate `1` must exist.
- Inclusive `[l,r]` becomes half-open `[l,r+1)`.
- Inversion after assignment toggles the pending assigned value.
- A sentinel is required when every operated coordinate is present.
- Large coordinates make physical materialization impossible.

## Brute force: mutate a finite set

```python
def mex_queries_brute(queries: list[tuple[int, int, int]]) -> list[int]:
    present: set[int] = set()
    answers = []
    for operation_type, left, right in queries:
        for value in range(left, right + 1):
            if operation_type == 1:
                present.add(value)
            elif operation_type == 2:
                present.discard(value)
            elif value in present:
                present.remove(value)
            else:
                present.add(value)
        answer = 1
        while answer in present:
            answer += 1
        answers.append(answer)
    return answers
```

Its running time depends on the numeric interval lengths.

## Better insight: preserve lengths between boundaries

Ordinary coordinate compression preserves order but loses gaps. Associating a
leaf with `[coordinate[i], coordinate[i+1])` preserves exactly how many
integers are covered and where the first missing one lies.

## Expert solution: lazy set, clear, and flip

```python
import sys


def solve() -> None:
    input_stream = sys.stdin.buffer
    query_count = int(input_stream.readline())
    queries = [
        tuple(map(int, input_stream.readline().split())) for _ in range(query_count)
    ]
    maximum_right = max(right for _, _, right in queries)
    coordinates = {1, maximum_right + 2}
    for _, left, right in queries:
        coordinates.add(left)
        coordinates.add(right + 1)
    ordered = sorted(coordinates)
    index = {coordinate: position for position, coordinate in enumerate(ordered)}
    leaf_count = len(ordered) - 1
    covered = [0] * (4 * leaf_count)
    assignment = [-1] * (4 * leaf_count)
    flipped = [False] * (4 * leaf_count)

    def length(left: int, right: int) -> int:
        return ordered[right] - ordered[left]

    def apply_assignment(node: int, left: int, right: int, value: int) -> None:
        covered[node] = value * length(left, right)
        assignment[node] = value
        flipped[node] = False

    def apply_flip(node: int, left: int, right: int) -> None:
        covered[node] = length(left, right) - covered[node]
        if assignment[node] != -1:
            assignment[node] ^= 1
        else:
            flipped[node] = not flipped[node]

    def push(node: int, left: int, right: int) -> None:
        if right - left == 1:
            return
        middle = (left + right) // 2
        if assignment[node] != -1:
            apply_assignment(node * 2, left, middle, assignment[node])
            apply_assignment(node * 2 + 1, middle, right, assignment[node])
            assignment[node] = -1
        if flipped[node]:
            apply_flip(node * 2, left, middle)
            apply_flip(node * 2 + 1, middle, right)
            flipped[node] = False

    def update(
        node: int,
        left: int,
        right: int,
        query_left: int,
        query_right: int,
        operation_type: int,
    ) -> None:
        if query_right <= left or right <= query_left:
            return
        if query_left <= left and right <= query_right:
            if operation_type == 1:
                apply_assignment(node, left, right, 1)
            elif operation_type == 2:
                apply_assignment(node, left, right, 0)
            else:
                apply_flip(node, left, right)
            return
        push(node, left, right)
        middle = (left + right) // 2
        update(
            node * 2,
            left,
            middle,
            query_left,
            query_right,
            operation_type,
        )
        update(
            node * 2 + 1,
            middle,
            right,
            query_left,
            query_right,
            operation_type,
        )
        covered[node] = covered[node * 2] + covered[node * 2 + 1]

    def first_missing(node: int, left: int, right: int) -> int:
        if right - left == 1:
            return ordered[left]
        push(node, left, right)
        middle = (left + right) // 2
        if covered[node * 2] < length(left, middle):
            return first_missing(node * 2, left, middle)
        return first_missing(node * 2 + 1, middle, right)

    output = []
    for operation_type, left, right in queries:
        update(
            1,
            0,
            leaf_count,
            index[left],
            index[right + 1],
            operation_type,
        )
        output.append(str(first_missing(1, 0, leaf_count)))
    print("\n".join(output))


if __name__ == "__main__":
    solve()
```

Each leaf is membership-uniform by construction. The first non-full descent
therefore returns the true smallest missing integer.

**Complexity:** `O(q log q)` time and `O(q)` space.
