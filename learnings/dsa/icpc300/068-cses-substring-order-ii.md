# ICPC300 068: CSES - Substring Order II

**Source:** [CSES - Substring Order II](https://cses.fi/problemset/task/2109/)  
**Pattern:** suffix automaton with occurrence-weighted lexicographic traversal  
**Goal:** Sort all substring occurrences lexicographically, keeping equal text
multiple times, and output the `k`-th string using one-based `k`.

## 1. Problem in plain words

For `aba`, the substring multiset is `a`, `a`, `ab`, `aba`, `b`, `ba` after
sorting. The two occurrences of `a` occupy two separate positions. This is the
difference from Substring Order I, where equal substrings count once.

## 2. First principles

A suffix-automaton state has an occurrence count shared by every substring in
its length interval. From automaton state `v`, choosing transition character
`c` reaches state `u` and creates one distinct current string. In the sorted
multiset, its block contains:

1. that exact string repeated `occurrence[u]` times;
2. every longer extension from `u`, grouped by next character.

Let `subtree[u]` be the total multiplicity of all nonempty extensions from
`u`. Transition `c` therefore owns a block of size
`occurrence[u] + subtree[u]`. Compare `k` with character blocks in sorted order
and descend into the one containing it.

## 3. Cases that decide correctness

| Case | Required behavior |
| --- | --- |
| Equal substring at several positions | Repeat it by its occurrence count. |
| One substring is a prefix of another | The shorter copies come first. |
| Repeated characters | Large multiplicities must be preserved. |
| `k = 1` | Return the lexicographically smallest occurrence. |
| `k = n(n+1)/2` | Return the final multiset element. |

## 4. Brute force: materialize and sort every occurrence

```python
def kth_substring_occurrence_brute_force(text: str, rank: int) -> str:
    if not text:
        raise ValueError("text must be nonempty")
    substrings = sorted(
        text[start:end]
        for start in range(len(text))
        for end in range(start + 1, len(text) + 1)
    )
    if not 1 <= rank <= len(substrings):
        raise ValueError("rank is outside the substring multiset")
    return substrings[rank - 1]
```

**Complexity:** `O(n^3 + n^2 log n)` character work and `O(n^3)` stored
characters.

## 5. Better: suffix trie with occurrence counts

A suffix trie has one node per distinct substring. Inserting every suffix
increments each traversed node once per occurrence. It gives the exact weighted
lexicographic traversal but may contain `O(n^2)` nodes.

```python
def kth_substring_occurrence_suffix_trie(text: str, rank: int) -> str:
    if not text:
        raise ValueError("text must be nonempty")
    total = len(text) * (len(text) + 1) // 2
    if not 1 <= rank <= total:
        raise ValueError("rank is outside the substring multiset")

    children: list[dict[str, int]] = [{}]
    occurrence = [0]
    for start in range(len(text)):
        node = 0
        for character in text[start:]:
            if character not in children[node]:
                children[node][character] = len(children)
                children.append({})
                occurrence.append(0)
            node = children[node][character]
            occurrence[node] += 1

    subtree = [0] * len(children)
    for node in range(len(children) - 1, -1, -1):
        subtree[node] = sum(
            occurrence[child] + subtree[child] for child in children[node].values()
        )

    node = 0
    answer: list[str] = []
    while True:
        for character, child in sorted(children[node].items()):
            block = occurrence[child] + subtree[child]
            if rank > block:
                rank -= block
                continue
            answer.append(character)
            if rank <= occurrence[child]:
                return "".join(answer)
            rank -= occurrence[child]
            node = child
            break
```

**Complexity:** `O(n^2)` nodes and insertion work, plus transition sorting.

## 6. Expert solution: occurrence-weighted suffix automaton

```python
def kth_substring_occurrence(text: str, rank: int) -> str:
    if not text:
        raise ValueError("text must be nonempty")
    total = len(text) * (len(text) + 1) // 2
    if not 1 <= rank <= total:
        raise ValueError("rank is outside the substring multiset")

    transitions: list[dict[str, int]] = [{}]
    suffix_link = [-1]
    max_length = [0]
    occurrence = [0]
    last = 0

    for character in text:
        current = len(transitions)
        transitions.append({})
        suffix_link.append(0)
        max_length.append(max_length[last] + 1)
        occurrence.append(1)

        previous = last
        while previous != -1 and character not in transitions[previous]:
            transitions[previous][character] = current
            previous = suffix_link[previous]
        if previous == -1:
            suffix_link[current] = 0
        else:
            next_state = transitions[previous][character]
            if max_length[previous] + 1 == max_length[next_state]:
                suffix_link[current] = next_state
            else:
                clone = len(transitions)
                transitions.append(transitions[next_state].copy())
                suffix_link.append(suffix_link[next_state])
                max_length.append(max_length[previous] + 1)
                occurrence.append(0)
                while (
                    previous != -1
                    and transitions[previous].get(character) == next_state
                ):
                    transitions[previous][character] = clone
                    previous = suffix_link[previous]
                suffix_link[next_state] = clone
                suffix_link[current] = clone
        last = current

    order = sorted(range(len(transitions)), key=max_length.__getitem__, reverse=True)
    for state in order:
        parent = suffix_link[state]
        if parent != -1:
            occurrence[parent] += occurrence[state]

    subtree = [0] * len(transitions)
    for state in order:
        subtree[state] = sum(
            occurrence[next_state] + subtree[next_state]
            for next_state in transitions[state].values()
        )

    state = 0
    answer: list[str] = []
    while True:
        for character, next_state in sorted(transitions[state].items()):
            block = occurrence[next_state] + subtree[next_state]
            if rank > block:
                rank -= block
                continue
            answer.append(character)
            if rank <= occurrence[next_state]:
                return "".join(answer)
            rank -= occurrence[next_state]
            state = next_state
            break
```

### Why the expert code is correct

- Suffix-link propagation gives each state the number of ending positions, the
  occurrence count shared by every substring represented by that state.
- A transition creates one exact substring whose copies precede every longer
  extension of it lexicographically.
- `subtree` sums all weighted extension blocks, and sorted transition order
  matches lexicographic character order.
- Subtracting whole blocks preserves `rank`; returning inside an occurrence
  block returns exactly the requested multiset element.

**Complexity:** `O(n log n)` time as written for state sorting and sorted
transitions, with `O(n)` automaton memory.

## 7. What to remember

Substring Order II weights each distinct automaton path by its end-position
count. The exact substring's copies come before all of its extensions.
