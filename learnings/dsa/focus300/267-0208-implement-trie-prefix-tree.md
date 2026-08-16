# Focus300 267: LeetCode 208 - Implement Trie (Prefix Tree)

**Source:** [LeetCode 208](https://leetcode.com/problems/implement-trie-prefix-tree/)  
**Difficulty:** Medium  
**Pattern:** tree traversal / recursion

## Exact contract

Solve the tree problem 'Implement Trie (Prefix Tree)' by returning the value or structure requested in the statement.

## First principles

Tree problems usually reduce to recursion on subtrees, with the current node combining the answers from the children.


## Classroom board: walk the tree once

```text
choose the root condition, then push the relevant subtree state down as
you recurse or iterate.
```



## Step-by-step transformation

1. Choose a start state such as a cell, node, or partial path.
2. Mark the state as visited or temporarily commit the choice.
3. Expand to valid neighbors or next choices while the invariant still holds.
4. Undo the temporary choice when the branch finishes, then return the collected answer.

These problems transform the input into output by exploring one branch at a time and backtracking whenever a branch can no longer produce a valid solution.


## Diagram: search and undo

```text

            start state
                |
                v
            choose one path
                |
                v
            explore neighbors
                |
                v
            undo and try next path
                |
                v
            answer
```

These notes use search, visit markers, and backtracking to turn one starting state into the final valid path or count.

## Cases that decide correctness

- An empty tree is often the simplest base case.
- A single node should satisfy the recurrence immediately.
- Balanced and skewed trees can behave very differently.
- The node's own value often combines child results.

## Brute force

```python
class TrieBrute:
    def __init__(self):
        self.words = set()

    def insert(self, word):
        self.words.add(word)

    def search(self, word):
        return word in self.words

    def startsWith(self, prefix):
        return any(word.startswith(prefix) for word in self.words)
```

Traverse the whole tree and recompute the same subtree facts repeatedly.

## Better insight

Use recursion or BFS so each node contributes to the answer exactly once.

## Expert solution

```python
class Trie:
    def __init__(self):
        self.children = {}
        self.end = False

    def insert(self, word):
        node = self
        for ch in word:
            node = node.children.setdefault(ch, Trie())
        node.end = True

    def search(self, word):
        node = self
        for ch in word:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return node.end

    def startsWith(self, prefix):
        node = self
        for ch in prefix:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return True
```

Define the subtree state precisely, combine child results at the current node, and pass the minimum amount of information upward.

**Complexity:** Usually O(n) time with O(h) recursion or queue space.
