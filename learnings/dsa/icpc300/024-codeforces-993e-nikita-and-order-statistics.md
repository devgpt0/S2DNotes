# ICPC300 024: Codeforces 993E - Nikita and Order Statistics

**Source:** [Codeforces 993E - Nikita and Order Statistics](https://codeforces.com/problemset/problem/993/E)  
**Pattern:** prefix-count correlation with exact CRT convolution

## Exact contract

Input gives `n` and `x` (`1 <= n <= 200000`) and an array of `n` integers.
For every `k` from `0` through `n`, output the number of nonempty contiguous
subarrays containing exactly `k` elements strictly smaller than `x`.

## First principles

Replace each value by `1` if it is below `x`, otherwise `0`. Let `prefix[i]`
be the sum before position `i`. Subarray `[left, right)` contains `k` small
values exactly when `prefix[right] - prefix[left] = k`.

Prefix values never decrease. If `frequency[v]` counts prefix value `v`, then:

- for `k = 0`, choose two distinct equal prefixes;
- for `k > 0`, every prefix with value `v` occurs before every prefix with
  value `v+k`, so the contribution is `frequency[v] * frequency[v+k]`.

All positive-`k` answers are one correlation of the frequency array.

## Cases that decide correctness

- `k = 0` uses `c * (c - 1) / 2`, not `c * c`.
- Values equal to `x` are not smaller and become zero.
- If no value is smaller than `x`, answer zero is `n(n+1)/2` and all others
  are zero.
- Answers can exceed `998244353`; a single modular NTT would be wrong. Two
  NTT primes and the Chinese remainder theorem recover exact integers.

## Brute force: recompute every subarray

```python
def count_subarrays_brute(values: list[int], threshold: int) -> list[int]:
    answers = [0] * (len(values) + 1)
    for left in range(len(values)):
        for right in range(left, len(values)):
            small_count = sum(value < threshold for value in values[left : right + 1])
            answers[small_count] += 1
    return answers
```

**Complexity:** `O(n^3)` time and `O(n)` output space.

## Better: extend each left endpoint once

```python
def count_subarrays_quadratic(values: list[int], threshold: int) -> list[int]:
    answers = [0] * (len(values) + 1)
    for left in range(len(values)):
        small_count = 0
        for right in range(left, len(values)):
            small_count += values[right] < threshold
            answers[small_count] += 1
    return answers
```

The running count removes the repeated scan inside each subarray.

**Complexity:** `O(n^2)` time and `O(n)` space.

## Expert solution: correlate frequencies under two primes

```python
import sys


MODULUS_1 = 998_244_353
MODULUS_2 = 1_004_535_809
PRIMITIVE_ROOT = 3


def ntt(values: list[int], invert: bool, modulus: int) -> None:
    size = len(values)
    target = 0
    for index in range(1, size):
        bit = size >> 1
        while target & bit:
            target ^= bit
            bit >>= 1
        target ^= bit
        if index < target:
            values[index], values[target] = values[target], values[index]

    block_size = 2
    while block_size <= size:
        root = pow(PRIMITIVE_ROOT, (modulus - 1) // block_size, modulus)
        if invert:
            root = pow(root, modulus - 2, modulus)
        half = block_size // 2

        for block_start in range(0, size, block_size):
            factor = 1
            for offset in range(half):
                even = values[block_start + offset]
                odd = values[block_start + offset + half] * factor % modulus
                values[block_start + offset] = (even + odd) % modulus
                values[block_start + offset + half] = (even - odd) % modulus
                factor = factor * root % modulus
        block_size <<= 1

    if invert:
        inverse_size = pow(size, modulus - 2, modulus)
        for index, value in enumerate(values):
            values[index] = value * inverse_size % modulus


def convolution_mod(left: list[int], right: list[int], modulus: int) -> list[int]:
    result_length = len(left) + len(right) - 1
    size = 1
    while size < result_length:
        size <<= 1
    left_values = left + [0] * (size - len(left))
    right_values = right + [0] * (size - len(right))

    ntt(left_values, False, modulus)
    ntt(right_values, False, modulus)
    for index in range(size):
        left_values[index] = left_values[index] * right_values[index] % modulus
    ntt(left_values, True, modulus)
    return left_values[:result_length]


def exact_convolution(left: list[int], right: list[int]) -> list[int]:
    residues_1 = convolution_mod(left, right, MODULUS_1)
    residues_2 = convolution_mod(left, right, MODULUS_2)
    modulus_1_inverse = pow(MODULUS_1, -1, MODULUS_2)
    result = [0] * len(residues_1)

    for index, residue_1 in enumerate(residues_1):
        multiplier = (residues_2[index] - residue_1) % MODULUS_2
        multiplier = multiplier * modulus_1_inverse % MODULUS_2
        result[index] = residue_1 + MODULUS_1 * multiplier
    return result


def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    length, threshold = data[0], data[1]
    values = data[2:]
    frequencies = [0] * (length + 1)
    prefix_count = 0
    frequencies[0] = 1

    for value in values:
        prefix_count += value < threshold
        frequencies[prefix_count] += 1

    products = exact_convolution(frequencies, frequencies[::-1])
    answers = [sum(count * (count - 1) // 2 for count in frequencies)]
    answers.extend(products[length - difference] for difference in range(1, length + 1))
    print(*answers)


if __name__ == "__main__":
    solve()
```

The product of the two moduli is far larger than the maximum possible answer
`n(n+1)/2`, so CRT reconstruction is unique. Reversal places correlation
difference `k` at convolution index `n-k`.

**Complexity:** `O(n log n)` time and `O(n)` space.

