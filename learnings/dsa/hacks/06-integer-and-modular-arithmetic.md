# Integer and Modular Arithmetic

## First principles

Python integers do not overflow, but arithmetic rules still matter. Reduce
modular values to keep them small, use integer division only when truncation is
intended, and replace modular division with multiplication by an inverse when
that inverse exists.

## Why it matters

Python integers do not overflow, but very large integers become slower. Modulo
rules, division, and negative values still cause wrong answers.

## Technique

- Reduce during long modular calculations.
- Use `pow(base, exponent, modulus)` for modular powers.
- Use `pow(value, -1, modulus)` only when the inverse exists.
- Use `//` for mathematical floor division; understand negative behavior.

## Python patterns

```python
MODULUS = 1_000_000_007

answer = (first + second) % MODULUS
answer = answer * factor % MODULUS
inverse = pow(value, MODULUS - 2, MODULUS)  # only for prime modulus
```

Safe ceiling division for positive divisor:

```python
def ceil_div(numerator: int, denominator: int) -> int:
    return -(-numerator // denominator)
```

Avoid floating point for integer ceilings:

```python
# Wrong for huge integers: math.ceil(numerator / denominator)
# Exact:
groups = (items + capacity - 1) // capacity  # when both are positive
```

## Pattern recognition

Check arithmetic whenever constraints contain `10^18`, answers are requested
modulo a number, or a binary search uses averages/division.

## Visual worked example: normalize before comparing

Modulo `5`:

```text
-3 and 2 represent the same remainder class

Python: -3 % 5 = 2
portable normalization: ((-3 % 5) + 5) % 5 = 2

divide by 2 modulo 5:
inverse of 2 is 3 because 2*3 % 5 = 1
4 / 2 mod 5 = 4*3 % 5 = 2
```

Do not use floating-point `/` when the mathematical result must remain an
exact integer.

## Traps

- Modular division is not `a // b % modulus`.
- Fermat's inverse needs a prime modulus and a nonzero residue.
- Python `%` is non-negative for positive modulus, unlike C++/Java behavior.
- `int(a / b)` converts through float and can lose precision; use integer
  division with the required rounding rule.
