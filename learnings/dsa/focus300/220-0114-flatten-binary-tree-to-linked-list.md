# Focus300 220: LeetCode 114 - Flatten Binary Tree to Linked List

**Source:** [LeetCode 114](https://leetcode.com/problems/flatten-binary-tree-to-linked-list/)  
**Difficulty:** Medium  
**Pattern:** preorder-style tree splicing

## Exact contract

Rewrite the tree in place so it becomes a right-skewed linked list that follows preorder order.

## First principles

The preorder sequence already tells us the final node order. The only challenge is rewiring pointers without losing the untouched subtrees.


## Classroom board: turn the tree into a preorder list

```text
          1
         /                 2   5

    result: 1 -> 2 -> 5
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

- A single node is already flat.
- Left subtrees must be moved into the right chain.
- The final structure must contain no left pointers.
- The original preorder order must be preserved exactly.

## Brute force

```python
def flatten_brute(root):
    nodes = []

    def preorder(node):
        if not node:
            return
        nodes.append(node)
        preorder(node.left)
        preorder(node.right)

    preorder(root)
    for i in range(len(nodes) - 1):
        nodes[i].left = None
        nodes[i].right = nodes[i + 1]
    if nodes:
        nodes[-1].left = None
        nodes[-1].right = None
```

Collect nodes in preorder and rebuild a fresh right chain.

## Better insight

Splice each left subtree between the current node and its original right subtree.

## Expert solution

```python
def flatten(root):
    def dfs(node):
        if not node:
            return None
        left_tail = dfs(node.left)
        right_tail = dfs(node.right)
        if left_tail:
            left_tail.right = node.right
            node.right = node.left
            node.left = None
        return right_tail or left_tail or node

    dfs(root)
```

Traverse recursively or iteratively, preserve the right subtree, move the left subtree to the right, and append the saved right subtree to the tail of the moved left chain.

**Complexity:** O(n) time and O(h) recursion space, or O(1) extra space with pointer walking.
