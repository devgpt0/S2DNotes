# Problem 21: Alien Dictionary (LeetCode #269)

**Difficulty:** Hard  
**Core pattern:** Build constraints, then topologically sort

## Problem statement

Words are already sorted using an unknown alphabet. Return one valid character
order, or an empty string if the input is invalid.

## Example

```text
words = ["wrt", "wrf", "er", "ett", "rftt"]
constraints: t -> f, w -> e, r -> t, e -> r
one valid answer: "wertf"
```

## Observation

Compare adjacent words. The **first different character** gives one ordering
rule; later differences tell us nothing because dictionary order was already
decided by the first mismatch.

```text
"wrt" before "wrf"
   first mismatch: t vs f
   rule: t -> f

Invalid prefix:
"abc" before "ab"  -> impossible
```

## Diagram

```text
adjacent words -> first-mismatch edges -> directed graph
                                              |
                                              v
                                      topological sort
                                      /              \
                               all chars used      cycle
                                  valid order      return ""
```

## Solution 1: Brute Force Character Permutations

### Observation

Try every alphabet permutation and test the words. This takes factorial time.

### Algorithm

1. Collect every distinct character.
2. Generate every possible character order.
3. Build a rank map for that order.
4. Check whether every adjacent word pair is correctly sorted.
5. Return the first valid order.

### C++ code

```cpp
class Solution {
   private:
    bool comesBefore(const string& first, const string& second,
                     const array<int, 26>& rank) {
        int limit = min(first.size(), second.size());
        for (int index = 0; index < limit; ++index) {
            if (first[index] != second[index]) {
                return rank[first[index] - 'a'] < rank[second[index] - 'a'];
            }
        }
        return first.size() <= second.size();
    }

   public:
    string alienOrderBruteForce(vector<string>& words) {
        set<char> uniqueCharacters;
        for (const string& word : words) {
            uniqueCharacters.insert(word.begin(), word.end());
        }

        string order(uniqueCharacters.begin(), uniqueCharacters.end());
        do {
            array<int, 26> rank{};
            for (int index = 0; index < static_cast<int>(order.size());
                 ++index) {
                rank[order[index] - 'a'] = index;
            }

            bool valid = true;
            for (int index = 0; index + 1 < static_cast<int>(words.size());
                 ++index) {
                if (!comesBefore(words[index], words[index + 1], rank)) {
                    valid = false;
                    break;
                }
            }
            if (valid) {
                return order;
            }
        } while (next_permutation(order.begin(), order.end()));

        return "";
    }
};
```

### Complexity

- Time: `O(V! * total characters)`
- Space: `O(V)`

## How we derive the optimal solution

```text
Try every alphabet permutation
          |
          v
Adjacent sorted words already reveal necessary ordering rules
          |
          v
Only the first mismatch creates a rule: charA -> charB
          |
          v
Rules form a directed graph
          |
          v
Topologically sort once: O(total characters + V + E)
```

## Optimized / CP approach

### Algorithm

1. Add every character as a graph node, including isolated characters.
2. Compare each adjacent word pair.
3. Reject a longer word that appears before its exact prefix.
4. Add an edge for the first mismatch; do not add duplicate edges.
5. Run Kahn's topological sort.
6. Return the order only if it contains every character.

### Complexity

- Time: `O(total characters + V + E)`
- Space: `O(V + E)`

## Pattern to remember

```text
Items are sorted by unknown rules
        -> extract pairwise constraints
        -> constraints form directed edges
        -> topological sort
```

## C++

```cpp
class Solution {
   public:
    string alienOrder(vector<string>& words) {
        unordered_map<char, unordered_set<char>> graph;
        unordered_map<char, int> indegree;

        for (const string& word : words) {
            for (char character : word) {
                indegree.try_emplace(character, 0);
            }
        }

        for (int index = 0; index + 1 < (int)words.size(); ++index) {
            const string& first = words[index];
            const string& second = words[index + 1];

            if (first.size() > second.size() && first.starts_with(second)) {
                return "";
            }

            int limit = min(first.size(), second.size());
            for (int position = 0; position < limit; ++position) {
                if (first[position] != second[position]) {
                    if (graph[first[position]]
                            .insert(second[position])
                            .second) {
                        ++indegree[second[position]];
                    }
                    break;
                }
            }
        }

        queue<char> ready;
        for (const auto& [character, degree] : indegree) {
            if (degree == 0) {
                ready.push(character);
            }
        }

        string order;
        while (!ready.empty()) {
            char current = ready.front();
            ready.pop();
            order += current;

            for (char next : graph[current]) {
                if (--indegree[next] == 0) {
                    ready.push(next);
                }
            }
        }

        return order.size() == indegree.size() ? order : "";
    }
};
```

## Python

```python
from collections import deque


class Solution:
    def alien_order(self, words: list[str]) -> str:
        graph = {character: set() for word in words for character in word}
        indegree = {character: 0 for character in graph}

        for first, second in zip(words, words[1:]):
            if len(first) > len(second) and first.startswith(second):
                return ""

            for left, right in zip(first, second):
                if left != right:
                    if right not in graph[left]:
                        graph[left].add(right)
                        indegree[right] += 1
                    break

        ready = deque(
            character for character, degree in indegree.items() if degree == 0
        )
        order: list[str] = []

        while ready:
            current = ready.popleft()
            order.append(current)

            for next_character in graph[current]:
                indegree[next_character] -= 1
                if indegree[next_character] == 0:
                    ready.append(next_character)

        return "".join(order) if len(order) == len(indegree) else ""
```

## Java

```java
class Solution {
    public String alienOrder(String[] words) {
        Map<Character, Set<Character>> graph = new HashMap<>();
        Map<Character, Integer> indegree = new HashMap<>();

        for (String word : words) {
            for (char character : word.toCharArray()) {
                graph.putIfAbsent(character, new HashSet<>());
                indegree.putIfAbsent(character, 0);
            }
        }

        for (int index = 0; index + 1 < words.length; index++) {
            String first = words[index];
            String second = words[index + 1];

            if (first.length() > second.length() && first.startsWith(second)) {
                return "";
            }

            int limit = Math.min(first.length(), second.length());
            for (int position = 0; position < limit; position++) {
                char left = first.charAt(position);
                char right = second.charAt(position);
                if (left != right) {
                    if (graph.get(left).add(right)) {
                        indegree.put(right, indegree.get(right) + 1);
                    }
                    break;
                }
            }
        }

        Queue<Character> ready = new ArrayDeque<>();
        for (Map.Entry<Character, Integer> entry : indegree.entrySet()) {
            if (entry.getValue() == 0) {
                ready.offer(entry.getKey());
            }
        }

        StringBuilder order = new StringBuilder();
        while (!ready.isEmpty()) {
            char current = ready.poll();
            order.append(current);
            for (char next : graph.get(current)) {
                indegree.put(next, indegree.get(next) - 1);
                if (indegree.get(next) == 0) {
                    ready.offer(next);
                }
            }
        }

        return order.length() == indegree.size() ? order.toString() : "";
    }
}
```

## Go

```go
func alienOrder(words []string) string {
	graph := map[byte]map[byte]bool{}
	indegree := map[byte]int{}

	for _, word := range words {
		for index := range word {
			character := word[index]
			if graph[character] == nil {
				graph[character] = map[byte]bool{}
			}
			indegree[character] += 0
		}
	}

	for index := 0; index+1 < len(words); index++ {
		first, second := words[index], words[index+1]
		if len(first) > len(second) && strings.HasPrefix(first, second) {
			return ""
		}

		limit := min(len(first), len(second))
		for position := 0; position < limit; position++ {
			left, right := first[position], second[position]
			if left != right {
				if !graph[left][right] {
					graph[left][right] = true
					indegree[right]++
				}
				break
			}
		}
	}

	ready := []byte{}
	for character, degree := range indegree {
		if degree == 0 {
			ready = append(ready, character)
		}
	}

	order := []byte{}
	for head := 0; head < len(ready); head++ {
		current := ready[head]
		order = append(order, current)
		for next := range graph[current] {
			indegree[next]--
			if indegree[next] == 0 {
				ready = append(ready, next)
			}
		}
	}

	if len(order) != len(indegree) {
		return ""
	}
	return string(order)
}
```

## Common mistakes

- Using every mismatch instead of only the first.
- Missing the invalid-prefix case.
- Forgetting isolated characters or counting duplicate edges twice.
