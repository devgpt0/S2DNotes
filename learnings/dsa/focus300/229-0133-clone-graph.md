# Focus300 229: LeetCode 133 - Clone Graph

**Source:** [LeetCode 133](https://leetcode.com/problems/clone-graph/)  
**Difficulty:** Medium  
**Pattern:** graph copy with memoized node mapping

## Exact contract

Deep-copy a graph so the clone has the same adjacency structure but entirely new nodes.

## First principles

A graph copy needs one fresh node per original node and one edge per original edge. The only subtlety is avoiding infinite recursion on cycles by remembering which originals have already been cloned.


## Classroom board: copy nodes before revisiting them

```text
    1 -- 2
    |    |
    3 --/

    remember old node -> new node so each vertex is cloned once.
```



## Step-by-step transformation

1. Choose a start state such as a cell, node, or partial path.
2. Mark the state as visited or temporarily commit the choice.
3. Expand to valid neighbors or next choices while the invariant still holds.
4. Undo the temporary choice when the branch finishes, then return the collected answer.

These problems transform the input into output by exploring one branch at a time and backtracking whenever a branch can no longer produce a valid solution.


## Diagram: search and undo

```text

            start state
                |
                v
            choose one path
                |
                v
            explore neighbors
                |
                v
            undo and try next path
                |
                v
            answer
```

These notes use search, visit markers, and backtracking to turn one starting state into the final valid path or count.

## Cases that decide correctness

- Cycles must not cause repeated cloning.
- Disconnected input is outside the usual problem contract; the traversal starts from the given node.
- Self-loops should be preserved in the clone.
- Neighbor order is usually preserved by cloning in traversal order.

## Brute force

```python
def clone_graph_brute(node):
    from collections import deque
    if not node:
        return None
    clones = {node: Node(node.val)}
    queue = deque([node])
    while queue:
        cur = queue.popleft()
        for nei in cur.neighbors:
            if nei not in clones:
                clones[nei] = Node(nei.val)
                queue.append(nei)
            clones[cur].neighbors.append(clones[nei])
    return clones[node]
```

Traverse the graph, build a raw adjacency list, and then reconstruct node objects later.

## Better insight

Use a hash map from original nodes to cloned nodes and create each clone at most once.

## Expert solution

```python
def clone_graph(node):
    if not node:
        return None
    clones = {}

    def dfs(cur):
        if cur in clones:
            return clones[cur]
        clone = Node(cur.val)
        clones[cur] = clone
        clone.neighbors = [dfs(nei) for nei in cur.neighbors]
        return clone

    return dfs(node)
```

DFS or BFS from the start node, clone unseen neighbors on demand, and reuse the cached clone whenever the same original node appears again.

**Complexity:** O(V+E) time and O(V) space.
