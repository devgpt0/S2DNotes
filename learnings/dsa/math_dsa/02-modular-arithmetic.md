# Modular Arithmetic, Fast Power, and Inverses

Modulo `m` keeps only a remainder in `0..m-1`. Reduce after every addition,
subtraction, and multiplication when a statement requests an answer modulo `m`.

## Laws and subtraction

`(a + b) % m`, `(a - b) % m`, and `(a * b) % m` may be reduced at any point.
Python already returns a non-negative remainder for positive `m`.

```python
modulus = 7
print((3 - 5) % modulus)
print((6 * 6) % modulus)
```

Output:

```text
5
1
```

Do not divide modulo `m` with `/` or `//`. Division needs an inverse and that
inverse may not exist.

## Binary exponentiation

Square the base and consume one bit of the exponent each iteration. `pow(base,
exponent, modulus)` is Python's tested implementation and runs in `O(log exponent)`.

```python
print(pow(3, 13, 1_000_000_007))
```

Output:

```text
1594323
```

Use it for enormous powers, matrix powers, and Fermat inverses.

## Modular inverse

`x` has an inverse modulo `m` exactly when `gcd(x, m) == 1`. If `m` is prime
and `x % m != 0`, Fermat gives `x^(m-2) mod m`; otherwise use extended GCD.

```python
MODULUS = 1_000_000_007


def inverse_prime(value: int) -> int:
    value %= MODULUS
    if value == 0:
        raise ValueError("zero has no inverse modulo MODULUS")
    return pow(value, MODULUS - 2, MODULUS)


print(7 * inverse_prime(7) % MODULUS)
```

Output:

```text
1
```

Fermat's formula is wrong for a composite modulus unless a separate theorem
proves it for that case.

## Prefix products and range products

With a prime modulus and nonzero values, store `prefix[i] = a[0] * ... * a[i-1]`.
Then product `[left, right)` is `prefix[right] * inverse(prefix[left]) % m`.
If zeros can appear, track zero counts separately; an inverse of zero does not
exist.

## Checklist

- Normalize subtraction with `% modulus`.
- Use `pow(a, b, m)`, not `a**b % m` for huge exponents.
- Check whether the modulus is prime before Fermat inversion.
- For combinations, also check `n < modulus`; otherwise use Lucas or
  prime-power methods from the advanced track.
