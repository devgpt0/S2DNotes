# Focus300 206: LeetCode 92 - Reverse Linked List II

**Source:** [LeetCode 92](https://leetcode.com/problems/reverse-linked-list-ii/)  
**Difficulty:** Medium  
**Pattern:** sublist pointer reversal

## Exact contract

Reverse the linked-list segment between the given positions, leaving the rest of the list in place.

## First principles

The safest approach is to walk to the node just before the segment, reverse only the targeted slice, and then reconnect both boundaries. The operation is local even though the list is global.


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

- A segment of length one should remain unchanged.
- The reversed window may begin at the head.
- The reversed window may end at the tail.
- The rest of the list must preserve its original order.

## Brute force

```python
def reverse_between_brute(head, left, right):
    values = []
    node = head
    while node:
        values.append(node.val)
        node = node.next
    values[left - 1 : right] = reversed(values[left - 1 : right])
    dummy = ListNode(0)
    tail = dummy
    for value in values:
        tail.next = ListNode(value)
        tail = tail.next
    return dummy.next
```

Copy the values in the segment, reverse them, and write them back.

## Better insight

Reverse pointers in place inside the window and preserve the two outer joins.

## Expert solution

```python
def reverse_between(head, left, right):
    dummy = ListNode(0, head)
    prev = dummy
    for _ in range(left - 1):
        prev = prev.next
    current = prev.next
    for _ in range(right - left):
        nxt = current.next
        current.next = nxt.next
        nxt.next = prev.next
        prev.next = nxt
    return dummy.next
```

Use a predecessor pointer, perform head insertion inside the target window, and reconnect the prefix and suffix after the reversal finishes.

**Complexity:** O(n) time and O(1) space.
