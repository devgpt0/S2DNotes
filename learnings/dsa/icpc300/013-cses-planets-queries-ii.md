# ICPC300 013: CSES - Planets Queries II

**Source:** [CSES - Planets Queries II](https://cses.fi/problemset/task/1160/)  
**Pattern:** functional-graph decomposition plus binary lifting  
**Goal:** For each ordered pair `(a, b)`, return the minimum number of
teleportations needed to reach `b` from `a`, or `-1` if it is impossible.

## 1. Problem in plain words

Every planet has exactly one outgoing teleporter. Following teleporters from a
planet eventually repeats a planet, so every weak component has exactly one
directed cycle. Directed trees feed into that cycle.

Direction matters. Two tree branches can enter the same cycle, yet neither can
reach the other. Once a walk reaches the cycle, it can never return to a tree.

## 2. First principles

Repeatedly remove vertices with indegree zero. Removed vertices are tree
vertices; the vertices left behind are exactly the cycles.

For every vertex, record:

- which functional-graph component it belongs to;
- its distance `depth` from the cycle;
- the cycle vertex it eventually enters;
- positions and lengths for actual cycle vertices.

Binary lifting computes the vertex reached after any needed number of tree
steps. A query then has only two possible shapes:

1. target in a tree: lift the start to the target's depth and compare;
2. target on a cycle: reach the start's cycle entry, then move around the cycle.

## 3. Cases that decide correctness

| Query shape | Result |
| --- | --- |
| `a == b` | `0`, including on a self-loop. |
| Different components | `-1`. |
| Cycle to tree | `-1`. |
| Deeper tree node to its ancestor | Their depth difference. |
| One tree branch to another | `-1`, even if both enter the same cycle. |
| Tree to cycle | Tree depth plus forward cyclic distance. |

## 4. Brute force: follow one teleporter at a time

After at most `n` moves, a functional-graph walk has repeated a vertex. If the
target was not seen by then, it never will be.

```python
def minimum_teleports_brute_force(
    successor: list[int], queries: list[tuple[int, int]]
) -> list[int]:
    planet_count = len(successor)
    answers: list[int] = []

    for start, target in queries:
        planet = start
        answer = -1
        for steps in range(planet_count + 1):
            if planet == target:
                answer = steps
                break
            planet = successor[planet]
        answers.append(answer)

    return answers
```

**Why it works:** before the first repeat, the walk contains every planet it
will ever reach and in minimum-step order.

**Complexity:** `O(nq)` time and `O(1)` extra space per query.

## 5. Better approach: why binary lifting alone is not enough

Binary lifting quickly answers "where am I after `k` moves?" The source asks
for the unknown minimum `k`, and reachability is not monotone in `k` on a
cycle. Binary search therefore does not apply. The tree/cycle structure is the
missing information; once it is known, lifting becomes useful.

There is no separate asymptotically competitive middle solution for arbitrary
queries. Per-start distance maps can help repeated starts, but still require
`O(n)` work and memory for each distinct start.

## 6. Expert solution: peel cycles, label trees, lift queries

Reverse edges let one breadth-first traversal spread each cycle's labels into
all trees feeding it. The lifting table stores successors after powers of two.

```python
from collections import deque


def minimum_teleports(
    successor: list[int], queries: list[tuple[int, int]]
) -> list[int]:
    planet_count = len(successor)
    if planet_count == 0:
        raise ValueError("at least one planet is required")
    if any(not 0 <= planet < planet_count for planet in successor):
        raise ValueError("successor index is outside the graph")

    reverse_graph: list[list[int]] = [[] for _ in range(planet_count)]
    indegree = [0] * planet_count
    for planet, next_planet in enumerate(successor):
        reverse_graph[next_planet].append(planet)
        indegree[next_planet] += 1

    queue = deque(planet for planet in range(planet_count) if indegree[planet] == 0)
    on_cycle = [True] * planet_count
    while queue:
        planet = queue.popleft()
        on_cycle[planet] = False
        next_planet = successor[planet]
        indegree[next_planet] -= 1
        if indegree[next_planet] == 0:
            queue.append(next_planet)

    component = [-1] * planet_count
    depth = [-1] * planet_count
    cycle_entry = [-1] * planet_count
    cycle_position = [-1] * planet_count
    cycle_lengths: list[int] = []
    cycle_vertices: list[int] = []

    for start in range(planet_count):
        if not on_cycle[start] or component[start] != -1:
            continue

        component_id = len(cycle_lengths)
        cycle: list[int] = []
        planet = start
        while component[planet] == -1:
            component[planet] = component_id
            cycle_position[planet] = len(cycle)
            depth[planet] = 0
            cycle_entry[planet] = planet
            cycle.append(planet)
            cycle_vertices.append(planet)
            planet = successor[planet]
        cycle_lengths.append(len(cycle))

    queue = deque(cycle_vertices)
    while queue:
        planet = queue.popleft()
        for predecessor in reverse_graph[planet]:
            if component[predecessor] != -1:
                continue
            component[predecessor] = component[planet]
            depth[predecessor] = depth[planet] + 1
            cycle_entry[predecessor] = cycle_entry[planet]
            queue.append(predecessor)

    level_count = max(1, planet_count.bit_length())
    jump_table = [successor.copy()]
    for _ in range(1, level_count):
        previous = jump_table[-1]
        jump_table.append([previous[previous[node]] for node in range(planet_count)])

    def jump(planet: int, steps: int) -> int:
        bit = 0
        while steps:
            if steps & 1:
                planet = jump_table[bit][planet]
            steps >>= 1
            bit += 1
        return planet

    answers: list[int] = []
    for start, target in queries:
        if not 0 <= start < planet_count or not 0 <= target < planet_count:
            raise ValueError("query index is outside the graph")
        if component[start] != component[target]:
            answers.append(-1)
            continue

        if depth[target] > 0:
            if depth[start] < depth[target]:
                answers.append(-1)
                continue
            difference = depth[start] - depth[target]
            answers.append(difference if jump(start, difference) == target else -1)
            continue

        entry = jump(start, depth[start])
        cycle_length = cycle_lengths[component[start]]
        around_cycle = (cycle_position[target] - cycle_position[entry]) % cycle_length
        answers.append(depth[start] + around_cycle)

    return answers
```

### Why the expert code is correct

- Indegree peeling removes every tree vertex and no cycle vertex.
- Reverse BFS assigns each tree vertex its unique cycle entry and exact depth.
- For a tree target, the only possible route stays on its ancestor chain; the
  depth-aligned equality test is therefore necessary and sufficient.
- For a cycle target, every reachable walk first spends `depth[start]` moves
  reaching its entry, then has one unique forward cyclic distance to target.

**Complexity:** `O((n + q) log n)` time and `O(n log n)` memory.

## 7. What to remember

A functional graph is not an arbitrary directed graph: it is one cycle with
in-trees per component. Name the query shape before writing any lifting code.
