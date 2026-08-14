# ICPC300 044: CSES - Hamming Distance

**Source:** [CSES - Hamming Distance](https://cses.fi/problemset/task/2136/)  
**Pattern:** bit packing and population count  
**Goal:** Among the given equal-length binary strings, find the minimum number
of bit positions in which any pair differs.

## 1. Problem in plain words

The Hamming distance between `00101` and `01100` is `2`: positions two and five
differ. The task asks for the smallest such distance over every pair of input
strings.

The source bit length fits in a machine word. Python integers also support the
same operation for longer strings.

## 2. First principles

For two bit vectors `a` and `b`, XOR has a `1` exactly where they differ.
Therefore:

`HammingDistance(a, b) = popcount(a XOR b)`.

Packing each string into one integer replaces a Python loop over characters
with XOR and `int.bit_count()`, both implemented by optimized integer code.

## 3. Cases that decide correctness

| Case | Required result |
| --- | --- |
| Two identical strings | `0`. |
| Every bit differs | The full bit length. |
| Leading zeroes | Preserve their positions through equal-length validation. |
| More than one closest pair | Return their common distance once. |
| Invalid character or unequal length | Reject instead of coercing it. |

## 4. Brute force: compare every character of every pair

```python
def minimum_hamming_distance_brute_force(bit_strings: list[str]) -> int:
    if len(bit_strings) < 2:
        raise ValueError("at least two bit strings are required")
    bit_count = len(bit_strings[0])
    if bit_count == 0:
        raise ValueError("bit strings must be nonempty")
    if any(len(bits) != bit_count or set(bits) - {"0", "1"} for bits in bit_strings):
        raise ValueError("all inputs must be equal-length binary strings")

    answer = bit_count
    for first in range(len(bit_strings)):
        for second in range(first + 1, len(bit_strings)):
            distance = sum(
                left != right
                for left, right in zip(
                    bit_strings[first], bit_strings[second], strict=True
                )
            )
            answer = min(answer, distance)
    return answer
```

**Complexity:** `O(n^2 k)` time and `O(1)` auxiliary memory for `n` strings of
length `k`.

## 5. Better approach: stop at the mathematical lower bound

An early return when distance becomes `0` can save work on duplicated input,
but no ordering makes all nonzero pairs safely skippable. Encoding the strings
is the genuine optimization intended by the source: it removes the factor of
`k` from interpreted Python work while retaining the required pair scan.

There is no separate broadly useful middle implementation; adding one would
only disguise the same quadratic comparisons.

## 6. Expert solution: XOR packed integers

```python
def minimum_hamming_distance(bit_strings: list[str]) -> int:
    if len(bit_strings) < 2:
        raise ValueError("at least two bit strings are required")
    bit_count = len(bit_strings[0])
    if bit_count == 0:
        raise ValueError("bit strings must be nonempty")
    if any(len(bits) != bit_count or set(bits) - {"0", "1"} for bits in bit_strings):
        raise ValueError("all inputs must be equal-length binary strings")

    values = [int(bits, 2) for bits in bit_strings]
    answer = bit_count
    for first in range(len(values)):
        first_value = values[first]
        for second in range(first + 1, len(values)):
            answer = min(answer, (first_value ^ values[second]).bit_count())
            if answer == 0:
                return 0
    return answer
```

### Why the expert code is correct

- Equal-length binary parsing maps each bit position to the same integer bit.
- XOR sets exactly the positions whose source characters differ.
- `bit_count()` counts those positions exactly.
- The nested loops inspect every unordered input pair, so their minimum is the
  requested answer.

**Complexity:** `O(n^2 ceil(k / w))` word operations and `O(n ceil(k / w))`
memory, where `w` is the integer implementation's word size. At the source's
small `k`, each distance is effectively one XOR and one population count.

## 7. What to remember

When the data consists of short bit vectors, pack first. XOR identifies
differences and population count measures them.
