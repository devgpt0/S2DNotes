# Focus300 211: LeetCode 98 - Validate Binary Search Tree

**Source:** [LeetCode 98](https://leetcode.com/problems/validate-binary-search-tree/)  
**Difficulty:** Medium  
**Pattern:** recursive bounds checking

## Exact contract

Determine whether a binary tree satisfies the BST ordering rule for every node.

## First principles

A node is valid only when it lies strictly inside the range allowed by all its ancestors. Passing the allowed interval downward is the cleanest proof of correctness.


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

- Duplicate values violate strict BST ordering.
- An empty tree is valid.
- Local parent-child order is not enough; ancestor bounds matter too.
- A deep subtree can invalidate the whole tree even when the root looks fine.

## Brute force

```python
def is_valid_bst_brute(root):
    values = []

    def inorder(node):
        if not node:
            return
        inorder(node.left)
        values.append(node.val)
        inorder(node.right)

    inorder(root)
    return all(a < b for a, b in zip(values, values[1:]))
```

Check only direct parent-child relations, which misses ancestor violations.

## Better insight

Carry lower and upper bounds through the recursion so every node is checked against all ancestors at once.

## Expert solution

```python
def is_valid_bst(root):
    def dfs(node, lo, hi):
        if not node:
            return True
        if not (lo < node.val < hi):
            return False
        return dfs(node.left, lo, node.val) and dfs(node.right, node.val, hi)

    return dfs(root, float("-inf"), float("inf"))
```

Traverse the tree with an open interval for each node and reject the tree immediately if a value falls outside its allowed interval.

**Complexity:** O(n) time and O(h) recursion space.
