# Focus300 165: LeetCode 24 - Swap Nodes in Pairs

**Source:** [LeetCode 24](https://leetcode.com/problems/swap-nodes-in-pairs/)  
**Difficulty:** Medium  
**Pattern:** local linked-list rewiring with a dummy predecessor

## Exact contract

Swap every adjacent pair of nodes in a singly linked list and return the new
head. The final node of an odd-length list stays in place. Node values may not
be swapped; the existing nodes themselves must be relinked.

## First principles

For predecessor `p` and pair `first -> second -> following`, the only required
updates are `p.next = second`, `second.next = first`, and
`first.next = following`. The first node then becomes the predecessor for the
next pair. A dummy node supplies `p` for the original head pair.


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
- An odd tail remains last.
- Existing node identities must be preserved.
- Saving `following` before rewiring prevents losing the suffix.
- The input must be acyclic and contain at most 100 valid nodes.

## Brute force: collect nodes, swap array entries, then relink

```python
from dataclasses import dataclass


@dataclass(slots=True)
class ListNode:
    value: int = 0
    next: "ListNode | None" = None


def swap_pairs_brute(head: ListNode | None) -> ListNode | None:
    nodes: list[ListNode] = []
    seen: set[int] = set()
    current = head
    while current is not None:
        if type(current) is not ListNode or id(current) in seen:
            raise ValueError("head must be an acyclic ListNode chain")
        seen.add(id(current))
        if type(current.value) is not int or not 0 <= current.value <= 100:
            raise ValueError("node values must be integers from 0 through 100")
        nodes.append(current)
        if len(nodes) > 100:
            raise ValueError("the list may contain at most 100 nodes")
        current = current.next

    for index in range(0, len(nodes) - 1, 2):
        nodes[index], nodes[index + 1] = nodes[index + 1], nodes[index]
    for index, node in enumerate(nodes):
        node.next = nodes[index + 1] if index + 1 < len(nodes) else None
    return nodes[0] if nodes else None
```

This preserves node identities but uses `O(length)` auxiliary storage.

## Better insight: one pair is a constant-size pointer transformation

Keep a predecessor to the next unswapped pair. After rewiring, the old first
node is exactly the predecessor needed for the following pair.

## Expert solution: iterative in-place pair rewiring

```python
from dataclasses import dataclass


@dataclass(slots=True)
class ListNode:
    value: int = 0
    next: "ListNode | None" = None


def swap_pairs(head: ListNode | None) -> ListNode | None:
    seen: set[int] = set()
    current = head
    length = 0
    while current is not None:
        if type(current) is not ListNode or id(current) in seen:
            raise ValueError("head must be an acyclic ListNode chain")
        seen.add(id(current))
        if type(current.value) is not int or not 0 <= current.value <= 100:
            raise ValueError("node values must be integers from 0 through 100")
        length += 1
        if length > 100:
            raise ValueError("the list may contain at most 100 nodes")
        current = current.next

    dummy = ListNode(next=head)
    predecessor = dummy
    while predecessor.next is not None and predecessor.next.next is not None:
        first = predecessor.next
        second = first.next
        if second is None:
            raise RuntimeError("loop condition guarantees a complete pair")
        following = second.next
        predecessor.next = second
        second.next = first
        first.next = following
        predecessor = first
    return dummy.next
```

After each iteration, the processed prefix is correctly swapped and
`predecessor.next` is the first unprocessed node.

**Complexity:** `O(length)` time and `O(1)` pointer space after validation.
