# Bitmasks and Subset Enumeration

## Idea

When `n` is small, an integer can represent a subset. Bit `i` is `1` exactly
when item `i` is selected.

| Operation | Expression |
| --- | --- |
| Test bit `i` | `(mask & (1 << i)) != 0` |
| Add `i` | `mask | (1 << i)` |
| Remove `i` | `mask & ~(1 << i)` |
| Toggle `i` | `mask ^ (1 << i)` |
| Lowest set bit | `mask & -mask` |

## Steps

1. Assign one bit to each item.
2. Enumerate masks from `0` to `2^n - 1`.
3. Test bits to know which items are selected.
4. Use bit operations to add, remove, or transition between subsets.

## First-principles derivation

A subset makes one yes/no decision for every item. A binary number already
stores exactly that pattern.

```text
item index:     2 1 0
mask 5 binary:  1 0 1
selected:       C - A
```

Bit `i` is the invariant source of truth for whether item `i` belongs to the
current subset.

## Classroom board: enumerate three items

```text
items = [A, B, C]

mask binary subset
0    000    {}
1    001    {A}
2    010    {B}
3    011    {A,B}
4    100    {C}
5    101    {A,C}
6    110    {B,C}
7    111    {A,B,C}
```

Three independent choices create `2 x 2 x 2 = 2^3` subsets. This is why the
method becomes expensive as `n` grows.

## Pattern recognition

Use bitmasks when the number of yes/no items is small, especially for subset
enumeration, visited sets in DP, or compact boolean states.

## Enumerate all subsets

There are `2^n` masks and `n * 2^(n-1)` selected-bit visits, so the code below
is `O(n 2^n)`.

### C++

```cpp
std::vector<std::vector<int>> subsets(const std::vector<int>& values) {
    std::vector<std::vector<int>> answer;
    const int count = 1 << values.size();
    for (int mask = 0; mask < count; ++mask) {
        std::vector<int> subset;
        for (int bit = 0; bit < static_cast<int>(values.size()); ++bit) {
            if ((mask & (1 << bit)) != 0) {
                subset.push_back(values[bit]);
            }
        }
        answer.push_back(std::move(subset));
    }
    return answer;
}
```

### Python

```python
def subsets(values: list[int]) -> list[list[int]]:
    answer: list[list[int]] = []
    for mask in range(1 << len(values)):
        subset = [
            value
            for bit, value in enumerate(values)
            if mask & (1 << bit)
        ]
        answer.append(subset)
    return answer
```

### Java

```java
static List<List<Integer>> subsets(int[] values) {
    List<List<Integer>> answer = new ArrayList<>();
    int count = 1 << values.length;
    for (int mask = 0; mask < count; mask++) {
        List<Integer> subset = new ArrayList<>();
        for (int bit = 0; bit < values.length; bit++) {
            if ((mask & (1 << bit)) != 0) {
                subset.add(values[bit]);
            }
        }
        answer.add(subset);
    }
    return answer;
}
```

## Enumerate submasks

```text
submask = mask
while submask > 0:
    use submask
    submask = (submask - 1) & mask
```

Across all masks this takes `O(3^n)`, because each bit is absent, in the mask
only, or in both mask and submask. Include submask `0` separately if needed.

## Limits

Use 64-bit masks when `n` can reach 63. In Java use `1L << bit`; in C++ use
`1LL << bit`. Exponential enumeration is normally practical only around
`n <= 22`, depending on work per subset.

## Complexity

All subsets take `O(2^n)` states; visiting every bit takes `O(n 2^n)`. Storage
depends on whether subsets are processed or saved.

## Common mistakes

- Shifting a 32-bit `1` when more bits are needed.
- Forgetting mask `0`, the empty subset.
- Assuming exponential code fits because each bit operation is constant.
- Enumerating submask `0` incorrectly.
