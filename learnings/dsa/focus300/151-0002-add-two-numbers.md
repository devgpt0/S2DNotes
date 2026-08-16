# Focus300 151: LeetCode 2 - Add Two Numbers

**Source:** [LeetCode 2](https://leetcode.com/problems/add-two-numbers/)  
**Difficulty:** Medium  
**Pattern:** elementary addition with a carry over linked digits

## Exact contract

Two nonempty singly linked lists store nonnegative integers in reverse digit
order: each node is one decimal digit, and the head is the ones place. Neither
number has a leading zero except the number zero itself. Return a new reverse-
order list containing their sum without mutating either input.

## First principles

At each place, add the two available digits and the incoming carry. The output
digit is `total % 10`, and the next carry is `total // 10`. Continue while an
input digit or carry remains. This is the same invariant as written decimal
addition, with the list already ordered from least to most significant.


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

- The lists may have different lengths.
- A final carry needs a new node.
- `0 + 0` returns one zero node, not an empty list.
- Input nodes must not be reused or modified.
- Each source list contains at most 100 valid digit nodes and no cycle.

## Brute force: convert both lists to integers

```python
from dataclasses import dataclass


@dataclass(slots=True)
class ListNode:
    value: int = 0
    next: "ListNode | None" = None


def add_two_numbers_brute(first: ListNode, second: ListNode) -> ListNode:
    def to_integer(head: ListNode) -> int:
        current: ListNode | None = head
        seen: set[int] = set()
        digits: list[int] = []
        place = 1
        value = 0
        while current is not None:
            if type(current) is not ListNode or id(current) in seen:
                raise ValueError("each input must be an acyclic ListNode chain")
            seen.add(id(current))
            if type(current.value) is not int or not 0 <= current.value <= 9:
                raise ValueError("every node value must be a decimal digit")
            digits.append(current.value)
            value += current.value * place
            place *= 10
            if len(digits) > 100:
                raise ValueError("each input may contain at most 100 nodes")
            current = current.next
        if not digits or len(digits) > 1 and digits[-1] == 0:
            raise ValueError("each input must encode a canonical nonempty number")
        return value

    total = to_integer(first) + to_integer(second)
    head = ListNode(total % 10)
    tail = head
    total //= 10
    while total:
        tail.next = ListNode(total % 10)
        tail = tail.next
        total //= 10
    return head
```

This relies on an arbitrary-precision integer and materializes each full number.

## Better insight: the linked representation is already in processing order

No reversal or numeric conversion is necessary. Advance both pointers together,
treat a missing digit as zero, and preserve only the one-digit carry.

## Expert solution: one-pass digit addition

```python
from dataclasses import dataclass


@dataclass(slots=True)
class ListNode:
    value: int = 0
    next: "ListNode | None" = None


def add_two_numbers(first: ListNode, second: ListNode) -> ListNode:
    def validate(head: ListNode) -> None:
        current: ListNode | None = head
        seen: set[int] = set()
        digits: list[int] = []
        while current is not None:
            if type(current) is not ListNode or id(current) in seen:
                raise ValueError("each input must be an acyclic ListNode chain")
            seen.add(id(current))
            if type(current.value) is not int or not 0 <= current.value <= 9:
                raise ValueError("every node value must be a decimal digit")
            digits.append(current.value)
            if len(digits) > 100:
                raise ValueError("each input may contain at most 100 nodes")
            current = current.next
        if not digits or len(digits) > 1 and digits[-1] == 0:
            raise ValueError("each input must encode a canonical nonempty number")

    validate(first)
    validate(second)

    dummy = ListNode()
    tail = dummy
    first_node: ListNode | None = first
    second_node: ListNode | None = second
    carry = 0
    while first_node is not None or second_node is not None or carry:
        total = carry
        if first_node is not None:
            total += first_node.value
            first_node = first_node.next
        if second_node is not None:
            total += second_node.value
            second_node = second_node.next
        carry, digit = divmod(total, 10)
        tail.next = ListNode(digit)
        tail = tail.next
    if dummy.next is None:
        raise RuntimeError("validated inputs always produce a digit")
    return dummy.next
```

Before each iteration, `carry` is exactly the amount transferred from the
already processed lower places, so the emitted prefix is final.

**Complexity:** `O(max(m, n))` time and `O(max(m, n))` output space, with
`O(1)` auxiliary arithmetic state.
