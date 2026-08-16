# Focus300 044: LeetCode 297 - Serialize and Deserialize Binary Tree

**Source:** [LeetCode 297](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/)  
**Difficulty:** Hard  
**Pattern:** structural traversal with explicit null markers

## Exact contract

Implement a codec for a binary tree of integer-valued nodes. `serialize(root)`
must return a string from which `deserialize(data)` reconstructs the same node
values and left/right structure. The wire format is implementation-defined,
but it must represent an empty tree and distinguish missing children.

## First principles

Node values alone do not determine structure. A traversal becomes reversible
when every absent child is represented explicitly. Preorder recursion consumes
one root followed by two subtrees; level order consumes child slots in queue
order.


## Classroom board: see the repeated work once

```text
brute force tries every choice.
the optimized solution keeps only the state that must survive to the
next step.
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

- An empty tree must round-trip.
- Negative and repeated values are valid.
- A node with only a right child differs from one with only a left child.
- Delimiters prevent ambiguity between multi-digit values.
- The iterative expert codec avoids Python recursion-depth failure on deep trees.

## Brute force: recursive preorder with null markers

```python
from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class TreeNode:
    val: int
    left: TreeNode | None = None
    right: TreeNode | None = None


class CodecPreorder:
    def serialize(self, root: TreeNode | None) -> str:
        tokens: list[str] = []

        def visit(node: TreeNode | None) -> None:
            if node is None:
                tokens.append("#")
                return
            tokens.append(str(node.val))
            visit(node.left)
            visit(node.right)

        visit(root)
        return ",".join(tokens)

    def deserialize(self, data: str) -> TreeNode | None:
        if not data:
            raise ValueError("serialized data must be nonempty")
        tokens = iter(data.split(","))

        def build() -> TreeNode | None:
            item = next(tokens)
            if item == "#":
                return None
            node = TreeNode(int(item))
            node.left = build()
            node.right = build()
            return node

        return build()
```

This is `O(n)` time and space but recursion depth can reach the tree height.

## Better transition: consume child slots iteratively

Level-order traversal exposes child slots in queue order. Writing `#` for a
missing slot makes the stream reversible, while trimming trailing null markers
keeps the representation compact.

## Expert solution: iterative level-order codec

```python
from __future__ import annotations

from collections import deque
from dataclasses import dataclass


@dataclass(slots=True)
class TreeNode:
    val: int
    left: TreeNode | None = None
    right: TreeNode | None = None


class Codec:
    def serialize(self, root: TreeNode | None) -> str:
        if root is None:
            return "#"
        queue: deque[TreeNode | None] = deque([root])
        tokens: list[str] = []
        while queue:
            node = queue.popleft()
            if node is None:
                tokens.append("#")
                continue
            tokens.append(str(node.val))
            queue.extend((node.left, node.right))
        while tokens[-1] == "#":
            tokens.pop()
        return ",".join(tokens)

    def deserialize(self, data: str) -> TreeNode | None:
        if not data:
            raise ValueError("serialized data must be nonempty")
        tokens = data.split(",")
        if tokens[0] == "#":
            return None
        root = TreeNode(int(tokens[0]))
        queue = deque([root])
        index = 1
        while queue and index < len(tokens):
            node = queue.popleft()
            if tokens[index] != "#":
                node.left = TreeNode(int(tokens[index]))
                queue.append(node.left)
            index += 1
            if index < len(tokens) and tokens[index] != "#":
                node.right = TreeNode(int(tokens[index]))
                queue.append(node.right)
            index += 1
        return root
```

Serialization emits child slots in the same order deserialization consumes
them. Missing markers preserve every structural distinction, and omitted
trailing markers can only describe children already known to be absent.

**Complexity:** `O(n)` time and `O(width)` queue space.
