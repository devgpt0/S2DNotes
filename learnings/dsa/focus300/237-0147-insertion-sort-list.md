# Focus300 237: LeetCode 147 - Insertion Sort List

**Source:** [LeetCode 147](https://leetcode.com/problems/insertion-sort-list/)  
**Difficulty:** Medium  
**Pattern:** linked-list insertion sort

## Exact contract

Sort the linked list in ascending order using insertion-sort behavior.

## First principles

Each node belongs in the prefix that has already been sorted. Because linked lists make insertion cheap once the spot is known, the algorithm walks the sorted prefix to find the insertion point for each node.

## Cases that decide correctness

- An already sorted list should remain unchanged.
- The head may need to move when the smallest value appears late.
- Duplicates should remain adjacent in sorted order.
- The algorithm operates by pointer rewiring, not value swapping.

## Brute force

```python
def insertion_sort_list_brute(head):
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

Copy values into an array, sort them, and rewrite the list.

## Better insight

Insert each node into the growing sorted prefix as soon as it is read.

## Expert solution

```python
def insertion_sort_list(head):
    dummy = ListNode(0)
    while head:
        prev = dummy
        while prev.next and prev.next.val < head.val:
            prev = prev.next
        nxt = head.next
        head.next = prev.next
        prev.next = head
        head = nxt
    return dummy.next
```

Maintain a dummy head for the sorted portion, splice each new node into its position, and advance through the unsorted remainder.

**Complexity:** O(n^2) time and O(1) space.
