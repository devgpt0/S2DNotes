# Aho-Corasick

## Idea

Aho-Corasick matches many patterns in one text scan. It combines a trie with
failure links that jump to the longest useful suffix after a mismatch.

## Visual model

```text
trie edge exists -> follow it
edge missing     -> follow failure links
node output      -> patterns ending here or through failure suffixes
```

## Classroom board: share work across patterns

```text
patterns "he" and "she" share suffix/prefix state "he"
while reading "she", trie reaches terminal "she"
failure link also reaches terminal "he"
report both matches ending at the same text position
```

## Steps

1. Insert every pattern into a trie and count terminal patterns.
2. BFS trie nodes to build failure links.
3. Add each failure node's output count to its child.
4. Scan text, following edges/failures, and add the current output count.

## First-principles derivation

Searching for many patterns independently repeats prefix work. Store all
patterns in one trie, then add failure links that point to the longest suffix
that is also a trie prefix.

After each text character, the current node represents the longest pattern
prefix matching a suffix of the text read so far.

## Classroom board: match he, she, his, hers

Text is `"ushers"`.

```text
read u: no trie edge -> root
read s: state "s"
read h: state "sh"
read e: state "she"
        output "she"
        failure link reaches "he" -> output "he"
read r: fallback, then state "her"
read s: state "hers" -> output "hers"

matches: she, he, hers
```

Failure links reuse suffixes instead of restarting every pattern at every text
position.

## Pattern recognition

Use it when many keywords must be found in one or many texts, including
overlapping matches.

## Implementation: lowercase English, count all matches

### C++

```cpp
class AhoCorasick {
    struct Node {
        std::array<int, 26> next;
        int failure = 0;
        int output = 0;
        Node() { next.fill(-1); }
    };
   public:
    AhoCorasick() : nodes_(1) {}
    void add(const std::string& pattern) {
        int node = 0;
        for (char character : pattern) {
            int edge = character - 'a';
            if (nodes_[node].next[edge] == -1) {
                nodes_[node].next[edge] = nodes_.size();
                nodes_.emplace_back();
            }
            node = nodes_[node].next[edge];
        }
        ++nodes_[node].output;
    }
    void build() {
        std::queue<int> queue;
        for (int edge = 0; edge < 26; ++edge) {
            int child = nodes_[0].next[edge];
            if (child == -1) nodes_[0].next[edge] = 0;
            else queue.push(child);
        }
        while (!queue.empty()) {
            int node = queue.front(); queue.pop();
            nodes_[node].output += nodes_[nodes_[node].failure].output;
            for (int edge = 0; edge < 26; ++edge) {
                int child = nodes_[node].next[edge];
                if (child == -1) nodes_[node].next[edge] = nodes_[nodes_[node].failure].next[edge];
                else {
                    nodes_[child].failure = nodes_[nodes_[node].failure].next[edge];
                    queue.push(child);
                }
            }
        }
    }
    long long countMatches(const std::string& text) const {
        long long answer = 0;
        int node = 0;
        for (char character : text) {
            node = nodes_[node].next[character - 'a'];
            answer += nodes_[node].output;
        }
        return answer;
    }
   private:
    std::vector<Node> nodes_;
};
```

### Python

```python
from collections import deque


class AhoCorasick:
    def __init__(self) -> None:
        self.children: list[dict[str, int]] = [{}]
        self.failure = [0]
        self.output = [0]

    def add(self, pattern: str) -> None:
        node = 0
        for character in pattern:
            if character not in self.children[node]:
                self.children[node][character] = len(self.children)
                self.children.append({})
                self.failure.append(0)
                self.output.append(0)
            node = self.children[node][character]
        self.output[node] += 1

    def build(self) -> None:
        queue = deque(self.children[0].values())
        while queue:
            node = queue.popleft()
            self.output[node] += self.output[self.failure[node]]
            for character, child in self.children[node].items():
                fallback = self.failure[node]
                while fallback and character not in self.children[fallback]:
                    fallback = self.failure[fallback]
                self.failure[child] = self.children[fallback].get(character, 0)
                queue.append(child)

    def count_matches(self, text: str) -> int:
        node = 0
        answer = 0
        for character in text:
            while node and character not in self.children[node]:
                node = self.failure[node]
            node = self.children[node].get(character, 0)
            answer += self.output[node]
        return answer
```

### Java

```java
final class AhoCorasick {
    private static final class Node {
        final int[] next = new int[26];
        int failure;
        int output;
        Node() { Arrays.fill(next, -1); }
    }
    private final List<Node> nodes = new ArrayList<>(List.of(new Node()));

    void add(String pattern) {
        int node = 0;
        for (char character : pattern.toCharArray()) {
            int edge = character - 'a';
            if (nodes.get(node).next[edge] == -1) {
                nodes.get(node).next[edge] = nodes.size();
                nodes.add(new Node());
            }
            node = nodes.get(node).next[edge];
        }
        nodes.get(node).output++;
    }

    void build() {
        Queue<Integer> queue = new ArrayDeque<>();
        for (int edge = 0; edge < 26; edge++) {
            int child = nodes.get(0).next[edge];
            if (child == -1) nodes.get(0).next[edge] = 0;
            else queue.add(child);
        }
        while (!queue.isEmpty()) {
            int node = queue.remove();
            nodes.get(node).output += nodes.get(nodes.get(node).failure).output;
            for (int edge = 0; edge < 26; edge++) {
                int child = nodes.get(node).next[edge];
                if (child == -1) nodes.get(node).next[edge] = nodes.get(nodes.get(node).failure).next[edge];
                else {
                    nodes.get(child).failure = nodes.get(nodes.get(node).failure).next[edge];
                    queue.add(child);
                }
            }
        }
    }

    long countMatches(String text) {
        long answer = 0;
        int node = 0;
        for (char character : text.toCharArray()) {
            node = nodes.get(node).next[character - 'a'];
            answer += nodes.get(node).output;
        }
        return answer;
    }
}
```

## Why it works

The failure link is the longest suffix of the current prefix that is also a
trie prefix. Propagated outputs report every pattern ending at the current text
position.

## Complexity

Build is `O(total pattern length * alphabet)` in the fixed-transition versions;
matching is `O(text length + matches)` and space is proportional to trie size.

## Common mistakes

- Searching before building failure links.
- Forgetting output patterns inherited through failure links.
- Using lowercase indexing without validating the alphabet.
