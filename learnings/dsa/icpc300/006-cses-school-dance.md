# ICPC300 006: CSES - School Dance

**Source:** [CSES - School Dance](https://cses.fi/problemset/task/1696/)  
**Pattern:** Hopcroft-Karp bipartite matching  
**Goal:** Match as many left-side students to compatible right-side students
as possible, using each student at most once.

`graph[left]` contains zero-based compatible right vertices. Each function
returns `(left, right)` pairs.

## 1. First principles

A **matching** has no repeated endpoint. An **augmenting path** alternates
between unmatched and matched edges, starts and ends at unmatched vertices,
and increases the matching size by one when all its edge choices are flipped.

Repeated DFS finds one augmenting path at a time. Hopcroft-Karp first uses BFS
to find the shortest augmenting-path length, then DFS finds many vertex-disjoint
paths of that length in one phase.

```text
unmatched left --free edge--> right --matched edge--> left --free--> right
after flipping: matching size increases by 1
```

## 2. Cases that decide correctness

| Case | Required behavior |
| --- | --- |
| Isolated vertex | Leave it unmatched. |
| Several left vertices want one right vertex | Match at most one of them. |
| A direct greedy choice blocks another pair | Follow an alternating path and reassign. |
| Duplicate compatibility edge | It must not create a duplicate match. |
| One side is larger | The answer is at most the smaller side. |

## 3. Brute force: try every assignment

For each left vertex, either skip it or pair it with one unused compatible
right vertex. Keep the largest complete choice.

```python
def maximum_matching_brute(
    graph: list[list[int]], right_count: int
) -> list[tuple[int, int]]:
    if right_count < 0:
        raise ValueError("right_count must be nonnegative")
    if any(
        right < 0 or right >= right_count for neighbors in graph for right in neighbors
    ):
        raise ValueError("right vertex is outside the graph")

    used_right = [False] * right_count
    chosen: list[tuple[int, int]] = []
    best: list[tuple[int, int]] = []

    def search(left: int) -> None:
        nonlocal best
        if len(chosen) + len(graph) - left <= len(best):
            return
        if left == len(graph):
            best = chosen.copy()
            return

        search(left + 1)
        tried_right: set[int] = set()
        for right in graph[left]:
            if right in tried_right or used_right[right]:
                continue
            tried_right.add(right)
            used_right[right] = True
            chosen.append((left, right))
            search(left + 1)
            chosen.pop()
            used_right[right] = False

    search(0)
    return best
```

**Complexity:** exponential time, `O(left_count + right_count)` recursion and
matching space.

## 4. Better: one augmenting DFS at a time

Kuhn's algorithm lets a left vertex take a free right vertex or recursively
move its current partner elsewhere.

```python
def maximum_matching_kuhn(
    graph: list[list[int]], right_count: int
) -> list[tuple[int, int]]:
    if right_count < 0:
        raise ValueError("right_count must be nonnegative")
    if any(
        right < 0 or right >= right_count for neighbors in graph for right in neighbors
    ):
        raise ValueError("right vertex is outside the graph")

    matched_left = [-1] * right_count

    def augment(left: int, seen_right: list[bool]) -> bool:
        for right in graph[left]:
            if seen_right[right]:
                continue
            seen_right[right] = True
            previous_left = matched_left[right]
            if previous_left == -1 or augment(previous_left, seen_right):
                matched_left[right] = left
                return True
        return False

    for left in range(len(graph)):
        augment(left, [False] * right_count)

    matching = [(left, right) for right, left in enumerate(matched_left) if left != -1]
    matching.sort()
    return matching
```

**Why it works:** a successful DFS flips one augmenting path. When no
augmenting path remains, Berge's lemma says the matching is maximum.

**Complexity:** `O(VE)` time and `O(V)` extra space.

## 5. Expert solution: Hopcroft-Karp

BFS assigns distances to unmatched left vertices and discovers the shortest
possible augmenting-path length. DFS follows only those layers, so one phase
augments along many shortest paths.

```python
from collections import deque


def maximum_matching_hopcroft_karp(
    graph: list[list[int]], right_count: int
) -> list[tuple[int, int]]:
    if right_count < 0:
        raise ValueError("right_count must be nonnegative")
    if any(
        right < 0 or right >= right_count for neighbors in graph for right in neighbors
    ):
        raise ValueError("right vertex is outside the graph")

    left_count = len(graph)
    pair_left = [-1] * left_count
    pair_right = [-1] * right_count
    infinity = left_count + right_count + 1
    distance = [infinity] * left_count

    def build_layers() -> int:
        queue: deque[int] = deque()
        for left in range(left_count):
            if pair_left[left] == -1:
                distance[left] = 0
                queue.append(left)
            else:
                distance[left] = infinity

        shortest_path = infinity
        while queue:
            left = queue.popleft()
            if distance[left] >= shortest_path:
                continue
            for right in graph[left]:
                next_left = pair_right[right]
                if next_left == -1:
                    shortest_path = distance[left] + 1
                elif distance[next_left] == infinity:
                    distance[next_left] = distance[left] + 1
                    queue.append(next_left)
        return shortest_path

    def augment(left: int, shortest_path: int) -> bool:
        for right in graph[left]:
            next_left = pair_right[right]
            if next_left == -1:
                if distance[left] + 1 != shortest_path:
                    continue
            elif distance[next_left] != distance[left] + 1 or not augment(
                next_left, shortest_path
            ):
                continue

            pair_left[left] = right
            pair_right[right] = left
            return True

        distance[left] = infinity
        return False

    while True:
        shortest_path = build_layers()
        if shortest_path == infinity:
            break
        for left in range(left_count):
            if pair_left[left] == -1:
                augment(left, shortest_path)

    return [(left, right) for left, right in enumerate(pair_left) if right != -1]
```

### Why the expert code is correct

- BFS permits only shortest alternating layers in a phase.
- Each successful DFS flips a valid augmenting path, so the result remains a
  matching and grows by one.
- A phase ends only after no more shortest augmenting paths exist; the outer
  loop stops only when none exists at all, which is maximum by Berge's lemma.

**Complexity:** `O(E sqrt(V))` time and `O(V + E)` space.

## 6. What to remember

```text
augmenting path exists -> matching is not maximum
Kuhn                -> find one path per DFS
Hopcroft-Karp       -> BFS shortest layers, then many DFS augmentations
```
