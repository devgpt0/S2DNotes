# ICPC300 163: Codeforces 893F - Subtree Minimum Query

**Source:** [Codeforces 893F](https://codeforces.com/problemset/problem/893/F)  
**Pattern:** persistent segment trees indexed by depth

## Exact contract

Each test case gives a tree rooted at `r`, one value per vertex, and online
encoded queries `(p,q)`. If the previous answer is `last`, decode

`x = (p + last) mod n + 1`, `k = (q + last) mod n`.

Output the minimum value among vertices in the subtree of `x` whose depth is at
most `depth[x] + k`. Initially `last = 0`; every printed minimum becomes the
next `last`.

## First principles

An Euler preorder makes every rooted subtree one interval `[tin,tout)`. Build
version `d` of a segment tree over Euler positions containing exactly vertices
of depth at most `d`; every other position stores infinity. The query uses
version `depth[x]+k` and takes a range minimum on `x`'s Euler interval.

Increasing the depth limit only inserts vertices, so each version is obtained
from the preceding one by persistent point updates. Online decoding is then
irrelevant to preprocessing.

## Cases that decide correctness

- Decode both numbers using the previous answer before each query.
- The depth bound is inclusive.
- The queried vertex itself is always eligible.
- Clamp a depth limit beyond the tree height to the final version.
- Reinitialize `last` and all persistent storage for every test case.

## Brute force: scan the decoded subtree

```python
def subtree_minimum_brute(
    values: list[int],
    edges: list[tuple[int, int]],
    root: int,
    encoded_queries: list[tuple[int, int]],
) -> list[int]:
    vertex_count = len(values)
    graph = [[] for _ in range(vertex_count)]
    for first, second in edges:
        graph[first - 1].append(second - 1)
        graph[second - 1].append(first - 1)

    parent = [-1] * vertex_count
    depth = [0] * vertex_count
    children = [[] for _ in range(vertex_count)]
    root -= 1
    parent[root] = root
    order = [root]
    for vertex in order:
        for neighbor in graph[vertex]:
            if parent[neighbor] == -1:
                parent[neighbor] = vertex
                depth[neighbor] = depth[vertex] + 1
                children[vertex].append(neighbor)
                order.append(neighbor)

    answers = []
    last = 0
    for encoded_vertex, encoded_extra_depth in encoded_queries:
        vertex = (encoded_vertex + last) % vertex_count
        extra_depth = (encoded_extra_depth + last) % vertex_count
        depth_limit = depth[vertex] + extra_depth
        answer = values[vertex]
        stack = [vertex]
        while stack:
            current = stack.pop()
            if depth[current] <= depth_limit:
                answer = min(answer, values[current])
                stack.extend(children[current])
        answers.append(answer)
        last = answer
    return answers
```

One query can inspect the entire rooted subtree.

## Better: merge-sort tree over Euler positions

```python
from bisect import bisect_right


def subtree_minimum_merge_sort_tree(
    values: list[int],
    edges: list[tuple[int, int]],
    root: int,
    encoded_queries: list[tuple[int, int]],
) -> list[int]:
    vertex_count = len(values)
    graph = [[] for _ in range(vertex_count)]
    for first, second in edges:
        graph[first - 1].append(second - 1)
        graph[second - 1].append(first - 1)

    root -= 1
    parent = [-1] * vertex_count
    depth = [0] * vertex_count
    children = [[] for _ in range(vertex_count)]
    parent[root] = root
    order = [root]
    for vertex in order:
        for neighbor in graph[vertex]:
            if parent[neighbor] == -1:
                parent[neighbor] = vertex
                depth[neighbor] = depth[vertex] + 1
                children[vertex].append(neighbor)
                order.append(neighbor)

    entry = [0] * vertex_count
    exit_time = [0] * vertex_count
    euler = []
    stack = [(root, False)]
    while stack:
        vertex, exiting = stack.pop()
        if exiting:
            exit_time[vertex] = len(euler)
            continue
        entry[vertex] = len(euler)
        euler.append(vertex)
        stack.append((vertex, True))
        for child in reversed(children[vertex]):
            stack.append((child, False))

    depth_lists: list[list[int]] = [[] for _ in range(4 * vertex_count)]
    sorted_values: list[list[int]] = [[] for _ in range(4 * vertex_count)]
    prefix_minima: list[list[int]] = [[] for _ in range(4 * vertex_count)]

    def build(node: int, left: int, right: int) -> None:
        if right - left == 1:
            vertex = euler[left]
            depth_lists[node] = [depth[vertex]]
            sorted_values[node] = [values[vertex]]
            prefix_minima[node] = [values[vertex]]
            return
        middle = (left + right) // 2
        build(node * 2, left, middle)
        build(node * 2 + 1, middle, right)
        pairs = sorted(
            zip(
                depth_lists[node * 2] + depth_lists[node * 2 + 1],
                sorted_values[node * 2] + sorted_values[node * 2 + 1],
                strict=True,
            )
        )
        depth_lists[node] = [pair[0] for pair in pairs]
        sorted_values[node] = [pair[1] for pair in pairs]
        minima = []
        current = 10**30
        for _, value in pairs:
            current = min(current, value)
            minima.append(current)
        prefix_minima[node] = minima

    build(1, 0, vertex_count)

    def query(
        node: int,
        left: int,
        right: int,
        query_left: int,
        query_right: int,
        depth_limit: int,
    ) -> int:
        if query_right <= left or right <= query_left:
            return 10**30
        if query_left <= left and right <= query_right:
            count = bisect_right(depth_lists[node], depth_limit)
            return 10**30 if count == 0 else prefix_minima[node][count - 1]
        middle = (left + right) // 2
        return min(
            query(
                node * 2,
                left,
                middle,
                query_left,
                query_right,
                depth_limit,
            ),
            query(
                node * 2 + 1,
                middle,
                right,
                query_left,
                query_right,
                depth_limit,
            ),
        )

    answers = []
    last = 0
    for encoded_vertex, encoded_extra_depth in encoded_queries:
        vertex = (encoded_vertex + last) % vertex_count
        extra_depth = (encoded_extra_depth + last) % vertex_count
        last = query(
            1,
            0,
            vertex_count,
            entry[vertex],
            exit_time[vertex],
            depth[vertex] + extra_depth,
        )
        answers.append(last)
    return answers
```

Every covered Euler segment binary-searches its depth-sorted values, giving
`O(log^2 n)` per online query.

## Expert solution: one persistent version per depth

```python
import sys


def solve() -> None:
    data = iter(map(int, sys.stdin.buffer.read().split()))
    test_count = next(data)
    output = []
    infinity = 10**30

    for _ in range(test_count):
        vertex_count = next(data)
        root = next(data) - 1
        values = [next(data) for _ in range(vertex_count)]
        graph = [[] for _ in range(vertex_count)]
        for _ in range(vertex_count - 1):
            first = next(data) - 1
            second = next(data) - 1
            graph[first].append(second)
            graph[second].append(first)

        parent = [-1] * vertex_count
        depth = [0] * vertex_count
        children = [[] for _ in range(vertex_count)]
        parent[root] = root
        order = [root]
        for vertex in order:
            for neighbor in graph[vertex]:
                if parent[neighbor] == -1:
                    parent[neighbor] = vertex
                    depth[neighbor] = depth[vertex] + 1
                    children[vertex].append(neighbor)
                    order.append(neighbor)

        entry = [0] * vertex_count
        exit_time = [0] * vertex_count
        euler = []
        stack = [(root, False)]
        while stack:
            vertex, exiting = stack.pop()
            if exiting:
                exit_time[vertex] = len(euler)
                continue
            entry[vertex] = len(euler)
            euler.append(vertex)
            stack.append((vertex, True))
            for child in reversed(children[vertex]):
                stack.append((child, False))

        maximum_depth = max(depth)
        vertices_at_depth = [[] for _ in range(maximum_depth + 1)]
        for vertex in range(vertex_count):
            vertices_at_depth[depth[vertex]].append(vertex)

        left_child = [0]
        right_child = [0]
        minimum = [infinity]

        def update(
            previous: int,
            left: int,
            right: int,
            position: int,
            value: int,
        ) -> int:
            node = len(minimum)
            left_child.append(left_child[previous])
            right_child.append(right_child[previous])
            minimum.append(minimum[previous])
            if right - left == 1:
                minimum[node] = value
                return node
            middle = (left + right) // 2
            if position < middle:
                left_child[node] = update(
                    left_child[previous], left, middle, position, value
                )
            else:
                right_child[node] = update(
                    right_child[previous], middle, right, position, value
                )
            minimum[node] = min(minimum[left_child[node]], minimum[right_child[node]])
            return node

        def range_minimum(
            node: int,
            left: int,
            right: int,
            query_left: int,
            query_right: int,
        ) -> int:
            if node == 0 or query_right <= left or right <= query_left:
                return infinity
            if query_left <= left and right <= query_right:
                return minimum[node]
            middle = (left + right) // 2
            return min(
                range_minimum(left_child[node], left, middle, query_left, query_right),
                range_minimum(
                    right_child[node], middle, right, query_left, query_right
                ),
            )

        versions = []
        current_root = 0
        for current_depth in range(maximum_depth + 1):
            for vertex in vertices_at_depth[current_depth]:
                current_root = update(
                    current_root,
                    0,
                    vertex_count,
                    entry[vertex],
                    values[vertex],
                )
            versions.append(current_root)

        query_count = next(data)
        last = 0
        for _ in range(query_count):
            encoded_vertex = next(data)
            encoded_extra_depth = next(data)
            vertex = (encoded_vertex + last) % vertex_count
            extra_depth = (encoded_extra_depth + last) % vertex_count
            version_depth = min(maximum_depth, depth[vertex] + extra_depth)
            last = range_minimum(
                versions[version_depth],
                0,
                vertex_count,
                entry[vertex],
                exit_time[vertex],
            )
            output.append(str(last))

    print("\n".join(output))


if __name__ == "__main__":
    solve()
```

Version `d` contains a point exactly when its vertex depth is at most `d`.
Intersecting that set with the Euler subtree interval is precisely the decoded
query domain.

**Complexity:** `O(n log n)` preprocessing time and storage per test case;
`O(log n)` per query.
