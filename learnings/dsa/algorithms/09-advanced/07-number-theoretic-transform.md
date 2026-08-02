# Number-Theoretic Transform (NTT)

## Idea

NTT is a modular version of FFT. It converts polynomial coefficients into
point values, multiplies point-by-point, then transforms back. This changes
polynomial multiplication from `O(n^2)` to `O(n log n)`.

## Visual model

```text
coefficients --NTT--> values at roots
values multiply pointwise
product values --inverse NTT--> product coefficients
```

The common prime `998244353 = 119 * 2^23 + 1` supports power-of-two transform
sizes, with primitive root `3`.

## Classroom board: convolution meaning

```text
(1 + 2x) * (3 + 4x)
coefficient x^0: 1*3 = 3
coefficient x^1: 1*4 + 2*3 = 10
coefficient x^2: 2*4 = 8
result: 3 + 10x + 8x^2
```

NTT computes the same convolution faster for large coefficient lists.

## Steps

1. Pad both coefficient arrays to the same power-of-two size.
2. Bit-reverse the array so iterative butterfly stages are contiguous.
3. Apply forward NTT to both arrays.
4. Multiply corresponding values modulo the prime.
5. Apply inverse NTT and trim to the required result length.

## First-principles derivation

Polynomial multiplication is convolution: every coefficient pair contributes
to the position equal to the sum of their indexes. Directly considering all
pairs is quadratic.

The transform evaluates both polynomials at special modular roots where
multiplication is pointwise; the inverse transform recovers all coefficients.

## Classroom board: see the convolution first

```text
A(x) = 1 + 2x       coefficients [1,2]
B(x) = 3 + 4x       coefficients [3,4]

degree 0: 1*3                 = 3
degree 1: 1*4 + 2*3           = 10
degree 2:       2*4           = 8

A(x)B(x) = 3 + 10x + 8x^2
result coefficients = [3,10,8]
```

NTT computes the same convolution in `O(n log n)` for large arrays; padding
prevents cyclic wraparound from mixing coefficients.

## Pattern recognition

Use NTT for large convolutions, polynomial products, pair-sum frequency counts,
or DP transitions expressible as convolution under a supported modulus.

## Implementation

### C++

```cpp
constexpr int MODULUS = 998244353;
constexpr int PRIMITIVE_ROOT = 3;

int modularPower(long long base, int exponent) {
    long long answer = 1;
    while (exponent > 0) {
        if (exponent & 1) answer = answer * base % MODULUS;
        base = base * base % MODULUS;
        exponent >>= 1;
    }
    return answer;
}

void ntt(std::vector<int>& values, bool inverse) {
    const int size = values.size();
    for (int index = 1, reversed = 0; index < size; ++index) {
        int bit = size >> 1;
        while (reversed & bit) { reversed ^= bit; bit >>= 1; }
        reversed ^= bit;
        if (index < reversed) std::swap(values[index], values[reversed]);
    }
    for (int length = 2; length <= size; length <<= 1) {
        int root = modularPower(PRIMITIVE_ROOT, (MODULUS - 1) / length);
        if (inverse) root = modularPower(root, MODULUS - 2);
        for (int start = 0; start < size; start += length) {
            long long power = 1;
            for (int offset = 0; offset < length / 2; ++offset) {
                int even = values[start + offset];
                int odd = static_cast<int>(values[start + offset + length / 2] * power % MODULUS);
                values[start + offset] = even + odd < MODULUS ? even + odd : even + odd - MODULUS;
                values[start + offset + length / 2] = even - odd >= 0 ? even - odd : even - odd + MODULUS;
                power = power * root % MODULUS;
            }
        }
    }
    if (inverse) {
        int inverseSize = modularPower(size, MODULUS - 2);
        for (int& value : values) value = static_cast<int>(1LL * value * inverseSize % MODULUS);
    }
}

std::vector<int> multiplyPolynomials(std::vector<int> first, std::vector<int> second) {
    if (first.empty() || second.empty()) return {};
    const int resultSize = first.size() + second.size() - 1;
    int size = 1;
    while (size < resultSize) size <<= 1;
    first.resize(size);
    second.resize(size);
    ntt(first, false);
    ntt(second, false);
    for (int index = 0; index < size; ++index) first[index] = static_cast<int>(1LL * first[index] * second[index] % MODULUS);
    ntt(first, true);
    first.resize(resultSize);
    return first;
}
```

### Python

```python
MODULUS = 998_244_353
PRIMITIVE_ROOT = 3


def ntt(values: list[int], inverse: bool) -> None:
    size = len(values)
    reversed_index = 0
    for index in range(1, size):
        bit = size >> 1
        while reversed_index & bit:
            reversed_index ^= bit
            bit >>= 1
        reversed_index ^= bit
        if index < reversed_index:
            values[index], values[reversed_index] = values[reversed_index], values[index]
    length = 2
    while length <= size:
        root = pow(PRIMITIVE_ROOT, (MODULUS - 1) // length, MODULUS)
        if inverse:
            root = pow(root, MODULUS - 2, MODULUS)
        for start in range(0, size, length):
            power = 1
            for offset in range(length // 2):
                even = values[start + offset]
                odd = values[start + offset + length // 2] * power % MODULUS
                values[start + offset] = (even + odd) % MODULUS
                values[start + offset + length // 2] = (even - odd) % MODULUS
                power = power * root % MODULUS
        length *= 2
    if inverse:
        inverse_size = pow(size, MODULUS - 2, MODULUS)
        for index in range(size):
            values[index] = values[index] * inverse_size % MODULUS


def multiply_polynomials(first: list[int], second: list[int]) -> list[int]:
    if not first or not second:
        return []
    result_size = len(first) + len(second) - 1
    size = 1
    while size < result_size:
        size *= 2
    left = first + [0] * (size - len(first))
    right = second + [0] * (size - len(second))
    ntt(left, False)
    ntt(right, False)
    for index in range(size):
        left[index] = left[index] * right[index] % MODULUS
    ntt(left, True)
    return left[:result_size]
```

### Java

```java
static final int MODULUS = 998_244_353;
static final int PRIMITIVE_ROOT = 3;

static int modularPower(long base, int exponent) {
    long answer = 1;
    while (exponent > 0) {
        if ((exponent & 1) == 1) answer = answer * base % MODULUS;
        base = base * base % MODULUS;
        exponent >>= 1;
    }
    return (int) answer;
}

static void ntt(int[] values, boolean inverse) {
    int size = values.length;
    for (int index = 1, reversed = 0; index < size; index++) {
        int bit = size >> 1;
        while ((reversed & bit) != 0) { reversed ^= bit; bit >>= 1; }
        reversed ^= bit;
        if (index < reversed) {
            int temporary = values[index]; values[index] = values[reversed]; values[reversed] = temporary;
        }
    }
    for (int length = 2; length <= size; length <<= 1) {
        int root = modularPower(PRIMITIVE_ROOT, (MODULUS - 1) / length);
        if (inverse) root = modularPower(root, MODULUS - 2);
        for (int start = 0; start < size; start += length) {
            long power = 1;
            for (int offset = 0; offset < length / 2; offset++) {
                int even = values[start + offset];
                int odd = (int) (values[start + offset + length / 2] * power % MODULUS);
                values[start + offset] = even + odd < MODULUS ? even + odd : even + odd - MODULUS;
                values[start + offset + length / 2] = even - odd >= 0 ? even - odd : even - odd + MODULUS;
                power = power * root % MODULUS;
            }
        }
    }
    if (inverse) {
        int inverseSize = modularPower(size, MODULUS - 2);
        for (int index = 0; index < size; index++) values[index] = (int) ((long) values[index] * inverseSize % MODULUS);
    }
}

static int[] multiplyPolynomials(int[] first, int[] second) {
    if (first.length == 0 || second.length == 0) return new int[0];
    int resultSize = first.length + second.length - 1;
    int size = 1;
    while (size < resultSize) size <<= 1;
    int[] left = Arrays.copyOf(first, size);
    int[] right = Arrays.copyOf(second, size);
    ntt(left, false);
    ntt(right, false);
    for (int index = 0; index < size; index++) left[index] = (int) ((long) left[index] * right[index] % MODULUS);
    ntt(left, true);
    return Arrays.copyOf(left, resultSize);
}
```

## Why it works

A degree-`d` polynomial is determined by enough point values. Convolution in
coefficient form becomes pointwise multiplication after evaluation. The
inverse transform interpolates the product coefficients.

## Complexity

Time is `O(n log n)` and space is `O(n)`, where `n` is the padded power-of-two
size.

## Common mistakes

- Using a transform size that does not divide `MODULUS - 1`.
- Forgetting inverse normalization.
- Passing negative or unreduced coefficients without normalization.
- Expecting coefficients under a different modulus without CRT or another
  suitable transform.
