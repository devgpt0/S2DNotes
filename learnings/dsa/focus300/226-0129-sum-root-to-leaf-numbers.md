# Focus300 226: LeetCode 129 - Sum Root to Leaf Numbers

**Source:** [LeetCode 129](https://leetcode.com/problems/sum-root-to-leaf-numbers/)  
**Difficulty:** Medium  
**Pattern:** tree DFS with digit accumulation

## Exact contract

Interpret each root-to-leaf path as a decimal number and return the sum of all such numbers.

## First principles

A path value can be updated incrementally by multiplying the running number by ten and adding the current digit. Leaves are the only places where a complete number exists.

## Cases that decide correctness

- A single-node tree contributes that node's digit as the whole number.
- Leaf detection is required before adding to the total.
- The same prefix contributes to many distinct root-to-leaf numbers.
- Node values are digits, not arbitrary large integers.

## Brute force

```python
def sum_numbers_brute(root):
    paths = []

    def dfs(node, value):
        if not node:
            return
        value = value * 10 + node.val
        if not node.left and not node.right:
            paths.append(value)
        dfs(node.left, value)
        dfs(node.right, value)

    dfs(root, 0)
    return sum(paths)
```

Build each root-to-leaf string, convert it to an integer, and sum the integers afterward.

## Better insight

Carry the partial numeric value down the DFS so no path string is needed.

## Expert solution

```python
def sum_numbers(root):
    def dfs(node, value):
        if not node:
            return 0
        value = value * 10 + node.val
        if not node.left and not node.right:
            return value
        return dfs(node.left, value) + dfs(node.right, value)

    return dfs(root, 0)
```

Traverse recursively, update the running number at each node, and add it to the total only when a leaf is reached.

**Complexity:** O(n) time and O(h) recursion space.
