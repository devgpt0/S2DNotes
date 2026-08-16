# Focus300 232: LeetCode 138 - Copy List with Random Pointer

**Source:** [LeetCode 138](https://leetcode.com/problems/copy-list-with-random-pointer/)  
**Difficulty:** Medium  
**Pattern:** linked-list deep copy with arbitrary references

## Exact contract

Deep-copy a linked list whose nodes include both next pointers and random pointers.

## First principles

A node may be referenced from many places, so every original node needs exactly one cloned counterpart. A hash map or interweaving trick keeps that one-to-one correspondence stable.


## Classroom board: clone next and random links separately

```text
    1 -> 2 -> 3
    random: 1->3, 2->1, 3->2

    first map old nodes to new nodes, then wire the random pointers.
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

- A random pointer may be null.
- Random pointers can form cycles independently of the next chain.
- The same original node may be pointed to by many nodes.
- The clone must not share nodes with the original list.

## Brute force

```python
def copy_random_list_brute(head):
    if not head:
        return None
    old_to_new = {}
    node = head
    while node:
        old_to_new[node] = Node(node.val)
        node = node.next
    node = head
    while node:
        clone = old_to_new[node]
        clone.next = old_to_new.get(node.next)
        clone.random = old_to_new.get(node.random)
        node = node.next
    return old_to_new[head]
```

Clone next pointers first and then search for each random target repeatedly.

## Better insight

Remember the clone for each original node the first time it is created.

## Expert solution

```python
def copy_random_list(head):
    if not head:
        return None
    old_to_new = {None: None}
    node = head
    while node:
        old_to_new[node] = Node(node.val)
        node = node.next
    node = head
    while node:
        clone = old_to_new[node]
        clone.next = old_to_new[node.next]
        clone.random = old_to_new[node.random]
        node = node.next
    return old_to_new[head]
```

Create all clones while walking the list and resolve each random pointer through the original-to-clone map, or interleave clone nodes beside originals and detach them at the end.

**Complexity:** O(n) time and O(n) space.
