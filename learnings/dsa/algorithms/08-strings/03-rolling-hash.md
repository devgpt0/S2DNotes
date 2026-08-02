# Rolling Hash

## Idea

A polynomial hash gives every prefix a numeric fingerprint. Subtracting two
prefix hashes returns a substring hash in `O(1)`.

## Visual model

```text
prefix[i+1] = prefix[i] * base + code(text[i])
hash(left, right) = prefix[right] - prefix[left] * base^(right-left)
```

## Classroom board: remove the earlier prefix

```text
prefix hash of "abcd" contains a,b,c,d
want hash of "cd"
shift hash("ab") into its old positions, then subtract it
remaining fingerprint represents exactly "cd"
```

Hashes make comparison fast, but equal hashes are not absolute proof because a
collision is possible.

## Steps

1. Precompute powers of the base.
2. Build prefix hashes left to right.
3. Use the subtraction formula for `[left, right)`.
4. Compare hashes only after aligning the same substring length.

## First-principles derivation

Comparing two substrings character by character repeats work. A polynomial hash
turns a substring into a numeric fingerprint; prefix hashes remove the unwanted
beginning in constant time.

Equal strings must have equal hashes, but unequal strings can collide, so hash
equality is evidence rather than a mathematical proof.

## Classroom board: remove a hashed prefix

Use base `10` only for a small illustration and map `a=1, b=2, c=3`.

```text
string "abc"
prefix[0] = 0
prefix[1] = 1
prefix[2] = 1*10 + 2 = 12
prefix[3] = 12*10 + 3 = 123

hash("bc") = prefix[3] - prefix[1] * 10^2
           = 123 - 1*100
           = 23
```

Real code uses a large modulus or multiple hashes and normalizes subtraction.

## Pattern recognition

Use rolling hash for many substring equality checks, palindrome queries, or
duplicate-substring searches when a tiny collision risk is acceptable.

## Implementation

### C++

```cpp
class RollingHash {
   public:
    explicit RollingHash(const std::string& text) : prefix_(text.size() + 1), power_(text.size() + 1, 1) {
        for (int index = 0; index < static_cast<int>(text.size()); ++index) {
            prefix_[index + 1] = (prefix_[index] * base_ + static_cast<unsigned char>(text[index]) + 1) % modulus_;
            power_[index + 1] = power_[index] * base_ % modulus_;
        }
    }
    long long query(int left, int right) const {
        return (prefix_[right] - prefix_[left] * power_[right - left] % modulus_ + modulus_) % modulus_;
    }
   private:
    static constexpr long long base_ = 911382323;
    static constexpr long long modulus_ = 972663749;
    std::vector<long long> prefix_, power_;
};
```

### Python

```python
class RollingHash:
    BASE = 911_382_323
    MODULUS = 972_663_749

    def __init__(self, text: str) -> None:
        self.prefix = [0] * (len(text) + 1)
        self.power = [1] * (len(text) + 1)
        for index, character in enumerate(text):
            self.prefix[index + 1] = (self.prefix[index] * self.BASE + ord(character) + 1) % self.MODULUS
            self.power[index + 1] = self.power[index] * self.BASE % self.MODULUS

    def query(self, left: int, right: int) -> int:
        return (self.prefix[right] - self.prefix[left] * self.power[right - left]) % self.MODULUS
```

### Java

```java
final class RollingHash {
    private static final long BASE = 911_382_323L;
    private static final long MODULUS = 972_663_749L;
    private final long[] prefix;
    private final long[] power;

    RollingHash(String text) {
        prefix = new long[text.length() + 1];
        power = new long[text.length() + 1];
        power[0] = 1;
        for (int index = 0; index < text.length(); index++) {
            prefix[index + 1] = (prefix[index] * BASE + text.charAt(index) + 1) % MODULUS;
            power[index + 1] = power[index] * BASE % MODULUS;
        }
    }

    long query(int left, int right) {
        return (prefix[right] - prefix[left] * power[right - left] % MODULUS + MODULUS) % MODULUS;
    }
}
```

## Why it works

Multiplying the earlier prefix by the missing power aligns its polynomial
positions. Subtraction removes exactly the characters before `left`.

## Complexity

Preprocessing is `O(n)` time and space; each substring hash is `O(1)`.

## Common mistakes

- Treating hash equality as a mathematical proof; collisions exist. Use two
  moduli or verify actual strings when correctness must be deterministic.
- Subtracting without normalizing a negative remainder.
- Multiplying values large enough to overflow before modulo.
