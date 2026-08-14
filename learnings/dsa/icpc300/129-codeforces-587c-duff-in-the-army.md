# ICPC300 129: Codeforces 587C - Duff in the Army

**Source:** [Codeforces 587C](https://codeforces.com/problemset/problem/587/C)  
**Pattern:** persistent root-path multisets with LCA inclusion-exclusion

## Exact contract

A tree has `n` cities and `m` people numbered `1..m`; each person lives in one
city. Each query gives cities `u`, `v` and `a` (`a <= 10`). Output up to `a`
smallest person numbers whose home lies on the inclusive tree path from `u` to
`v`: first the number printed, then those IDs in increasing order.

## First principles

Root the tree at city `1`. Build for every vertex `v` a persistent frequency
segment tree containing the person IDs on the root-to-`v` path. If `l` is the
LCA of query endpoints, their path multiset is

`version[u] + version[v] - version[l] - version[parent(l)]`.

This subtracts every strict ancestor of `l` twice and leaves `l` once. Descend
the four segment-tree roots together, always visiting the lower ID half first,
and stop after `a` present leaves.

## Cases that decide correctness

- The LCA city is included exactly once.
- For root LCA, the parent version is the empty version.
- Person IDs, not city numbers, determine output order.
- Several people may live in one city.
- Print fewer than `a` IDs when the path contains fewer people.

## Brute force: recover each path with BFS

```python
from collections import deque


def duff_path_bfs(
    vertex_count: int,
    edges: list[tuple[int, int]],
    homes: list[int],
    queries: list[tuple[int, int, int]],
) -> list[list[int]]:
    graph = [[] for _ in range(vertex_count)]
    for first, second in edges:
        graph[first - 1].append(second - 1)
        graph[second - 1].append(first - 1)
    people_at = [[] for _ in range(vertex_count)]
    for person, city in enumerate(homes, start=1):
        people_at[city - 1].append(person)

    answers = []
    for raw_start, raw_target, limit in queries:
        start = raw_start - 1
        target = raw_target - 1
        parent = [-1] * vertex_count
        parent[start] = start
        queue = deque([start])
        while queue and parent[target] == -1:
            vertex = queue.popleft()
            for neighbor in graph[vertex]:
                if parent[neighbor] == -1:
                    parent[neighbor] = vertex
                    queue.append(neighbor)

        people = []
        vertex = target
        while vertex != start:
            people.extend(people_at[vertex])
            vertex = parent[vertex]
        people.extend(people_at[start])
        answers.append(sorted(people)[:limit])
    return answers
```

Every query can search the full tree and sort all people on its path.

## Better: root parents, then climb both endpoints

```python
def duff_parent_climb(
    vertex_count: int,
    edges: list[tuple[int, int]],
    homes: list[int],
    queries: list[tuple[int, int, int]],
) -> list[list[int]]:
    graph = [[] for _ in range(vertex_count)]
    for first, second in edges:
        graph[first - 1].append(second - 1)
        graph[second - 1].append(first - 1)
    people_at = [[] for _ in range(vertex_count)]
    for person, city in enumerate(homes, start=1):
        people_at[city - 1].append(person)

    parent = [-1] * vertex_count
    depth = [0] * vertex_count
    parent[0] = 0
    order = [0]
    for vertex in order:
        for neighbor in graph[vertex]:
            if parent[neighbor] == -1:
                parent[neighbor] = vertex
                depth[neighbor] = depth[vertex] + 1
                order.append(neighbor)

    answers = []
    for raw_first, raw_second, limit in queries:
        first = raw_first - 1
        second = raw_second - 1
        people = []
        while depth[first] > depth[second]:
            people.extend(people_at[first])
            first = parent[first]
        while depth[second] > depth[first]:
            people.extend(people_at[second])
            second = parent[second]
        while first != second:
            people.extend(people_at[first])
            people.extend(people_at[second])
            first = parent[first]
            second = parent[second]
        people.extend(people_at[first])
        answers.append(sorted(people)[:limit])
    return answers
```

Preprocessing removes BFS, but a long path can still cost linear time.

## Expert solution: persistent person-ID segment trees

```python
import sys
from array import array


def solve() -> None:
    input_stream = sys.stdin.buffer
    vertex_count, person_count, query_count = map(int, input_stream.readline().split())
    graph = [[] for _ in range(vertex_count)]
    for _ in range(vertex_count - 1):
        first, second = map(int, input_stream.readline().split())
        graph[first - 1].append(second - 1)
        graph[second - 1].append(first - 1)

    people_at = [[] for _ in range(vertex_count)]
    homes = list(map(int, input_stream.readline().split()))
    for person, city in enumerate(homes, start=1):
        people_at[city - 1].append(person)

    parent = [-1] * vertex_count
    depth = [0] * vertex_count
    parent[0] = 0
    order = [0]
    for vertex in order:
        for neighbor in graph[vertex]:
            if parent[neighbor] == -1:
                parent[neighbor] = vertex
                depth[neighbor] = depth[vertex] + 1
                order.append(neighbor)

    level_count = max(1, vertex_count.bit_length())
    ancestors = [parent.copy()]
    for _ in range(1, level_count):
        previous = ancestors[-1]
        ancestors.append([previous[previous[v]] for v in range(vertex_count)])

    def lowest_common_ancestor(first: int, second: int) -> int:
        if depth[first] < depth[second]:
            first, second = second, first
        difference = depth[first] - depth[second]
        for level in range(level_count):
            if difference >> level & 1:
                first = ancestors[level][first]
        if first == second:
            return first
        for level in range(level_count - 1, -1, -1):
            if ancestors[level][first] != ancestors[level][second]:
                first = ancestors[level][first]
                second = ancestors[level][second]
        return parent[first]

    left_child = array("i", [0])
    right_child = array("i", [0])
    node_count = array("i", [0])

    def insert(previous: int, left: int, right: int, person: int) -> int:
        node = len(node_count)
        left_child.append(left_child[previous])
        right_child.append(right_child[previous])
        node_count.append(node_count[previous] + 1)
        if right - left == 1:
            return node
        middle = (left + right) // 2
        if person < middle:
            left_child[node] = insert(left_child[previous], left, middle, person)
        else:
            right_child[node] = insert(right_child[previous], middle, right, person)
        return node

    versions = [0] * vertex_count
    for vertex in order:
        version = 0 if vertex == 0 else versions[parent[vertex]]
        for person in people_at[vertex]:
            version = insert(version, 1, person_count + 1, person)
        versions[vertex] = version

    def smallest_on_path(first: int, second: int, limit: int) -> list[int]:
        ancestor = lowest_common_ancestor(first, second)
        before_ancestor = 0 if ancestor == 0 else versions[parent[ancestor]]
        answer = []

        def collect(
            first_root: int,
            second_root: int,
            ancestor_root: int,
            before_root: int,
            left: int,
            right: int,
        ) -> None:
            total = (
                node_count[first_root]
                + node_count[second_root]
                - node_count[ancestor_root]
                - node_count[before_root]
            )
            if total == 0 or len(answer) == limit:
                return
            if right - left == 1:
                answer.append(left)
                return
            middle = (left + right) // 2
            collect(
                left_child[first_root],
                left_child[second_root],
                left_child[ancestor_root],
                left_child[before_root],
                left,
                middle,
            )
            collect(
                right_child[first_root],
                right_child[second_root],
                right_child[ancestor_root],
                right_child[before_root],
                middle,
                right,
            )

        collect(
            versions[first],
            versions[second],
            versions[ancestor],
            before_ancestor,
            1,
            person_count + 1,
        )
        return answer

    output = []
    for _ in range(query_count):
        first, second, limit = map(int, input_stream.readline().split())
        people = smallest_on_path(first - 1, second - 1, limit)
        output.append(" ".join(map(str, (len(people), *people))))
    print("\n".join(output))


if __name__ == "__main__":
    solve()
```

Persistent versions make the four-root count exact for every person-ID range.
Lower halves are exhausted first, so the reported leaves are precisely the
smallest IDs on the path.

**Complexity:** `O((n+m) log m + n log n)` preprocessing and
`O(log n + a log m)` per query, with `a <= 10`.
