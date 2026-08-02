# Unbounded Knapsack

## Idea

Each item may be reused any number of times. The capacity loop goes upward so
the current item can build on a state that already used it.

## Visual model

```text
dp[c] <- dp[c - itemWeight] + itemValue
current item may already be inside dp[c - itemWeight]
```

## Classroom board: why capacity goes upward

```text
unlimited item: weight 2, value 5; capacity 4
dp[2] = dp[0]+5 = 5
dp[4] = dp[2]+5 = 10
```

Here reading the newly updated `dp[2]` is intentional: it represents using a
second copy.

## Steps

1. Start all capacities at `0`.
2. Process one item type.
3. Loop capacities **upward** from its weight to the limit.
4. Keep the better value.

## First-principles derivation

The choice is still skip or take, but taking an item does not remove it from
future choices. That single rule changes the dependency direction.

Iterating capacity upward lets a state reuse an answer already improved by the
same item, representing unlimited copies.

## Pattern recognition

Use it for unlimited coins/items, rod cutting, or repeated choices under a
capacity. Verify that zero-weight positive-value items are impossible.

## Implementation

### C++

```cpp
long long unboundedKnapsack(const std::vector<int>& weight, const std::vector<int>& value, int capacity) {
    std::vector<long long> dp(capacity + 1, 0);
    for (int item = 0; item < static_cast<int>(weight.size()); ++item) {
        for (int current = weight[item]; current <= capacity; ++current) {
            dp[current] = std::max(dp[current], dp[current - weight[item]] + value[item]);
        }
    }
    return dp[capacity];
}
```

### Python

```python
def unbounded_knapsack(weight: list[int], value: list[int], capacity: int) -> int:
    dp = [0] * (capacity + 1)
    for item_weight, item_value in zip(weight, value, strict=True):
        for current in range(item_weight, capacity + 1):
            dp[current] = max(dp[current], dp[current - item_weight] + item_value)
    return dp[capacity]
```

### Java

```java
static long unboundedKnapsack(int[] weight, int[] value, int capacity) {
    long[] dp = new long[capacity + 1];
    for (int item = 0; item < weight.length; item++) {
        for (int current = weight[item]; current <= capacity; current++) {
            dp[current] = Math.max(dp[current], dp[current - weight[item]] + value[item]);
        }
    }
    return dp[capacity];
}
```

## Why it works

The upward loop makes `dp[current - weight]` the best state that may already
contain this item. Thus every legal number of copies is considered.

## Complexity

Time is `O(items * capacity)` and space is `O(capacity)`.

## Common mistakes

- Copying the 0/1 downward loop.
- Allowing a zero-weight item with positive value, making the optimum infinite.
- Confusing combinations with permutations in coin-counting variants; loop
  order decides which one is counted.
