# Chinese Remainder Theorem (CRT)

## Idea

CRT combines congruences. For coprime moduli, the system

```text
x = firstRemainder  (mod firstModulus)
x = secondRemainder (mod secondModulus)
```

has one solution modulo their product.

## Classroom board: two clocks

```text
x mod 3 = 2 -> candidates 2,5,8,11,...
x mod 5 = 1 -> among them 11 works
solutions repeat every 3*5=15: 11,26,41,...
```

## Steps

1. Write `x = firstRemainder + firstModulus * k`.
2. Substitute into the second congruence.
3. Solve for `k` using the modular inverse of the first modulus modulo the
   second modulus.
4. Normalize the result modulo the product.

## First-principles derivation

For coprime moduli, each remainder combination identifies one value modulo the
product. Build a term that is `1` under one modulus and `0` under every
other modulus, then scale it by the wanted remainder.

## Classroom board: combine two congruences

Solve:

```text
x = 2 (mod 3)
x = 3 (mod 5)
```

List the first progression:

```text
2 mod 3 values: 2, 5, 8, 11, 14, ...
first value also 3 mod 5 is 8

x = 8 (mod 15)
check: 8 mod 3 = 2, 8 mod 5 = 3
```

The product `15` is the repeat period because the moduli are coprime.

## Pattern recognition

Use CRT for simultaneous periodic schedules, reconstructing a number from
remainders, or splitting computation across coprime moduli.

## Implementation: two coprime moduli

This uses `extendedGcd` from the [previous note](02-extended-euclid.md).

### C++

```cpp
std::pair<long long, long long> combineCongruences(
    long long firstRemainder, long long firstModulus,
    long long secondRemainder, long long secondModulus) {
    ExtendedGcd result = extendedGcd(firstModulus, secondModulus);
    if (result.gcd != 1) throw std::invalid_argument("moduli must be coprime");
    long long difference = (secondRemainder - firstRemainder) % secondModulus;
    long long multiplier = difference * result.x % secondModulus;
    long long modulus = firstModulus * secondModulus;
    long long remainder = (firstRemainder + firstModulus * multiplier) % modulus;
    if (remainder < 0) remainder += modulus;
    return {remainder, modulus};
}
```

### Python

```python
def combine_congruences(
    first_remainder: int,
    first_modulus: int,
    second_remainder: int,
    second_modulus: int,
) -> tuple[int, int]:
    divisor, inverse, _ = extended_gcd(first_modulus, second_modulus)
    if divisor != 1:
        raise ValueError('moduli must be coprime')
    multiplier = (second_remainder - first_remainder) * inverse % second_modulus
    modulus = first_modulus * second_modulus
    remainder = (first_remainder + first_modulus * multiplier) % modulus
    return remainder, modulus
```

### Java

```java
static long[] combineCongruences(
    long firstRemainder, long firstModulus,
    long secondRemainder, long secondModulus) {
    ExtendedGcd result = extendedGcd(firstModulus, secondModulus);
    if (result.gcd() != 1) throw new IllegalArgumentException("moduli must be coprime");
    long difference = (secondRemainder - firstRemainder) % secondModulus;
    long multiplier = difference * result.x() % secondModulus;
    long modulus = firstModulus * secondModulus;
    long remainder = (firstRemainder + firstModulus * multiplier) % modulus;
    if (remainder < 0) remainder += modulus;
    return new long[] {remainder, modulus};
}
```

## Why it works

The constructed number automatically satisfies the first congruence. The
chosen multiplier makes its difference from the second remainder divisible by
the second modulus.

## Complexity

Time is `O(log min(moduli))` and space follows extended Euclid.

## Common mistakes

- Assuming non-coprime moduli always have a solution; generalized CRT must
  check remainder compatibility.
- Overflowing the modulus product.
- Forgetting to normalize negative remainders.
