# Queue

## Idea

A queue stores values in **first in, first out** order. Items leave in the same
order they entered.

## Visual model

```text
remove <- [oldest ... newest] <- add
```

## Classroom board: BFS levels

```text
tree:       1
          /   \
         2     3
        /
       4

queue [1]     -> level [1], add 2,3
queue [2,3]   -> level [2,3], add 4
queue [4]     -> level [4]
```

Older discovered nodes leave first, so all of one distance/level is processed
before the next.

## Steps

1. Add newly discovered work at the back.
2. Remove the oldest work from the front.
3. Continue until the queue is empty.

## First-principles derivation

When work must be handled in discovery order, removing an arbitrary item is
wrong. A queue preserves first-in, first-out order.

The front is always the oldest unprocessed item; new work joins only at the
back.

## Pattern recognition

Use a queue for level-order processing, BFS, simulations, and tasks that must
be handled in arrival order.

## Implementation: level order of a tree

### C++

```cpp
struct TreeNode {
    int value;
    TreeNode* left = nullptr;
    TreeNode* right = nullptr;
};

std::vector<std::vector<int>> levelOrder(TreeNode* root) {
    if (root == nullptr) return {};
    std::queue<TreeNode*> queue;
    queue.push(root);
    std::vector<std::vector<int>> levels;
    while (!queue.empty()) {
        const int levelSize = queue.size();
        std::vector<int> level;
        for (int count = 0; count < levelSize; ++count) {
            TreeNode* node = queue.front();
            queue.pop();
            level.push_back(node->value);
            if (node->left != nullptr) queue.push(node->left);
            if (node->right != nullptr) queue.push(node->right);
        }
        levels.push_back(std::move(level));
    }
    return levels;
}
```

### Python

```python
from __future__ import annotations

from collections import deque
from dataclasses import dataclass


@dataclass
class TreeNode:
    value: int
    left: TreeNode | None = None
    right: TreeNode | None = None


def level_order(root: TreeNode | None) -> list[list[int]]:
    if root is None:
        return []
    queue = deque([root])
    levels: list[list[int]] = []
    while queue:
        level: list[int] = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.value)
            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)
        levels.append(level)
    return levels
```

### Java

```java
static final class TreeNode {
    final int value;
    TreeNode left;
    TreeNode right;

    TreeNode(int value) {
        this.value = value;
    }
}

static List<List<Integer>> levelOrder(TreeNode root) {
    if (root == null) return List.of();
    Queue<TreeNode> queue = new ArrayDeque<>();
    queue.add(root);
    List<List<Integer>> levels = new ArrayList<>();
    while (!queue.isEmpty()) {
        int levelSize = queue.size();
        List<Integer> level = new ArrayList<>(levelSize);
        for (int count = 0; count < levelSize; count++) {
            TreeNode node = queue.remove();
            level.add(node.value);
            if (node.left != null) queue.add(node.left);
            if (node.right != null) queue.add(node.right);
        }
        levels.add(level);
    }
    return levels;
}
```

## Why it works

All nodes of one level are already queued before their children, so recording
the current queue size cleanly separates levels.

## Complexity

Time is `O(n)` and space is `O(w)`, where `w` is the maximum tree width.

## Common mistakes

- Removing from the front of a Python list, which is `O(n)`; use `deque`.
- Recomputing the level size after adding children.
- Marking graph nodes visited only when removed, which can enqueue duplicates.
