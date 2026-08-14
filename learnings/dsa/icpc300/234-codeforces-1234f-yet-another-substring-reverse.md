# ICPC300 234: Codeforces 1234F - Yet Another Substring Reverse

**Source:** [Codeforces 1234F - Yet Another Substring Reverse](https://codeforces.com/problemset/problem/1234/F)  
**Difficulty:** 2400  
**Pattern:** distinct-substring masks plus SOS maximum DP

## Exact contract

The string uses the first 20 lowercase letters. Reverse at most one substring,
then maximize the length of a substring whose characters are pairwise distinct.

## First principles

The reversal can join two original distinct-character substrings in opposite
order. Their character sets must be disjoint, and every such pair can be joined
by a suitable reversal. Thus the answer is the maximum combined popcount of two
disjoint masks that occur as distinct-character substrings.

Enumerate every such substring in at most 20 steps per start. SOS DP records,
for every mask, the largest occurring submask.

## Cases that decide correctness

- A repeated character ends extension from one start.
- Either chosen substring may be empty.
- Only character sets matter after each substring is known to be distinct.
- Complement lookup enforces disjointness.
- Reversing nothing is represented by pairing with the empty mask.

## Brute force: simulate every reversal

```python
def substring_reverse_brute(text: str) -> int:
    if not text or any(character < "a" or character > "t" for character in text):
        raise ValueError("text must use lowercase letters a through t")

    def longest_distinct(candidate: str) -> int:
        last: dict[str, int] = {}
        left = 0
        best = 0
        for right, character in enumerate(candidate):
            left = max(left, last.get(character, -1) + 1)
            last[character] = right
            best = max(best, right - left + 1)
        return best

    answer = 0
    for left in range(len(text) + 1):
        for right in range(left, len(text) + 1):
            changed = text[:left] + text[left:right][::-1] + text[right:]
            answer = max(answer, longest_distinct(changed))
    return answer
```

This is `O(n^4)` with direct string construction and scanning.

## Better approach: pair every occurring mask

Enumerating distinct-character substrings gives at most `2^20` masks, but
testing all disjoint mask pairs is quadratic. SOS DP replaces the inner search
with one complement lookup.

## Expert solution: submask maxima by SOS DP

```python
ALPHABET_SIZE = 20


def maximum_distinct_after_reverse(text: str) -> int:
    if not text or any(
        not 0 <= ord(character) - ord("a") < ALPHABET_SIZE for character in text
    ):
        raise ValueError("text uses a character outside the configured alphabet")

    mask_count = 1 << ALPHABET_SIZE
    occurring = bytearray(mask_count)
    occurring[0] = 1
    for start in range(len(text)):
        mask = 0
        for end in range(start, min(len(text), start + ALPHABET_SIZE)):
            bit = 1 << (ord(text[end]) - ord("a"))
            if mask & bit:
                break
            mask |= bit
            occurring[mask] = 1

    best = bytearray(
        mask.bit_count() if present else 0 for mask, present in enumerate(occurring)
    )
    for bit in range(ALPHABET_SIZE):
        bit_value = 1 << bit
        for mask in range(mask_count):
            if mask & bit_value and best[mask ^ bit_value] > best[mask]:
                best[mask] = best[mask ^ bit_value]

    full_mask = mask_count - 1
    answer = 0
    for mask, present in enumerate(occurring):
        if present:
            answer = max(answer, mask.bit_count() + best[full_mask ^ mask])
    return answer
```

After SOS propagation, `best[M]` is the greatest size of any occurring submask
of `M`. Looking up the complement of an occurring mask therefore selects the
best possible disjoint partner.

**Complexity:** `O(20n + 20*2^20)` time and `O(2^20)` space.
