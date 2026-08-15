# Focus300 206: LeetCode 92 - Reverse Linked List II

**Source:** [LeetCode 92](https://leetcode.com/problems/reverse-linked-list-ii/)  
**Difficulty:** Medium  
**Pattern:** sublist pointer reversal

## Exact contract

Reverse the linked-list segment between the given positions, leaving the rest of the list in place.

## First principles

The safest approach is to walk to the node just before the segment, reverse only the targeted slice, and then reconnect both boundaries. The operation is local even though the list is global.

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
