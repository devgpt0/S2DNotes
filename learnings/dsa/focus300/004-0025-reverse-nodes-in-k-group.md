# Focus300 004: LeetCode 25 - Reverse Nodes in k-Group

**Source:** [LeetCode 25](https://leetcode.com/problems/reverse-nodes-in-k-group/)  
**Difficulty:** Hard  
**Pattern:** bounded linked-list reversal with a sentinel

## Exact contract

Reverse a singly linked list in consecutive groups of exactly `k` nodes. Leave
the final group unchanged when it has fewer than `k` nodes. Change node links,
not node values, and return the new head.

## First principles

Before reversing a group, locate its `k`th node. If it does not exist, the work
is complete. Otherwise remember the node after the group, reverse links until
that boundary, connect the previous group to the new head, and advance the
group predecessor to the old head.

A dummy node removes the special case for reversing the original head group.

## Cases that decide correctness

- `k=1` leaves every link unchanged.
- A list shorter than `k` is returned unchanged.
- A final incomplete group is never partially reversed.
- The old group head becomes its tail and must connect to the next group.
- The source guarantees positive `k`; reusable code should reject nonpositive values.

## Brute force: copy values through chunk reversal

```python
from dataclasses import dataclass


@dataclass(slots=True)
class ListNode:
    val: int
    next: "ListNode | None" = None


def reverse_k_group_copy(head: ListNode | None, group_size: int) -> ListNode | None:
    if group_size <= 0:
        raise ValueError("group_size must be positive")
    values: list[int] = []
    node = head
    while node is not None:
        values.append(node.val)
        node = node.next
    for start in range(0, len(values) - group_size + 1, group_size):
        values[start : start + group_size] = reversed(
            values[start : start + group_size]
        )
    dummy = ListNode(0)
    tail = dummy
    for value in values:
        tail.next = ListNode(value)
        tail = tail.next
    return dummy.next
```

This is `O(n)` time and `O(n)` extra space, and it does not preserve node
identity.

## Better approach: recursive group reversal

```python
from dataclasses import dataclass


@dataclass(slots=True)
class ListNode:
    val: int
    next: "ListNode | None" = None


def reverse_k_group_recursive(
    head: ListNode | None, group_size: int
) -> ListNode | None:
    if group_size <= 0:
        raise ValueError("group_size must be positive")
    if head is None:
        return None
    boundary: ListNode | None = head
    for _ in range(group_size):
        if boundary is None:
            return head
        boundary = boundary.next

    suffix = reverse_k_group_recursive(boundary, group_size)
    current: ListNode | None = head
    for _ in range(group_size):
        if current is None:
            raise RuntimeError("validated group ended early")
        next_node = current.next
        current.next = suffix
        suffix = current
        current = next_node
    return suffix
```

This relinks nodes in `O(n)` time but uses `O(n/k)` call-stack space.

## Expert solution: iterative constant-space relinking

```python
from dataclasses import dataclass


@dataclass(slots=True)
class ListNode:
    val: int
    next: "ListNode | None" = None


def reverse_k_group(head: ListNode | None, group_size: int) -> ListNode | None:
    if group_size <= 0:
        raise ValueError("group_size must be positive")
    dummy = ListNode(0, head)
    group_previous = dummy

    while True:
        kth: ListNode | None = group_previous
        for _ in range(group_size):
            kth = kth.next
            if kth is None:
                return dummy.next
        group_next = kth.next
        old_group_head = group_previous.next
        if old_group_head is None:
            raise RuntimeError("validated group has no head")

        previous = group_next
        current: ListNode | None = old_group_head
        while current is not group_next:
            if current is None:
                raise RuntimeError("validated group ended early")
            next_node = current.next
            current.next = previous
            previous = current
            current = next_node

        group_previous.next = kth
        group_previous = old_group_head
```

Every iteration reverses one verified complete group and leaves the first
unverified suffix untouched.

**Complexity:** `O(n)` time and `O(1)` auxiliary space.
