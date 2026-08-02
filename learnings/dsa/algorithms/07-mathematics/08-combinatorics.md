# Combinations Modulo a Prime

## Idea

`C(n, r)` counts ways to choose `r` items from `n` without order:

```text
C(n, r) = n! / (r! * (n-r)!)
```

Under a prime modulus, divide by multiplying modular inverses.

## Classroom board: choose 2 of 4

```text
items A,B,C,D
pairs: AB, AC, AD, BC, BD, CD -> 6
C(4,2) = 4! / (2!*2!) = 6
```

Modulo arithmetic replaces division with multiplication by an inverse.

## Steps

1. Precompute factorials up to the largest `n`.
2. Compute inverse factorial of the largest factorial with Fermat's theorem.
3. Fill remaining inverse factorials downward.
4. Answer with `factorial[n] * inverseFactorial[r] * inverseFactorial[n-r]`.

## First-principles derivation

Choosing `k` ordered items gives `n*(n-1)*...*(n-k+1)` arrangements. Every
unordered chosen set appears in exactly `k!` orders, so divide by `k!`.

Modulo a prime, division becomes multiplication by a modular inverse.

## Classroom board: choose 2 from 5

```text
ordered choices = 5 * 4 = 20

each pair counted twice:
(A,B) and (B,A)

C(5,2) = 20 / 2! = 10

factorial formula:
5! / (2! * 3!) = 120 / (2 * 6) = 10
```

Symmetry gives `C(n,k) = C(n,n-k)`.

## Pattern recognition

Use it for many combination queries under a prime modulus when all `n` values
are smaller than the modulus.

## Implementation

### C++

```cpp
class Combinations {
   public:
    Combinations(int maximum, long long modulus) : modulus_(modulus), factorial_(maximum + 1, 1), inverse_(maximum + 1, 1) {
        for (int value = 1; value <= maximum; ++value) factorial_[value] = factorial_[value - 1] * value % modulus_;
        inverse_[maximum] = power(factorial_[maximum], modulus_ - 2);
        for (int value = maximum; value > 0; --value) inverse_[value - 1] = inverse_[value] * value % modulus_;
    }

    long long choose(int total, int selected) const {
        if (selected < 0 || selected > total) return 0;
        return factorial_[total] * inverse_[selected] % modulus_ * inverse_[total - selected] % modulus_;
    }

   private:
    long long modulus_;
    std::vector<long long> factorial_, inverse_;
    long long power(long long base, long long exponent) const {
        long long answer = 1;
        while (exponent) {
            if (exponent & 1) answer = answer * base % modulus_;
            base = base * base % modulus_;
            exponent >>= 1;
        }
        return answer;
    }
};
```

### Python

```python
class Combinations:
    def __init__(self, maximum: int, modulus: int) -> None:
        self.modulus = modulus
        self.factorial = [1] * (maximum + 1)
        self.inverse = [1] * (maximum + 1)
        for value in range(1, maximum + 1):
            self.factorial[value] = self.factorial[value - 1] * value % modulus
        self.inverse[maximum] = pow(self.factorial[maximum], modulus - 2, modulus)
        for value in range(maximum, 0, -1):
            self.inverse[value - 1] = self.inverse[value] * value % modulus

    def choose(self, total: int, selected: int) -> int:
        if selected < 0 or selected > total:
            return 0
        return (
            self.factorial[total]
            * self.inverse[selected]
            * self.inverse[total - selected]
            % self.modulus
        )
```

### Java

```java
final class Combinations {
    private final long modulus;
    private final long[] factorial;
    private final long[] inverse;

    Combinations(int maximum, long modulus) {
        this.modulus = modulus;
        factorial = new long[maximum + 1];
        inverse = new long[maximum + 1];
        factorial[0] = 1;
        for (int value = 1; value <= maximum; value++) factorial[value] = factorial[value - 1] * value % modulus;
        inverse[maximum] = power(factorial[maximum], modulus - 2);
        for (int value = maximum; value > 0; value--) inverse[value - 1] = inverse[value] * value % modulus;
    }

    long choose(int total, int selected) {
        if (selected < 0 || selected > total) return 0;
        return factorial[total] * inverse[selected] % modulus * inverse[total - selected] % modulus;
    }

    private long power(long base, long exponent) {
        long answer = 1;
        while (exponent > 0) {
            if ((exponent & 1) == 1) answer = answer * base % modulus;
            base = base * base % modulus;
            exponent >>= 1;
        }
        return answer;
    }
}
```

## Why it works

Fermat's theorem gives `x^(p-2)` as `x`'s inverse modulo prime `p`. The stored
inverse factorials therefore implement the division in the formula.

## Complexity

Preprocessing is `O(maximum + log modulus)` time and `O(maximum)` space; each
query is `O(1)`.

## Common mistakes

- Using this when the modulus is composite or `n >= modulus` without Lucas or
  prime-power methods.
- Precomputing below the largest queried `n`.
- Forgetting invalid `r` returns zero.
