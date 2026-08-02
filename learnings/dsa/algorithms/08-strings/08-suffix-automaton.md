# Suffix Automaton

## Idea

A suffix automaton is the smallest deterministic automaton containing every
substring of a text. Each state represents a group of substrings sharing the
same ending positions.

## Visual model

```text
state.length - link(state).length
= number of new distinct substrings represented by that state
```

## Classroom board: one state represents many substrings

```text
for a state v:
maximum represented length = length[v]
minimum represented length = length[link[v]] + 1
count contributed = length[v] - length[link[v]]
```

Clones split states when one group no longer has identical future behavior.

## Steps

1. Extend the automaton one character at a time from the last state.
2. Add missing transitions while following suffix links.
3. Link directly when lengths fit.
4. Otherwise clone a state, redirect transitions, and repair suffix links.
5. Sum length differences to count distinct substrings.

## First-principles derivation

Many substrings share the same possible continuations. A suffix automaton
merges substring occurrences whose end positions behave identically.

Each state represents a range of substring lengths; suffix links move to the
largest strictly shorter suffix class.

## Classroom board: distinct substrings of aba

Build one character at a time:

```text
state  max length  suffix link  new distinct substrings
0      0           -            -
1      1 ("a")     0            1
2      2 ("ab")    0            2
3      3 ("aba")   1            2

contribution = len[state] - len[link[state]]
total = 1 + 2 + 2 = 5

substrings: a, b, ab, ba, aba
```

State `3` contributes lengths `2..3`: `"ba"` and `"aba"`.

## Pattern recognition

Use it for distinct substrings, longest common substring, substring occurrence
structure, or online construction of all substrings.

## Implementation: count distinct substrings

### C++

```cpp
long long countDistinctSubstrings(const std::string& text) {
    struct State { int length = 0; int link = -1; std::unordered_map<char, int> next; };
    std::vector<State> states(1);
    int last = 0;
    for (char character : text) {
        int current = states.size(); states.push_back(states[last]);
        states[current].length = states[last].length + 1;
        states[current].next.clear();
        int parent = last;
        while (parent != -1 && states[parent].next.find(character) == states[parent].next.end()) {
            states[parent].next[character] = current;
            parent = states[parent].link;
        }
        if (parent == -1) states[current].link = 0;
        else {
            int target = states[parent].next[character];
            if (states[parent].length + 1 == states[target].length) states[current].link = target;
            else {
                int clone = states.size(); states.push_back(states[target]);
                states[clone].length = states[parent].length + 1;
                while (parent != -1 && states[parent].next[character] == target) {
                    states[parent].next[character] = clone;
                    parent = states[parent].link;
                }
                states[target].link = states[current].link = clone;
            }
        }
        last = current;
    }
    long long answer = 0;
    for (int state = 1; state < static_cast<int>(states.size()); ++state) answer += states[state].length - states[states[state].link].length;
    return answer;
}
```

### Python

```python
def count_distinct_substrings(text: str) -> int:
    length = [0]
    link = [-1]
    transitions: list[dict[str, int]] = [{}]
    last = 0
    for character in text:
        current = len(length)
        length.append(length[last] + 1)
        link.append(0)
        transitions.append({})
        parent = last
        while parent != -1 and character not in transitions[parent]:
            transitions[parent][character] = current
            parent = link[parent]
        if parent != -1:
            target = transitions[parent][character]
            if length[parent] + 1 == length[target]:
                link[current] = target
            else:
                clone = len(length)
                length.append(length[parent] + 1)
                link.append(link[target])
                transitions.append(transitions[target].copy())
                while parent != -1 and transitions[parent].get(character) == target:
                    transitions[parent][character] = clone
                    parent = link[parent]
                link[target] = link[current] = clone
        last = current
    return sum(length[state] - length[link[state]] for state in range(1, len(length)))
```

### Java

```java
static long countDistinctSubstrings(String text) {
    List<Integer> length = new ArrayList<>(List.of(0));
    List<Integer> link = new ArrayList<>(List.of(-1));
    List<Map<Character, Integer>> next = new ArrayList<>(List.of(new HashMap<>()));
    int last = 0;
    for (char character : text.toCharArray()) {
        int current = length.size();
        length.add(length.get(last) + 1);
        link.add(0);
        next.add(new HashMap<>());
        int parent = last;
        while (parent != -1 && !next.get(parent).containsKey(character)) {
            next.get(parent).put(character, current);
            parent = link.get(parent);
        }
        if (parent != -1) {
            int target = next.get(parent).get(character);
            if (length.get(parent) + 1 == length.get(target)) link.set(current, target);
            else {
                int clone = length.size();
                length.add(length.get(parent) + 1);
                link.add(link.get(target));
                next.add(new HashMap<>(next.get(target)));
                while (parent != -1 && Objects.equals(next.get(parent).get(character), target)) {
                    next.get(parent).put(character, clone);
                    parent = link.get(parent);
                }
                link.set(target, clone);
                link.set(current, clone);
            }
        }
        last = current;
    }
    long answer = 0;
    for (int state = 1; state < length.size(); state++) answer += length.get(state) - length.get(link.get(state));
    return answer;
}
```

## Why it works

State `v` represents substring lengths from `length[link[v]] + 1` through
`length[v]`, and each distinct substring belongs to exactly one state.

## Complexity

Expected time and space are `O(n)` with hash-map transitions; at most `2n - 1`
states are created.

## Common mistakes

- Copying outgoing transitions into a normal new state; only clones copy them.
- Forgetting to redirect transitions that formerly pointed to the cloned target.
- Confusing suffix automaton states with individual substrings.
