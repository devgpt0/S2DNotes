# Focus300 280: LeetCode 235 - Lowest Common Ancestor of a Binary Search Tree

**Source:** [LeetCode 235](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/)  
**Difficulty:** Easy  
**Pattern:** BST-guided descent

## Exact contract

Return the lowest common ancestor of two nodes in a BST.

## First principles

BST ordering tells us whether both targets lie left, both lie right, or they split on opposite sides of the current node. The split point is the LCA.


## Classroom board: meet where the two paths overlap

```text
          3
         /                 5   1
       /               6   2

    the first shared ancestor of 6 and 2 is 5.
```



## Step-by-step transformation

1. Traverse the structure and keep the pointer, node, or subtree state that matters.
2. Rewire links or combine child results without losing the part of the structure you still need.
3. Carry the surviving state forward to the next node or subtree.
4. Return the rebuilt structure, node value, or accumulated traversal result.

These notes work by preserving the structure while changing just the links or the returned subtree results that lead to the final answer.


## Diagram: walk and reconnect pointers

```text

            original nodes
                |
                v
            read or split the structure
                |
                v
            reconnect links or combine child results
                |
                v
            rebuilt list / tree / value
```

The algorithm walks the structure, keeps only the needed pointers or subtree results, and returns the rebuilt output.

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
