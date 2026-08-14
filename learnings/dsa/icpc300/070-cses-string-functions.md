# ICPC300 070: CSES - String Functions

**Source:** [CSES - String Functions](https://cses.fi/problemset/task/2107/)  
**Pattern:** linear Z-function and prefix-function construction  
**Goal:** Output the complete Z-function array and prefix-function array of the
string. Both arrays use `0` at index `0`.

## 1. Problem in plain words

For each position `i`:

- `z[i]` is the longest prefix equal to the substring beginning at `i`;
- `prefix[i]` is the longest proper prefix of `text[:i+1]` that is also its
  suffix.

They measure different alignments and must both be produced in source order:
the Z-array first, then the prefix-function array.

## 2. First principles

The Z algorithm maintains a half-open interval `[left, right)` known to match
the string prefix. A position inside it can reuse the mirrored Z-value up to
the interval boundary, then extend by direct comparison.

The prefix function maintains the best border length of the previous prefix.
On mismatch, following `prefix[matched-1]` tries the next shorter border without
rechecking characters already proved equal.

Both right boundaries and fallback links avoid repeated quadratic comparisons.

## 3. Cases that decide correctness

| Case | Required behavior |
| --- | --- |
| Index `0` | Both values are `0` by source convention. |
| One character | Return `[0]` for both arrays. |
| All characters equal | Values grow predictably to the boundaries. |
| No repeated prefix | All later values may be zero. |
| Overlapping prefix matches | Reuse the current Z-box or prefix border. |

## 4. Brute force: compare definitions directly

```python
def string_functions_brute_force(text: str) -> tuple[list[int], list[int]]:
    if not text:
        raise ValueError("text must be nonempty")

    z = [0] * len(text)
    for index in range(1, len(text)):
        while index + z[index] < len(text) and text[z[index]] == text[index + z[index]]:
            z[index] += 1

    prefix = [0] * len(text)
    for end in range(1, len(text)):
        for border in range(end, 0, -1):
            if text[:border] == text[end - border + 1 : end + 1]:
                prefix[end] = border
                break
    return z, prefix
```

**Complexity:** `O(n^3)` copied-character work in the direct border checks and
`O(n)` output memory.

## 5. Better approach: why both linear invariants are the real step

Hashing could compare prefixes faster, but collision-free verification would
reintroduce character work. Computing only one array would not satisfy the
source contract. The useful deterministic improvement is to maintain the Z-box
for one array and border fallbacks for the other; both are already linear.

There is no separate asymptotically meaningful middle implementation to add.

## 6. Expert solution: compute both arrays in linear passes

```python
def string_functions(text: str) -> tuple[list[int], list[int]]:
    if not text:
        raise ValueError("text must be nonempty")

    length = len(text)
    z = [0] * length
    left = 0
    right = 0
    for index in range(1, length):
        if index < right:
            z[index] = min(right - index, z[index - left])
        while index + z[index] < length and text[z[index]] == text[index + z[index]]:
            z[index] += 1
        if index + z[index] > right:
            left = index
            right = index + z[index]

    prefix = [0] * length
    for index in range(1, length):
        matched = prefix[index - 1]
        while matched and text[index] != text[matched]:
            matched = prefix[matched - 1]
        if text[index] == text[matched]:
            matched += 1
        prefix[index] = matched

    return z, prefix
```

### Why the expert code is correct

- The Z-box contains a prefix match already proved character by character;
  mirrored reuse never crosses its right boundary without fresh verification.
- Direct extension makes every stored Z-value maximal.
- Prefix fallback visits exactly the nested proper borders of the previous
  prefix until one can accept the new character.
- Extending that border produces the longest border of the current prefix, so
  both returned arrays match their definitions at every index.

**Complexity:** `O(n)` time and `O(n)` output memory.

## 7. What to remember

Z-values reuse a rightmost prefix-match interval. Prefix values reuse the chain
of nested borders. They solve related but different alignment questions.
