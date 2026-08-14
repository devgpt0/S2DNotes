# Primes, Factorization, Divisors, and Sieve Functions

Prime preprocessing turns repeated `sqrt(n)` work into near-linear setup. Pick
the table from the query pattern, not from habit.

## Prime checks and factorization

For one positive `n`, trial divide only up to `d * d <= n`. After removing a
prime factor completely, the exponent is known and the remaining value may be
a final prime.

```python
def factorize(value: int) -> list[tuple[int, int]]:
    if value <= 0:
        raise ValueError("value must be positive")
    factors: list[tuple[int, int]] = []
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            exponent = 0
            while value % divisor == 0:
                value //= divisor
                exponent += 1
            factors.append((divisor, exponent))
        divisor += 1 if divisor == 2 else 2
    if value > 1:
        factors.append((value, 1))
    return factors


print(factorize(360))
```

Output:

```text
[(2, 3), (3, 2), (5, 1)]
```

`1` is not prime and has no prime factors. Trial factorization is `O(sqrt(n))`.

## Smallest prime factor sieve

For many values up to `limit`, store the smallest prime dividing every number.
Each query then factors in `O(log n)` divisions.

```python
def smallest_prime_factors(limit: int) -> list[int]:
    if limit < 1:
        raise ValueError("limit must be positive")
    spf = list(range(limit + 1))
    spf[1] = 1
    for prime in range(2, limit + 1):
        if spf[prime] != prime:
            continue
        for multiple in range(prime * prime, limit + 1, prime):
            if spf[multiple] == multiple:
                spf[multiple] = prime
    return spf


print(smallest_prime_factors(12)[2:])
```

Output:

```text
[2, 3, 2, 5, 2, 7, 2, 3, 2, 11, 2]
```

The ordinary sieve is `O(n log log n)` time and `O(n)` memory. For very large
limits, memory is usually the real constraint in Python.

## Divisor formulas

For `n = p1^e1 * p2^e2 * ...`:

| Quantity | Formula |
| --- | --- |
| number of divisors | `product((ei + 1))` |
| sum of divisors | `product((pi^(ei + 1) - 1) / (pi - 1))` |
| Euler phi | `n * product((pi - 1) / pi)` |

Compute these from factorization. Under a modulus, division in the divisor-sum
formula needs an inverse, so handle a non-coprime denominator separately.

## Multiples sieve

When a function needs contributions from every divisor, iterate the divisor and
visit its multiples. The total work is `O(n log n)`.

```python
def divisor_counts(limit: int) -> list[int]:
    count = [0] * (limit + 1)
    for divisor in range(1, limit + 1):
        for multiple in range(divisor, limit + 1, divisor):
            count[multiple] += 1
    return count


print(divisor_counts(10)[1:])
```

Output:

```text
[1, 2, 2, 3, 2, 4, 2, 4, 3, 4]
```

## Checklist

- One number: trial divide. Many bounded numbers: sieve/SPF.
- Remove a factor repeatedly to get its exponent.
- Enumerate divisors in pairs; avoid adding `sqrt(n)` twice.
- Use the divisor/multiple loop for aggregate values over every integer.
