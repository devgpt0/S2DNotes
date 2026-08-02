# Difference Arrays

## Idea

A difference array reverses prefix sums. It supports each offline range
addition in `O(1)`, then materializes all final values in `O(n)`.

## Visual model

To add `delta` to inclusive range `[left, right]`:

```text
difference[left]     += delta   // start the effect
difference[right + 1] -= delta  // stop it after right
```

The running prefix of `difference` is the amount added at each position.

## Classroom board: two range updates

Start with five zeroes. Add `3` to indexes `[1, 3]`, then add `2` to `[2, 4]`.

```text
markers after first:  [0, +3,  0,  0, -3,  0]
markers after second: [0, +3, +2,  0, -3, -2]

running prefix:          0   3   5   5   2
final values:           [0,  3,  5,  5,  2]
```

We mark where an effect starts and where it stops. One final walk applies every
active effect.

## Steps

1. Allocate `n + 1` zeroes.
2. For each inclusive update, add at `left` and subtract at `right + 1`.
3. Take a prefix sum to rebuild every final value.

## First-principles derivation

Adding to every element of every range repeats work. Record only where an
effect starts and where it stops.

```text
add value on [left,right)
difference[left]  += value
difference[right] -= value
```

A final prefix sum carries each active change forward until its stop boundary.

## Pattern recognition

Use a difference array for many range additions when no value is queried until
all updates are finished.

## Implementation

### C++

```cpp
std::vector<long long> applyRangeAdds(
    int size,
    const std::vector<std::array<int, 3>>& updates) {
    std::vector<long long> difference(size + 1, 0);
    for (const auto& [left, right, delta] : updates) {
        difference[left] += delta;
        difference[right + 1] -= delta;
    }
    std::vector<long long> values(size);
    long long running = 0;
    for (int index = 0; index < size; ++index) {
        running += difference[index];
        values[index] = running;
    }
    return values;
}
```

### Python

```python
def apply_range_adds(
    size: int, updates: list[tuple[int, int, int]]
) -> list[int]:
    difference = [0] * (size + 1)
    for left, right, delta in updates:
        difference[left] += delta
        difference[right + 1] -= delta

    values = [0] * size
    running = 0
    for index in range(size):
        running += difference[index]
        values[index] = running
    return values
```

### Java

```java
static long[] applyRangeAdds(int size, int[][] updates) {
    long[] difference = new long[size + 1];
    for (int[] update : updates) {
        int left = update[0];
        int right = update[1];
        int delta = update[2];
        difference[left] += delta;
        difference[right + 1] -= delta;
    }
    long[] values = new long[size];
    long running = 0;
    for (int index = 0; index < size; index++) {
        running += difference[index];
        values[index] = running;
    }
    return values;
}
```

## Why it works

The added value begins at `left`. The negative marker cancels it immediately
after `right`, so the running sum applies it to exactly the requested range.

## Complexity

For `q` updates, total time is `O(n + q)` and space is `O(n)`.

## When it works

Use it when all updates are known before any final value is needed. If updates
and queries interleave, use a Fenwick tree or lazy segment tree. A 2D
difference grid extends the same start/stop idea with four corner updates.

## Common mistakes

- Forgetting the extra cell for `right + 1`.
- Mixing inclusive updates with a half-open formula.
- Trying to answer online queries before rebuilding the values.
