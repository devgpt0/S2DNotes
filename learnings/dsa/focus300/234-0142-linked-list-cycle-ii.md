# Focus300 234: LeetCode 142 - Linked List Cycle II

**Source:** [LeetCode 142](https://leetcode.com/problems/linked-list-cycle-ii/)  
**Difficulty:** Medium  
**Pattern:** Floyd cycle detection and entry finding

## Exact contract

Return the node where the cycle begins, or null if the list has no cycle.

## First principles

Fast and slow pointers meet only if a cycle exists. Once they meet, the distance algebra of the pointers identifies the cycle entry.


## Classroom board: see the repeated work once

```text
brute force tries every choice.
the optimized solution keeps only the state that must survive to the
next step.
```



## Step-by-step transformation

1. Read the input and identify the smallest state that still determines the answer.
2. Process one element, node, or row at a time while preserving that state.
3. Discard work that can no longer change the result.
4. Convert the surviving state into the output the problem requests.

The examples and code below show this transformation on the specific problem instance.


## Diagram: input to output

```text

        input
            |
            v
        core invariant
            |
            v
        process one step at a time
            |
            v
        output
```

The note shows the main idea, the repeated work, and the small state that turns the input into the output.

## Cases that decide correctness

- A single-node self-loop is still a cycle.
- An acyclic list should return null.
- The cycle entry may be the head itself.
- The meeting point is not usually the entry point.

## Brute force

```python
def detect_cycle_brute(head):
    seen = set()
    while head:
        if head in seen:
            return head
        seen.add(head)
        head = head.next
    return None
```

Store every visited node in a set until a repeat appears.

## Better insight

Use tortoise-and-hare pointers to detect the cycle with constant extra memory.

## Expert solution

```python
def detect_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            slow = head
            while slow != fast:
                slow = slow.next
                fast = fast.next
            return slow
    return None
```

Find the meeting point with two speeds, reset one pointer to the head, and walk both at one step per move until they meet again at the entry.

**Complexity:** O(n) time and O(1) space.
