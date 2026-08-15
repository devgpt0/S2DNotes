# Focus300 270: LeetCode 211 - Design Add and Search Words Data Structure

**Source:** [LeetCode 211](https://leetcode.com/problems/design-add-and-search-words-data-structure/)  
**Difficulty:** Medium  
**Pattern:** binary search / two-pointer / rank selection

## Exact contract

Solve the ordered-data problem 'Design Add and Search Words Data Structure' by exploiting sorted structure, rank order, or monotonicity.

## First principles

Ordered data usually lets you discard large portions of the search space at once. The key is to identify what remains monotone enough to justify the elimination step.

## Cases that decide correctness

- Boundary values often determine whether the elimination rule is valid.
- Duplicates may weaken but not necessarily destroy the ordering logic.
- The answer may be a value, an index, or a boolean depending on the statement.
- A correct invariant matters more than the exact loop shape.

## Brute force

```python
class WordDictionaryBrute:
    def __init__(self):
        self.words = set()

    def addWord(self, word):
        self.words.add(word)

    def search(self, word):
        return any(len(w) == len(word) and all(a == b or b == "." for a, b in zip(w, word)) for w in self.words)
```

Check every candidate directly.

## Better insight

Use the monotone property to cut the candidate space in half or move two pointers inward.

## Expert solution

```python
class WordDictionary:
    def __init__(self):
        self.children = {}
        self.end = False

    def addWord(self, word):
        node = self
        for ch in word:
            node = node.children.setdefault(ch, WordDictionary())
        node.end = True

    def search(self, word):
        def dfs(node, i):
            if i == len(word):
                return node.end
            ch = word[i]
            if ch == ".":
                return any(dfs(child, i + 1) for child in node.children.values())
            return ch in node.children and dfs(node.children[ch], i + 1)

        return dfs(self, 0)
```

Maintain a tight invariant and update only the side of the search space that the ordering rule rules out.

**Complexity:** Typically O(log n) for binary-search problems or O(n) for two-pointer sweeps.
