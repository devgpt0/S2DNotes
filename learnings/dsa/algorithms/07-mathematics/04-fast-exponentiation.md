# Fast Exponentiation

## Idea

Binary exponentiation computes `base^exponent` by reading exponent bits. Square
the base each step and multiply it into the answer when the current bit is `1`.

## Visual model

```text
13 = 1101₂ -> base^13 = base^8 * base^4 * base^1
```

## Classroom board: compute `3^13`

```text
13 = 8+4+1 = 1101₂
powers by squaring: 3, 9, 81, 6561
select bit powers 1,4,8 -> 3 * 81 * 6561
```

Only one square is needed per exponent bit.

## Steps

1. Start `answer = 1`.
2. If the exponent is odd, multiply the current base into the answer.
3. Square the base.
4. Divide the exponent by two.
5. Repeat until the exponent is zero.

## First-principles derivation

Multiplying `base` exactly `exponent` times repeats work. Squaring creates
powers `base^1, base^2, base^4, ...`; the binary digits of the exponent choose
which powers belong in the answer.

The invariant is
`answer * base^remaining_exponent = original_base^original_exponent`.

## Classroom board: compute 3^13

`13 = 8 + 4 + 1 = 1101` in binary.

```text
remaining  bit  answer       base
13         1    1*3 = 3      3^2 = 9
 6         0    3            9^2 = 81
 3         1    3*81 = 243   81^2 = 6561
 1         1    243*6561     done

answer = 1,594,323
```

Only four loop iterations are needed because the exponent is halved each time.

## Pattern recognition

Use it for huge powers, modular inverses under a prime modulus, matrix powers,
or repeatedly applying an associative operation.

## Implementation: modular power

### C++

```cpp
long long powerModulo(long long base, long long exponent, long long modulus) {
    base %= modulus;
    long long answer = 1 % modulus;
    while (exponent > 0) {
        if (exponent & 1) answer = answer * base % modulus;
        base = base * base % modulus;
        exponent >>= 1;
    }
    return answer;
}
```

### Python

```python
def power_modulo(base: int, exponent: int, modulus: int) -> int:
    base %= modulus
    answer = 1 % modulus
    while exponent:
        if exponent & 1:
            answer = answer * base % modulus
        base = base * base % modulus
        exponent >>= 1
    return answer
```

### Java

```java
static long powerModulo(long base, long exponent, long modulus) {
    base %= modulus;
    long answer = 1 % modulus;
    while (exponent > 0) {
        if ((exponent & 1) == 1) answer = answer * base % modulus;
        base = base * base % modulus;
        exponent >>= 1;
    }
    return answer;
}
```

## Why it works

Each exponent bit selects one power `base^(2^bit)`. Squaring creates the next
power, so every selected power is multiplied once.

## Complexity

Time is `O(log exponent)` and space is `O(1)`.

## Common mistakes

- Forgetting exponent `0`.
- Using it for negative exponents without defining inverses.
- Overflowing multiplication before modulo; use a wider type or safe modular
  multiplication when the modulus is very large.
