# Focus300 127: LeetCode 828 - Count Unique Characters of All Substrings

**Source:** [LeetCode 828](https://leetcode.com/problems/count-unique-characters-of-all-substrings-of-a-given-string/)  
**Difficulty:** Hard  
**Pattern:** contribution counting between neighboring occurrences

## Exact contract

For every nonempty substring of an uppercase ASCII string, count the letters
that occur exactly once in that substring. Return the sum of those counts
modulo `1_000_000_007`.

## First principles

Reverse the summation: count substrings in which one occurrence at index `i` is
unique. If the previous and next occurrences of the same letter are at `p` and
`q`, a substring must start in `(p, i]` and end in `[i, q)`. That occurrence
therefore contributes `(i-p)*(q-i)`.

Every unique letter counted by every substring corresponds to exactly one such
occurrence-and-boundary choice.

## Cases that decide correctness

- Repeated letters contribute through different occurrence intervals.
- A missing previous occurrence uses sentinel `-1`.
- A missing next occurrence uses sentinel `len(text)`.
- Single-character substrings each contribute one.
- Apply the modulus to the final sum without changing contribution logic.

## Brute force: extend every substring while maintaining frequencies

```python
MODULUS = 1_000_000_007


def unique_letter_sum_brute(text: str) -> int:
    if (
        type(text) is not str
        or not 1 <= len(text) <= 100_000
        or any(not "A" <= character <= "Z" for character in text)
    ):
        raise ValueError("text must be an uppercase ASCII string of length 1..100,000")

    total = 0
    for start in range(len(text)):
        counts = [0] * 26
        unique_count = 0
        for end in range(start, len(text)):
            letter = ord(text[end]) - ord("A")
            if counts[letter] == 0:
                unique_count += 1
            elif counts[letter] == 1:
                unique_count -= 1
            counts[letter] += 1
            total += unique_count
    return total % MODULUS
```

This takes `O(n^2)` time and `O(1)` auxiliary space for the fixed alphabet.

## Better insight: let each occurrence select all substrings it uniquely serves

Neighboring equal occurrences are the only boundaries that matter. Recording
positions for each of 26 letters makes every contribution constant-time.

## Expert solution: previous/next occurrence contributions

```python
MODULUS = 1_000_000_007


def unique_letter_sum(text: str) -> int:
    if (
        type(text) is not str
        or not 1 <= len(text) <= 100_000
        or any(not "A" <= character <= "Z" for character in text)
    ):
        raise ValueError("text must be an uppercase ASCII string of length 1..100,000")

    positions = [[-1] for _ in range(26)]
    for index, character in enumerate(text):
        positions[ord(character) - ord("A")].append(index)

    total = 0
    for occurrences in positions:
        occurrences.append(len(text))
        for occurrence_index in range(1, len(occurrences) - 1):
            previous = occurrences[occurrence_index - 1]
            current = occurrences[occurrence_index]
            following = occurrences[occurrence_index + 1]
            total += (current - previous) * (following - current)
    return total % MODULUS
```

The contribution intervals partition all `(substring, uniquely occurring
letter)` pairs exactly once.

**Complexity:** `O(n)` time and `O(n)` space for occurrence positions.
