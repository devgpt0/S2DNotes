# Focus300 213: LeetCode 102 - Binary Tree Level Order Traversal

**Source:** [LeetCode 102](https://leetcode.com/problems/binary-tree-level-order-traversal/)  
**Difficulty:** Medium  
**Pattern:** breadth-first traversal by tree levels

## Exact contract

Return the tree values grouped by depth in the order requested by the problem.

## First principles

A queue naturally separates one depth from the next. Once the current layer size is known, that entire level can be consumed before the next one starts.


## Classroom board: visit the tree level by level

```text
          1
         /                 2   3

    levels: [1], [2, 3]
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

- An empty tree returns an empty result.
- A single node produces one one-element level.
- Skewed trees still form one node per level.
- The zigzag variant must reverse every other layer only.

## Brute force

```python
from collections import deque

def level_order_brute(root):
    if not root:
        return []
    result = []
    queue = deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(level)
    return result
```

Traverse the whole tree and then sort the nodes by depth afterward.

## Better insight

Process one queue layer at a time so each level is emitted directly.

## Expert solution

```python
from collections import deque

def level_order(root):
    if not root:
        return []
    result = []
    queue = deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(level)
    return result
```

Use BFS to consume one depth per loop iteration and append each finished layer in the requested orientation.

**Complexity:** O(n) time and O(n) space.
