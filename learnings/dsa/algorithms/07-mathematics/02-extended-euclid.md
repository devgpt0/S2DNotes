# Extended Euclidean Algorithm

## Idea

Extended Euclid finds integers `x` and `y` such that:

```text
a*x + b*y = gcd(a, b)
```

These coefficients solve linear Diophantine equations and modular inverses.

## Visual model

Normal Euclid computes remainders; extended Euclid substitutes backward to
express the GCD using the original numbers.

## Classroom board: write GCD as a combination

```text
gcd(30,12)=6
30 = 2*12 + 6
therefore 6 = 30 - 2*12
x=1, y=-2 gives 30*x + 12*y = 6
```

## Steps

1. Base case: `gcd(a, 0) = a`, with coefficients `(1, 0)`.
2. Recursively solve `(b, a mod b)`.
3. Transform its coefficients back to the equation for `(a, b)`.

## First-principles derivation

Euclid's algorithm finds the GCD. Keeping the substitutions used by Euclid
expresses that GCD as `a*x + b*y`.

Those coefficients solve modular inverses and linear Diophantine equations.

## Classroom board: recover the coefficients

Find `x, y` such that `30x + 18y = gcd(30,18)`.

```text
30 = 1*18 + 12
18 = 1*12 + 6
12 = 2*6  + 0

back-substitute:
6 = 18 - 12
  = 18 - (30 - 18)
  = 2*18 - 30

x = -1, y = 2
30*(-1) + 18*2 = 6
```

## Pattern recognition

Use it for modular inverse when the modulus is not known prime, equations
`a*x + b*y = c`, and the Chinese remainder theorem.

## Implementation

### C++

```cpp
struct ExtendedGcd { long long gcd; long long x; long long y; };

ExtendedGcd extendedGcd(long long first, long long second) {
    if (second == 0) return {first, 1, 0};
    const ExtendedGcd next = extendedGcd(second, first % second);
    return {next.gcd, next.y, next.x - (first / second) * next.y};
}
```

### Python

```python
def extended_gcd(first: int, second: int) -> tuple[int, int, int]:
    if second == 0:
        return first, 1, 0
    divisor, next_x, next_y = extended_gcd(second, first % second)
    return divisor, next_y, next_x - (first // second) * next_y
```

### Java

```java
record ExtendedGcd(long gcd, long x, long y) {}

static ExtendedGcd extendedGcd(long first, long second) {
    if (second == 0) return new ExtendedGcd(first, 1, 0);
    ExtendedGcd next = extendedGcd(second, first % second);
    return new ExtendedGcd(next.gcd(), next.y(), next.x() - (first / second) * next.y());
}
```

## Why it works

Substitute `a mod b = a - floor(a/b)*b` into the recursive equation. The
returned coefficient formula is exactly the collected coefficient of `a` and
`b` after that substitution.

## Complexity

Time and recursion space are `O(log min(a, b))`.

## Common mistakes

- Using negative inputs without defining division/remainder behavior.
- Assuming an inverse exists when `gcd(value, modulus) != 1`.
- Overflowing coefficient multiplication for very large inputs.
