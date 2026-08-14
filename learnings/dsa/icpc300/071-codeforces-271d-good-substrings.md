# ICPC300 071: Codeforces 271D - Good Substrings

**Source:** [Codeforces 271D - Good Substrings](https://codeforces.com/problemset/problem/271/D)  
**Pattern:** sliding window plus suffix automaton

## Exact contract

Input gives a lowercase string `s` (`1 <= |s| <= 1500`), a 26-character
binary mask, and `k`. Mask position `i` is `1` when letter `a+i` is good and
`0` when it is bad. Output the number of distinct nonempty substrings of `s`
that contain at most `k` bad characters.

## First principles

For every ending position, a sliding window gives the longest suffix containing
at most `k` bad characters. A suffix automaton state represents substring
lengths from `len(link[state]) + 1` through `len(state)` that share the same end
positions.

Record the longest valid suffix at each prefix state, then propagate those
limits through suffix links from longer states to shorter states. State `v`
contributes every length above `len(link[v])` and at most its propagated valid
limit.

## Cases that decide correctness

- `k = 0` permits only substrings made entirely of good letters.
- Distinctness is by string content, not occurrence.
- A suffix-link propagation is capped at the parent state's maximum length.
- Clone states need no direct occurrence update; descending states propagate
  their valid end-position information into them.

## Brute force: materialize and filter every substring

```python
def good_substrings_brute(text: str, good_mask: str, limit: int) -> int:
    substrings = set()
    for left in range(len(text)):
        for right in range(left + 1, len(text) + 1):
            candidate = text[left:right]
            bad_count = sum(
                good_mask[ord(character) - ord("a")] == "0" for character in candidate
            )
            if bad_count <= limit:
                substrings.add(candidate)
    return len(substrings)
```

**Complexity:** `O(n^3)` time and `O(n^3)` stored characters in the worst case.

## Better: insert only valid substrings into a trie

```python
def good_substrings_trie(text: str, good_mask: str, limit: int) -> int:
    children: list[dict[str, int]] = [{}]
    answer = 0

    for left in range(len(text)):
        node = 0
        bad_count = 0
        for right in range(left, len(text)):
            character = text[right]
            bad_count += good_mask[ord(character) - ord("a")] == "0"
            if bad_count > limit:
                break
            next_node = children[node].get(character)
            if next_node is None:
                next_node = len(children)
                children[node][character] = next_node
                children.append({})
                answer += 1
            node = next_node
    return answer
```

Each trie node is one distinct valid substring, reducing time to `O(n^2)` but
still requiring `O(n^2)` nodes.

## Expert solution: linear suffix-automaton aggregation

```python
import sys


def solve() -> None:
    input_stream = sys.stdin.buffer
    text = input_stream.readline().strip().decode()
    good_mask = input_stream.readline().strip().decode()
    limit = int(input_stream.readline())

    transitions: list[dict[str, int]] = [{}]
    suffix_link = [-1]
    maximum_length = [0]
    valid_length = [0]
    last = 0
    left = 0
    bad_count = 0

    for right, character in enumerate(text):
        bad_count += good_mask[ord(character) - ord("a")] == "0"
        while bad_count > limit:
            bad_count -= good_mask[ord(text[left]) - ord("a")] == "0"
            left += 1

        current = len(transitions)
        transitions.append({})
        suffix_link.append(0)
        maximum_length.append(maximum_length[last] + 1)
        valid_length.append(right - left + 1)
        previous = last

        while previous != -1 and character not in transitions[previous]:
            transitions[previous][character] = current
            previous = suffix_link[previous]

        if previous == -1:
            suffix_link[current] = 0
        else:
            target = transitions[previous][character]
            if maximum_length[previous] + 1 == maximum_length[target]:
                suffix_link[current] = target
            else:
                clone = len(transitions)
                transitions.append(transitions[target].copy())
                suffix_link.append(suffix_link[target])
                maximum_length.append(maximum_length[previous] + 1)
                valid_length.append(0)
                while previous != -1 and transitions[previous].get(character) == target:
                    transitions[previous][character] = clone
                    previous = suffix_link[previous]
                suffix_link[target] = clone
                suffix_link[current] = clone
        last = current

    states_by_length = sorted(
        range(1, len(transitions)), key=maximum_length.__getitem__, reverse=True
    )
    for state in states_by_length:
        parent = suffix_link[state]
        valid_length[parent] = max(
            valid_length[parent],
            min(valid_length[state], maximum_length[parent]),
        )

    answer = 0
    for state in range(1, len(transitions)):
        longest = min(maximum_length[state], valid_length[state])
        answer += max(0, longest - maximum_length[suffix_link[state]])
    print(answer)


if __name__ == "__main__":
    solve()
```

Suffix-link propagation collects the best valid occurrence for every end-position
class. The state's counted length interval is disjoint from every other state's,
so summing its valid prefix counts each distinct substring exactly once.

**Complexity:** `O(n log n)` time because states are sorted by length and
`O(n)` space.

