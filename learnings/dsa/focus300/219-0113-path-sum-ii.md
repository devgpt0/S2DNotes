# Focus300 219: LeetCode 113 - Path Sum II

**Source:** [LeetCode 113](https://leetcode.com/problems/path-sum-ii/)  
**Difficulty:** Medium  
**Pattern:** root-to-leaf DFS with path tracking

## Exact contract

Return every root-to-leaf path whose node values add up to the target sum.

## First principles

The path sum is just a running total along one branch of the tree. A path is valid only when both the leaf condition and the sum condition are satisfied together.


## Classroom board: visit each region or node once

```text
mark what is already seen, expand to neighbors, and stop when the region
is fully explored.
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
