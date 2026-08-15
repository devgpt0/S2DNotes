# Focus300 218: LeetCode 109 - Convert Sorted List to Binary Search Tree

**Source:** [LeetCode 109](https://leetcode.com/problems/convert-sorted-list-to-binary-search-tree/)  
**Difficulty:** Medium  
**Pattern:** balanced BST construction from sorted input

## Exact contract

Build a height-balanced BST from the sorted linked list.

## First principles

The sorted order implies that the middle element should become the root of each subproblem. Splitting around the middle preserves balance and ordering simultaneously.

## Cases that decide correctness

- A one-node list becomes a one-node tree.
- The middle selection should keep the tree balanced.
- The list traversal order must be preserved as inorder order.
- A slow/fast split or array conversion can both serve as the midpoint mechanism.

## Brute force

```python
def sorted_list_to_bst_brute(head):
    values = []
    while head:
        values.append(head.val)
        head = head.next

    def build(lo, hi):
        if lo > hi:
            return None
        mid = (lo + hi) // 2
        root = TreeNode(values[mid])
        root.left = build(lo, mid - 1)
        root.right = build(mid + 1, hi)
        return root

    return build(0, len(values) - 1)
```

Insert list nodes into a BST one by one, which can skew the tree.

## Better insight

Choose the middle as the root recursively so each subtree stays balanced.

## Expert solution

```python
def sorted_list_to_bst(head):
    def find_mid(start):
        slow = fast = start
        prev = None
        while fast and fast.next:
            prev = slow
            slow = slow.next
            fast = fast.next.next
        if prev:
            prev.next = None
        return slow

    if not head:
        return None
    if not head.next:
        return TreeNode(head.val)
    mid = find_mid(head)
    root = TreeNode(mid.val)
    if head != mid:
        root.left = sorted_list_to_bst(head)
    root.right = sorted_list_to_bst(mid.next)
    return root
```

Find the midpoint, make it the subtree root, and recurse on the left and right halves.

**Complexity:** O(n log n) with list splitting, or O(n) with an inorder-driven build strategy.
