# Focus300 209: LeetCode 96 - Unique Binary Search Trees

**Source:** [LeetCode 96](https://leetcode.com/problems/unique-binary-search-trees/)  
**Difficulty:** Medium  
**Pattern:** Catalan dynamic programming

## Exact contract

Count how many structurally unique BSTs can be built from `1` through `n`.

## First principles

Every root choice splits the tree into independent left and right subtree counts. The total is the sum of all product combinations across possible roots.

## Cases that decide correctness

- `n = 0` yields one empty tree by convention in the recurrence.
- The same left/right count pair can appear from many root choices.
- Symmetry helps sanity-check the recurrence, but not the final arithmetic.
- The answer grows according to the Catalan sequence.

## Brute force

```python
def num_trees_brute(n):
    dp = [0] * (n + 1)
    dp[0] = 1
    for nodes in range(1, n + 1):
        for root in range(1, nodes + 1):
            dp[nodes] += dp[root - 1] * dp[nodes - root]
    return dp[n]
```

Enumerate every BST structure and count the valid ones.

## Better insight

Use a DP table where each entry sums left-subtree count times right-subtree count over all root splits.

## Expert solution

```python
def num_trees(n):
    dp = [0] * (n + 1)
    dp[0] = dp[1] = 1
    for nodes in range(2, n + 1):
        for root in range(1, nodes + 1):
            dp[nodes] += dp[root - 1] * dp[nodes - root]
    return dp[n]
```

Fill the Catalan recurrence bottom-up from small subtree sizes to the full range.

**Complexity:** O(n^2) time and O(n) space.
