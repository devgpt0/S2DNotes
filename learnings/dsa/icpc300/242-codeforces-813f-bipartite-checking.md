# ICPC300 242: Codeforces 813F - Bipartite Checking

**Source:** [Codeforces 813F](https://codeforces.com/problemset/problem/813/F)  
**Difficulty:** 2500  
**Pattern:** time-segment tree with rollback parity DSU

## Exact contract

An initially empty undirected graph receives edge toggles. A listed edge is
added when absent and removed when present. After every toggle, print whether
the graph is bipartite.

## First principles

Offline, each edge is active on disjoint time intervals. Add an edge to the
nodes of a segment tree whose time ranges partition each active interval.

During a DFS of that tree, a rollback DSU maintains component parity. An edge
requires its endpoints to have opposite parity. A same-component edge whose
parities are equal creates one conflict. Roll back every union and conflict
when leaving a time node.

## Cases that decide correctness

- Edges toggle rather than having explicit add/remove types.
- The same edge endpoints must use one canonical order.
- Parallel active copies do not occur under toggle semantics.
- Self-loops immediately violate bipartiteness.
- Rollback DSU must not use path compression.

## Brute force: rebuild and two-color after every toggle

```python
from collections import deque


def bipartite_checking_brute(
    vertex_count: int, toggles: list[tuple[int, int]]
) -> list[bool]:
    active: set[tuple[int, int]] = set()
    answers = []
    for first, second in toggles:
        edge = (first, second) if first <= second else (second, first)
        if edge in active:
            active.remove(edge)
        else:
            active.add(edge)
        graph = [[] for _ in range(vertex_count)]
        for left, right in active:
            graph[left].append(right)
            graph[right].append(left)
        color = [-1] * vertex_count
        valid = True
        for start in range(vertex_count):
            if color[start] != -1:
                continue
            color[start] = 0
            queue = deque([start])
            while queue and valid:
                vertex = queue.popleft()
                for neighbor in graph[vertex]:
                    if color[neighbor] == -1:
                        color[neighbor] = color[vertex] ^ 1
                        queue.append(neighbor)
                    elif color[neighbor] == color[vertex]:
                        valid = False
                        break
        answers.append(valid)
    return answers
```

This repeats `O(n+m)` work after every toggle.

## Better insight: edge lifetimes are static offline intervals

The time segment tree exposes each active edge during exactly the leaves where
it exists. Rollback makes one DSU reusable across its DFS branches.

## Expert solution: rollback parity constraints

```python
import sys


class RollbackParityDsu:
    def __init__(self, size: int) -> None:
        self.parent = list(range(size))
        self.size = [1] * size
        self.parity = [0] * size
        self.conflicts = 0
        self.history: list[tuple[int, int, int, int] | bool] = []

    def find(self, vertex: int) -> tuple[int, int]:
        parity = 0
        while vertex != self.parent[vertex]:
            parity ^= self.parity[vertex]
            vertex = self.parent[vertex]
        return vertex, parity

    def snapshot(self) -> int:
        return len(self.history)

    def union_opposite(self, first: int, second: int) -> None:
        first_root, first_parity = self.find(first)
        second_root, second_parity = self.find(second)
        if first_root == second_root:
            creates_conflict = first_parity == second_parity
            self.history.append(creates_conflict)
            if creates_conflict:
                self.conflicts += 1
            return
        if self.size[first_root] < self.size[second_root]:
            first_root, second_root = second_root, first_root
            first_parity, second_parity = second_parity, first_parity
        self.history.append(
            (second_root, first_root, self.size[first_root], self.conflicts)
        )
        self.parent[second_root] = first_root
        self.parity[second_root] = first_parity ^ second_parity ^ 1
        self.size[first_root] += self.size[second_root]

    def rollback(self, snapshot: int) -> None:
        while len(self.history) > snapshot:
            change = self.history.pop()
            if isinstance(change, bool):
                self.conflicts -= int(change)
                continue
            child, parent, old_size, old_conflicts = change
            self.parent[child] = child
            self.parity[child] = 0
            self.size[parent] = old_size
            self.conflicts = old_conflicts


def solve() -> None:
    input_stream = sys.stdin.buffer
    vertex_count, query_count = map(int, input_stream.readline().split())
    toggles = []
    for _ in range(query_count):
        first, second = map(int, input_stream.readline().split())
        first -= 1
        second -= 1
        toggles.append((first, second) if first <= second else (second, first))

    intervals: list[tuple[int, int, tuple[int, int]]] = []
    opened: dict[tuple[int, int], int] = {}
    for time, edge in enumerate(toggles):
        if edge in opened:
            intervals.append((opened.pop(edge), time, edge))
        else:
            opened[edge] = time
    for edge, start in opened.items():
        intervals.append((start, query_count, edge))

    time_tree: list[list[tuple[int, int]]] = [[] for _ in range(4 * query_count)]

    def add_interval(
        node: int,
        left: int,
        right: int,
        query_left: int,
        query_right: int,
        edge: tuple[int, int],
    ) -> None:
        if query_right <= left or right <= query_left:
            return
        if query_left <= left and right <= query_right:
            time_tree[node].append(edge)
            return
        middle = (left + right) // 2
        add_interval(node * 2, left, middle, query_left, query_right, edge)
        add_interval(node * 2 + 1, middle, right, query_left, query_right, edge)

    for left, right, edge in intervals:
        add_interval(1, 0, query_count, left, right, edge)

    dsu = RollbackParityDsu(vertex_count)
    answers = [False] * query_count

    def visit(node: int, left: int, right: int) -> None:
        snapshot = dsu.snapshot()
        for first, second in time_tree[node]:
            dsu.union_opposite(first, second)
        if right - left == 1:
            answers[left] = dsu.conflicts == 0
        else:
            middle = (left + right) // 2
            visit(node * 2, left, middle)
            visit(node * 2 + 1, middle, right)
        dsu.rollback(snapshot)

    visit(1, 0, query_count)
    print("\n".join("YES" if answer else "NO" for answer in answers))


if __name__ == "__main__":
    solve()
```

Each leaf sees exactly its active constraints, and parity conflicts precisely
characterize odd cycles.

**Complexity:** `O(q log q log n)` time and `O(q log q+n)` space.
