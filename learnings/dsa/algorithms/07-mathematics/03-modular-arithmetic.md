# Modular Arithmetic

## Idea

Modulo keeps large integer results in a fixed range. Addition, subtraction,
and multiplication can reduce operands without changing the final remainder.

```text
(a + b) mod m = ((a mod m) + (b mod m)) mod m
(a * b) mod m = ((a mod m) * (b mod m)) mod m
```

Division is multiplication by a modular inverse, not normal integer division.

## Classroom board: a clock of size 5

```text
8 mod 5 = 3
12 mod 5 = 2
(8+12) mod 5 = 20 mod 5 = 0
(3+2) mod 5 = 0  -> same answer with small representatives
```

## Steps

1. Normalize negative values into `[0, modulus)`.
2. Reduce after additions and multiplications.
3. Before division by `b`, prove an inverse exists.
4. For prime modulus `p` and `b` not divisible by `p`, use
   `b^(p-2) mod p`.

## First-principles derivation

Modulo `m`, numbers with the same remainder are equivalent. Addition and
multiplication preserve this equivalence, so values can be reduced after each
operation.

Division is different: divide by `b` only by multiplying with an inverse that
exists when `gcd(b,m)=1`.

## Classroom board: work with remainder classes

Modulo `7`:

```text
17 is equivalent to 3
 9 is equivalent to 2

(17 + 9) mod 7 = (3 + 2) mod 7 = 5
(17 * 9) mod 7 = (3 * 2) mod 7 = 6

inverse of 3 is 5 because 3*5 mod 7 = 1
10 / 3 mod 7 = 10*5 mod 7 = 1
```

Normalize negative results because language remainder operators may return a
negative value.

## Pattern recognition

Use it when the statement asks for an answer modulo a number, counts grow
huge, or cyclic arithmetic is involved.

## Implementation: safe basic operations

### C++

```cpp
long long normalize(long long value, long long modulus) {
    value %= modulus;
    return value < 0 ? value + modulus : value;
}

long long addModulo(long long first, long long second, long long modulus) {
    return (normalize(first, modulus) + normalize(second, modulus)) % modulus;
}
```

### Python

```python
def normalize(value: int, modulus: int) -> int:
    return value % modulus


def add_modulo(first: int, second: int, modulus: int) -> int:
    return (first + second) % modulus
```

### Java

```java
static long normalize(long value, long modulus) {
    value %= modulus;
    return value < 0 ? value + modulus : value;
}

static long addModulo(long first, long second, long modulus) {
    return (normalize(first, modulus) + normalize(second, modulus)) % modulus;
}
```

## Why it works

Numbers with the same remainder differ by a multiple of the modulus. Adding or
multiplying such differences still produces a multiple of the modulus.

## Complexity

Each shown operation is `O(1)` for fixed-width integers.

## Common mistakes

- Treating `(a / b) % m` as modular division.
- Forgetting C++/Java `%` can return a negative value.
- Multiplying two 64-bit values before reducing when their product can overflow.
- Using Fermat's inverse when the modulus is not prime.
