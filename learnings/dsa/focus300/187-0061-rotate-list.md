# Focus300 187: LeetCode 61 - Rotate List

**Source:** [LeetCode 61](https://leetcode.com/problems/rotate-list/)  
**Difficulty:** Medium  
**Pattern:** linked-list cycle and modular split

## Exact contract

Rotate a singly linked list right by nonnegative `k`: the final node moves to
the front once per rotation. Return the new head. The list has at most 500
nodes and `k <= 2_000_000_000`.

## First principles

Rotation depends only on `k mod length`. Connecting the tail to the head makes
the list circular; the new tail is `length - k mod length - 1` steps from the
old head. Breaking after it produces the rotated list.


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

- Empty and one-node lists are unchanged.
- A multiple of the length returns the original head.
- The old tail becomes internal after the temporary cycle.
- The cycle must be broken exactly once.
- Cyclic or oversized input violates the source contract.

## Brute force: move the tail to the front k times

```python
class ListNode:
    def __init__(self, value: int, next_node: "ListNode | None" = None) -> None:
        self.value = value
        self.next = next_node


def rotate_list_brute(head: ListNode | None, rotations: int) -> ListNode | None:
    if head is not None and type(head) is not ListNode:
        raise TypeError("head must be a ListNode or None")
    if type(rotations) is not int:
        raise TypeError("rotations must be an integer")
    if not 0 <= rotations <= 2_000_000_000:
        raise ValueError("rotations must be between 0 and 2000000000")
    seen: set[int] = set()
    node = head
    length = 0
    while node is not None:
        if id(node) in seen:
            raise ValueError("input list must not contain a cycle")
        if type(node.value) is not int:
            raise TypeError("node values must be integers")
        seen.add(id(node))
        length += 1
        if length > 500:
            raise ValueError("input list may contain at most 500 nodes")
        node = node.next

    for _ in range(rotations):
        if head is None or head.next is None:
            return head
        new_tail = head
        while new_tail.next is not None and new_tail.next.next is not None:
            new_tail = new_tail.next
        new_head = new_tail.next
        new_tail.next = None
        if new_head is None:
            raise RuntimeError("a multi-node list must have a tail")
        new_head.next = head
        head = new_head
    return head
```

This takes `O(k * n)` time and `O(n)` validation space.

## Better approach: copy values through modular indices

An array of node references can rotate in `O(n)` time and `O(n)` space. The
cycle method finds the same split with constant algorithmic storage.

## Expert solution: close the cycle, then break at the new tail

```python
class ListNode:
    def __init__(self, value: int, next_node: "ListNode | None" = None) -> None:
        self.value = value
        self.next = next_node


def rotate_list(head: ListNode | None, rotations: int) -> ListNode | None:
    if head is not None and type(head) is not ListNode:
        raise TypeError("head must be a ListNode or None")
    if type(rotations) is not int:
        raise TypeError("rotations must be an integer")
    if not 0 <= rotations <= 2_000_000_000:
        raise ValueError("rotations must be between 0 and 2000000000")
    if head is None:
        return None

    seen: set[int] = set()
    tail = head
    length = 0
    while True:
        if id(tail) in seen:
            raise ValueError("input list must not contain a cycle")
        if type(tail.value) is not int:
            raise TypeError("node values must be integers")
        seen.add(id(tail))
        length += 1
        if length > 500:
            raise ValueError("input list may contain at most 500 nodes")
        if tail.next is None:
            break
        tail = tail.next

    rotations %= length
    if rotations == 0:
        return head
    tail.next = head
    new_tail = head
    for _ in range(length - rotations - 1):
        if new_tail.next is None:
            raise RuntimeError("temporary cycle ended unexpectedly")
        new_tail = new_tail.next
    new_head = new_tail.next
    new_tail.next = None
    return new_head
```

The temporary cycle preserves list order while allowing one modular cut. Its
successor is precisely the new head.

**Complexity:** `O(n)` time and `O(n)` validation space; the rotation itself
uses `O(1)` space.
