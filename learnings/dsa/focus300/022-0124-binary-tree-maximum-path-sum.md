# Focus300 022: LeetCode 124 - Binary Tree Maximum Path Sum

**Source:** [LeetCode 124](https://leetcode.com/problems/binary-tree-maximum-path-sum/)  
**Difficulty:** Hard  
**Pattern:** tree DP separating extendable gain from complete paths

## Exact contract

Given a nonempty binary tree with integer values, return the largest sum of a
nonempty simple path. A path may start and end at any nodes, follows parent-child
edges, and cannot repeat a node.

## First principles

A path whose highest node is `u` may use the best nonnegative downward branch
from both children. That complete path updates the global answer.

The value returned to `u`'s parent is different: it may include only one child
branch, because including both would fork rather than remain a path. Negative
child gains are clipped to zero.

## Cases that decide correctness

- All node values may be negative; the answer is still one node, not zero.
- A maximum path need not include the root.
- A complete path may use both child branches.
- A parent-extendable path may use at most one child branch.
- The input tree is nonempty by source contract.

## Brute force: enumerate paths from every start node

```python
from dataclasses import dataclass


@dataclass(slots=True)
class TreeNode:
    val: int
    left: "TreeNode | None" = None
    right: "TreeNode | None" = None


def max_path_sum_brute(root: TreeNode | None) -> int:
    if root is None:
        raise ValueError("tree must be nonempty")
    nodes: list[TreeNode] = []
    adjacency: list[list[int]] = []
    stack: list[tuple[TreeNode, int]] = [(root, -1)]
    while stack:
        node, parent = stack.pop()
        index = len(nodes)
        nodes.append(node)
        adjacency.append([])
        if parent != -1:
            adjacency[index].append(parent)
            adjacency[parent].append(index)
        if node.left is not None:
            stack.append((node.left, index))
        if node.right is not None:
            stack.append((node.right, index))

    answer = nodes[0].val
    for start in range(len(nodes)):
        traversal = [(start, -1, 0)]
        while traversal:
            vertex, parent, path_sum = traversal.pop()
            path_sum += nodes[vertex].val
            answer = max(answer, path_sum)
            for neighbor in adjacency[vertex]:
                if neighbor != parent:
                    traversal.append((neighbor, vertex, path_sum))
    return answer
```

Every unordered path is visited from at least one endpoint, taking `O(n^2)`
time and `O(n)` traversal space.

## Better insight: each path has one highest node

Root the tree. The optimum is completely characterized by two downward gains
meeting at its unique highest node, so one postorder traversal is sufficient.

## Expert solution: postorder gain DP

```python
from dataclasses import dataclass


@dataclass(slots=True)
class TreeNode:
    val: int
    left: "TreeNode | None" = None
    right: "TreeNode | None" = None


def max_path_sum(root: TreeNode | None) -> int:
    if root is None:
        raise ValueError("tree must be nonempty")
    answer = root.val

    def downward_gain(node: TreeNode | None) -> int:
        nonlocal answer
        if node is None:
            return 0
        left_gain = max(0, downward_gain(node.left))
        right_gain = max(0, downward_gain(node.right))
        answer = max(answer, node.val + left_gain + right_gain)
        return node.val + max(left_gain, right_gain)

    downward_gain(root)
    return answer
```

Every possible highest node contributes its best complete path once, while the
returned state remains a valid single branch.

**Complexity:** `O(n)` time and `O(h)` recursion space for tree height `h`.
