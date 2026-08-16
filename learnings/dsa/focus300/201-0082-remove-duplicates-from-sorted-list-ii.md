# Focus300 201: LeetCode 82 - Remove Duplicates from Sorted List II

**Source:** [LeetCode 82](https://leetcode.com/problems/remove-duplicates-from-sorted-list-ii/)  
**Difficulty:** Medium  
**Pattern:** linked-list duplicate skipping

## Exact contract

Remove every value that appears more than once from a sorted linked list, leaving only values that occur exactly once.

## First principles

Because the list is sorted, duplicates always form one contiguous run. A dummy head and a trailing pointer make it easy to splice out an entire run once the run's length is known.


## Classroom board: move pointers carefully

```text
a linked-list problem usually changes only `next` links, so keep track of
the node before, the node after, and any middle segment you need to reuse.
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

- The first run may need to be removed entirely.
- A list with all unique values should remain unchanged.
- A run can end at the tail of the list.
- Multiple duplicate blocks may appear back to back.

## Brute force

```python
def delete_duplicates_brute(head):
    dummy = ListNode(0, head)
    prev = dummy
    current = head
    while current:
        duplicate = False
        while current.next and current.val == current.next.val:
            duplicate = True
            current = current.next
        if duplicate:
            prev.next = current.next
        else:
            prev = prev.next
        current = current.next
    return dummy.next
```

Count each run, then rebuild a fresh list containing only singletons.

## Better insight

Use one pass with a predecessor pointer and skip any duplicate block in one splice.

## Expert solution

```python
def delete_duplicates(head):
    dummy = ListNode(0, head)
    prev = dummy
    current = head
    while current:
        while current.next and current.val == current.next.val:
            current = current.next
        if prev.next == current:
            prev = prev.next
        else:
            prev.next = current.next
        current = current.next
    return dummy.next
```

Walk the list with two pointers, detect duplicate runs, and reconnect the predecessor directly to the next unique node.

**Complexity:** O(n) time and O(1) extra space.
