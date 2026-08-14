# ICPC300 245: Codeforces 1060E - Sergey and Subway

**Source:** [Codeforces 1060E](https://codeforces.com/problemset/problem/1060/E)  
**Difficulty:** 2200  
**Pattern:** tree distance sum plus bipartite parity count

## Exact contract

Start with a tree. Add a direct subway edge between every pair of vertices at
tree distance two. Output the sum of new shortest-path distances over all
unordered vertex pairs.

## First principles

Along any tree path, one subway edge can replace two original edges. Therefore
the new distance is `ceil(original_distance / 2)`.

Sum original tree distances by edge contributions: deleting an edge with one
side of size `s` contributes `s*(n-s)`. Odd tree distances occur exactly between
opposite bipartition colors, giving `color_count[0]*color_count[1]` pairs. Thus

`sum ceil(d/2) = (sum d + number_of_odd_d) / 2`.

## Cases that decide correctness

- Pairs are unordered and exclude pairing a vertex with itself.
- Every tree is bipartite.
- Even distances contribute exactly half; odd distances round upward.
- Each tree edge contribution uses one subtree size.
- The answer requires wide integers.

## Brute force: BFS from every vertex after adding edges

```python
from collections import deque


def sergey_subway_brute(vertex_count: int, edges: list[tuple[int, int]]) -> int:
    tree = [[] for _ in range(vertex_count)]
    for first, second in edges:
        tree[first].append(second)
        tree[second].append(first)
    distance_two_edges: set[tuple[int, int]] = set()
    for start in range(vertex_count):
        for middle in tree[start]:
            for target in tree[middle]:
                if start < target:
                    distance_two_edges.add((start, target))
    graph = [neighbors.copy() for neighbors in tree]
    for first, second in distance_two_edges:
        graph[first].append(second)
        graph[second].append(first)
    answer = 0
    for source in range(vertex_count):
        distance = [-1] * vertex_count
        distance[source] = 0
        queue = deque([source])
        while queue:
            vertex = queue.popleft()
            for neighbor in graph[vertex]:
                if distance[neighbor] == -1:
                    distance[neighbor] = distance[vertex] + 1
                    queue.append(neighbor)
        answer += sum(distance[source + 1 :])
    return answer
```

This explicitly builds the augmented graph and repeats BFS.

## Better insight: the augmented distance depends only on tree distance

Every two consecutive tree edges can be replaced, and no subway edge advances
more than two tree edges. Hence the ceiling formula is exact.

## Expert solution: edge cuts and parity classes

```python
import sys


def solve() -> None:
    input_stream = sys.stdin.buffer
    vertex_count = int(input_stream.readline())
    graph = [[] for _ in range(vertex_count)]
    for _ in range(vertex_count - 1):
        first, second = map(int, input_stream.readline().split())
        first -= 1
        second -= 1
        graph[first].append(second)
        graph[second].append(first)

    parent = [-1] * vertex_count
    parent[0] = 0
    color = [0] * vertex_count
    order = [0]
    for vertex in order:
        for neighbor in graph[vertex]:
            if parent[neighbor] == -1:
                parent[neighbor] = vertex
                color[neighbor] = color[vertex] ^ 1
                order.append(neighbor)

    subtree_size = [1] * vertex_count
    tree_distance_sum = 0
    for vertex in reversed(order[1:]):
        size = subtree_size[vertex]
        tree_distance_sum += size * (vertex_count - size)
        subtree_size[parent[vertex]] += size
    first_color_count = color.count(0)
    odd_distance_pairs = first_color_count * (vertex_count - first_color_count)
    print((tree_distance_sum + odd_distance_pairs) // 2)


if __name__ == "__main__":
    solve()
```

Edge cuts count the sum of original distances; bipartite colors count exactly
which of those distances need rounding up.

**Complexity:** `O(n)` time and space.
