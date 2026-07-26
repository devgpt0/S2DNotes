# Problem 17: Binary Tree Maximum Path Sum (LeetCode #124)

**Difficulty:** Hard  
**Core pattern:** Tree DP / postorder DFS

## Problem statement

A path may start and end at any two nodes, but adjacent path nodes must be
connected by an edge and no node may be used twice. Return the largest possible
path sum.

## Example

```text
       -10
       / \
      9   20
         /  \
        15   7

Best path: 15 -> 20 -> 7
Answer: 42
```

## Observation

There are two different values at each node:

1. **Path through this node:** may use both children and can update the answer.
2. **Gain returned to the parent:** may use only one child, because a path sent
   upward cannot branch.

Negative child gains should be ignored. Adding them would only reduce the sum.

## Value-flow diagram

```text
             parent
                ^
                | return node + max(left, right)
                |
              node
             /    \
       left gain  right gain

Candidate answer at node:
node + max(0, left gain) + max(0, right gain)
```

## Solution 1: Brute Force by Recomputing Every Turning Point

### Observation

Treat every node as a possible path endpoint or turning point and repeatedly
search the tree. This repeats the same subtree work and can take `O(n^2)` time.

### Algorithm

1. Treat every node as the highest point of a possible path.
2. Recursively compute the best downward gain from each child.
3. Update the answer with `node + leftGain + rightGain`.
4. Repeat the downward searches independently for every node.

### C++ code

```cpp
class Solution {
   private:
    int downwardGain(TreeNode* node) {
        if (node == nullptr) {
            return 0;
        }
        return node->val +
               max({0, downwardGain(node->left), downwardGain(node->right)});
    }

    void tryEveryTurningPoint(TreeNode* node, int& best) {
        if (node == nullptr) {
            return;
        }

        int left = max(0, downwardGain(node->left));
        int right = max(0, downwardGain(node->right));
        best = max(best, node->val + left + right);

        tryEveryTurningPoint(node->left, best);
        tryEveryTurningPoint(node->right, best);
    }

   public:
    int maxPathSum(TreeNode* root) {
        int best = INT_MIN;
        tryEveryTurningPoint(root, best);
        return best;
    }
};
```

### Complexity

- Time: `O(n^2)` in a skewed tree because gains are recomputed
- Space: `O(h)` recursion space

## How we derive the optimal solution

```text
Recompute downward gains for every turning point
                    |
                    v
The same subtree gain is calculated many times
                    |
                    v
Calculate each gain once during postorder DFS
                    |
                    v
Use both child gains for the answer at this node
Return only the better one-child gain to the parent
                    |
                    v
O(n) time
```

## Optimized / CP approach: Postorder tree DP

### Algorithm

1. Recursively compute the best downward gain from the left child.
2. Recursively compute the best downward gain from the right child.
3. Replace a negative gain with `0`.
4. Update the global answer with `node + left gain + right gain`.
5. Return `node + max(left gain, right gain)` to the parent.

### Why it works

Every possible path has one highest node. When DFS processes that node, the
path's left and right parts are available as downward gains, so the algorithm
considers that path exactly where it should.

### Complexity

- Time: `O(n)`
- Space: `O(h)` recursion space

## Pattern to remember

```text
Tree path may bend at a node:

answer candidate = node + best left branch + best right branch
value returned   = node + only one best branch

Use this pattern for maximum paths, diameters, and tree gains.
```

## C++

```cpp
class Solution {
   private:
    int best = INT_MIN;

    int gain(TreeNode* node) {
        if (node == nullptr) {
            return 0;
        }

        int left = max(0, gain(node->left));
        int right = max(0, gain(node->right));

        best = max(best, node->val + left + right);
        return node->val + max(left, right);
    }

   public:
    int maxPathSum(TreeNode* root) {
        gain(root);
        return best;
    }
};
```

## Python

```python
class Solution:
    def max_path_sum(self, root: TreeNode) -> int:
        best = float("-inf")

        def gain(node: TreeNode | None) -> int:
            nonlocal best

            if node is None:
                return 0

            left = max(0, gain(node.left))
            right = max(0, gain(node.right))

            best = max(best, node.val + left + right)
            return node.val + max(left, right)

        gain(root)
        return int(best)
```

## Java

```java
class Solution {
    private int best = Integer.MIN_VALUE;

    public int maxPathSum(TreeNode root) {
        gain(root);
        return best;
    }

    private int gain(TreeNode node) {
        if (node == null) {
            return 0;
        }

        int left = Math.max(0, gain(node.left));
        int right = Math.max(0, gain(node.right));

        best = Math.max(best, node.val + left + right);
        return node.val + Math.max(left, right);
    }
}
```

## Go

```go
func maxPathSum(root *TreeNode) int {
	best := math.MinInt

	var gain func(*TreeNode) int
	gain = func(node *TreeNode) int {
		if node == nil {
			return 0
		}

		left := max(0, gain(node.Left))
		right := max(0, gain(node.Right))

		best = max(best, node.Val+left+right)
		return node.Val + max(left, right)
	}

	gain(root)
	return best
}
```

## Common mistakes

- Returning both child branches to the parent, which creates an invalid fork.
- Initializing the answer to `0`; an all-negative tree must return its largest
  negative node.
- Forgetting to ignore negative child gains.
