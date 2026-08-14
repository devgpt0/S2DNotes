# Bits, XOR, Binary Basis, and Subset Enumeration

Bits turn a set of yes/no choices into an integer. They are central whenever a
statement mentions parity, toggles, masks, powers of two, or XOR.

## Essential operations

| Operation | Python | Meaning |
| --- | --- | --- |
| test bit `k` | `(mask >> k) & 1` | `0` or `1` |
| set bit `k` | `mask | (1 << k)` | force it to one |
| clear bit `k` | `mask & ~(1 << k)` | force it to zero |
| toggle bit `k` | `mask ^ (1 << k)` | flip it |
| lowest set bit | `mask & -mask` | isolate rightmost one |
| remove lowest set bit | `mask & (mask - 1)` | useful in bit loops |
| number of set bits | `mask.bit_count()` | popcount |

Python's `~mask` conceptually has infinitely many leading one bits. Always
combine it with a finite mask or use it only to clear known bit positions.

## XOR invariant

XOR is associative and commutative, `x ^ x == 0`, and `x ^ 0 == x`. Therefore
XOR of a multiset cancels values that occur an even number of times.

```python
numbers = [4, 1, 4, 7, 1]
answer = 0
for number in numbers:
    answer ^= number

print(answer)
```

Output:

```text
7
```

For a range XOR, use a prefix-XOR pattern exactly like prefix sums because
`prefix[right] ^ prefix[left]` cancels the shared prefix.

## Enumerate subsets

For `n <= 20` to `22`, every subset of `n` items is often feasible. Bit `i`
represents whether item `i` is selected; there are `2^n` masks.

```python
values = [2, 5, 9]
subset_sums: list[int] = []

for mask in range(1 << len(values)):
    total = sum(values[index] for index in range(len(values)) if mask & (1 << index))
    subset_sums.append(total)

print(subset_sums)
```

Output:

```text
[0, 2, 5, 7, 9, 11, 14, 16]
```

To enumerate every submask of a fixed `mask`, use
`submask = (submask - 1) & mask` until zero. Across all masks this is `O(3^n)`.

## XOR basis

An XOR basis stores numbers with distinct highest set bits. Insert `value` by
XORing away every existing leading bit; if a new leading bit remains, store it.
It answers maximum subset XOR, whether an XOR target is representable, and the
number of distinct subset XORs. This is `O(B)` per insertion for `B` bits.

Do not use a basis when the problem needs ordinary sums: XOR has no carry and
is a different algebra.

## Checklist

- Use a bitmask only when the state has a small number of independent flags.
- Confirm whether the operation is XOR, OR, AND, or ordinary addition.
- `2^n` is not feasible for `n = 40`; use meet-in-the-middle or another idea.
- Treat bit width explicitly when porting fixed-width C++ logic to Python.
