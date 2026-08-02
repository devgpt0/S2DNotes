# 0/1 Knapsack

## Idea

Each item may be used zero or one time. `dp[capacity]` stores the maximum value
obtainable within that capacity.

## Visual model

```text
skip item: dp[c]
take item: dp[c - weight] + value
```

## Classroom board: why capacity goes downward

```text
one item: weight 2, value 5; capacity 4
start dp = [0,0,0,0,0]
update downward: dp[4] reads old dp[2]=0 -> 5
                 dp[2] reads old dp[0]=0 -> 5
item used at most once
```

Upward order would let `dp[4]` read the just-updated `dp[2]=5` and use the same
item twice.

## Steps

1. Start all capacities at value `0`.
2. Process items one by one.
3. Loop capacities **downward** from the limit to the item weight.
4. Keep the better of skipping and taking the item.

## First-principles derivation

For each item there are two choices: skip it or take it once. The future needs
only the processed-item boundary and remaining or used capacity.

In one-dimensional DP, capacities must run downward so the current item cannot
be reused during its own iteration.

## Pattern recognition

Use it for choose-or-skip items with a capacity/budget and each item usable at
most once. Subset sum is the boolean version.

## Implementation

### C++

```cpp
long long zeroOneKnapsack(const std::vector<int>& weight, const std::vector<int>& value, int capacity) {
    std::vector<long long> dp(capacity + 1, 0);
    for (int item = 0; item < static_cast<int>(weight.size()); ++item) {
        for (int current = capacity; current >= weight[item]; --current) {
            dp[current] = std::max(dp[current], dp[current - weight[item]] + value[item]);
        }
    }
    return dp[capacity];
}
```

### Python

```python
def zero_one_knapsack(weight: list[int], value: list[int], capacity: int) -> int:
    dp = [0] * (capacity + 1)
    for item_weight, item_value in zip(weight, value, strict=True):
        for current in range(capacity, item_weight - 1, -1):
            dp[current] = max(dp[current], dp[current - item_weight] + item_value)
    return dp[capacity]
```

### Java

```java
static long zeroOneKnapsack(int[] weight, int[] value, int capacity) {
    long[] dp = new long[capacity + 1];
    for (int item = 0; item < weight.length; item++) {
        for (int current = capacity; current >= weight[item]; current--) {
            dp[current] = Math.max(dp[current], dp[current - weight[item]] + value[item]);
        }
    }
    return dp[capacity];
}
```

## Why it works

The downward loop reads states from before the current item was processed, so
that item cannot be selected twice. Both skip and take choices are considered.

## Complexity

Time is `O(items * capacity)` and space is `O(capacity)`.

## Common mistakes

- Looping capacity upward, which changes the problem to unbounded knapsack.
- Using this method when capacity is too large; consider value-based DP or
  meet in the middle.
- Assuming `dp[c]` means exact weight when it means weight at most `c`.
