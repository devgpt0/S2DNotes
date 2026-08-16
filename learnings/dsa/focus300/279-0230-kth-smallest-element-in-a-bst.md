# Focus300 279: LeetCode 230 - Kth Smallest Element in a BST

**Source:** [LeetCode 230](https://leetcode.com/problems/kth-smallest-element-in-a-bst/)  
**Difficulty:** Medium  
**Pattern:** inorder rank selection

## Exact contract

Return the `k`th smallest value in the BST.

## First principles

Inorder traversal of a BST visits values in sorted order. The `k`th smallest value is therefore the `k`th node visited in that traversal.


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

- `k = 1` returns the minimum value.
- A skewed tree still works as long as the inorder order is respected.
- The traversal can stop early once the answer is found.
- Duplicates, if present, follow the BST ordering convention of the problem.

## Brute force

```python
def kth_smallest_brute(root, k):
    values = []

    def inorder(node):
        if not node:
            return
        inorder(node.left)
        values.append(node.val)
        inorder(node.right)

    inorder(root)
    return values[k - 1]
```

Collect all values, sort them, and index the answer.

## Better insight

Traverse inorder and stop at the `k`th visit.

## Expert solution

```python
def kth_smallest(root, k):
    stack = []
    node = root
    while stack or node:
        while node:
            stack.append(node)
            node = node.left
        node = stack.pop()
        k -= 1
        if k == 0:
            return node.val
        node = node.right
```

Use recursive or iterative inorder traversal, decrement `k` on each visit, and return immediately when `k` reaches zero.

**Complexity:** `O(h + k)` average traversal effort with early exit and `O(h)` stack space.
