# Focus300 212: LeetCode 99 - Recover Binary Search Tree

**Source:** [LeetCode 99](https://leetcode.com/problems/recover-binary-search-tree/)  
**Difficulty:** Medium  
**Pattern:** inorder anomaly detection

## Exact contract

Restore a BST in which exactly two nodes were swapped by mistake.

## First principles

An inorder traversal of a valid BST is sorted. The swapped nodes show up as one or two local inversions in that sorted sequence, and those inversions identify the corrupted values.


## Classroom board: see the repeated work once

```text
brute force tries every choice.
the optimized solution keeps only the state that must survive to the
next step.
```



## Step-by-step transformation

1. Read the input and identify the smallest state that still determines the answer.
2. Process one element, node, or row at a time while preserving that state.
3. Discard work that can no longer change the result.
4. Convert the surviving state into the output the problem requests.

The examples and code below show this transformation on the specific problem instance.


## Diagram: input to output

```text

        input
            |
            v
        core invariant
            |
            v
        process one step at a time
            |
            v
        output
```

The note shows the main idea, the repeated work, and the small state that turns the input into the output.

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
