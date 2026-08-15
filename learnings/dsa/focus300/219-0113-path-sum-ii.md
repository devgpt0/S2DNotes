# Focus300 219: LeetCode 113 - Path Sum II

**Source:** [LeetCode 113](https://leetcode.com/problems/path-sum-ii/)  
**Difficulty:** Medium  
**Pattern:** root-to-leaf DFS with path tracking

## Exact contract

Return every root-to-leaf path whose node values add up to the target sum.

## First principles

The path sum is just a running total along one branch of the tree. A path is valid only when both the leaf condition and the sum condition are satisfied together.

## Cases that decide correctness

- An empty tree produces no paths.
- Only root-to-leaf paths count.
- Negative values are allowed and may be necessary.
- The same prefix can lead to different suffix outcomes.

## Brute force

```python
def path_sum_brute(root, target_sum):
    result = []

    def dfs(node, path, total):
        if not node:
            return
        path.append(node.val)
        total += node.val
        if not node.left and not node.right and total == target_sum:
            result.append(path.copy())
        dfs(node.left, path, total)
        dfs(node.right, path, total)
        path.pop()

    dfs(root, [], 0)
    return result
```

Enumerate every root-to-leaf path and sum it after the fact.

## Better insight

Carry the remaining sum and the current path as the DFS descends.

## Expert solution

```python
def path_sum(root, target_sum):
    result = []

    def dfs(node, path, remaining):
        if not node:
            return
        path.append(node.val)
        remaining -= node.val
        if not node.left and not node.right and remaining == 0:
            result.append(path.copy())
        else:
            dfs(node.left, path, remaining)
            dfs(node.right, path, remaining)
        path.pop()

    dfs(root, [], target_sum)
    return result
```

Recursively explore left and right children, subtract the node value from the target, and copy the current path only when a leaf completes the target.

**Complexity:** `O(n)` worst-case search with path-copy output cost and `O(h)` recursion space.
