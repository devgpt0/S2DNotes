# ICPC300 162: Codeforces 932F - Escape Through Leaf

**Source:** [Codeforces 932F](https://codeforces.com/problemset/problem/932/F)  
**Pattern:** small-to-large merging of Li Chao hulls on a tree

## Exact contract

A tree rooted at vertex `1` gives integers `a[v]` and `b[v]`. For a leaf,
`dp[v] = 0`. For every other vertex,

`dp[v] = min(dp[u] + a[v] * b[u])`

over all proper descendants `u` of `v`. Output `dp[1..n]`.

## First principles

Every processed descendant `u` contributes the line
`y = b[u] * x + dp[u]`. A vertex queries the minimum at `x = a[v]`, then adds
its own line for ancestors.

Child subtrees provide separate line containers. Retain the container with the
most lines and insert every line from smaller containers. A moved line enters
a container at least twice as large, so it moves only `O(log n)` times. A Li
Chao tree answers arbitrary-slope minimum queries on the compressed set of all
`a` coordinates.

## Cases that decide correctness

- A vertex cannot use its own line when computing its answer.
- A leaf has no proper descendant and therefore answer zero.
- Candidates include all descendants, not only direct children.
- Slopes and query coordinates can be negative.
- Products and DP values require wide signed integers.

## Brute force: scan every proper descendant

```python
def escape_through_leaf_brute(
    first_coefficients: list[int],
    second_coefficients: list[int],
    edges: list[tuple[int, int]],
) -> list[int]:
    vertex_count = len(first_coefficients)
    graph = [[] for _ in range(vertex_count)]
    for first, second in edges:
        graph[first - 1].append(second - 1)
        graph[second - 1].append(first - 1)

    parent = [-1] * vertex_count
    parent[0] = 0
    children = [[] for _ in range(vertex_count)]
    order = [0]
    for vertex in order:
        for neighbor in graph[vertex]:
            if parent[neighbor] == -1:
                parent[neighbor] = vertex
                children[vertex].append(neighbor)
                order.append(neighbor)

    descendants: list[list[int]] = [[] for _ in range(vertex_count)]
    answer = [0] * vertex_count
    for vertex in reversed(order):
        for child in children[vertex]:
            descendants[vertex].append(child)
            descendants[vertex].extend(descendants[child])
        if descendants[vertex]:
            answer[vertex] = min(
                answer[descendant]
                + first_coefficients[vertex] * second_coefficients[descendant]
                for descendant in descendants[vertex]
            )
    return answer
```

On a chain, descendant lists and scans take quadratic time and space.

## Better insight: one hull per subtree still duplicates work

Building an independent Li Chao tree from every subtree's lines improves each
minimum query but reinserts a line for every ancestor, remaining quadratic on
a chain. The essential improvement is ownership: merge smaller containers into
the largest and never rebuild the retained hull.

## Expert solution: compressed Li Chao trees with DSU merging

```python
import sys


class LiChaoTree:
    def __init__(self, coordinates: list[int]) -> None:
        self.coordinates = coordinates
        self.lines: dict[int, tuple[int, int]] = {}

    @staticmethod
    def value(line: tuple[int, int], coordinate: int) -> int:
        slope, intercept = line
        return slope * coordinate + intercept

    def add(
        self,
        new_line: tuple[int, int],
        node: int = 1,
        left: int = 0,
        right: int | None = None,
    ) -> None:
        if right is None:
            right = len(self.coordinates)
        current = self.lines.get(node)
        if current is None:
            self.lines[node] = new_line
            return

        middle = (left + right) // 2
        if self.value(new_line, self.coordinates[middle]) < self.value(
            current, self.coordinates[middle]
        ):
            self.lines[node] = new_line
            new_line = current
        active = self.lines[node]
        if right - left == 1:
            return
        if self.value(new_line, self.coordinates[left]) < self.value(
            active, self.coordinates[left]
        ):
            self.add(new_line, node * 2, left, middle)
        elif self.value(new_line, self.coordinates[right - 1]) < self.value(
            active, self.coordinates[right - 1]
        ):
            self.add(new_line, node * 2 + 1, middle, right)

    def query(
        self,
        coordinate: int,
        node: int = 1,
        left: int = 0,
        right: int | None = None,
    ) -> int:
        if right is None:
            right = len(self.coordinates)
        line = self.lines.get(node)
        answer = 10**40 if line is None else self.value(line, coordinate)
        if right - left == 1:
            return answer
        middle = (left + right) // 2
        if coordinate < self.coordinates[middle]:
            return min(answer, self.query(coordinate, node * 2, left, middle))
        return min(answer, self.query(coordinate, node * 2 + 1, middle, right))


def solve() -> None:
    input_stream = sys.stdin.buffer
    vertex_count = int(input_stream.readline())
    first_coefficients = list(map(int, input_stream.readline().split()))
    second_coefficients = list(map(int, input_stream.readline().split()))
    graph = [[] for _ in range(vertex_count)]
    for _ in range(vertex_count - 1):
        first, second = map(int, input_stream.readline().split())
        graph[first - 1].append(second - 1)
        graph[second - 1].append(first - 1)

    parent = [-1] * vertex_count
    parent[0] = 0
    children = [[] for _ in range(vertex_count)]
    order = [0]
    for vertex in order:
        for neighbor in graph[vertex]:
            if parent[neighbor] == -1:
                parent[neighbor] = vertex
                children[vertex].append(neighbor)
                order.append(neighbor)

    coordinates = sorted(set(first_coefficients))
    hulls: list[LiChaoTree | None] = [None] * vertex_count
    hull_lines: list[list[tuple[int, int]] | None] = [None] * vertex_count
    answer = [0] * vertex_count

    for vertex in reversed(order):
        heavy_child = max(
            children[vertex],
            key=lambda child: len(hull_lines[child] or []),
            default=-1,
        )
        if heavy_child == -1:
            hull = LiChaoTree(coordinates)
            lines: list[tuple[int, int]] = []
        else:
            heavy_hull = hulls[heavy_child]
            heavy_lines = hull_lines[heavy_child]
            if heavy_hull is None or heavy_lines is None:
                raise RuntimeError("child hull was not built")
            hull = heavy_hull
            lines = heavy_lines

        for child in children[vertex]:
            if child == heavy_child:
                continue
            child_lines = hull_lines[child]
            if child_lines is None:
                raise RuntimeError("child lines were not built")
            for line in child_lines:
                hull.add(line)
                lines.append(line)

        if lines:
            answer[vertex] = hull.query(first_coefficients[vertex])
        own_line = (second_coefficients[vertex], answer[vertex])
        hull.add(own_line)
        lines.append(own_line)

        for child in children[vertex]:
            hulls[child] = None
            hull_lines[child] = None
        hulls[vertex] = hull
        hull_lines[vertex] = lines

    print(" ".join(map(str, answer)))


if __name__ == "__main__":
    solve()
```

Before a vertex queries, its retained hull contains exactly the lines of all
proper descendants. The query is therefore the recurrence minimum, and adding
the vertex line establishes the same invariant for its ancestors.

**Complexity:** `O(n log^2 n)` time and `O(n log n)` Li Chao nodes in the
worst case, with `O(n)` live line entries.
