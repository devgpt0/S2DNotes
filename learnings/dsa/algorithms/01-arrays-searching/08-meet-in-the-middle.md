# Meet in the Middle

## Idea

Meet in the middle reduces a `2^n` search to roughly `2 * 2^(n/2)` by splitting
the choices, enumerating both halves, and combining their results.

## Visual model

```text
all choices -> left half sums + right half sums -> sort/search to combine
```

## Classroom board: split four choices

For values `[2, 5, 7, 9]`, split into `[2, 5]` and `[7, 9]`.

```text
left subset sums:  0, 2, 5, 7
right subset sums: 0, 7, 9, 16

Want a total <= 12.
left sum 5 can pair with right sums <= 7: 0 and 7 -> two choices
```

Every full subset is exactly one left subset plus one right subset. We search
two lists of size `2^(n/2)` instead of one list of size `2^n`.

## Steps

Generate every subset sum of each half. Sort the right sums. For each left sum,
binary-search how many right sums are at most `limit - leftSum`.

1. Split the items into two nearly equal halves.
2. Enumerate all subset results for each half.
3. Sort or hash one side.
4. For each result on the other side, find compatible partners.

## First-principles derivation

Full subset search has `2^n` choices. Split the independent choices into two
halves and enumerate `2^(n/2)` results from each side.

The combination step must find exactly the left-right pairs that form a valid
whole answer.

## Pattern recognition

Think of meet in the middle when `n` is about `35` to `45`: too large for
`2^n`, but small enough for `2^(n/2)`.

## Implementation

### C++

```cpp
std::vector<long long> subsetSums(const std::vector<int>& values, int begin, int end) {
    std::vector<long long> sums{0};
    for (int index = begin; index < end; ++index) {
        const int size = static_cast<int>(sums.size());
        for (int current = 0; current < size; ++current) {
            sums.push_back(sums[current] + values[index]);
        }
    }
    return sums;
}

long long countSubsetsAtMost(const std::vector<int>& values, long long limit) {
    const int middle = static_cast<int>(values.size()) / 2;
    auto left = subsetSums(values, 0, middle);
    auto right = subsetSums(values, middle, values.size());
    std::sort(right.begin(), right.end());
    long long answer = 0;
    for (long long sum : left) {
        answer += std::upper_bound(right.begin(), right.end(), limit - sum) - right.begin();
    }
    return answer;
}
```

### Python

```python
from bisect import bisect_right


def subset_sums(values: list[int]) -> list[int]:
    sums = [0]
    for value in values:
        sums += [current + value for current in sums]
    return sums


def count_subsets_at_most(values: list[int], limit: int) -> int:
    middle = len(values) // 2
    left = subset_sums(values[:middle])
    right = sorted(subset_sums(values[middle:]))
    return sum(bisect_right(right, limit - value) for value in left)
```

### Java

```java
static long countSubsetsAtMost(int[] values, long limit) {
    int middle = values.length / 2;
    long[] left = subsetSums(values, 0, middle);
    long[] right = subsetSums(values, middle, values.length);
    Arrays.sort(right);
    long answer = 0;
    for (long sum : left) {
        answer += upperBound(right, limit - sum);
    }
    return answer;
}

static long[] subsetSums(int[] values, int begin, int end) {
    long[] sums = new long[1 << (end - begin)];
    for (int mask = 0; mask < sums.length; mask++) {
        for (int bit = 0; bit < end - begin; bit++) {
            if ((mask & (1 << bit)) != 0) {
                sums[mask] += values[begin + bit];
            }
        }
    }
    return sums;
}

static int upperBound(long[] values, long target) {
    int left = 0;
    int right = values.length;
    while (left < right) {
        int middle = left + (right - left) / 2;
        if (values[middle] <= target) left = middle + 1;
        else right = middle;
    }
    return left;
}
```

## Why it works

Every full subset is uniquely one left subset plus one right subset, so the
combination step counts every valid full choice exactly once.

## Complexity

Time is `O(2^(n/2) log 2^(n/2))`; space is `O(2^(n/2))`. It is a key signal
when `n` is near `40`, where full subset enumeration is impossible.

## Common mistakes

- Splitting into very unequal halves.
- Forgetting the empty subset.
- Using 32-bit integers for subset sums or the answer count.
- Applying pruning that assumes values are positive when they are not.
