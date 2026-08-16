# Focus300 250: LeetCode 173 - Binary Search Tree Iterator

**Source:** [LeetCode 173](https://leetcode.com/problems/binary-search-tree-iterator/)  
**Difficulty:** Medium  
**Pattern:** iterative inorder traversal with a stack

## Exact contract

Implement an iterator over a BST that returns the next smallest value each time.

## First principles

Inorder traversal visits BST values in sorted order. A stack can hold the path to the next unvisited node so the iterator only exposes one value at a time.


## Classroom board: keep only the useful unfinished work

```text
a stack stores the part of the state that can still matter after the next step.
```



## Step-by-step transformation

1. Choose a start state such as a cell, node, or partial path.
2. Mark the state as visited or temporarily commit the choice.
3. Expand to valid neighbors or next choices while the invariant still holds.
4. Undo the temporary choice when the branch finishes, then return the collected answer.

These problems transform the input into output by exploring one branch at a time and backtracking whenever a branch can no longer produce a valid solution.


## Diagram: search and undo

```text

            start state
                |
                v
            choose one path
                |
                v
            explore neighbors
                |
                v
            undo and try next path
                |
                v
            answer
```

These notes use search, visit markers, and backtracking to turn one starting state into the final valid path or count.

## Cases that decide correctness

- An empty tree has no next value.
- The iterator should advance lazily instead of traversing the whole tree up front.
- Repeated `next` calls should keep pulling the next inorder node.
- The `hasNext` result depends on whether the stack still contains unvisited nodes.

## Brute force

```python
class BSTIteratorBrute:
    def __init__(self, root):
        self.values = []

        def inorder(node):
            if not node:
                return
            inorder(node.left)
            self.values.append(node.val)
            inorder(node.right)

        inorder(root)
        self.index = 0

    def next(self):
        value = self.values[self.index]
        self.index += 1
        return value

    def hasNext(self):
        return self.index < len(self.values)
```

Flatten the entire tree into a sorted array first.

## Better insight

Keep only the current left spine on a stack and advance lazily.

## Expert solution

```python
class BSTIterator:
    def __init__(self, root):
        self.stack = []
        self._push_left(root)

    def _push_left(self, node):
        while node:
            self.stack.append(node)
            node = node.left

    def next(self):
        node = self.stack.pop()
        self._push_left(node.right)
        return node.val

    def hasNext(self):
        return bool(self.stack)
```

Push the left path from the current node, pop the next inorder node on demand, and then explore its right subtree.

**Complexity:** `O(h)` amortized per operation and `O(h)` space.
