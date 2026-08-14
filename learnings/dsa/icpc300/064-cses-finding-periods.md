# ICPC300 064: CSES - Finding Periods

**Source:** [CSES - Finding Periods](https://cses.fi/problemset/task/1733/)  
**Pattern:** Z-function period test  
**Goal:** Output every period length of the string in increasing order. The
last repetition may be only a prefix of the repeated block.

## 1. Problem in plain words

Length `p` is a period when `text[i] == text[i-p]` for every `i >= p`. For
`ababab`, the periods are `2`, `4`, and `6`. Length `4` is valid even though a
second full four-character block does not fit: the remaining `ab` matches the
start of the block.

The full string length is always a period.

## 2. First principles

For candidate period `p`, the suffix `text[p:]` must equal the prefix
`text[:n-p]`. The Z-function value `z[p]` is exactly the length of the prefix
matching at position `p`. Therefore:

`p is a period` exactly when `z[p] >= n-p`.

This condition tests every candidate in constant time after one linear
Z-function pass.

## 3. Cases that decide correctness

| Case | Required result |
| --- | --- |
| One character | Period `1`. |
| No shorter repetition | Only period `n`. |
| All characters equal | Every length `1..n`. |
| Partial final block | Still valid when all remaining characters match. |
| Full length | Always include it. |

## 4. Brute force: test the definition for every length

```python
def period_lengths_brute_force(text: str) -> list[int]:
    if not text:
        raise ValueError("text must be nonempty")
    return [
        period
        for period in range(1, len(text) + 1)
        if all(
            text[index] == text[index - period] for index in range(period, len(text))
        )
    ]
```

**Complexity:** `O(n^2)` time and `O(n)` output memory.

## 5. Better: derive periods from the prefix-function border chain

A period `p < n` is equivalent to a border of length `n-p`. Prefix-function
links enumerate every border, so converting each border length gives every
period.

```python
def period_lengths_prefix_function(text: str) -> list[int]:
    if not text:
        raise ValueError("text must be nonempty")

    prefix = [0] * len(text)
    for index in range(1, len(text)):
        matched = prefix[index - 1]
        while matched and text[index] != text[matched]:
            matched = prefix[matched - 1]
        if text[index] == text[matched]:
            matched += 1
        prefix[index] = matched

    periods = [len(text)]
    border = prefix[-1]
    while border:
        periods.append(len(text) - border)
        border = prefix[border - 1]
    periods.sort()
    return periods
```

**Complexity:** `O(n)` time and `O(n)` memory.

## 6. Expert solution: one Z-function scan

The Z-array directly stores the prefix-suffix comparison needed by each period
candidate, so no border conversion or final sorting is needed.

```python
def period_lengths(text: str) -> list[int]:
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

    return [
        period
        for period in range(1, length + 1)
        if period == length or z[period] >= length - period
    ]
```

### Why the expert code is correct

- `z[p]` is the longest prefix equal to the suffix beginning at `p`.
- Period `p` requires equality for exactly the `n-p` overlapping characters.
- Thus `z[p] >= n-p` is both necessary and sufficient.
- Candidates are scanned increasingly, and the explicit full-length case adds
  the always-valid period `n` without indexing beyond the Z-array.

**Complexity:** `O(n)` time and `O(n)` memory.

## 7. What to remember

A period of length `p` means the suffix at `p` matches the first `n-p`
characters. That is exactly one Z-function inequality.
