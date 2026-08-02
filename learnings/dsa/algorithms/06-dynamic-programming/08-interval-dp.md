# Interval Dynamic Programming

## Idea

Interval DP solves every contiguous interval, usually by choosing its final
split, merge, or action.

## Visual model

For matrix-chain multiplication:

```text
dp[left][right] = min over split:
    dp[left][split] + dp[split+1][right] + cost of final multiplication
```

## Classroom board: choose the final split

```text
matrices A, B, C
only two full parenthesizations:
(A*B)*C  -> solve A*B, then final multiply with C
A*(B*C)  -> solve B*C, then final multiply with A
take the cheaper cost
```

Long intervals depend on already solved shorter intervals.

## Steps

1. Define states for one-item intervals.
2. Increase interval length from small to large.
3. Try every legal split inside the interval.
4. Keep the best transition.

## First-principles derivation

When the last operation splits a contiguous range, guess that final split.
Everything on its left and right becomes an independent smaller interval.

Compute shorter intervals first so every possible subinterval needed by a
larger interval is already solved.

## Pattern recognition

Use interval DP when operations combine or remove contiguous ranges and the
last/first operation splits a range into independent smaller ranges.

## Implementation: matrix-chain multiplication

`dimensions[i] x dimensions[i+1]` describes matrix `i`.

### C++

```cpp
long long matrixChainCost(const std::vector<int>& dimensions) {
    const int count = dimensions.size() - 1;
    std::vector<std::vector<long long>> dp(count, std::vector<long long>(count, 0));
    for (int length = 2; length <= count; ++length) {
        for (int left = 0; left + length <= count; ++left) {
            const int right = left + length - 1;
            dp[left][right] = std::numeric_limits<long long>::max();
            for (int split = left; split < right; ++split) {
                const long long cost = dp[left][split] + dp[split + 1][right]
                    + 1LL * dimensions[left] * dimensions[split + 1] * dimensions[right + 1];
                dp[left][right] = std::min(dp[left][right], cost);
            }
        }
    }
    return count == 0 ? 0 : dp[0][count - 1];
}
```

### Python

```python
def matrix_chain_cost(dimensions: list[int]) -> int:
    count = len(dimensions) - 1
    if count == 0:
        return 0
    dp = [[0] * count for _ in range(count)]
    for length in range(2, count + 1):
        for left in range(count - length + 1):
            right = left + length - 1
            dp[left][right] = min(
                dp[left][split]
                + dp[split + 1][right]
                + dimensions[left] * dimensions[split + 1] * dimensions[right + 1]
                for split in range(left, right)
            )
    return dp[0][count - 1]
```

### Java

```java
static long matrixChainCost(int[] dimensions) {
    int count = dimensions.length - 1;
    if (count == 0) return 0;
    long[][] dp = new long[count][count];
    for (int length = 2; length <= count; length++) {
        for (int left = 0; left + length <= count; left++) {
            int right = left + length - 1;
            dp[left][right] = Long.MAX_VALUE;
            for (int split = left; split < right; split++) {
                long cost = dp[left][split] + dp[split + 1][right]
                    + (long) dimensions[left] * dimensions[split + 1] * dimensions[right + 1];
                dp[left][right] = Math.min(dp[left][right], cost);
            }
        }
    }
    return dp[0][count - 1];
}
```

## Why it works

Every full parenthesization has one final split. The DP tries every possible
final split and uses optimal costs for both resulting subchains.

## Complexity

Time is `O(n^3)` and space is `O(n^2)`.

## Common mistakes

- Filling long intervals before short dependencies.
- Off-by-one errors between matrix indices and dimension indices.
- Assuming every interval problem uses the same split cost.
