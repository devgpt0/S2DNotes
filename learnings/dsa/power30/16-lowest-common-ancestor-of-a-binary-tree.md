# Problem 16: Lowest Common Ancestor of a Binary Tree (LeetCode #236)

**Difficulty:** Medium  
**Core pattern:** Postorder tree DFS

## Problem statement

Given the root of a binary tree and two existing nodes `p` and `q`, return their
lowest common ancestor (LCA).

The LCA is the lowest node whose subtree contains both targets. A node may be an
ancestor of itself.

## Example

```text
            3
          /   \
         5     1
        / \   / \
       6   2 0   8
          / \
         7   4

p = 5, q = 1  ->  LCA = 3
p = 5, q = 4  ->  LCA = 5
```

## Observation

Ask each subtree a simpler question:

> Did you find `p`, `q`, or an LCA that was already discovered below you?

For a node:

- if the node is `p` or `q`, return it;
- if only one child returns a node, pass that result upward;
- if both children return a node, the current node is where the two targets
  meet, so it is the LCA.

## Decision diagram

```text
dfs(node)
   |
   +-- node is null ------------------------> return null
   |
   +-- node is p or q ----------------------> return node
   |
   +-- search left and right
           |
           +-- both found ------------------> return node (LCA)
           +-- only left found -------------> return left
           +-- only right found ------------> return right
           +-- neither found ---------------> return null
```

## Solution 1: Brute Force with Root-to-Node Paths

### Observation

Find the path from the root to `p` and the path from the root to `q`. The last
common node in the two paths is the answer.

- Time: `O(n)`
- Extra space: `O(n)` for the paths

This works, but it stores more information than necessary.

### Algorithm

1. Find and store the path from the root to `p`.
2. Find and store the path from the root to `q`.
3. Compare both paths from the root.
4. The last equal node is the lowest common ancestor.

### C++ code

```cpp
class Solution {
   private:
    bool findPath(TreeNode* node, TreeNode* target, vector<TreeNode*>& path) {
        if (node == nullptr) {
            return false;
        }

        path.push_back(node);
        if (node == target || findPath(node->left, target, path) ||
            findPath(node->right, target, path)) {
            return true;
        }

        path.pop_back();
        return false;
    }

   public:
    TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {
        vector<TreeNode*> pathToP;
        vector<TreeNode*> pathToQ;
        findPath(root, p, pathToP);
        findPath(root, q, pathToQ);

        TreeNode* answer = nullptr;
        int limit = min(pathToP.size(), pathToQ.size());
        for (int index = 0; index < limit; ++index) {
            if (pathToP[index] != pathToQ[index]) {
                break;
            }
            answer = pathToP[index];
        }
        return answer;
    }
};
```

### Complexity

- Time: `O(n)`
- Space: `O(n)` for two paths

## How we derive the optimal solution

```text
Store both complete root-to-node paths
               |
               v
Most path nodes are needed only to report whether a target was found
               |
               v
Let each subtree return p, q, an LCA, or null
               |
               v
Both children return a target -> current node is the LCA
               |
               v
One postorder DFS using O(h) recursion space
```

## Optimized / CP approach: One postorder DFS

### Algorithm

1. Return `null` when the current node is `null`.
2. Return the current node when it equals `p` or `q`.
3. Recursively search the left and right subtrees.
4. If both searches return a node, return the current node.
5. Otherwise, return whichever non-null result exists.

### Why it works

The first node that receives a non-null result from both sides is the lowest
place where the targets meet. After that node is returned, every ancestor simply
passes the same answer upward.

### Complexity

- Time: `O(n)` because every node is visited at most once.
- Space: `O(h)` for recursion, where `h` is the tree height.

## Pattern to remember

```text
Tree asks: "Where are two targets located?"
Think: postorder DFS + combine left and right answers.

left found + right found = current node is the answer
one side found          = pass that result upward
```

## C++

```cpp
class Solution {
   public:
    TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {
        if (root == nullptr || root == p || root == q) {
            return root;
        }

        TreeNode* left = lowestCommonAncestor(root->left, p, q);
        TreeNode* right = lowestCommonAncestor(root->right, p, q);

        if (left != nullptr && right != nullptr) {
            return root;
        }

        return left != nullptr ? left : right;
    }
};
```

## Python

```python
class Solution:
    def lowest_common_ancestor(
        self,
        root: TreeNode | None,
        p: TreeNode,
        q: TreeNode,
    ) -> TreeNode | None:
        if root is None or root is p or root is q:
            return root

        left = self.lowest_common_ancestor(root.left, p, q)
        right = self.lowest_common_ancestor(root.right, p, q)

        if left is not None and right is not None:
            return root

        return left if left is not None else right
```

## Java

```java
class Solution {
    public TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
        if (root == null || root == p || root == q) {
            return root;
        }

        TreeNode left = lowestCommonAncestor(root.left, p, q);
        TreeNode right = lowestCommonAncestor(root.right, p, q);

        if (left != null && right != null) {
            return root;
        }

        return left != null ? left : right;
    }
}
```

## Go

```go
func lowestCommonAncestor(root, p, q *TreeNode) *TreeNode {
	if root == nil || root == p || root == q {
		return root
	}

	left := lowestCommonAncestor(root.Left, p, q)
	right := lowestCommonAncestor(root.Right, p, q)

	if left != nil && right != nil {
		return root
	}
	if left != nil {
		return left
	}
	return right
}
```

## Common mistakes

- Comparing node values instead of node identities.
- Returning immediately after finding a target in only one child.
- Forgetting that `p` can itself be the LCA of `q`.
