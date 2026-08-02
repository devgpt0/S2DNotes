# Longest Increasing Subsequence (LIS)

## Idea

Maintain `tails[length - 1]`: the smallest possible final value of an
increasing subsequence with that length.

## Visual model

```text
new value x -> first tail >= x -> replace it
no such tail -> extend the longest subsequence
```

## Classroom board: improve tails

```text
values 3, 5, 2, 4
3 -> tails [3]
5 -> tails [3,5]
2 -> replace first >=2 -> [2,5]
4 -> replace first >=4 -> [2,4]
length 2
```

Replacing `3` by `2` does not lose a length-1 subsequence; it makes that length
easier to extend.

## Steps

1. Start with no tails.
2. Binary-search the first tail at least as large as the current value.
3. Replace it, or append when all tails are smaller.
4. The number of tails is the LIS length.

## First-principles derivation

The quadratic DP asks which earlier value can precede each item. The faster
method keeps, for every length, the smallest possible tail of an increasing
subsequence of that length.

A smaller tail is always at least as extendable as a larger tail, so replacing
it cannot destroy a future optimum.

## Pattern recognition

Use it for longest strictly increasing subsequence length or problems reducible
to ordered nesting after sorting one dimension.

## Implementation

### C++

```cpp
int lisLength(const std::vector<int>& values) {
    std::vector<int> tails;
    for (int value : values) {
        auto position = std::lower_bound(tails.begin(), tails.end(), value);
        if (position == tails.end()) tails.push_back(value);
        else *position = value;
    }
    return tails.size();
}
```

### Python

```python
from bisect import bisect_left


def lis_length(values: list[int]) -> int:
    tails: list[int] = []
    for value in values:
        position = bisect_left(tails, value)
        if position == len(tails):
            tails.append(value)
        else:
            tails[position] = value
    return len(tails)
```

### Java

```java
static int lisLength(int[] values) {
    int[] tails = new int[values.length];
    int size = 0;
    for (int value : values) {
        int left = 0;
        int right = size;
        while (left < right) {
            int middle = left + (right - left) / 2;
            if (tails[middle] < value) left = middle + 1;
            else right = middle;
        }
        tails[left] = value;
        if (left == size) size++;
    }
    return size;
}
```

## Why it works

A smaller tail always leaves at least as much room for future extension.
Replacing a tail preserves the subsequence length while improving its ending.

## Complexity

Time is `O(n log n)` and space is `O(n)`.

## Common mistakes

- Thinking `tails` itself is always an actual LIS; it may mix replacements.
- Using upper bound for strictly increasing LIS. Upper bound is for
  non-decreasing LIS.
- Sorting the original sequence and destroying its order.
