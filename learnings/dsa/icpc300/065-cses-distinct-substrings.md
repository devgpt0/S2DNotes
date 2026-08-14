# ICPC300 065: CSES - Distinct Substrings

**Source:** [CSES - Distinct Substrings](https://cses.fi/problemset/task/2105/)  
**Pattern:** suffix automaton substring counting  
**Goal:** Count how many different nonempty substrings occur in the string.

## 1. Problem in plain words

Positions do not create new answers when the extracted text is equal. For
`aaa`, the distinct substrings are `a`, `aa`, and `aaa`, so the answer is `3`
even though there are six substring occurrences.

## 2. First principles

In a suffix automaton, state `v` represents an equivalence class of substrings
with the same possible continuation positions. Their lengths form the interval:

`max_length[link[v]] + 1 ... max_length[v]`.

Every length in this interval corresponds to one distinct substring, and no
substring belongs to two states. Therefore state `v` contributes:

`max_length[v] - max_length[link[v]]`.

Sum this over every non-root state.

## 3. Cases that decide correctness

| Case | Required result |
| --- | --- |
| One character | `1`. |
| All characters distinct | `n(n+1)/2`. |
| All characters equal | `n`. |
| Repeated substring at many positions | Count its text once. |
| Clone state | Count its own adjusted length interval, not occurrences. |

## 4. Brute force: store every substring text

```python
def count_distinct_substrings_brute_force(text: str) -> int:
    if not text:
        raise ValueError("text must be nonempty")
    return len(
        {
            text[start:end]
            for start in range(len(text))
            for end in range(start + 1, len(text) + 1)
        }
    )
```

**Complexity:** `O(n^3)` copied-character work and `O(n^3)` worst-case stored
characters.

## 5. Better: suffix array total minus adjacent LCP overlap

Every suffix contributes all its prefixes. In suffix-array order, the prefixes
already seen from earlier suffixes are exactly the longest common prefix with
the previous suffix. Subtract all adjacent LCP values from `n(n+1)/2`.

```python
def count_distinct_substrings_suffix_array(text: str) -> int:
    if not text:
        raise ValueError("text must be nonempty")

    length = len(text)
    suffix_array = list(range(length))
    rank = [ord(character) for character in text]
    step = 1
    while step < length:
        suffix_array.sort(
            key=lambda start: (
                rank[start],
                rank[start + step] if start + step < length else -1,
            )
        )
        next_rank = [0] * length
        for index in range(1, length):
            previous = suffix_array[index - 1]
            current = suffix_array[index]
            previous_key = (
                rank[previous],
                rank[previous + step] if previous + step < length else -1,
            )
            current_key = (
                rank[current],
                rank[current + step] if current + step < length else -1,
            )
            next_rank[current] = next_rank[previous] + (current_key != previous_key)
        rank = next_rank
        step *= 2

    suffix_rank = [0] * length
    for index, start in enumerate(suffix_array):
        suffix_rank[start] = index

    common_prefix_sum = 0
    matched = 0
    for start in range(length):
        rank_index = suffix_rank[start]
        if rank_index == 0:
            matched = 0
            continue
        previous = suffix_array[rank_index - 1]
        while (
            start + matched < length
            and previous + matched < length
            and text[start + matched] == text[previous + matched]
        ):
            matched += 1
        common_prefix_sum += matched
        if matched:
            matched -= 1

    return length * (length + 1) // 2 - common_prefix_sum
```

**Complexity:** `O(n log^2 n)` time with comparison sorting and `O(n)` memory.

## 6. Expert solution: sum suffix-automaton length intervals

```python
def count_distinct_substrings(text: str) -> int:
    if not text:
        raise ValueError("text must be nonempty")

    transitions: list[dict[str, int]] = [{}]
    suffix_link = [-1]
    max_length = [0]
    last = 0

    for character in text:
        current = len(transitions)
        transitions.append({})
        suffix_link.append(0)
        max_length.append(max_length[last] + 1)

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
                while (
                    previous != -1
                    and transitions[previous].get(character) == next_state
                ):
                    transitions[previous][character] = clone
                    previous = suffix_link[previous]
                suffix_link[next_state] = clone
                suffix_link[current] = clone
        last = current

    return sum(
        max_length[state] - max_length[suffix_link[state]]
        for state in range(1, len(transitions))
    )
```

### Why the expert code is correct

- The automaton recognizes exactly all substrings of the source text.
- Every non-root state owns one nonoverlapping interval of substring lengths
  from its suffix link's maximum plus one through its own maximum.
- Each length in that interval identifies exactly one distinct substring in
  the state's end-position class.
- Cloning preserves recognized substrings while splitting classes so these
  intervals remain disjoint and complete.

**Complexity:** `O(n)` expected time and `O(n)` states and transitions for a
fixed-size alphabet.

## 7. What to remember

A suffix-automaton state contributes the number of new lengths beyond its
suffix link: `len[state] - len[link[state]]`.
