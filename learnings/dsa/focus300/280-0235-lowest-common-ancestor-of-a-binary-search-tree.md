# Focus300 280: LeetCode 235 - Lowest Common Ancestor of a Binary Search Tree

**Source:** [LeetCode 235](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/)  
**Difficulty:** Easy  
**Pattern:** BST-guided descent

## Exact contract

Return the lowest common ancestor of two nodes in a BST.

## First principles

BST ordering tells us whether both targets lie left, both lie right, or they split on opposite sides of the current node. The split point is the LCA.

## Cases that decide correctness

- If one target is the current node, that node is the LCA.
- Both targets can lie in the same subtree.
- The root itself may be the answer.
- The BST ordering is enough; no full subtree scan is needed.

## Brute force

```python
def lowest_common_ancestor_brute(root, p, q):
    while root:
        if p.val < root.val and q.val < root.val:
            root = root.left
        elif p.val > root.val and q.val > root.val:
            root = root.right
        else:
            return root
```

Collect all ancestors of both nodes and compare the paths.

## Better insight

Walk downward using the BST ordering to stop at the split point.

## Expert solution

```python
def lowest_common_ancestor(root, p, q):
    while root:
        if p.val < root.val and q.val < root.val:
            root = root.left
        elif p.val > root.val and q.val > root.val:
            root = root.right
        else:
            return root
```

Move left when both targets are smaller, right when both are larger, and return the current node when the targets diverge.

**Complexity:** O(h) time and O(1) space.
