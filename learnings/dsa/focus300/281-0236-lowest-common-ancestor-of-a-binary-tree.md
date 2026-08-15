# Focus300 281: LeetCode 236 - Lowest Common Ancestor of a Binary Tree

**Source:** [LeetCode 236](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/)  
**Difficulty:** Medium  
**Pattern:** postorder recursion with ancestor propagation

## Exact contract

Return the lowest common ancestor of two nodes in a general binary tree.

## First principles

A node is the LCA if one target appears in each subtree or if the node itself is one of the targets and the other is found below. The recursion naturally reports that information upward.

## Cases that decide correctness

- Either node may be the ancestor of the other.
- The tree is not ordered, so BST shortcuts do not apply.
- The LCA may be the root.
- The recursion should stop early once both targets are proven to lie below one node.

## Brute force

```python
def lowest_common_ancestor_brute(root, p, q):
    parent = {root: None}
    stack = [root]
    while p not in parent or q not in parent:
        node = stack.pop()
        if node.left:
            parent[node.left] = node
            stack.append(node.left)
        if node.right:
            parent[node.right] = node
            stack.append(node.right)
    ancestors = set()
    while p:
        ancestors.add(p)
        p = parent[p]
    while q not in ancestors:
        q = parent[q]
    return q
```

Build ancestor sets for both nodes and compare them.

## Better insight

Use a single DFS that returns whether each subtree contains one of the targets.

## Expert solution

```python
def lowest_common_ancestor(root, p, q):
    if not root or root == p or root == q:
        return root
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)
    if left and right:
        return root
    return left or right
```

Recurse left and right, and when both sides report a hit, the current node is the LCA.

**Complexity:** O(n) time and O(h) space.
