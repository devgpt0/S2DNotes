# Focus300 003: LeetCode 23 - Merge k Sorted Lists

**Source:** [LeetCode 23](https://leetcode.com/problems/merge-k-sorted-lists/)  
**Difficulty:** Hard  
**Pattern:** k-way merge with a min-heap

## Exact contract

Given `k` heads of individually sorted singly linked lists, return one sorted
list containing every node value. Inputs may include empty lists and duplicate
values.

## First principles

At any time, the smallest unmerged value must be one of the current list
heads. A min-heap keeps exactly those candidates. After removing one node, only
its successor becomes newly eligible.

Heap entries need a unique serial field because two nodes may have equal values
and linked-list nodes are not orderable.


## Classroom board: keep only the useful unfinished work

```text
a stack stores the part of the state that can still matter after the next step.
```



## Step-by-step transformation

1. Load the current candidates into a stack, queue, heap, or window.
2. Push or pop the structure while the current element keeps the invariant true.
3. Drop stale candidates and keep only the ones that can still affect the answer.
4. Read the final top, window score, or popped order as the output.

These problems transform the input by keeping just the active frontier of candidates instead of rescanning the whole array every time.


## Diagram: active frontier only

```text

            scan left to right
                |
                v
            keep active candidates
                |
                v
            pop stale work
                |
                v
            current best answer
```

These notes keep only the active frontier of useful candidates instead of rescanning the whole input.

## Cases that decide correctness

- The list of heads may itself be empty.
- Any individual head may be `None`.
- Equal values from different lists need a deterministic heap tie-breaker.
- The result tail must terminate after the final node.
- Relinking input nodes is allowed by the source contract.

## Brute force: collect, sort, and rebuild values

```python
from dataclasses import dataclass


@dataclass(slots=True)
class ListNode:
    val: int
    next: "ListNode | None" = None


def merge_k_lists_sort(lists: list[ListNode | None]) -> ListNode | None:
    values: list[int] = []
    for node in lists:
        while node is not None:
            values.append(node.val)
            node = node.next
    dummy = ListNode(0)
    tail = dummy
    for value in sorted(values):
        tail.next = ListNode(value)
        tail = tail.next
    return dummy.next
```

This is `O(N log N)` time and `O(N)` extra space.

## Better approach: merge lists into the result one at a time

```python
from dataclasses import dataclass


@dataclass(slots=True)
class ListNode:
    val: int
    next: "ListNode | None" = None


def merge_k_lists_sequential(lists: list[ListNode | None]) -> ListNode | None:
    def merge(first: ListNode | None, second: ListNode | None) -> ListNode | None:
        dummy = ListNode(0)
        tail = dummy
        while first is not None and second is not None:
            if first.val <= second.val:
                tail.next = first
                first = first.next
            else:
                tail.next = second
                second = second.next
            tail = tail.next
        tail.next = first if first is not None else second
        return dummy.next

    result: ListNode | None = None
    for head in lists:
        result = merge(result, head)
    return result
```

This uses constant auxiliary node space but can revisit early values `k` times,
for `O(kN)` worst-case time.

## Expert solution: heap of current heads

```python
from dataclasses import dataclass
import heapq
from itertools import count


@dataclass(slots=True)
class ListNode:
    val: int
    next: "ListNode | None" = None


def merge_k_lists(lists: list[ListNode | None]) -> ListNode | None:
    serials = count()
    heap: list[tuple[int, int, ListNode]] = []
    for node in lists:
        if node is not None:
            heapq.heappush(heap, (node.val, next(serials), node))

    dummy = ListNode(0)
    tail = dummy
    while heap:
        _, _, node = heapq.heappop(heap)
        successor = node.next
        tail.next = node
        tail = node
        if successor is not None:
            heapq.heappush(heap, (successor.val, next(serials), successor))
    tail.next = None
    return dummy.next
```

The heap contains one and only one eligible node from each nonempty remaining
list, so every extracted node is globally next.

**Complexity:** `O(N log k)` time and `O(k)` auxiliary space.
