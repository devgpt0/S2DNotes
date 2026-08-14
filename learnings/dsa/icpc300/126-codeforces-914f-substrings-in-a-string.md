# ICPC300 126: Codeforces 914F - Substrings in a String

**Source:** [Codeforces 914F](https://codeforces.com/problemset/problem/914/F)  
**Pattern:** shifted character bitsets under point updates

## Exact contract

Maintain a lowercase Latin string under `q` online operations:

- `1 p c`: replace the character at one-based position `p` by `c`;
- `2 l r t`: output how many occurrences of pattern `t` lie completely inside
  the inclusive substring from `l` through `r`.

Occurrences may overlap.

## First principles

For each character, store a bitset whose bit `i` is one exactly when the
current string has that character at position `i`. For a pattern character at
offset `j`, shifting its bitset right by `j` marks possible *start positions*.
Intersect all shifted bitsets; surviving starts match every character.

Finally mask starts from `l-1` through `r-|t|`. A point replacement clears one
bit in the old character bitset and sets it in the new one.

## Cases that decide correctness

- Count overlapping matches.
- If the pattern is longer than the query interval, the answer is zero.
- The last valid start is `r-|t|+1` in one-based indexing.
- Updates affect subsequent queries immediately.
- Shifts align pattern offsets with candidate starts; shifting the opposite
  direction is incorrect.

## Brute force: compare every candidate slice

```python
def dynamic_substrings_brute(
    initial: str,
    queries: list[tuple[int | str, ...]],
) -> list[int]:
    text = list(initial)
    answers = []
    for query in queries:
        if query[0] == 1:
            position = int(query[1]) - 1
            text[position] = str(query[2])
            continue
        left = int(query[1]) - 1
        right = int(query[2])
        pattern = str(query[3])
        answers.append(
            sum(
                "".join(text[start : start + len(pattern)]) == pattern
                for start in range(left, right - len(pattern) + 1)
            )
        )
    return answers
```

The worst-case comparison work is `O(|interval| * |pattern|)` per query.

## Better: KMP after each update

```python
def dynamic_substrings_kmp(
    initial: str,
    queries: list[tuple[int | str, ...]],
) -> list[int]:
    text = list(initial)
    answers = []
    for query in queries:
        if query[0] == 1:
            text[int(query[1]) - 1] = str(query[2])
            continue

        left = int(query[1]) - 1
        right = int(query[2])
        pattern = str(query[3])
        prefix = [0] * len(pattern)
        border = 0
        for index in range(1, len(pattern)):
            while border and pattern[index] != pattern[border]:
                border = prefix[border - 1]
            if pattern[index] == pattern[border]:
                border += 1
            prefix[index] = border

        matched = 0
        occurrences = 0
        for index in range(left, right):
            while matched and text[index] != pattern[matched]:
                matched = prefix[matched - 1]
            if text[index] == pattern[matched]:
                matched += 1
            if matched == len(pattern):
                occurrences += 1
                matched = prefix[matched - 1]
        answers.append(occurrences)
    return answers
```

KMP makes a query linear in the interval plus pattern length, independent of
how repetitive the strings are.

## Expert solution: Python integers as packed bitsets

```python
import sys


def solve() -> None:
    input_stream = sys.stdin.buffer
    text = bytearray(input_stream.readline().strip())
    character_bits = [0] * 26
    for position, character in enumerate(text):
        character_bits[character - ord("a")] |= 1 << position

    query_count = int(input_stream.readline())
    answers = []
    for _ in range(query_count):
        query = input_stream.readline().split()
        query_type = int(query[0])
        if query_type == 1:
            position = int(query[1]) - 1
            new_character = query[2][0]
            bit = 1 << position
            character_bits[text[position] - ord("a")] &= ~bit
            text[position] = new_character
            character_bits[new_character - ord("a")] |= bit
            continue

        left = int(query[1]) - 1
        right = int(query[2]) - 1
        pattern = query[3]
        valid_start_count = right - left - len(pattern) + 2
        if valid_start_count <= 0:
            answers.append("0")
            continue

        matches = character_bits[pattern[0] - ord("a")]
        for offset, character in enumerate(pattern[1:], start=1):
            matches &= character_bits[character - ord("a")] >> offset
        interval_mask = (1 << valid_start_count) - 1
        answers.append(str(((matches >> left) & interval_mask).bit_count()))

    print("\n".join(answers))


if __name__ == "__main__":
    solve()
```

After intersection, bit `i` survives exactly when every pattern character is
present at `i + offset`. The final mask selects precisely the legal starts, so
`bit_count` is the required number of occurrences.

**Complexity:** because Python integers are immutable, an update takes
`O(n / word_size)` packed-word work in the worst case; a query takes
`O(|t| * n / word_size)` work. Storage is `O(n)` bits per alphabet character.
