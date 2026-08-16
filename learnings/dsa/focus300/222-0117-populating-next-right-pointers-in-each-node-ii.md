# Focus300 222: LeetCode 117 - Populating Next Right Pointers in Each Node II

**Source:** [LeetCode 117](https://leetcode.com/problems/populating-next-right-pointers-in-each-node-ii/)  
**Difficulty:** Medium  
**Pattern:** level-by-level next-pointer wiring

## Exact contract

Populate each node's next pointer so nodes at the same depth form a linked list.

## First principles

Nodes on the same level are naturally processed together. Once a level is known, linking its children only requires keeping track of the previous child encountered on the next level.


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

- The last node of each level points to `None`.
- A perfect tree and a general tree differ only in how children appear, not in the level-linking idea.
- The root has no next neighbor.
- Missing children must not break the chain-building logic.

## Brute force

```python
from collections import deque

def connect_brute(root):
    if not root:
        return root
    queue = deque([root])
    while queue:
        prev = None
        for _ in range(len(queue)):
            node = queue.popleft()
            if prev:
                prev.next = node
            prev = node
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        if prev:
            prev.next = None
    return root
```

Gather every level into arrays and then assign next pointers afterward.

## Better insight

Walk one level at a time and thread the next level while traversing the current one.

## Expert solution

```python
def connect(root):
    if not root:
        return root
    head = root
    while head:
        dummy = Node(0)
        tail = dummy
        cur = head
        while cur:
            for child in (cur.left, cur.right):
                if child:
                    tail.next = child
                    tail = tail.next
            cur = cur.next
        head = dummy.next
    return root
```

Use BFS or a dummy-head approach to connect nodes horizontally one layer at a time.

**Complexity:** O(n) time and O(1) extra space for the constant-space variant, or O(n) queue space with BFS.
