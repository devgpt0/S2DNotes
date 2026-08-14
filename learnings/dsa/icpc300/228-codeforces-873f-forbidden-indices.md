# ICPC300 228: Codeforces 873F - Forbidden Indices

**Source:** [Codeforces 873F - Forbidden Indices](https://codeforces.com/problemset/problem/873/F)  
**Rating:** 2300  
**Pattern:** reversed suffix automaton with allowed-occurrence propagation  
**Goal:** Maximize `substring_length * allowed_occurrences`, where an occurrence
counts only when its starting position is marked `0` rather than forbidden.

## 1. First principles

Reverse the text and marker string. An original occurrence start becomes an
occurrence end in the reversed text. While building a suffix automaton, assign
one count to the state for each reversed position whose marker is `0`.

Propagate counts from longer states to suffix links. Every state then knows the
number of allowed end positions for all substrings it represents. Those
substrings share the count, so the longest one maximizes the product:

```text
maximum_length[state] * allowed_count[state]
```

## 2. Cases that decide correctness

- Marker `0` means the original occurrence start is allowed.
- Multiple occurrences of the same substring contribute separately.
- Clone states begin with zero direct occurrences.
- Counts propagate from longer states to suffix links.
- A state with zero allowed occurrences contributes zero.

## 3. Brute force: count every distinct substring

```python
def forbidden_indices_score_brute(text: str, markers: str) -> int:
    if (
        not text
        or len(text) != len(markers)
        or any(not "a" <= character <= "z" for character in text)
        or any(marker not in "01" for marker in markers)
    ):
        raise ValueError("invalid text or markers")

    answer = 0
    candidates = {
        text[left:right]
        for left in range(len(text))
        for right in range(left + 1, len(text) + 1)
    }
    for candidate in candidates:
        occurrences = sum(
            markers[start] == "0" and text.startswith(candidate, start)
            for start in range(len(text) - len(candidate) + 1)
        )
        answer = max(answer, len(candidate) * occurrences)
    return answer
```

**Complexity:** `O(n^4)` time and `O(n^3)` stored substring data in the worst
case.

## 4. Better transition: turn starts into automaton end positions

Suffix automata naturally aggregate occurrence ends, not starts. Reversal maps
the source's allowed starts to exactly those end positions, after which the
standard suffix-link occurrence propagation applies unchanged.

## 5. Expert solution: occurrence-count suffix automaton

```python
def forbidden_indices_score(text: str, markers: str) -> int:
    if (
        not text
        or len(text) != len(markers)
        or any(not "a" <= character <= "z" for character in text)
        or any(marker not in "01" for marker in markers)
    ):
        raise ValueError("invalid text or markers")

    reversed_text = text[::-1]
    reversed_markers = markers[::-1]
    transitions: list[dict[str, int]] = [{}]
    suffix_link = [-1]
    maximum_length = [0]
    allowed_count = [0]
    last = 0

    for character, marker in zip(reversed_text, reversed_markers):
        current = len(transitions)
        transitions.append({})
        suffix_link.append(0)
        maximum_length.append(maximum_length[last] + 1)
        allowed_count.append(int(marker == "0"))
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
                allowed_count.append(0)
                while previous != -1 and transitions[previous].get(character) == target:
                    transitions[previous][character] = clone
                    previous = suffix_link[previous]
                suffix_link[target] = clone
                suffix_link[current] = clone
        last = current

    order = sorted(
        range(1, len(transitions)), key=maximum_length.__getitem__, reverse=True
    )
    for state in order:
        allowed_count[suffix_link[state]] += allowed_count[state]
    return max(
        maximum_length[state] * allowed_count[state]
        for state in range(1, len(transitions))
    )
```

### Why the expert code is correct

Reversal bijects original starts with reversed ends while preserving substring
length and equality. A suffix-automaton state's end-position set is accumulated
by adding every longer state to its suffix link. Therefore `allowed_count` is
exactly the number of source-allowed occurrences for every substring in the
state, and choosing its maximum represented length gives that state's best
product.

**Complexity:** `O(n log n)` time because of sorting and `O(n)` space.

## 6. What to remember

```text
condition on occurrence starts -> reverse into end positions
substring occurrence sets -> suffix automaton states
all occurrence counts -> propagate along suffix links
```
