# ICPC300 060: CSES - Repeating Substring

**Source:** [CSES - Repeating Substring](https://cses.fi/problemset/task/2106/)  
**Pattern:** suffix array + longest common prefix  
**Goal:** Return a longest substring that occurs at least twice, allowing
overlapping occurrences, or `-1` when none exists.

The source accepts any longest answer. For deterministic testing, these
implementations return the lexicographically smallest one when several tie.

## 1. First principles

Every repeated substring is a common prefix of two suffixes. After suffixes are
sorted, the pair with the greatest common prefix can be chosen among adjacent
suffixes: any suffixes between a non-adjacent pair share at least that ordering
boundary.

```text
longest repeated substring
    = maximum LCP of adjacent suffixes in suffix-array order
```

Build the suffix array with prefix doubling, then compute adjacent LCP values
in linear time with Kasai's algorithm.

## 2. Cases that decide correctness

| Case | Required behavior |
| --- | --- |
| All characters distinct | Return `-1`. |
| Overlap, such as `aaa` | Return `aa`. |
| Repetition reaches the text end | Suffix comparisons must stop at bounds. |
| Several longest answers | Return the lexicographically smallest here. |
| One-character repetition | Return that character. |

## 3. Brute force: materialize substrings by length

Track which substrings of each length have appeared before.

```python
def repeating_substring_brute(text: str) -> str:
    if not text:
        raise ValueError("text must not be empty")

    best = ""
    for length in range(1, len(text) + 1):
        seen: set[str] = set()
        repeated: set[str] = set()
        for start in range(len(text) - length + 1):
            candidate = text[start : start + length]
            if candidate in seen:
                repeated.add(candidate)
            else:
                seen.add(candidate)
        if repeated:
            best = min(repeated)
    return best if best else "-1"
```

**Complexity:** `O(n^3)` copied characters and `O(n^2)` substring storage in
the worst case.

## 4. Better: suffix trie occurrence counts

Insert every suffix into a trie. A node's visit count is the number of starting
positions at which its path string occurs.

```python
def repeating_substring_suffix_trie(text: str) -> str:
    if not text:
        raise ValueError("text must not be empty")

    transitions: list[dict[str, int]] = [{}]
    visits = [0]
    best = ""

    for start in range(len(text)):
        state = 0
        for end in range(start, len(text)):
            character = text[end]
            next_state = transitions[state].get(character)
            if next_state is None:
                next_state = len(transitions)
                transitions[state][character] = next_state
                transitions.append({})
                visits.append(0)
            state = next_state
            visits[state] += 1

            if visits[state] >= 2:
                candidate = text[start : end + 1]
                if len(candidate) > len(best) or (
                    len(candidate) == len(best) and candidate < best
                ):
                    best = candidate

    return best if best else "-1"
```

**Complexity:** `O(n^2)` time and `O(n^2)` trie space.

## 5. Expert solution: suffix array and Kasai LCP

A unique sentinel converts suffix sorting into cyclic-shift sorting. Prefix
doubling and counting by equivalence class build the suffix array in
`O(n log n)`; Kasai then scans all adjacent LCPs in `O(n)`.

```python
def repeating_substring_suffix_array(text: str) -> str:
    if not text:
        raise ValueError("text must not be empty")
    if "\0" in text:
        raise ValueError("text must not contain the sentinel character")

    original_length = len(text)
    combined = text + "\0"
    total_length = len(combined)

    order = sorted(range(total_length), key=combined.__getitem__)
    equivalence_class = [0] * total_length
    for index in range(1, total_length):
        previous = order[index - 1]
        current = order[index]
        equivalence_class[current] = equivalence_class[previous] + (
            combined[current] != combined[previous]
        )

    prefix_length = 1
    while prefix_length < total_length:
        shifted = [(position - prefix_length) % total_length for position in order]
        class_count = max(equivalence_class) + 1
        count = [0] * class_count
        for position in shifted:
            count[equivalence_class[position]] += 1

        class_start = [0] * class_count
        for class_index in range(1, class_count):
            class_start[class_index] = (
                class_start[class_index - 1] + count[class_index - 1]
            )

        new_order = [0] * total_length
        for position in shifted:
            class_index = equivalence_class[position]
            new_order[class_start[class_index]] = position
            class_start[class_index] += 1

        new_class = [0] * total_length
        for index in range(1, total_length):
            previous = new_order[index - 1]
            current = new_order[index]
            previous_pair = (
                equivalence_class[previous],
                equivalence_class[(previous + prefix_length) % total_length],
            )
            current_pair = (
                equivalence_class[current],
                equivalence_class[(current + prefix_length) % total_length],
            )
            new_class[current] = new_class[previous] + (current_pair != previous_pair)

        order = new_order
        equivalence_class = new_class
        prefix_length *= 2

    suffix_order = [position for position in order if position != original_length]
    rank = [0] * original_length
    for index, start in enumerate(suffix_order):
        rank[start] = index

    best = ""
    common_length = 0
    for start in range(original_length):
        suffix_index = rank[start]
        if suffix_index == original_length - 1:
            common_length = 0
            continue

        next_start = suffix_order[suffix_index + 1]
        while (
            start + common_length < original_length
            and next_start + common_length < original_length
            and text[start + common_length] == text[next_start + common_length]
        ):
            common_length += 1

        if common_length > 0:
            candidate = text[start : start + common_length]
            if len(candidate) > len(best) or (
                len(candidate) == len(best) and candidate < best
            ):
                best = candidate
        if common_length > 0:
            common_length -= 1

    return best if best else "-1"
```

### Why the expert code is correct

- Every repeated substring is a common prefix of at least two suffixes.
- The maximum common prefix over all suffix pairs appears between an adjacent
  pair in sorted suffix order.
- Kasai computes exactly those adjacent LCPs, so the greatest candidate is a
  longest repeated substring; the tie comparison makes the output deterministic.

**Complexity:** `O(n log n)` time and `O(n)` space.

## 6. What to remember

```text
substring occurrence -> prefix of a suffix
repeated substring -> common prefix of two suffixes
longest repetition -> maximum adjacent suffix-array LCP
```
