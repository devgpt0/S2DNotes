# Focus300 065: LeetCode 440 - K-th Smallest in Lexicographical Order

**Source:** [LeetCode 440](https://leetcode.com/problems/k-th-smallest-in-lexicographical-order/)  
**Difficulty:** Hard  
**Pattern:** skip decimal-prefix subtrees

## Exact contract

List integers `1..n` in lexicographical string order and return the one-based
`k`th value, without constructing the full list.

## First principles

Integers form a decimal trie. Prefix `p` has children `p0..p9`. Count how many
valid integers lie between adjacent prefixes `p` and `p+1` by widening both
bounds one decimal level at a time.

If that subtree contains at most the remaining rank, skip it and move to the
next sibling. Otherwise descend to `p*10`, consuming the prefix itself.


## Classroom board: walk the tree once

```text
choose the root condition, then push the relevant subtree state down as
you recurse or iterate.
```



## Step-by-step transformation

1. Traverse the structure and keep the pointer, node, or subtree state that matters.
2. Rewire links or combine child results without losing the part of the structure you still need.
3. Carry the surviving state forward to the next node or subtree.
4. Return the rebuilt structure, node value, or accumulated traversal result.

These notes work by preserving the structure while changing just the links or the returned subtree results that lead to the final answer.


## Diagram: walk and reconnect pointers

```text

            original nodes
                |
                v
            read or split the structure
                |
                v
            reconnect links or combine child results
                |
                v
            rebuilt list / tree / value
```

The algorithm walks the structure, keeps only the needed pointers or subtree results, and returns the rebuilt output.

## Cases that decide correctness

- `k` is one-based.
- Prefix counts are clipped at `n+1` on every depth.
- Moving to a sibling does not consume that sibling yet.
- Descending consumes the current prefix as one lexicographical item.
- `n` need not end at a complete decimal-trie level.

## Brute force: sort all decimal strings

```python
def find_kth_number_brute(limit: int, rank: int) -> int:
    if not 1 <= rank <= limit:
        raise ValueError("rank must be between one and limit")
    ordered = sorted(range(1, limit + 1), key=str)
    return ordered[rank - 1]
```

This takes `O(n log n)` comparisons and `O(n)` storage.

## Better insight: lexicographical order is preorder traversal of a decimal trie

Prefix subtree sizes let the traversal skip thousands or millions of numbers
in one step instead of generating each integer.

## Expert solution: count and skip prefix subtrees

```python
def find_kth_number(limit: int, rank: int) -> int:
    if not 1 <= rank <= limit:
        raise ValueError("rank must be between one and limit")

    def subtree_size(prefix: int, next_prefix: int) -> int:
        count = 0
        while prefix <= limit:
            count += min(limit + 1, next_prefix) - prefix
            prefix *= 10
            next_prefix *= 10
        return count

    current = 1
    remaining = rank - 1
    while remaining:
        count = subtree_size(current, current + 1)
        if count <= remaining:
            current += 1
            remaining -= count
        else:
            current *= 10
            remaining -= 1
    return current
```

Each decision matches one preorder action: skip an entire subtree or visit its
root and descend.

**Complexity:** `O(log(n)^2)` time and `O(1)` space.
