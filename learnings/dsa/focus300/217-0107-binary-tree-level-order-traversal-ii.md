# Focus300 217: LeetCode 107 - Binary Tree Level Order Traversal II

**Source:** [LeetCode 107](https://leetcode.com/problems/binary-tree-level-order-traversal-ii/)  
**Difficulty:** Medium  
**Pattern:** breadth-first traversal by tree levels

## Exact contract

Return the tree values grouped by depth in the order requested by the problem.

## First principles

A queue naturally separates one depth from the next. Once the current layer size is known, that entire level can be consumed before the next one starts.

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

def level_order_bottom(root):
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
    return result[::-1]
```

Use BFS to consume one depth per loop iteration and append each finished layer in the requested orientation.

**Complexity:** O(n) time and O(n) space.
