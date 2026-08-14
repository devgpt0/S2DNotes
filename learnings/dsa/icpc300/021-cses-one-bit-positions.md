# ICPC300 021: CSES - One Bit Positions

**Source:** [CSES - One Bit Positions](https://cses.fi/problemset/task/2110/)  
**Pattern:** cross-correlation with the number theoretic transform (NTT)

## Exact contract

The input is one binary string `s` of length `n`, where
`2 <= n <= 200000`. For every distance `d` from `1` through `n - 1`, output
the number of index pairs `(i, j)` such that `i < j`, `j - i = d`, and both
`s[i]` and `s[j]` are `1`. Output the `n - 1` answers in increasing order of
`d`.

## First principles

For a fixed distance `d`, every possible pair has the forced form `(i, i+d)`.
Its contribution is therefore `a[i] * a[i+d]`, where `a` is the zero-one
array represented by the string. The required answer is a cross-correlation:

`answer[d] = sum(a[i] * a[i+d])`.

Convolution can calculate all correlations together. If `b` is `a` reversed,
then coefficient `n - 1 - d` of `a * b` is exactly `answer[d]`.

## Cases that decide correctness

- Distances start at `1`; pairs of a position with itself are not requested.
- A string with fewer than two ones produces only zeroes.
- The last answer, for `d = n - 1`, considers only `(0, n - 1)`.
- Every answer is at most `n`, so one convolution modulo `998244353` is exact,
  not merely a modular answer.

## Brute force: test every forced pair

```python
def count_one_pairs_brute(bits: str) -> list[int]:
    length = len(bits)
    return [
        sum(
            bits[index] == "1" and bits[index + distance] == "1"
            for index in range(length - distance)
        )
        for distance in range(1, length)
    ]
```

For each distance this checks every legal left endpoint.

**Complexity:** `O(n^2)` time and `O(n)` output space.

## Better for sparse strings: enumerate pairs of ones

```python
def count_one_pairs_sparse(bits: str) -> list[int]:
    one_positions = [index for index, bit in enumerate(bits) if bit == "1"]
    answers = [0] * (len(bits) - 1)

    for left_index, left_position in enumerate(one_positions):
        for right_position in one_positions[left_index + 1 :]:
            answers[right_position - left_position - 1] += 1

    return answers
```

This does no work for zero bits. It is a real improvement when the number of
ones `z` is small, but is still quadratic when the string is dense.

**Complexity:** `O(n + z^2)` time and `O(n + z)` space.

## Expert solution: one exact NTT convolution

```python
import sys


MODULUS = 998_244_353
PRIMITIVE_ROOT = 3


def ntt(values: list[int], invert: bool) -> None:
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
        root = pow(PRIMITIVE_ROOT, (MODULUS - 1) // block_size, MODULUS)
        if invert:
            root = pow(root, MODULUS - 2, MODULUS)

        half = block_size // 2
        for block_start in range(0, size, block_size):
            factor = 1
            for offset in range(half):
                even = values[block_start + offset]
                odd = values[block_start + offset + half] * factor % MODULUS
                values[block_start + offset] = (even + odd) % MODULUS
                values[block_start + offset + half] = (even - odd) % MODULUS
                factor = factor * root % MODULUS
        block_size <<= 1

    if invert:
        inverse_size = pow(size, MODULUS - 2, MODULUS)
        for index, value in enumerate(values):
            values[index] = value * inverse_size % MODULUS


def convolution(left: list[int], right: list[int]) -> list[int]:
    result_length = len(left) + len(right) - 1
    size = 1
    while size < result_length:
        size <<= 1

    left_values = left + [0] * (size - len(left))
    right_values = right + [0] * (size - len(right))
    ntt(left_values, False)
    ntt(right_values, False)

    for index in range(size):
        left_values[index] = left_values[index] * right_values[index] % MODULUS

    ntt(left_values, True)
    return left_values[:result_length]


def solve() -> None:
    bits = sys.stdin.readline().strip()
    values = [int(bit) for bit in bits]
    products = convolution(values, values[::-1])
    answers = [products[len(bits) - 1 - distance] for distance in range(1, len(bits))]
    print(*answers)


if __name__ == "__main__":
    solve()
```

The transform converts convolution into pointwise multiplication. The inverse
transform returns every coefficient, and reversing the second array places
distance `d` at coefficient `n - 1 - d`.

**Complexity:** `O(n log n)` time and `O(n)` space.

