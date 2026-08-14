# ICPC300 046: CSES - Minimal Rotation

**Source:** [CSES - Minimal Rotation](https://cses.fi/problemset/task/1110/)  
**Pattern:** Booth's algorithm  
**Goal:** Output the lexicographically smallest cyclic rotation of a nonempty
string.

## 1. Problem in plain words

Moving any prefix to the end creates a cyclic rotation. The rotations of
`baca` are `baca`, `acab`, `caba`, and `abac`; the answer is `abac`.

Rotations are compared as full strings of the original length. A periodic
string may have several starting indices that produce the same minimum text.

## 2. First principles

All rotations occur as length-`n` slices of `text + text`. Booth's algorithm
keeps two candidate starts `i` and `j` and compares their characters at offset
`k`.

If the first mismatch has rotation `i` larger than rotation `j`, then starts
`i, i+1, ..., i+k` cannot be minimal: each has already lost against a rotation
beginning within the same compared block. Skip all of them at once. Apply the
symmetric rule when `j` loses.

## 3. Cases that decide correctness

| Case | Required behavior |
| --- | --- |
| One character | Return it unchanged. |
| All characters equal | Any start produces the same returned text. |
| Periodic string | Tied starts are harmless. |
| Minimum starts near the end | Slice from the doubled string. |
| Already minimal | Keep start `0`. |

## 4. Brute force: materialize every rotation

```python
def minimum_rotation_brute_force(text: str) -> str:
    if not text:
        raise ValueError("text must be nonempty")
    return min(text[start:] + text[:start] for start in range(len(text)))
```

**Complexity:** `O(n^2)` time and `O(n^2)` transient character storage.

## 5. Better: suffix array of the doubled string

Every rotation is a length-`n` prefix of a suffix of `text + text`. Build a
suffix array by doubling ranked prefix lengths, then select the first suffix
whose start is in the original string. If periodic rotations tie for their
first `n` characters, either produces the same returned text.

```python
def minimum_rotation_suffix_array(text: str) -> str:
    if not text:
        raise ValueError("text must be nonempty")

    original_length = len(text)
    doubled = text + text
    suffix_count = len(doubled)
    order = sorted(range(suffix_count), key=doubled.__getitem__)
    rank = [0] * suffix_count

    for index in range(1, suffix_count):
        rank[order[index]] = rank[order[index - 1]] + (
            doubled[order[index]] != doubled[order[index - 1]]
        )

    prefix_length = 1
    while prefix_length < suffix_count:
        order.sort(
            key=lambda start: (
                rank[start],
                rank[start + prefix_length]
                if start + prefix_length < suffix_count
                else -1,
            )
        )
        next_rank = [0] * suffix_count
        for index in range(1, suffix_count):
            previous = order[index - 1]
            current = order[index]
            previous_key = (
                rank[previous],
                rank[previous + prefix_length]
                if previous + prefix_length < suffix_count
                else -1,
            )
            current_key = (
                rank[current],
                rank[current + prefix_length]
                if current + prefix_length < suffix_count
                else -1,
            )
            next_rank[current] = next_rank[previous] + (current_key != previous_key)
        rank = next_rank
        prefix_length *= 2

    start = next(index for index in order if index < original_length)
    return doubled[start : start + original_length]
```

**Complexity:** `O(n log^2 n)` time with comparison sorting in each doubling
round, and `O(n)` memory.

## 6. Expert solution: Booth's linear candidate elimination

```python
def minimum_rotation(text: str) -> str:
    if not text:
        raise ValueError("text must be nonempty")

    length = len(text)
    doubled = text + text
    first = 0
    second = 1
    offset = 0

    while first < length and second < length and offset < length:
        first_character = doubled[first + offset]
        second_character = doubled[second + offset]
        if first_character == second_character:
            offset += 1
            continue

        if first_character > second_character:
            first += offset + 1
            if first == second:
                first += 1
        else:
            second += offset + 1
            if first == second:
                second += 1
        offset = 0

    start = min(first, second)
    return doubled[start : start + length]
```

### Why the expert code is correct

- The doubled string exposes every cyclic comparison without modular indexing.
- At a mismatch after `offset` equal characters, the lexicographically larger
  candidate loses.
- Every start through that loser's mismatch position shares a prefix that
  proves it cannot beat the winning candidate, so skipping the whole block is
  safe.
- Each candidate index moves only forward, and the remaining smaller start is
  a minimum rotation start.

**Complexity:** `O(n)` time and `O(n)` memory for the doubled string.

## 7. What to remember

For cyclic lexicographic order, compare two starts in the doubled string. One
mismatch eliminates an entire block of losing starts, not just one.
