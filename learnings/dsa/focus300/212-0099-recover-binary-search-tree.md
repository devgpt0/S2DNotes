# Focus300 212: LeetCode 99 - Recover Binary Search Tree

**Source:** [LeetCode 99](https://leetcode.com/problems/recover-binary-search-tree/)  
**Difficulty:** Medium  
**Pattern:** inorder anomaly detection

## Exact contract

Restore a BST in which exactly two nodes were swapped by mistake.

## First principles

An inorder traversal of a valid BST is sorted. The swapped nodes show up as one or two local inversions in that sorted sequence, and those inversions identify the corrupted values.

## Cases that decide correctness

- The swapped nodes may be adjacent in inorder order or far apart.
- The tree structure itself must not change.
- Only two values are incorrect, not two whole subtrees.
- The solution should work even when the wrong nodes are separated by many levels.

## Brute force

```python
def recover_tree_brute(root):
    nodes = []

    def inorder(node):
        if not node:
            return
        inorder(node.left)
        nodes.append(node)
        inorder(node.right)

    inorder(root)
    vals = sorted(node.val for node in nodes)
    for node, value in zip(nodes, vals):
        node.val = value
```

Collect all values, sort them, and rewrite the tree.

## Better insight

Use inorder traversal to detect the two offending nodes directly without extra storage for the full value list.

## Expert solution

```python
def recover_tree(root):
    first = second = prev = None

    def inorder(node):
        nonlocal first, second, prev
        if not node:
            return
        inorder(node.left)
        if prev and prev.val > node.val:
            first = first or prev
            second = node
        prev = node
        inorder(node.right)

    inorder(root)
    first.val, second.val = second.val, first.val
```

Track the previous inorder node, record the first and second inversions, and swap only those two node values at the end.

**Complexity:** O(n) time and O(h) space.
