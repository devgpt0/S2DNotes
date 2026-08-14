# ICPC300 072: CSES - Planets Cycles

**Source:** [CSES - Planets Cycles](https://cses.fi/problemset/task/1751/)  
**Pattern:** functional-graph cycle peeling

## Exact contract

Input gives `n` (`1 <= n <= 200000`) and, for every planet, its single outgoing
teleporter destination. For each starting planet, output how many distinct
planets are visited before a planet repeats.

## First principles

Every functional-graph component consists of one directed cycle with directed
trees feeding into it. A cycle vertex visits exactly the cycle length. A tree
vertex visits one more planet than its successor.

Indegree peeling removes all non-cycle vertices. The remaining vertices are
exactly the cycles. Assign each cycle length, then process peeled vertices in
reverse removal order with `answer[v] = 1 + answer[next[v]]`.

## Cases that decide correctness

- A self-loop is a cycle of length one.
- Different trees can feed the same cycle and reuse its computed length.
- Peeling order must be reversed so every successor answer already exists.
- Every planet has exactly one outgoing edge, but may have any indegree.

## Brute force: simulate with a fresh visited set

```python
def planet_visits_brute(successor: list[int]) -> list[int]:
    answers = []
    for start in range(len(successor)):
        seen = set()
        planet = start
        while planet not in seen:
            seen.add(planet)
            planet = successor[planet]
        answers.append(len(seen))
    return answers
```

**Complexity:** `O(n^2)` time and `O(n)` temporary space per start.

## Better space: Floyd's cycle detection per start

```python
def planet_visits_floyd(successor: list[int]) -> list[int]:
    answers = []
    for start in range(len(successor)):
        slow = successor[start]
        fast = successor[successor[start]]
        while slow != fast:
            slow = successor[slow]
            fast = successor[successor[fast]]

        distance_to_cycle = 0
        slow = start
        while slow != fast:
            slow = successor[slow]
            fast = successor[fast]
            distance_to_cycle += 1

        cycle_length = 1
        fast = successor[slow]
        while fast != slow:
            fast = successor[fast]
            cycle_length += 1
        answers.append(distance_to_cycle + cycle_length)
    return answers
```

Floyd removes the per-start set and uses `O(1)` extra space, but still repeats
long walks and takes `O(n^2)` time overall.

## Expert solution: peel trees, label cycles, restore trees

```python
from collections import deque
import sys


def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    vertex_count = data[0]
    successor = [value - 1 for value in data[1:]]
    indegree = [0] * vertex_count
    for destination in successor:
        indegree[destination] += 1

    queue = deque(vertex for vertex in range(vertex_count) if indegree[vertex] == 0)
    removed_order = []
    while queue:
        vertex = queue.popleft()
        removed_order.append(vertex)
        destination = successor[vertex]
        indegree[destination] -= 1
        if indegree[destination] == 0:
            queue.append(destination)

    answer = [0] * vertex_count
    for start in range(vertex_count):
        if indegree[start] == 0 or answer[start] != 0:
            continue
        cycle = [start]
        vertex = successor[start]
        while vertex != start:
            cycle.append(vertex)
            vertex = successor[vertex]
        cycle_length = len(cycle)
        for vertex in cycle:
            answer[vertex] = cycle_length

    for vertex in reversed(removed_order):
        answer[vertex] = answer[successor[vertex]] + 1
    print(*answer)


if __name__ == "__main__":
    solve()
```

Peeling removes no cycle vertex and removes every tree vertex. Cycle traversal
therefore labels precisely the recurrent parts; reverse restoration applies the
one-step recurrence along every incoming tree.

**Complexity:** `O(n)` time and `O(n)` space.

