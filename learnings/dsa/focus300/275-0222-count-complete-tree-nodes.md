# Focus300 275: LeetCode 222 - Count Complete Tree Nodes

**Source:** [LeetCode 222](https://leetcode.com/problems/count-complete-tree-nodes/)  
**Difficulty:** Medium  
**Pattern:** height-aware complete-tree counting

## Exact contract

Count the nodes in a complete binary tree faster than a full traversal when possible.

## First principles

A complete tree's left and right subtree heights reveal whether a subtree is perfect. If one side is perfect, its node count can be computed directly instead of recursing all the way down.


## Classroom board: walk the tree once

```text
choose the root condition, then push the relevant subtree state down as
you recurse or iterate.
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
