# ICPC300 130: Codeforces 19E - Fairy

**Source:** [Codeforces 19E](https://codeforces.com/problemset/problem/19/E)  
**Pattern:** parity back-edge coverage on a DFS forest

## Exact contract

Given an undirected graph with edges numbered in input order, output every edge
whose removal makes the entire graph bipartite. Print the count, followed by
the qualifying edge numbers in any order.

## First principles

Color vertices by depth parity in a DFS forest. A non-tree edge joining equal
parities closes an odd fundamental cycle; call it bad. An edge joining opposite
parities closes an even fundamental cycle.

If there are no bad edges, the DFS coloring already proves the graph
bipartite, so every removal works. Otherwise:

- the sole bad non-tree edge works when exactly one exists;
- a tree edge works exactly when every bad back edge crosses its child-subtree
  cut and no even back edge crosses that cut.

Mark `+1` at each back edge's descendant and `-1` at its ancestor, then sum
marks upward. The subtree sum is the number of back edges crossing that tree
edge, so both conditions are checked in constant time per edge.

## Cases that decide correctness

- Process every connected component; an odd cycle elsewhere invalidates a
  local candidate.
- Parallel edges are distinguished by input edge number.
- Skip only the exact parent edge during DFS.
- If the graph is already bipartite, all `m` edges qualify.
- Even back edges matter: combining one with an odd fundamental cycle can
  preserve an odd cycle after a tree edge is removed.

## Brute force: remove each edge and recolor

```python
from collections import deque


def fairy_brute(vertex_count: int, edges: list[tuple[int, int]]) -> list[int]:
    answers = []
    for removed_edge in range(len(edges)):
        graph = [[] for _ in range(vertex_count)]
        for edge_index, (first, second) in enumerate(edges):
            if edge_index != removed_edge:
                graph[first - 1].append(second - 1)
                graph[second - 1].append(first - 1)

        color = [-1] * vertex_count
        bipartite = True
        for start in range(vertex_count):
            if color[start] != -1:
                continue
            color[start] = 0
            queue = deque([start])
            while queue and bipartite:
                vertex = queue.popleft()
                for neighbor in graph[vertex]:
                    if color[neighbor] == -1:
                        color[neighbor] = color[vertex] ^ 1
                        queue.append(neighbor)
                    elif color[neighbor] == color[vertex]:
                        bipartite = False
                        break
            if not bipartite:
                break
        if bipartite:
            answers.append(removed_edge + 1)
    return answers
```

This costs `O(m(n+m))` because it rebuilds and recolors the graph for every
candidate.

## Better insight: why testing one found odd cycle is insufficient

Every valid edge must lie on every odd cycle, so restricting candidates to one
odd cycle reduces practical work. Rechecking each such candidate can still be
quadratic, however, and merely intersecting a few discovered cycles is not an
exact intermediate algorithm. The DFS coverage counts below perform the full
condition in one traversal.

## Expert solution: accumulate odd and even back-edge coverage

```python
import sys


def solve() -> None:
    input_stream = sys.stdin.buffer
    vertex_count, edge_count = map(int, input_stream.readline().split())
    edges = []
    graph: list[list[tuple[int, int]]] = [[] for _ in range(vertex_count)]
    for edge_index in range(edge_count):
        first, second = map(int, input_stream.readline().split())
        first -= 1
        second -= 1
        edges.append((first, second))
        graph[first].append((second, edge_index))
        graph[second].append((first, edge_index))

    parent = [-1] * vertex_count
    parent_edge = [-1] * vertex_count
    depth = [0] * vertex_count
    color = [0] * vertex_count
    odd_coverage = [0] * vertex_count
    even_coverage = [0] * vertex_count
    finish_order = []
    bad_edges = []

    for start in range(vertex_count):
        if parent[start] != -1:
            continue
        parent[start] = start
        stack = [(start, 0)]
        while stack:
            vertex, adjacency_index = stack[-1]
            if adjacency_index == len(graph[vertex]):
                finish_order.append(vertex)
                stack.pop()
                continue
            neighbor, edge_index = graph[vertex][adjacency_index]
            stack[-1] = (vertex, adjacency_index + 1)
            if edge_index == parent_edge[vertex]:
                continue
            if parent[neighbor] == -1:
                parent[neighbor] = vertex
                parent_edge[neighbor] = edge_index
                depth[neighbor] = depth[vertex] + 1
                color[neighbor] = color[vertex] ^ 1
                stack.append((neighbor, 0))
            elif depth[neighbor] < depth[vertex]:
                if color[neighbor] == color[vertex]:
                    bad_edges.append(edge_index)
                    odd_coverage[vertex] += 1
                    odd_coverage[neighbor] -= 1
                else:
                    even_coverage[vertex] += 1
                    even_coverage[neighbor] -= 1

    bad_count = len(bad_edges)
    if bad_count == 0:
        answers = list(range(1, edge_count + 1))
    else:
        answers = []
        if bad_count == 1:
            answers.append(bad_edges[0] + 1)
        for vertex in finish_order:
            if parent[vertex] == vertex:
                continue
            if odd_coverage[vertex] == bad_count and even_coverage[vertex] == 0:
                answers.append(parent_edge[vertex] + 1)
            odd_coverage[parent[vertex]] += odd_coverage[vertex]
            even_coverage[parent[vertex]] += even_coverage[vertex]
        answers.sort()

    print(len(answers))
    if answers:
        print(" ".join(map(str, answers)))


if __name__ == "__main__":
    solve()
```

Subtree accumulation counts precisely which fundamental cycles use each tree
edge. Covering all odd back edges is necessary, and excluding every even back
edge makes it sufficient; the remaining DFS coloring is then a valid
bipartition.

**Complexity:** `O(n+m)` time and space.
