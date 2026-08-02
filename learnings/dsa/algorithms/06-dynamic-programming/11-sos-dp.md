# Sum Over Subsets (SOS) DP

## Idea

Given a value `f[mask]`, SOS DP computes the sum of `f[submask]` over every
submask of every mask in `O(n 2^n)` instead of `O(3^n)`.

## Visual model

```text
for each bit:
answer[mask] += answer[mask without that bit]
```

## Classroom board: collect submasks one bit at a time

```text
mask 11₂ has submasks 00,01,10,11
process bit 0 -> include versions with bit 0 removed
process bit 1 -> include versions with bit 1 removed
after both bits, all four contributions are present exactly once
```

## Steps

1. Copy `f` into `answer`.
2. Process bits one by one.
3. For each mask containing that bit, add the state with the bit removed.
4. After all bits, every submask contribution has been included once.

## First-principles derivation

Computing every mask's submask aggregate separately revisits the same submasks.
Process one bit at a time and copy contributions from the mask with that bit
removed.

After bit `i`, each mask has collected exactly the submasks that may differ
from it only among the processed bits.

## Pattern recognition

Use it when every mask needs an aggregate over all of its submasks or
supermasks, often for bitwise AND/OR counting problems.

## Implementation

### C++

```cpp
std::vector<long long> subsetSums(std::vector<long long> values, int bits) {
    for (int bit = 0; bit < bits; ++bit) {
        for (int mask = 0; mask < (1 << bits); ++mask) {
            if (mask & (1 << bit)) values[mask] += values[mask ^ (1 << bit)];
        }
    }
    return values;
}
```

### Python

```python
def subset_sums(values: list[int], bits: int) -> list[int]:
    answer = values.copy()
    for bit in range(bits):
        for mask in range(1 << bits):
            if mask & (1 << bit):
                answer[mask] += answer[mask ^ (1 << bit)]
    return answer
```

### Java

```java
static long[] subsetSums(long[] values, int bits) {
    long[] answer = values.clone();
    for (int bit = 0; bit < bits; bit++) {
        for (int mask = 0; mask < 1 << bits; mask++) {
            if ((mask & (1 << bit)) != 0) answer[mask] += answer[mask ^ (1 << bit)];
        }
    }
    return answer;
}
```

## Why it works

After processing the first `k` bits, each state includes exactly the submasks
that may differ only in those `k` positions. Induction over bits proves the
final result includes all submasks.

## Complexity

Time is `O(n 2^n)` and extra space is `O(2^n)` for the returned copy.

## Common mistakes

- Providing an array whose length is not exactly `2^bits`.
- Updating masks that do not contain the current bit.
- Confusing submask sums with superset sums; reverse the condition/transition
  for supersets.
