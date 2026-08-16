# Focus300 235: LeetCode 143 - Reorder List

**Source:** [LeetCode 143](https://leetcode.com/problems/reorder-list/)  
**Difficulty:** Medium  
**Pattern:** split, reverse, and merge linked-list halves

## Exact contract

Reorder the list so the first node is followed by the last, then the second, then the second-last, and so on.

## First principles

The list can be decomposed into two halves, the second half reversed, and then woven together. The whole problem is pointer choreography, not value manipulation.


## Classroom board: split, reverse, and weave

```text
    1 -> 2 -> 3 -> 4

    split into 1 -> 2 and 3 -> 4, reverse the second half, then weave.
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

- A short list of length zero, one, or two is already in the correct shape.
- The middle node of an odd-length list stays in the front half.
- The second half must be reversed before merging.
- The final list must preserve all original nodes exactly once.

## Brute force

```python
def reorder_list_brute(head):
    nodes = []
    while head:
        nodes.append(head)
        head = head.next
    i, j = 0, len(nodes) - 1
    dummy = ListNode(0)
    tail = dummy
    while i <= j:
        tail.next = nodes[i]
        tail = tail.next
        if i != j:
            tail.next = nodes[j]
            tail = tail.next
        i += 1
        j -= 1
    tail.next = None
    return dummy.next
```

Copy the nodes into an array and rebuild the required order.

## Better insight

Find the middle, reverse the second half in place, and merge the two chains alternately.

## Expert solution

```python
def reorder_list(head):
    if not head or not head.next:
        return head
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    prev = None
    cur = slow
    while cur:
        nxt = cur.next
        cur.next = prev
        prev = cur
        cur = nxt
    first = head
    second = prev
    while second.next:
        tmp1 = first.next
        tmp2 = second.next
        first.next = second
        second.next = tmp1
        first = tmp1
        second = tmp2
    return head
```

Split the list at the midpoint, reverse the tail, and interleave one node from each half until the tail is exhausted.

**Complexity:** O(n) time and O(1) extra space.
