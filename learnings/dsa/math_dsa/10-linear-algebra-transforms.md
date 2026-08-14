# Gaussian Elimination, Polynomials, FFT, and NTT

These are high-end tools for the upper part of the target range. Use them only
after proving the problem truly reduces to equations or polynomial convolution.

## Gaussian elimination

Row reduction solves a linear system and identifies no solution or infinitely
many solutions. Over real values, choose the largest available pivot and use an
epsilon. Over a prime modulus, divide by multiplying a modular inverse; over a
composite modulus, ordinary elimination can fail because pivots need not invert.

| Result | Row-reduced evidence |
| --- | --- |
| unique solution | pivot in every variable column |
| no solution | row `0 ... 0 | nonzero` |
| multiple solutions | at least one free variable and no contradiction |

The usual dense algorithm is `O(n^3)`. For exact integer equations, first ask
whether modular methods or an invariant avoids division altogether.

## Polynomial convolution

If arrays hold polynomial coefficients, their convolution is
`result[k] = sum(left[i] * right[k-i])`. Naive convolution is `O(n*m)` and is
often faster for small arrays. FFT/NTT lowers long, dense multiplication to
`O(n log n)`.

## Number-theoretic transform

NTT is an exact FFT modulo a suitable prime. `998244353 = 119 * 2^23 + 1` with
primitive root `3` supports power-of-two transform sizes through `2^23`.
The template below is only for coefficients modulo that prime.

```python
MODULUS = 998_244_353
PRIMITIVE_ROOT = 3


def ntt(values: list[int], invert: bool) -> None:
    size = len(values)
    index = 0
    for value in range(1, size):
        bit = size >> 1
        while index & bit:
            index ^= bit
            bit >>= 1
        index ^= bit
        if value < index:
            values[value], values[index] = values[index], values[value]

    length = 2
    while length <= size:
        root = pow(PRIMITIVE_ROOT, (MODULUS - 1) // length, MODULUS)
        if invert:
            root = pow(root, MODULUS - 2, MODULUS)
        half = length // 2
        for start in range(0, size, length):
            weight = 1
            for offset in range(half):
                even = values[start + offset]
                odd = values[start + offset + half] * weight % MODULUS
                values[start + offset] = (even + odd) % MODULUS
                values[start + offset + half] = (even - odd) % MODULUS
                weight = weight * root % MODULUS
        length *= 2

    if invert:
        inverse_size = pow(size, MODULUS - 2, MODULUS)
        for index, value in enumerate(values):
            values[index] = value * inverse_size % MODULUS


def convolution(left: list[int], right: list[int]) -> list[int]:
    if not left or not right:
        return []
    target_size = len(left) + len(right) - 1
    size = 1
    while size < target_size:
        size *= 2
    first = [value % MODULUS for value in left] + [0] * (size - len(left))
    second = [value % MODULUS for value in right] + [0] * (size - len(right))
    ntt(first, invert=False)
    ntt(second, invert=False)
    for index in range(size):
        first[index] = first[index] * second[index] % MODULUS
    ntt(first, invert=True)
    return first[:target_size]


print(convolution([1, 2, 3], [4, 5]))
```

Output:

```text
[4, 13, 22, 15]
```

## Checklist

- Count operations: NTT helps only when naive convolution is too slow.
- NTT length must be a supported power of two for its modulus.
- Distinguish real-valued FFT rounding from exact modular NTT.
- In elimination, define the coefficient field before dividing by a pivot.
