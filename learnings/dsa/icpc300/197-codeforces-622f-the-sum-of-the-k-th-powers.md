# ICPC300 197: Codeforces 622F - The Sum of the k-th Powers

**Source:** [Codeforces 622F - The Sum of the k-th Powers](https://codeforces.com/problemset/problem/622/F)  
**Rating:** 2300  
**Pattern:** Lagrange interpolation on consecutive points  
**Goal:** Compute `1^k + 2^k + ... + n^k` modulo `1_000_000_007` when `n` is
too large to iterate.

## 1. First principles

The prefix sum of `i^k` is a polynomial in `n` of degree `k+1`. Its values at
`0, 1, ..., k+1` determine it uniquely. For consecutive interpolation points,
the denominator of basis `i` is

```text
i! * (k + 1 - i)! * (-1)^(k + 1 - i)
```

Prefix and suffix products of `(n-j)` provide every numerator in linear time.

## 2. Cases that decide correctness

- `k = 0` returns `n`.
- Sample point zero has prefix sum zero.
- If `n <= k+1`, return the already computed sample directly.
- Negative Lagrange signs are reduced modulo the prime.
- The source bounds keep the polynomial degree below the modulus.

## 3. Brute force: sum every power

```python
MODULO = 1_000_000_007


def power_sum_brute(n: int, exponent: int) -> int:
    if n <= 0 or exponent < 0:
        raise ValueError("n must be positive and exponent nonnegative")
    return sum(pow(value, exponent, MODULO) for value in range(1, n + 1)) % MODULO
```

**Complexity:** `O(n log k)` time and `O(1)` extra space.

## 4. Better transition: evaluate the prefix-sum polynomial

Ordinary Lagrange interpolation would spend quadratic time multiplying all
`n-j` factors for every basis. Consecutive integer points expose factorial
denominators, and two product scans reuse all numerator factors.

## 5. Expert solution: linear consecutive-point interpolation

```python
MODULO = 1_000_000_007


def power_sum_lagrange(n: int, exponent: int) -> int:
    if n <= 0 or exponent < 0:
        raise ValueError("n must be positive and exponent nonnegative")

    degree = exponent + 1
    samples = [0] * (degree + 1)
    for value in range(1, degree + 1):
        samples[value] = (samples[value - 1] + pow(value, exponent, MODULO)) % MODULO
    if n <= degree:
        return samples[n]

    factorial = [1] * (degree + 1)
    for value in range(1, degree + 1):
        factorial[value] = factorial[value - 1] * value % MODULO
    inverse_factorial = [1] * (degree + 1)
    inverse_factorial[degree] = pow(factorial[degree], MODULO - 2, MODULO)
    for value in range(degree, 0, -1):
        inverse_factorial[value - 1] = inverse_factorial[value] * value % MODULO

    prefix_product = [1] * (degree + 2)
    for point in range(degree + 1):
        prefix_product[point + 1] = prefix_product[point] * (n - point) % MODULO
    suffix_product = [1] * (degree + 2)
    for point in range(degree, -1, -1):
        suffix_product[point] = suffix_product[point + 1] * (n - point) % MODULO

    answer = 0
    for point, sample in enumerate(samples):
        term = sample * prefix_product[point] % MODULO
        term = term * suffix_product[point + 1] % MODULO
        term = term * inverse_factorial[point] % MODULO
        term = term * inverse_factorial[degree - point] % MODULO
        if (degree - point) % 2 == 1:
            answer -= term
        else:
            answer += term
    return answer % MODULO
```

### Why the expert code is correct

Faulhaber's result makes the target a degree-`k+1` polynomial, and the computed
samples are its exact values at `k+2` distinct field points. Each loop term is
the corresponding Lagrange basis value at `n`, using the correct factorial
denominator and sign. Polynomial uniqueness therefore makes the sum exact.

**Complexity:** `O(k log k + log MODULO)` time and `O(k)` space.

## 6. What to remember

```text
sum of k-th powers -> polynomial of degree k+1
consecutive sample points -> factorial denominators
all basis numerators -> prefix and suffix products
```
