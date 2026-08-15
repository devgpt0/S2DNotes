# Focus300 202: LeetCode 86 - Partition List

**Source:** [LeetCode 86](https://leetcode.com/problems/partition-list/)  
**Difficulty:** Medium  
**Pattern:** stable linked-list partition

## Exact contract

Reorder the linked list so that nodes smaller than the pivot come before nodes greater than or equal to the pivot, while preserving the original relative order inside each group.

## First principles

This is a stable partition, not a sort. The simplest invariant is two separate chains: one for nodes that belong left of the pivot and one for nodes that belong right of it.

## Cases that decide correctness

- All nodes can belong to the same side of the pivot.
- The original node order inside each partition must be preserved.
- The pivot value itself belongs to the right partition.
- The original list must be reconnected cleanly at the end.

## Brute force

```python
def partition_brute(head, x):
    before = []
    after = []
    while head:
        (before if head.val < x else after).append(head.val)
        head = head.next
    values = before + after
    dummy = ListNode(0)
    tail = dummy
    for value in values:
        tail.next = ListNode(value)
        tail = tail.next
    return dummy.next
```

Copy nodes into two arrays and rebuild the list from scratch.

## Better insight

Maintain two temporary linked lists and stitch them together after one pass.

## Expert solution

```python
def partition(head, x):
    small_dummy = ListNode(0)
    large_dummy = ListNode(0)
    small = small_dummy
    large = large_dummy
    while head:
        next_node = head.next
        head.next = None
        if head.val < x:
            small.next = head
            small = small.next
        else:
            large.next = head
            large = large.next
        head = next_node
    small.next = large_dummy.next
    return small_dummy.next
```

Detach nodes one by one, append them to the correct side, and then connect the smaller side to the larger side.

**Complexity:** O(n) time and O(1) extra list-node space.
