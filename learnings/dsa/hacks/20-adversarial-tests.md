# Build Adversarial Tests

## First principles

Random inputs tend to be average-shaped. Adversarial tests deliberately
maximize depth, duplicates, collisions, stale states, boundary movement, or
another weakness implied by the algorithm.

## Why it matters

Random tests find ordinary bugs. Adversarial tests attack the exact assumption
that makes the algorithm fast or correct.

## Technique

For every structure, construct its worst shape:

| Technique | Adversarial input |
| --- | --- |
| recursive DFS | one long path |
| naive quicksort | already sorted values with bad pivot rule |
| hash/frequency logic | many duplicates and missing complements |
| sliding window | answer changes at every step; include zeros if allowed |
| binary search | answer at each boundary and no exact match |
| Dijkstra | many stale improvements to the same vertex |
| DSU without balancing | sequential chain unions |
| greedy | smallest counterexamples to alternative local rules |
| DP | all states reachable; maximum answer magnitude |

## Python generator pattern

```python
def path_graph(size: int) -> list[list[int]]:
    graph = [[] for _ in range(size)]
    for vertex in range(size - 1):
        graph[vertex].append(vertex + 1)
        graph[vertex + 1].append(vertex)
    return graph
```

## Pattern recognition

Read the proof and complexity analysis. Negate each helpful assumption: balanced
becomes skewed, distinct becomes equal, middle answer becomes boundary answer.

## Expert habit

Attack both correctness and resources. A solution can return correct answers
on small tests yet exceed stack, time, or memory on the maximum shape.

## Visual worked example: attack DFS depth

Both graphs have `100,000` vertices.

```text
balanced tree:
depth about 17
recursive stack is shallow

path:
0-1-2-3-...-99999
depth = 100,000
recursive DFS risks stack failure
```

The path is not an invalid corner case; it is a legal input that maximizes the
chosen implementation's recursion depth.

## Traps

- Testing maximum random input but not maximum worst-case structure.
- Assuming average-case hash or pivot behavior is always safe.
- Creating invalid adversarial data outside statement constraints.
