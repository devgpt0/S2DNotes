# Trie (Prefix Tree)

## Idea

A trie stores strings one character per edge. Strings with the same prefix
share nodes.

## Visual model

```text
root --c-- a --t*       stores "cat"
            \\--r*      stores "car"
```

`*` marks the end of a complete word.

## Classroom board: insert `cat`, then `car`

```text
insert cat: root -> c -> a -> t*
insert car: root -> c -> a already exist; create r*

search ca  reaches a but no * -> prefix only, not a stored word
search car reaches r*         -> stored word
```

Shared prefixes are stored once.

## Steps

1. Start at the root.
2. Follow or create the edge for each character.
3. Mark the final node as a complete word.
4. Search by following the same path; distinguish a prefix from a full word.

## First-principles derivation

Comparing a query with every word repeats prefix comparisons. A trie stores
each shared prefix once as a path.

After reading `i` characters, the current node represents exactly that
length-`i` prefix; terminal markers distinguish words from mere prefixes.

## Pattern recognition

Use a trie for prefix queries, dictionaries, autocomplete, XOR tries, or many
string lookups where shared prefixes matter.

## Implementation: lowercase English words

### C++

```cpp
class Trie {
    struct Node {
        std::array<int, 26> next;
        bool terminal = false;
        Node() { next.fill(-1); }
    };

   public:
    Trie() : nodes_(1) {}

    void insert(const std::string& word) {
        int node = 0;
        for (char character : word) {
            const int edge = character - 'a';
            if (nodes_[node].next[edge] == -1) {
                nodes_[node].next[edge] = nodes_.size();
                nodes_.emplace_back();
            }
            node = nodes_[node].next[edge];
        }
        nodes_[node].terminal = true;
    }

    bool contains(const std::string& word) const {
        int node = 0;
        for (char character : word) {
            node = nodes_[node].next[character - 'a'];
            if (node == -1) return false;
        }
        return nodes_[node].terminal;
    }

   private:
    std::vector<Node> nodes_;
};
```

### Python

```python
class Trie:
    def __init__(self) -> None:
        self.children: list[dict[str, int]] = [{}]
        self.terminal = [False]

    def insert(self, word: str) -> None:
        node = 0
        for character in word:
            if character not in self.children[node]:
                self.children[node][character] = len(self.children)
                self.children.append({})
                self.terminal.append(False)
            node = self.children[node][character]
        self.terminal[node] = True

    def contains(self, word: str) -> bool:
        node = 0
        for character in word:
            if character not in self.children[node]:
                return False
            node = self.children[node][character]
        return self.terminal[node]
```

### Java

```java
final class Trie {
    private static final class Node {
        final int[] next = new int[26];
        boolean terminal;

        Node() { Arrays.fill(next, -1); }
    }

    private final List<Node> nodes = new ArrayList<>(List.of(new Node()));

    void insert(String word) {
        int node = 0;
        for (char character : word.toCharArray()) {
            int edge = character - 'a';
            if (nodes.get(node).next[edge] == -1) {
                nodes.get(node).next[edge] = nodes.size();
                nodes.add(new Node());
            }
            node = nodes.get(node).next[edge];
        }
        nodes.get(node).terminal = true;
    }

    boolean contains(String word) {
        int node = 0;
        for (char character : word.toCharArray()) {
            node = nodes.get(node).next[character - 'a'];
            if (node == -1) return false;
        }
        return nodes.get(node).terminal;
    }
}
```

## Why it works

Each root-to-node path spells exactly one prefix. The terminal marker tells
whether that prefix is also a complete stored word.

## Complexity

Insert and lookup take `O(length)` time. Space is proportional to the total
number of created prefix nodes.

## Common mistakes

- Treating every existing prefix as a complete word.
- Allocating a huge fixed alphabet per node when a map is more suitable.
- Using `character - 'a'` without guaranteeing lowercase English input.
