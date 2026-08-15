# Focus300 216: LeetCode 106 - Construct Binary Tree from Inorder and Postorder Traversal

**Source:** [LeetCode 106](https://leetcode.com/problems/construct-binary-tree-from-inorder-and-postorder-traversal/)  
**Difficulty:** Medium  
**Pattern:** tree reconstruction from traversal boundaries

## Exact contract

Rebuild the unique binary tree that matches the two traversal orders.

## First principles

One traversal reveals the root order, and the other reveals where each subtree splits. An index map turns the split lookup into constant time.

## Cases that decide correctness

- The empty traversal pair yields no tree.
- A leaf node is a base case in both orders.
- The root position in the inorder traversal determines left and right subtree sizes.
- The recursive slices must stay aligned with the traversal conventions.

## Brute force

```python
def build_tree_brute(preorder, inorder):
    if not preorder:
        return None
    root = TreeNode(preorder[0])
    mid = inorder.index(preorder[0])
    root.left = build_tree_brute(preorder[1 : 1 + mid], inorder[:mid])
    root.right = build_tree_brute(preorder[1 + mid :], inorder[mid + 1 :])
    return root
```

Generate all trees and compare their traversals until one matches.

## Better insight

Use the root traversal order plus an index map to split each subtree exactly once.

## Expert solution

```python
def build_tree(inorder, postorder):
    index = {value: i for i, value in enumerate(inorder)}

    def build(il, ir, pl, pr):
        if il > ir:
            return None
        root_val = postorder[pr]
        mid = index[root_val]
        left_size = mid - il
        root = TreeNode(root_val)
        root.left = build(il, mid - 1, pl, pl + left_size - 1)
        root.right = build(mid + 1, ir, pl + left_size, pr - 1)
        return root

    return build(0, len(inorder) - 1, 0, len(postorder) - 1)
```

Pick the next root from the traversal that identifies roots, locate it in the inorder sequence, and recurse on the left and right intervals.

**Complexity:** O(n) time and O(n) space.
