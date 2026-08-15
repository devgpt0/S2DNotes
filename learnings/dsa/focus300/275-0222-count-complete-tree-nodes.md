# Focus300 275: LeetCode 222 - Count Complete Tree Nodes

**Source:** [LeetCode 222](https://leetcode.com/problems/count-complete-tree-nodes/)  
**Difficulty:** Medium  
**Pattern:** height-aware complete-tree counting

## Exact contract

Count the nodes in a complete binary tree faster than a full traversal when possible.

## First principles

A complete tree's left and right subtree heights reveal whether a subtree is perfect. If one side is perfect, its node count can be computed directly instead of recursing all the way down.

## Cases that decide correctness

- An empty tree has zero nodes.
- A perfect subtree has a closed-form node count.
- The last level may be only partially filled from left to right.
- Height comparisons should drive the recursion.

## Brute force

```python
def count_nodes_brute(root):
    if not root:
        return 0
    return 1 + count_nodes_brute(root.left) + count_nodes_brute(root.right)
```

Traverse every node and count them.

## Better insight

Use subtree heights to skip over perfect subtrees in constant time.

## Expert solution

```python
def count_nodes(root):
    def left_depth(node):
        depth = 0
        while node:
            depth += 1
            node = node.left
        return depth

    def right_depth(node):
        depth = 0
        while node:
            depth += 1
            node = node.right
        return depth

    if not root:
        return 0
    ld = left_depth(root)
    rd = right_depth(root)
    if ld == rd:
        return (1 << ld) - 1
    return 1 + count_nodes(root.left) + count_nodes(root.right)
```

Compare the leftmost depths of the left and right subtrees, and recurse only into the incomplete side while counting the perfect side directly.

**Complexity:** `O(log^2 n)` in the common complete-tree solution and `O(log n)` extra space.
