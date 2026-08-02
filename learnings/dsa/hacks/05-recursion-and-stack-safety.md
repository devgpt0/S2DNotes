# Recursion and Stack Safety

## First principles

Each recursive call consumes a stack frame. Algorithmic `O(n)` memory can
still fail when that memory is the language call stack. Input shape determines
depth: a balanced tree is shallow, while a path is maximally deep.

## Why it matters

Python's default recursion limit is near one thousand. A path-shaped tree can
crash a correct recursive DFS.

## Technique

Prefer an explicit stack when depth can be large or adversarial.

## Iterative DFS pattern

```python
def traversal_order(graph: list[list[int]], start: int) -> list[int]:
    visited = [False] * len(graph)
    visited[start] = True
    stack = [start]
    order: list[int] = []
    while stack:
        vertex = stack.pop()
        order.append(vertex)
        for neighbor in graph[vertex]:
            if not visited[neighbor]:
                visited[neighbor] = True
                stack.append(neighbor)
    return order
```

## Entry/exit event pattern

Use this when recursive code needs postorder work:

```python
stack = [(root, -1, False)]
while stack:
    vertex, parent, exiting = stack.pop()
    if exiting:
        finish(vertex)
        continue
    start(vertex)
    stack.append((vertex, parent, True))
    for child in reversed(tree[vertex]):
        if child != parent:
            stack.append((child, vertex, False))
```

## When recursion is reasonable

It is clear and often fine when the proven maximum depth is small. If you raise
the limit, do it deliberately and still understand that the native stack has a
finite memory limit.

```python
import sys
sys.setrecursionlimit(300_000)
```

## Visual worked example: the same DFS, different storage

Path graph `0-1-2-3-4`:

```text
recursive:
dfs(0)
  dfs(1)
    dfs(2)
      dfs(3)
        dfs(4)      depth = 5

iterative:
stack [0]
pop 0, push 1
pop 1, push 2
...
stack container grows in heap memory; Python call depth stays constant
```

For adversarial large graphs, prefer an explicit stack instead of relying on a
higher recursion limit.

## Traps

- Raising the limit does not create infinite stack memory.
- Marking visited after pushing neighbors can create many duplicates.
- Iterative postorder needs an exit event or a separately reversed order.
- Recursive memoization can still be deep even when the number of states fits.
