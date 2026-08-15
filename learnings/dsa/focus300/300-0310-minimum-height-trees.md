# Focus300 300: LeetCode 310 - Minimum Height Trees

**Source:** [LeetCode 310](https://leetcode.com/problems/minimum-height-trees/)  
**Difficulty:** Medium  
**Pattern:** leaf trimming on an unrooted tree

## Exact contract

Return all roots that produce minimum-height trees.

## First principles

The tree center is what remains after repeatedly removing leaves. Trimming from the outside inward converges on the one or two centroid nodes that minimize height.

## Cases that decide correctness

- A single node is its own center.
- A path graph may have one or two centers.
- Leaves should be removed in layers.
- The answer is a set of centroids, not necessarily one node.

## Brute force

```python
def find_min_height_trees_brute(n, edges):
    from collections import defaultdict, deque
    graph = defaultdict(list)
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)
    best = None
    answer = []
    for root in range(n):
        queue = deque([(root, -1)])
        height = -1
        while queue:
            for _ in range(len(queue)):
                node, parent = queue.popleft()
                for nxt in graph[node]:
                    if nxt != parent:
                        queue.append((nxt, node))
            height += 1
        if best is None or height < best:
            best = height
            answer = [root]
        elif height == best:
            answer.append(root)
    return answer
```

Root the tree at every node and compute the height each time.

## Better insight

Trim leaves level by level until only the center nodes remain.

## Expert solution

```python
from collections import deque, defaultdict

def find_min_height_trees(n, edges):
    if n == 1:
        return [0]
    graph = defaultdict(set)
    degree = [0] * n
    for a, b in edges:
        graph[a].add(b)
        graph[b].add(a)
        degree[a] += 1
        degree[b] += 1
    leaves = deque(i for i in range(n) if degree[i] == 1)
    remaining = n
    while remaining > 2:
        size = len(leaves)
        remaining -= size
        for _ in range(size):
            leaf = leaves.popleft()
            for nxt in list(graph[leaf]):
                graph[nxt].remove(leaf)
                degree[nxt] -= 1
                if degree[nxt] == 1:
                    leaves.append(nxt)
    return list(leaves)
```

Use degree counts and a queue of current leaves, peel the tree layer by layer, and return the final one or two nodes.

**Complexity:** O(n) time and O(n) space.
