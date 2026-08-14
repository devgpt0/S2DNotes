# ICPC300 244: Codeforces 915E - Physical Education Lessons

**Source:** [Codeforces 915E](https://codeforces.com/problemset/problem/915/E)  
**Difficulty:** 2300  
**Pattern:** compressed weighted intervals with lazy assignment

## Exact contract

All `n` days initially have lessons. Each query `(l,r,k)` changes every day in
the inclusive interval: `k=1` cancels lessons and `k=2` restores them. After
each query, output the number of days that still have lessons.

## First principles

Only query boundaries can change lesson status. Compress `1`, `n+1`, every
`l`, and every `r+1`. A leaf represents a half-open interval of equal status
and stores its physical length when active.

Range assignment sets a covered length to either zero or the node's coordinate
length. A lazy assignment tag overrides older tags.

## Cases that decide correctness

- Input intervals are inclusive.
- Days outside all operations remain active.
- Repeating the same assignment changes nothing.
- Compressed leaves have different physical lengths.
- `n` can be much larger than the number of queries.

## Brute force: assign every day

```python
def physical_education_brute(
    day_count: int, queries: list[tuple[int, int, int]]
) -> list[int]:
    active = [True] * day_count
    answers = []
    for left, right, operation in queries:
        active[left - 1 : right] = [operation == 2] * (right - left + 1)
        answers.append(sum(active))
    return answers
```

This is linear in the assigned interval length.

## Better insight: preserve coordinate lengths during compression

Status is constant between consecutive operation boundaries. Weighted leaves
make their active sum equal the number of real days.

## Expert solution: weighted lazy assignment tree

```python
import sys


def solve() -> None:
    input_stream = sys.stdin.buffer
    day_count, query_count = map(int, input_stream.readline().split())
    queries = [
        tuple(map(int, input_stream.readline().split())) for _ in range(query_count)
    ]
    coordinates = {1, day_count + 1}
    for left, right, _ in queries:
        coordinates.add(left)
        coordinates.add(right + 1)
    ordered = sorted(coordinates)
    index = {coordinate: position for position, coordinate in enumerate(ordered)}
    leaf_count = len(ordered) - 1
    active = [0] * (4 * leaf_count)
    assignment = [-1] * (4 * leaf_count)

    def build(node: int, left: int, right: int) -> None:
        active[node] = ordered[right] - ordered[left]
        if right - left == 1:
            return
        middle = (left + right) // 2
        build(node * 2, left, middle)
        build(node * 2 + 1, middle, right)

    def apply(node: int, left: int, right: int, value: int) -> None:
        active[node] = value * (ordered[right] - ordered[left])
        assignment[node] = value

    def push(node: int, left: int, right: int) -> None:
        if assignment[node] == -1 or right - left == 1:
            return
        middle = (left + right) // 2
        apply(node * 2, left, middle, assignment[node])
        apply(node * 2 + 1, middle, right, assignment[node])
        assignment[node] = -1

    def update(
        node: int,
        left: int,
        right: int,
        query_left: int,
        query_right: int,
        value: int,
    ) -> None:
        if query_right <= left or right <= query_left:
            return
        if query_left <= left and right <= query_right:
            apply(node, left, right, value)
            return
        push(node, left, right)
        middle = (left + right) // 2
        update(node * 2, left, middle, query_left, query_right, value)
        update(node * 2 + 1, middle, right, query_left, query_right, value)
        active[node] = active[node * 2] + active[node * 2 + 1]

    build(1, 0, leaf_count)
    output = []
    for left, right, operation in queries:
        update(
            1,
            0,
            leaf_count,
            index[left],
            index[right + 1],
            operation - 1,
        )
        output.append(str(active[1]))
    print("\n".join(output))


if __name__ == "__main__":
    solve()
```

Every real day belongs to exactly one weighted leaf, and lazy assignments match
the latest operation covering it.

**Complexity:** `O(q log q)` time and `O(q)` space.
