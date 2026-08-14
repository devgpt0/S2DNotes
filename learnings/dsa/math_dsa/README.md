# Mathematics for Codeforces: 0 to 2500

This is a practical mathematics track for Codeforces problems rated through
roughly 2500. It teaches recognition and implementation, not school-style
proofs for their own sake. Ratings are approximate: a 1200 problem can hide an
advanced idea, and a 2400 problem can need only one formula plus a hard DP.

## Study order

| Rating band | Learn to recognize | Notes |
| --- | --- | --- |
| 0-800 | simulation, parity, digit arithmetic, direct formulas | [01](01-integers-gcd.md) |
| 800-1200 | divisibility, GCD/LCM, remainders, counting multiples | [01](01-integers-gcd.md), [02](02-modular-arithmetic.md) |
| 1200-1500 | fast power, modular inverse, prime tests, factorization | [02](02-modular-arithmetic.md), [03](03-primes-divisors.md) |
| 1500-1800 | sieve, SPF, combinations, XOR, subset masks | [03](03-primes-divisors.md), [04](04-combinatorics.md), [05](05-bits-xor.md), [11](11-pnc-patterns.md) |
| 1800-2100 | inclusion-exclusion, matrices, expectation, games | [04](04-combinatorics.md), [06](06-recurrences-matrices.md), [08](08-probability-games.md), [12](12-probability-patterns.md) |
| 2100-2300 | extended GCD, CRT, phi, Mobius, geometry | [07](07-advanced-number-theory.md), [09](09-geometry.md) |
| 2300-2500 | Gaussian elimination, convex hull, FFT/NTT, discrete log | [07](07-advanced-number-theory.md), [09](09-geometry.md), [10](10-linear-algebra-transforms.md) |

## Complete topic map

1. [Integer arithmetic, divisibility, GCD, and LCM](01-integers-gcd.md)
2. [Modular arithmetic, fast power, and inverses](02-modular-arithmetic.md)
3. [Primes, SPF, factorization, divisors, and sieve functions](03-primes-divisors.md)
4. [Combinatorics and inclusion-exclusion](04-combinatorics.md)
5. [Bits, XOR, binary basis, and subset enumeration](05-bits-xor.md)
6. [Recurrences, matrix exponentiation, and linear recurrences](06-recurrences-matrices.md)
7. [Advanced number theory: extended GCD, CRT, phi, Mobius, BSGS](07-advanced-number-theory.md)
8. [Probability, expected value, and impartial games](08-probability-games.md)
9. [Geometry and lattice points](09-geometry.md)
10. [Gaussian elimination, polynomials, FFT, and NTT](10-linear-algebra-transforms.md)
11. [PnC patterns with worked questions](11-pnc-patterns.md)
12. [Probability patterns with worked questions](12-probability-patterns.md)

## Contest decision guide

| Statement signal | First tool to test |
| --- | --- |
| "divides", "common", "period", "equal groups" | GCD, LCM, factorization |
| answer is modulo `p` | modular arithmetic; check whether `p` is prime |
| many queries about factors or primes up to `N` | sieve or smallest-prime-factor table |
| choose/rearrange/count equal objects | combinations, multinomial, inclusion-exclusion |
| parity, toggles, XOR of ranges or subsets | bit operations and XOR identities |
| `n` is huge but recurrence state is small | matrix exponentiation or linear recurrence |
| coprime moduli or `ax + by = c` | extended GCD and CRT |
| random process, average moves, optimal play | linearity of expectation, DP, Grundy values |
| points, area, collinearity, polygon | cross product; avoid floating point first |
| multiply long polynomials or solve equations | NTT/FFT or Gaussian elimination |

## Rules that prevent most wrong answers

- Write constraints beside the intended complexity before coding.
- State every modulus precondition. Fermat inversion requires a prime modulus
  and a nonzero residue; factorial inverse formulas also need `n < modulus`.
- Python integers do not overflow, but `O(sqrt(n))` factorization and `O(n^2)`
  DP still time out.
- Use exact integers for divisibility and geometry. Introduce floats only when
  the statement makes an approximate value unavoidable.
- Prove a counting formula on a tiny example before taking it modulo anything.

For slower derivations and implementations in three languages, use the
repository's [mathematics stage](../algorithms/07-mathematics/).
