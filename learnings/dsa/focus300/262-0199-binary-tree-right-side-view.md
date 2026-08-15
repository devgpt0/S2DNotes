# Focus300 262: LeetCode 199 - Binary Tree Right Side View

**Source:** [LeetCode 199](https://leetcode.com/problems/binary-tree-right-side-view/)  
**Difficulty:** Medium  
**Pattern:** tree traversal / recursion

## Exact contract

Solve the tree problem 'Binary Tree Right Side View' by returning the value or structure requested in the statement.

## First principles

Tree problems usually reduce to recursion on subtrees, with the current node combining the answers from the children.

## Cases that decide correctness

- An empty tree is often the simplest base case.
- A single node should satisfy the recurrence immediately.
- Balanced and skewed trees can behave very differently.
- The node's own value often combines child results.

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

Traverse the whole tree and recompute the same subtree facts repeatedly.

## Better insight

Use recursion or BFS so each node contributes to the answer exactly once.

## Expert solution

```python
from collections import deque

def right_side_view(root):
    if not root:
        return []
    result = []
    queue = deque([root])
    while queue:
        rightmost = None
        for _ in range(len(queue)):
            node = queue.popleft()
            rightmost = node.val
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(rightmost)
    return result
```

Define the subtree state precisely, combine child results at the current node, and pass the minimum amount of information upward.

**Complexity:** Usually O(n) time with O(h) recursion or queue space.
