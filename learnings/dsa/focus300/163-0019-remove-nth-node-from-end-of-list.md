# Focus300 163: LeetCode 19 - Remove Nth Node From End of List

**Source:** [LeetCode 19](https://leetcode.com/problems/remove-nth-node-from-end-of-list/)  
**Difficulty:** Medium  
**Pattern:** fixed-gap linked-list pointers

## Exact contract

Given a nonempty singly linked list and a valid one-based position `n` from its
end, unlink that node and return the possibly new head. Node values are not the
target; position is.

## First principles

If a fast pointer is `n` nodes ahead of a slow pointer, then when fast reaches
the end, slow is immediately before the node to remove. A dummy node makes
removing the original head follow the same pointer update as every other case.

## Cases that decide correctness

- Removing position equal to list length removes the head.
- Removing position one removes the tail.
- A one-node list returns `None`.
- The list must be acyclic and contain at most 30 source-valid nodes.
- Only one `next` link needs to change after locating the predecessor.

## Brute force: store every node before unlinking

```python
from dataclasses import dataclass


@dataclass(slots=True)
class ListNode:
    value: int = 0
    next: "ListNode | None" = None


def remove_from_end_brute(head: ListNode, position: int) -> ListNode | None:
    nodes: list[ListNode] = []
    seen: set[int] = set()
    current: ListNode | None = head
    while current is not None:
        if type(current) is not ListNode or id(current) in seen:
            raise ValueError("head must be an acyclic ListNode chain")
        seen.add(id(current))
        if type(current.value) is not int or not 0 <= current.value <= 100:
            raise ValueError("node values must be integers from 0 through 100")
        nodes.append(current)
        if len(nodes) > 30:
            raise ValueError("the list may contain at most 30 nodes")
        current = current.next
    if not nodes:
        raise ValueError("the source list must be nonempty")
    if type(position) is not int or not 1 <= position <= len(nodes):
        raise ValueError("position must identify an existing node from the end")

    removed_index = len(nodes) - position
    if removed_index == 0:
        return head.next
    nodes[removed_index - 1].next = nodes[removed_index].next
    return head
```

The node array makes indexing easy but consumes `O(length)` auxiliary space.

## Better insight: encode the from-end position as a pointer gap

Advance fast by `n` nodes from a dummy head, then move fast and slow together.
The maintained gap converts an unknown length into a one-pass predecessor.

## Expert solution: dummy node and two pointers

```python
from dataclasses import dataclass


@dataclass(slots=True)
class ListNode:
    value: int = 0
    next: "ListNode | None" = None


def remove_from_end(head: ListNode, position: int) -> ListNode | None:
    seen: set[int] = set()
    current: ListNode | None = head
    length = 0
    while current is not None:
        if type(current) is not ListNode or id(current) in seen:
            raise ValueError("head must be an acyclic ListNode chain")
        seen.add(id(current))
        if type(current.value) is not int or not 0 <= current.value <= 100:
            raise ValueError("node values must be integers from 0 through 100")
        length += 1
        if length > 30:
            raise ValueError("the list may contain at most 30 nodes")
        current = current.next
    if length == 0:
        raise ValueError("the source list must be nonempty")
    if type(position) is not int or not 1 <= position <= length:
        raise ValueError("position must identify an existing node from the end")

    dummy = ListNode(next=head)
    fast: ListNode | None = dummy
    for _ in range(position):
        if fast is None:
            raise RuntimeError("validated position keeps fast in range")
        fast = fast.next
    slow = dummy
    while fast is not None and fast.next is not None:
        fast = fast.next
        if slow.next is None:
            raise RuntimeError("validated list keeps slow in range")
        slow = slow.next
    if slow.next is None:
        raise RuntimeError("validated position identifies a node")
    slow.next = slow.next.next
    return dummy.next
```

When the loop stops, the `position`-node gap places `slow.next` exactly at the
requested node, including the head-removal case.

**Complexity:** `O(length)` time and `O(1)` pointer space after validation.
