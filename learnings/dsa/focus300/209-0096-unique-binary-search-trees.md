# Focus300 209: LeetCode 96 - Unique Binary Search Trees

**Source:** [LeetCode 96](https://leetcode.com/problems/unique-binary-search-trees/)  
**Difficulty:** Medium  
**Pattern:** Catalan dynamic programming

## Exact contract

Count how many structurally unique BSTs can be built from `1` through `n`.

## First principles

Every root choice splits the tree into independent left and right subtree counts. The total is the sum of all product combinations across possible roots.


## Classroom board: store the repeated state once

```text
brute force recomputes the same subproblem many times.
dp keeps the smallest useful state and extends it one step at a time.
```



## Step-by-step transformation

1. Turn the input into subproblems, prefixes, or states that can be reused.
2. Fill the base cases first so later states have something correct to build on.
3. Update each new state from earlier states while keeping the recurrence valid.
4. Read the answer from the final table entry or the best state collected at the end.

Dynamic-programming style notes transform the input by compressing many repeated choices into a small set of reusable states.


## Diagram: state table to answer

```text

            input
                |
                v
            base states
                |
                v
            reuse smaller states
                |
                v
            final dp answer
```

These notes compress repeated choices into reusable states, then read the answer from the last state that matters.

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
