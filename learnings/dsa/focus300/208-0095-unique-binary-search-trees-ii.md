# Focus300 208: LeetCode 95 - Unique Binary Search Trees II

**Source:** [LeetCode 95](https://leetcode.com/problems/unique-binary-search-trees-ii/)  
**Difficulty:** Medium  
**Pattern:** recursive tree enumeration

## Exact contract

Generate every structurally unique BST that stores the values `1` through `n`.

## First principles

Choosing a root partitions the values into smaller left and right subproblems. Every unique tree is formed by combining one left shape, one right shape, and the chosen root value.


## Classroom board: choose the root and split the remaining keys

```text
    keys = [1, 2, 3]

    root = 2
    left subtree uses [1]
    right subtree uses [3]
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

- An empty range must contribute a single empty tree to the combination logic.
- Different root choices create different partitions of the same value set.
- The subproblem result is a list of trees, not a count.
- Recursive reuse is natural because the same interval appears many times.

## Brute force

```python
def generate_trees_brute(n):
    from functools import lru_cache

    @lru_cache(None)
    def build(lo, hi):
        if lo > hi:
            return [None]
        trees = []
        for root in range(lo, hi + 1):
            for left in build(lo, root - 1):
                for right in build(root + 1, hi):
                    node = TreeNode(root)
                    node.left = left
                    node.right = right
                    trees.append(node)
        return trees

    return build(1, n)
```

Generate all binary trees and keep only the ones that satisfy the BST ordering rule.

## Better insight

Use the root-as-divider recurrence so only valid BST shapes are ever built.

## Expert solution

```python
def generate_trees(n):
    if n == 0:
        return []

    from functools import lru_cache

    @lru_cache(None)
    def build(lo, hi):
        if lo > hi:
            return (None,)
        trees = []
        for root in range(lo, hi + 1):
            for left in build(lo, root - 1):
                for right in build(root + 1, hi):
                    node = TreeNode(root)
                    node.left = left
                    node.right = right
                    trees.append(node)
        return tuple(trees)

    return list(build(1, n))
```

Recursively enumerate all left and right trees for each root value, then combine every pair around that root.

**Complexity:** Catalan-number output size, with recursion and memoization overhead proportional to the subproblem reuse.
