# Focus300 282: LeetCode 237 - Delete Node in a Linked List

**Source:** [LeetCode 237](https://leetcode.com/problems/delete-node-in-a-linked-list/)  
**Difficulty:** Easy  
**Pattern:** in-place node overwrite

## Exact contract

Delete the given node from a singly linked list when only that node is provided.

## First principles

Because the predecessor is unavailable, the trick is to copy the next node's value into the current node and bypass the next node instead. The node identity stays, but its contents and next pointer change.


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

- The node to delete is never the tail under the usual contract.
- Only one node needs to be physically removed.
- The list head does not need to move.
- The visible value sequence must match the list with the node removed.

## Brute force

```python
def delete_node_brute(node):
    node.val = node.next.val
    node.next = node.next.next
```

Search from the head for the predecessor, then unlink the target.

## Better insight

Overwrite the current node with its successor and skip the successor node.

## Expert solution

```python
def delete_node(node):
    node.val = node.next.val
    node.next = node.next.next
```

Copy the next node's value into the current node and redirect the current node's next pointer to the successor of the successor.

**Complexity:** O(1) time and O(1) space.
