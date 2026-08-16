# Focus300 238: LeetCode 148 - Sort List

**Source:** [LeetCode 148](https://leetcode.com/problems/sort-list/)  
**Difficulty:** Medium  
**Pattern:** linked-list merge sort

## Exact contract

Sort the linked list in ascending order with better-than-quadratic behavior.

## First principles

Merge sort matches linked lists well because splitting by midpoints and merging by pointer comparison are both natural. The divide step shrinks the problem and the merge step preserves stability.


## Classroom board: relink nodes instead of swapping values

```text
    4 -> 2 -> 1 -> 3

    merge or insert nodes into the correct place while keeping the chain.
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

- An empty list or one-node list is already sorted.
- The split point must preserve both halves correctly.
- The merge step must not lose tail nodes.
- The final ordering should remain stable for equal values.

## Brute force

```python
def sort_list_brute(head):
    values = []
    while head:
        values.append(head.val)
        head = head.next
    values.sort()
    dummy = ListNode(0)
    tail = dummy
    for value in values:
        tail.next = ListNode(value)
        tail = tail.next
    return dummy.next
```

Use insertion sort or value copying, which degrades on long inputs.

## Better insight

Split recursively, sort both halves, and merge the two sorted chains.

## Expert solution

```python
def sort_list(head):
    if not head or not head.next:
        return head

    def split(node):
        slow = fast = node
        prev = None
        while fast and fast.next:
            prev = slow
            slow = slow.next
            fast = fast.next.next
        prev.next = None
        return node, slow

    def merge(a, b):
        dummy = tail = ListNode(0)
        while a and b:
            if a.val < b.val:
                tail.next, a = a, a.next
            else:
                tail.next, b = b, b.next
            tail = tail.next
        tail.next = a or b
        return dummy.next

    left, right = split(head)
    left = sort_list(left)
    right = sort_list(right)
    return merge(left, right)
```

Find the midpoint with slow and fast pointers, sort each half recursively, and merge them into one sorted list.

**Complexity:** O(n log n) time and O(log n) recursion space.
