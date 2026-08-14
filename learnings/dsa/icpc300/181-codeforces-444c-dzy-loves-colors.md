# ICPC300 181: Codeforces 444C - DZY Loves Colors

**Source:** [Codeforces 444C](https://codeforces.com/problemset/problem/444/C)  
**Pattern:** amortized lazy segment tree over monochromatic ranges

## Exact contract

Position `i` initially has color `i` and accumulated beauty `0`. A type `1`
operation recolors every position in `[l,r]` to `x`; each position gains the
absolute difference between its old and new colors. A type `2` operation asks
for the sum of accumulated beauty in `[l,r]`.

## First principles

If a segment is one color `c`, repainting all of it to `x` adds
`length * abs(c-x)` to its beauty sum. A mixed segment must be split because
its positions have different increments.

Store each node's beauty sum and either its uniform color or `-1` for mixed.
A full repaint stops at every uniform node. Repainting cannot create more than
two new color boundaries, while every visited internal boundary is removed by
the assignment; this gives the usual amortized logarithmic behavior.

## Cases that decide correctness

- Beauty is cumulative; recoloring never resets it.
- Repainting to the current color adds zero.
- A pending repaint must carry both the latest color and all accumulated
  per-position beauty increments to children.
- Query ranges are inclusive in the input.
- Large answers require wide integers.

## Brute force: repaint every position

```python
def dzy_colors_brute(size: int, operations: list[tuple[int, ...]]) -> list[int]:
    colors = list(range(1, size + 1))
    beauty = [0] * size
    answers = []
    for operation in operations:
        if operation[0] == 1:
            _, left, right, new_color = operation
            for index in range(left - 1, right):
                beauty[index] += abs(colors[index] - new_color)
                colors[index] = new_color
        else:
            _, left, right = operation
            answers.append(sum(beauty[left - 1 : right]))
    return answers
```

This is `O(n)` per operation.

## Better insight: operate on color runs

An ordered map of maximal equal-color intervals avoids touching every
position, but Python has no built-in balanced ordered map and adversarial
splits require careful accounting. The segment tree below represents the same
runs while also answering beauty sums.

## Expert solution: stop repainting at uniform nodes

```python
import sys


def solve() -> None:
    input_stream = sys.stdin.buffer
    size, operation_count = map(int, input_stream.readline().split())
    node_count = 4 * size
    beauty_sum = [0] * node_count
    color = [-1] * node_count
    pending_color = [0] * node_count
    pending_beauty = [0] * node_count

    def build(node: int, left: int, right: int) -> None:
        if right - left == 1:
            color[node] = left + 1
            return
        middle = (left + right) // 2
        build(node * 2, left, middle)
        build(node * 2 + 1, middle, right)

    def apply(
        node: int,
        left: int,
        right: int,
        new_color: int,
        added_beauty: int,
    ) -> None:
        beauty_sum[node] += added_beauty * (right - left)
        color[node] = new_color
        pending_color[node] = new_color
        pending_beauty[node] += added_beauty

    def push(node: int, left: int, right: int) -> None:
        if right - left == 1 or pending_color[node] == 0:
            return
        middle = (left + right) // 2
        apply(
            node * 2,
            left,
            middle,
            pending_color[node],
            pending_beauty[node],
        )
        apply(
            node * 2 + 1,
            middle,
            right,
            pending_color[node],
            pending_beauty[node],
        )
        pending_color[node] = 0
        pending_beauty[node] = 0

    def pull(node: int) -> None:
        beauty_sum[node] = beauty_sum[node * 2] + beauty_sum[node * 2 + 1]
        left_color = color[node * 2]
        color[node] = left_color if left_color == color[node * 2 + 1] else -1

    def repaint(
        node: int,
        left: int,
        right: int,
        query_left: int,
        query_right: int,
        new_color: int,
    ) -> None:
        if query_right <= left or right <= query_left:
            return
        if query_left <= left and right <= query_right and color[node] != -1:
            apply(
                node,
                left,
                right,
                new_color,
                abs(color[node] - new_color),
            )
            return
        push(node, left, right)
        middle = (left + right) // 2
        repaint(node * 2, left, middle, query_left, query_right, new_color)
        repaint(
            node * 2 + 1,
            middle,
            right,
            query_left,
            query_right,
            new_color,
        )
        pull(node)

    def range_sum(
        node: int,
        left: int,
        right: int,
        query_left: int,
        query_right: int,
    ) -> int:
        if query_right <= left or right <= query_left:
            return 0
        if query_left <= left and right <= query_right:
            return beauty_sum[node]
        push(node, left, right)
        middle = (left + right) // 2
        return range_sum(node * 2, left, middle, query_left, query_right) + range_sum(
            node * 2 + 1, middle, right, query_left, query_right
        )

    build(1, 0, size)
    output = []
    for _ in range(operation_count):
        operation = list(map(int, input_stream.readline().split()))
        if operation[0] == 1:
            _, left, right, new_color = operation
            repaint(1, 0, size, left - 1, right, new_color)
        else:
            _, left, right = operation
            output.append(str(range_sum(1, 0, size, left - 1, right)))
    print("\n".join(output))


if __name__ == "__main__":
    solve()
```

Every stopped node is uniformly colored, so its beauty increment is exact.
Pushing preserves that increment and color for later partial operations.

**Complexity:** amortized `O((n+q) log n)` time and `O(n)` space.
