# Problem 20: Word Ladder (LeetCode #127)

**Difficulty:** Hard  
**Core pattern:** BFS for an unweighted shortest path

## Problem statement

Transform `beginWord` into `endWord` by changing one letter at a time. Every
intermediate word must exist in `wordList`. Return the number of words in the
shortest sequence, or `0` if no sequence exists.

## Example

```text
beginWord = "hit"
endWord   = "cog"

hit -> hot -> dot -> dog -> cog
 1      2      3      4      5

Answer = 5
```

## Observation

Treat each word as a graph node. Two words have an edge when they differ by one
letter. Every edge costs one transformation, so BFS finds the shortest path.

Building every pairwise edge is expensive. Instead, generate possible neighbors
by changing each position to `'a'` through `'z'`.

## BFS-level diagram

```text
Level 1: hit
           |
Level 2:  hot
          / \
Level 3: dot lot
          |   |
Level 4: dog log
          \   /
Level 5:  cog

The first time BFS reaches cog is the shortest transformation.
```

## Solution 1: Brute Force by Building the Complete Graph

### Observation

Compare every pair of words and connect pairs that differ in one position, then
run BFS. Building the graph costs `O(N^2 * L)`.

### Algorithm

1. Add `beginWord` to the word list.
2. Compare every pair of words.
3. Add an edge when they differ in exactly one position.
4. Run BFS from `beginWord` over the constructed graph.
5. Return the BFS level that first reaches `endWord`.

### C++ code

```cpp
class Solution {
   private:
    bool differsByOne(const string& first, const string& second) {
        int differences = 0;
        for (int index = 0; index < static_cast<int>(first.size()); ++index) {
            differences += first[index] != second[index];
        }
        return differences == 1;
    }

   public:
    int ladderLength(string beginWord, string endWord,
                     vector<string>& wordList) {
        if (find(wordList.begin(), wordList.end(), endWord) == wordList.end()) {
            return 0;
        }

        vector<string> words = wordList;
        words.push_back(beginWord);
        int start = words.size() - 1;
        vector<vector<int>> graph(words.size());

        for (int left = 0; left < static_cast<int>(words.size()); ++left) {
            for (int right = left + 1; right < static_cast<int>(words.size());
                 ++right) {
                if (differsByOne(words[left], words[right])) {
                    graph[left].push_back(right);
                    graph[right].push_back(left);
                }
            }
        }

        queue<pair<int, int>> pending;
        vector<bool> visited(words.size(), false);
        pending.push({start, 1});
        visited[start] = true;

        while (!pending.empty()) {
            auto [node, length] = pending.front();
            pending.pop();
            if (words[node] == endWord) {
                return length;
            }

            for (int neighbor : graph[node]) {
                if (!visited[neighbor]) {
                    visited[neighbor] = true;
                    pending.push({neighbor, length + 1});
                }
            }
        }
        return 0;
    }
};
```

### Complexity

- Time: `O(N^2 * L)` to build the graph, plus BFS
- Space: `O(N^2)` in the worst case

## How we derive the optimal solution

```text
Compare every pair and store every graph edge
                 |
                 v
Most word pairs are not neighbors
                 |
                 v
From one word, only L * 25 useful mutations are possible
                 |
                 v
Generate those neighbors only when BFS visits the word
                 |
                 v
Keep BFS for shortest path; avoid the complete graph
```

## Optimized / CP approach: Generate neighbors during BFS

### Algorithm

1. Put all dictionary words in a hash set.
2. Return `0` immediately if `endWord` is absent.
3. Start BFS with `beginWord` at sequence length `1`.
4. For every position, replace its letter with `'a'` through `'z'`.
5. If the generated word is in the set, remove it and enqueue it.
6. When BFS removes `endWord`, return the current level.
7. Return `0` if the queue becomes empty.

### Why remove a word immediately?

The first BFS visit is always its shortest distance. Removing it prevents later
paths from enqueuing the same word again.

### Complexity

Let `N` be the dictionary size and `L` the word length.

- Time: `O(N * L^2 * 26)` when creating/hash-checking a word costs `O(L)`
- Space: `O(N * L)`

## Pattern to remember

```text
Minimum number of equal-cost moves
        => BFS

Huge implicit graph
        => generate neighbors only when a node is visited
```

## C++

```cpp
class Solution {
   public:
    int ladderLength(string beginWord, string endWord,
                     vector<string>& wordList) {
        unordered_set<string> unused(wordList.begin(), wordList.end());
        if (!unused.contains(endWord)) {
            return 0;
        }

        queue<string> words;
        words.push(beginWord);
        int length = 1;

        while (!words.empty()) {
            int levelSize = words.size();

            while (levelSize-- > 0) {
                string word = words.front();
                words.pop();

                if (word == endWord) {
                    return length;
                }

                for (int index = 0; index < (int)word.size(); ++index) {
                    char original = word[index];

                    for (char letter = 'a'; letter <= 'z'; ++letter) {
                        if (letter == original) {
                            continue;
                        }

                        word[index] = letter;
                        if (unused.erase(word) == 1) {
                            words.push(word);
                        }
                    }

                    word[index] = original;
                }
            }

            ++length;
        }

        return 0;
    }
};
```

## Python

```python
from collections import deque


class Solution:
    def ladder_length(
        self,
        begin_word: str,
        end_word: str,
        word_list: list[str],
    ) -> int:
        unused = set(word_list)
        if end_word not in unused:
            return 0

        words = deque([begin_word])
        length = 1

        while words:
            for _ in range(len(words)):
                word = words.popleft()
                if word == end_word:
                    return length

                letters = list(word)
                for index, original in enumerate(letters):
                    for letter_code in range(ord("a"), ord("z") + 1):
                        letter = chr(letter_code)
                        if letter == original:
                            continue

                        letters[index] = letter
                        neighbor = "".join(letters)
                        if neighbor in unused:
                            unused.remove(neighbor)
                            words.append(neighbor)

                    letters[index] = original

            length += 1

        return 0
```

## Java

```java
class Solution {
    public int ladderLength(String beginWord, String endWord, List<String> wordList) {
        Set<String> unused = new HashSet<>(wordList);
        if (!unused.contains(endWord)) {
            return 0;
        }

        Queue<String> words = new ArrayDeque<>();
        words.offer(beginWord);
        int length = 1;

        while (!words.isEmpty()) {
            int levelSize = words.size();

            for (int item = 0; item < levelSize; item++) {
                String word = words.poll();
                if (word.equals(endWord)) {
                    return length;
                }

                char[] letters = word.toCharArray();
                for (int index = 0; index < letters.length; index++) {
                    char original = letters[index];

                    for (char letter = 'a'; letter <= 'z'; letter++) {
                        if (letter == original) {
                            continue;
                        }

                        letters[index] = letter;
                        String neighbor = new String(letters);
                        if (unused.remove(neighbor)) {
                            words.offer(neighbor);
                        }
                    }

                    letters[index] = original;
                }
            }

            length++;
        }

        return 0;
    }
}
```

## Go

```go
func ladderLength(beginWord string, endWord string, wordList []string) int {
	unused := make(map[string]struct{}, len(wordList))
	for _, word := range wordList {
		unused[word] = struct{}{}
	}
	if _, exists := unused[endWord]; !exists {
		return 0
	}

	words := []string{beginWord}
	length := 1

	for len(words) > 0 {
		levelSize := len(words)

		for item := 0; item < levelSize; item++ {
			word := words[0]
			words = words[1:]

			if word == endWord {
				return length
			}

			letters := []byte(word)
			for index, original := range letters {
				for letter := byte('a'); letter <= byte('z'); letter++ {
					if letter == original {
						continue
					}

					letters[index] = letter
					neighbor := string(letters)
					if _, exists := unused[neighbor]; exists {
						delete(unused, neighbor)
						words = append(words, neighbor)
					}
				}
				letters[index] = original
			}
		}

		length++
	}

	return 0
}
```

## Common mistakes

- Using DFS for a shortest path in an unweighted graph.
- Marking a word visited only when dequeued, which creates duplicates.
- Forgetting to restore the original letter after trying replacements.
