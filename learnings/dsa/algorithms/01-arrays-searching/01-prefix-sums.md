# Prefix Sums

## Idea

A prefix sum stores the total before each position. It turns a static range-sum
query from `O(n)` into `O(1)` after `O(n)` preprocessing.

## Visual model

For `values = [3, -1, 4, 2]`:

```text
index:   0   1   2   3   4
prefix:  0   3   2   6   8
                 |-------|  sum [2, 4) = 8 - 2 = 6
```

Define `prefix[i]` as the sum of `values[0:i]`. Then:

`sum(left, right) = prefix[right] - prefix[left]` for `[left, right)`.

## Classroom board: build and query it

```text
values = [3, -1, 4, 2]

read value       3   -1   4   2
running total    3    2   6   8
prefix        [0,    3,  2,  6,  8]

Query indexes [1, 4): values -1 + 4 + 2
total before index 4 = 8
total before index 1 = 3
answer = 8 - 3 = 5
```

The extra starting `0` means a range beginning at index `0` needs no special
case.

## Steps

1. Create `prefix` with `n + 1` values and set `prefix[0] = 0`.
2. Build `prefix[i + 1] = prefix[i] + values[i]`.
3. Answer `[left, right)` with `prefix[right] - prefix[left]`.

## First-principles derivation

A range sum repeats additions. Store the total before every boundary once.

```text
sum(left..right) = total before right - total before left
```

The invariant is `prefix[i] = sum(values[0:i])`; subtraction cancels the
unwanted beginning.

## Pattern recognition

Use prefix sums when the array does not change and the problem asks many
range-sum or range-count queries.

## Implementation

### C++

```cpp
class PrefixSum {
   public:
    explicit PrefixSum(const std::vector<int>& values)
        : prefix_(values.size() + 1, 0) {
        for (int index = 0; index < static_cast<int>(values.size()); ++index) {
            prefix_[index + 1] = prefix_[index] + values[index];
        }
    }

    long long query(int left, int right) const {
        return prefix_[right] - prefix_[left];
    }

   private:
    std::vector<long long> prefix_;
};
```

### Python

```python
class PrefixSum:
    def __init__(self, values: list[int]) -> None:
        self._prefix = [0]
        for value in values:
            self._prefix.append(self._prefix[-1] + value)

    def query(self, left: int, right: int) -> int:
        return self._prefix[right] - self._prefix[left]
```

### Java

```java
final class PrefixSum {
    private final long[] prefix;

    PrefixSum(int[] values) {
        prefix = new long[values.length + 1];
        for (int index = 0; index < values.length; index++) {
            prefix[index + 1] = prefix[index] + values[index];
        }
    }

    long query(int left, int right) {
        return prefix[right] - prefix[left];
    }
}
```

## Why it works

`prefix[right]` contains the wanted range plus everything before `left`.
Subtracting `prefix[left]` removes exactly that unwanted beginning.

## Complexity

Build time and space are `O(n)`; each query is `O(1)`. Use 64-bit totals.

## Extensions

- Count items satisfying a property by prefix-summing `0/1` indicators.
- A 2D prefix sum answers rectangle queries using inclusion-exclusion.
- Prefix XOR works because equal prefixes cancel: `xor(l, r) = p[r] ^ p[l]`.

> [!TIP]
> Prefix sums are for mostly static arrays. For updates plus queries, use a
> Fenwick or segment tree.

## Common mistakes

- Mixing inclusive ranges with the `[left, right)` formula.
- Creating only `n` prefix entries instead of `n + 1`.
- Storing a large sum in a 32-bit integer.
