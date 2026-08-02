# Euler's Totient Function

## Idea

`phi(n)` counts integers from `1` to `n` that are coprime with `n`. If the
distinct prime factors of `n` are `p`, then:

```text
phi(n) = n * product over p of (1 - 1/p)
```

## Visual model

For `n = 12`, remove multiples of prime factors `2` and `3`. The remaining
numbers `1, 5, 7, 11` are coprime, so `phi(12) = 4`.

## Classroom board: `phi(12)`

```text
numbers 1..12
remove multiples of 2 -> 1,3,5,7,9,11
remove multiples of 3 -> 1,5,7,11
four remain, so phi(12)=4
```

## Steps

1. Start `result = n`.
2. Factor `n` into distinct primes.
3. For each prime `p`, set `result -= result / p`.
4. Handle a remaining prime factor after trial division.

## First-principles derivation

`phi(n)` counts integers from `1` to `n` that share no prime factor with
`n`. For each distinct prime factor `p`, remove the fraction `1/p` of
candidates divisible by `p`.

This gives `phi(n) = n * product(1 - 1/p)`.

## Classroom board: compute phi(12)

```text
12 = 2^2 * 3
numbers 1..12: 1 2 3 4 5 6 7 8 9 10 11 12

start answer = 12
remove multiples of 2: answer = 12 - 12/2 = 6
remove multiples of 3: answer =  6 -  6/3 = 4

coprime values: 1, 5, 7, 11
phi(12) = 4
```

Each distinct prime is applied once; its exponent does not create another
removal step.

## Pattern recognition

Use totient for counting coprime residues, multiplicative order, Euler's
theorem, and some modular exponent reductions.

## Implementation

### C++

```cpp
long long totient(long long value) {
    long long result = value;
    for (long long prime = 2; prime <= value / prime; ++prime) {
        if (value % prime != 0) continue;
        while (value % prime == 0) value /= prime;
        result -= result / prime;
    }
    if (value > 1) result -= result / value;
    return result;
}
```

### Python

```python
def totient(value: int) -> int:
    result = value
    prime = 2
    while prime * prime <= value:
        if value % prime == 0:
            while value % prime == 0:
                value //= prime
            result -= result // prime
        prime += 1
    if value > 1:
        result -= result // value
    return result
```

### Java

```java
static long totient(long value) {
    long result = value;
    for (long prime = 2; prime <= value / prime; prime++) {
        if (value % prime != 0) continue;
        while (value % prime == 0) value /= prime;
        result -= result / prime;
    }
    if (value > 1) result -= result / value;
    return result;
}
```

## Why it works

For every distinct prime factor `p`, exactly a `1/p` fraction of the current
candidates are divisible by `p`. Applying each factor once performs the needed
inclusion-exclusion.

## Complexity

Time is `O(sqrt(n))` and space is `O(1)`.

## Common mistakes

- Applying the formula once per prime exponent instead of once per distinct
  prime.
- Forgetting a remaining large prime.
- Assuming `phi(1)` is `0`; by convention it is `1`.
