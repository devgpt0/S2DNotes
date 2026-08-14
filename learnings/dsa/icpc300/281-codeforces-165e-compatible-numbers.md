# ICPC300 281: Codeforces 165E - Compatible Numbers

**Source:** [Codeforces 165E - Compatible Numbers](https://codeforces.com/problemset/problem/165/E)  
**Rating:** 2200  
**Pattern:** subset DP over bitmasks  
**Goal:** For every array value, return any array value whose bitwise AND with
it is zero, or `-1` when none exists.

## 1. First principles

`first & second == 0` means every set bit of `second` lies inside the zero-bit
mask of `first`. Thus, after learning whether every mask contains an input
value in one of its submasks, the answer for `value` is stored at its
complement.

## 2. Cases that decide correctness

- Repeated values do not change feasibility.
- Zero is compatible with every value, including itself.
- A nonzero value may be compatible with another copy only if their AND is zero.
- `-1` is returned only when no input value is a submask of the complement.
- Source values fit in 22 bits.

## 3. Brute force: inspect every ordered pair

```python
def compatible_numbers_brute(values: list[int]) -> list[int]:
    if not values or any(not 0 <= value < 1 << 22 for value in values):
        raise ValueError("values must be nonempty 22-bit integers")

    answers: list[int] = []
    for first in values:
        answers.append(next((second for second in values if first & second == 0), -1))
    return answers
```

**Complexity:** `O(n^2)` time and `O(n)` output space.

## 4. Better transition: propagate witnesses to supersets

Initialize `witness[mask]` for masks present in the array. For each bit,
an empty mask can inherit a witness from the same mask with that bit cleared.
After all bits, every mask knows an input value contained in some submask.

## 5. Expert solution: SOS witness DP

```python
from array import array


def compatible_numbers(values: list[int]) -> list[int]:
    if not values or any(not 0 <= value < 1 << 22 for value in values):
        raise ValueError("values must be nonempty 22-bit integers")

    bit_count = max(1, max(values).bit_length())
    mask_count = 1 << bit_count
    witness = array("i", [-1]) * mask_count
    for value in values:
        witness[value] = value

    for bit in range(bit_count):
        bit_mask = 1 << bit
        for mask in range(mask_count):
            if mask & bit_mask and witness[mask] == -1:
                witness[mask] = witness[mask ^ bit_mask]

    full_mask = mask_count - 1
    return [witness[full_mask ^ value] for value in values]
```

### Why the expert code is correct

After processing a set of bits, `witness[mask]` is an input value obtained by
clearing only processed bits from `mask`, if one exists. Induction over all
bits therefore makes it a witness from any submask. A submask of the complement
shares no set bit with the original value, and every compatible input value is
such a submask.

**Complexity:** `O(B * 2^B + n)` time and `O(2^B)` space for `B <= 22`.

## 6. What to remember

```text
AND equals zero -> partner is a submask of the complement
need any partner -> store one witness, not a count
all submasks at once -> SOS propagation
```
