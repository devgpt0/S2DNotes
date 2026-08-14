# ICPC300 059: CSES - Substring Order I

**Source:** [CSES - Substring Order I](https://cses.fi/problemset/task/2108/)  
**Pattern:** suffix automaton + path counting  
**Goal:** Return the `k`-th lexicographically smallest distinct non-empty
substring.

`k` is one-based. The functions raise `ValueError` when it exceeds the number
of distinct substrings.

## 1. First principles

Every path starting at the suffix automaton's initial state spells one distinct
substring. Transitions always move toward states with greater maximum length,
so this transition graph is acyclic.

Let `ways[state]` be the number of non-empty strings obtainable from a state:

```text
ways[state] = sum over transitions of (1 + ways[next_state])
```

The `1` is the substring ending immediately after that transition. Visit
outgoing characters in sorted order, subtract whole branch sizes, and descend
into the branch containing `k`.

## 2. Cases that decide correctness

| Case | Required behavior |
| --- | --- |
| Repeated occurrence of one substring | Count it once. |
| One substring prefixes another | The shorter substring comes first. |
| `k = 1` | Return the smallest one-character substring. |
| `k` equals the distinct count | Return the final lexicographic substring. |
| `k` too large | Fail explicitly. |

## 3. Brute force: materialize every substring

```python
def substring_order_i_brute(text: str, k: int) -> str:
    if not text or k <= 0:
        raise ValueError("text must be non-empty and k must be positive")

    substrings = {
        text[left:right]
        for left in range(len(text))
        for right in range(left + 1, len(text) + 1)
    }
    ordered = sorted(substrings)
    if k > len(ordered):
        raise ValueError("k exceeds the number of distinct substrings")
    return ordered[k - 1]
```

**Complexity:** `O(n^3)` total copied characters in the worst case and
`O(n^2)` distinct substring entries.

## 4. Better: suffix ordering and adjacent LCP

Sort all suffix strings. A suffix contributes prefixes longer than its longest
common prefix with the preceding suffix; shorter prefixes were already seen.

```python
def substring_order_i_suffixes(text: str, k: int) -> str:
    if not text or k <= 0:
        raise ValueError("text must be non-empty and k must be positive")

    suffix_order = sorted(range(len(text)), key=lambda start: text[start:])
    previous_start: int | None = None

    for start in suffix_order:
        common_length = 0
        if previous_start is not None:
            while (
                start + common_length < len(text)
                and previous_start + common_length < len(text)
                and text[start + common_length] == text[previous_start + common_length]
            ):
                common_length += 1

        new_substrings = len(text) - start - common_length
        if k <= new_substrings:
            return text[start : start + common_length + k]
        k -= new_substrings
        previous_start = start

    raise ValueError("k exceeds the number of distinct substrings")
```

**Complexity:** `O(n^2 log n)` worst-case comparison/copying time and `O(n^2)`
suffix-key storage.

## 5. Expert solution: suffix automaton

Build the automaton, count transition paths in decreasing state-length order,
then perform a lexicographic branch selection.

```python
def substring_order_i_suffix_automaton(text: str, k: int) -> str:
    if not text or k <= 0:
        raise ValueError("text must be non-empty and k must be positive")

    transitions: list[dict[str, int]] = [{}]
    suffix_link = [-1]
    maximum_length = [0]
    last = 0

    for character in text:
        current = len(transitions)
        transitions.append({})
        suffix_link.append(0)
        maximum_length.append(maximum_length[last] + 1)

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

                while previous != -1 and transitions[previous].get(character) == target:
                    transitions[previous][character] = clone
                    previous = suffix_link[previous]
                suffix_link[target] = clone
                suffix_link[current] = clone
        last = current

    ways = [0] * len(transitions)
    states_by_decreasing_length = sorted(
        range(len(transitions)),
        key=maximum_length.__getitem__,
        reverse=True,
    )
    for state in states_by_decreasing_length:
        ways[state] = sum(
            1 + ways[next_state] for next_state in transitions[state].values()
        )

    if k > ways[0]:
        raise ValueError("k exceeds the number of distinct substrings")

    result: list[str] = []
    state = 0
    while True:
        for character, next_state in sorted(transitions[state].items()):
            branch_size = 1 + ways[next_state]
            if k > branch_size:
                k -= branch_size
                continue

            result.append(character)
            if k == 1:
                return "".join(result)
            k -= 1
            state = next_state
            break
        else:
            raise RuntimeError("a valid k must select an automaton branch")
```

### Why the expert code is correct

- Suffix-automaton paths from the initial state are in one-to-one
  correspondence with distinct substrings.
- `ways` counts every continuation once because the transition graph is a DAG.
- Sorted transitions partition all remaining substrings into lexicographically
  ordered branches, with the transition's one-character ending first.

**Complexity:** `O(n log alphabet + answer_length * alphabet)` time with sorted
transitions and `O(n)` automaton states.

## 6. What to remember

```text
suffix-automaton path = one distinct substring
branch size through edge = 1 + ways[next]
scan characters in order, subtract branches, descend at k
```
