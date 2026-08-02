# Greatest Common Divisor (Euclid's Algorithm)

## Idea

The greatest common divisor (GCD) of `a` and `b` is the largest positive number
dividing both. Replacing `(a, b)` by `(b, a mod b)` preserves the GCD.

## Visual model

```text
gcd(48, 18) -> gcd(18, 12) -> gcd(12, 6) -> gcd(6, 0) = 6
```

## Classroom board: `gcd(48,18)`

```text
48 = 2*18 + 12 -> gcd(48,18) = gcd(18,12)
18 = 1*12 +  6 -> gcd(18,12) = gcd(12,6)
12 = 2* 6 +  0 -> answer 6
```

## Steps

1. While `b` is not zero, replace `(a, b)` with `(b, a mod b)`.
2. The remaining `a` is the GCD.
3. Compute `lcm(a, b) = abs(a / gcd(a, b) * b)` to reduce overflow risk.

## First-principles derivation

A number divides both `a` and `b` exactly when it divides `b` and the
remainder `a mod b`. Replacing the larger pair by the smaller pair therefore
keeps the same common divisors.

Continue until the remainder is zero; the last nonzero value is the GCD.

## Classroom board: Euclid shrinks the pair

```text
gcd(48, 18)
48 = 2 * 18 + 12  -> gcd(18, 12)
18 = 1 * 12 +  6  -> gcd(12, 6)
12 = 2 *  6 +  0  -> gcd = 6
```

The pair becomes strictly smaller each step, so the algorithm terminates.

## Pattern recognition

Use GCD for divisibility, simplifying ratios, periodic alignment, lattice
steps, or checking whether integer linear combinations are possible.

## Implementation

### C++

```cpp
long long gcd(long long first, long long second) {
    first = std::abs(first);
    second = std::abs(second);
    while (second != 0) {
        const long long remainder = first % second;
        first = second;
        second = remainder;
    }
    return first;
}
```

### Python

```python
def gcd(first: int, second: int) -> int:
    first = abs(first)
    second = abs(second)
    while second:
        first, second = second, first % second
    return first
```

### Java

```java
static long gcd(long first, long second) {
    first = Math.abs(first);
    second = Math.abs(second);
    while (second != 0) {
        long remainder = first % second;
        first = second;
        second = remainder;
    }
    return first;
}
```

## Why it works

Any common divisor of `a` and `b` also divides `a - q*b`, including the
remainder. The common divisors therefore never change, while the second value
strictly decreases.

## Complexity

Time is `O(log min(a, b))` and space is `O(1)`.

## Common mistakes

- Dividing before handling `gcd(0, 0)` according to the problem's contract.
- Multiplying before dividing in LCM and overflowing.
- Forgetting sign handling.
