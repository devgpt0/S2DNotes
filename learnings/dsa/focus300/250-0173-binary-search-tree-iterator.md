# Focus300 250: LeetCode 173 - Binary Search Tree Iterator

**Source:** [LeetCode 173](https://leetcode.com/problems/binary-search-tree-iterator/)  
**Difficulty:** Medium  
**Pattern:** iterative inorder traversal with a stack

## Exact contract

Implement an iterator over a BST that returns the next smallest value each time.

## First principles

Inorder traversal visits BST values in sorted order. A stack can hold the path to the next unvisited node so the iterator only exposes one value at a time.

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
