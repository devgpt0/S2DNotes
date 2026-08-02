# Digit Dynamic Programming

## Idea

Digit DP counts numbers in a huge numeric range by building digits from left
to right. A `tight` state says whether the current prefix still equals the
limit's prefix.

## Visual model

```text
tight = true  -> next digit cannot exceed limit digit
choose smaller -> tight becomes false -> later digits are unrestricted
```

## Classroom board: count up to 325

```text
first digit choices: 0,1,2,3
choose 2 -> prefix is smaller than 3 -> later digits may be 0..9
choose 3 -> still tight -> second digit may only be 0..2
choose 3 then 2 -> third digit may only be 0..5
```

`tight` remembers whether the chosen prefix still exactly matches the limit.

## Steps

1. Convert the upper bound to digits.
2. Define state `(position, property, tight)`.
3. Try every digit up to the current allowed maximum.
4. Memoize states where `tight` is false.
5. Count `[left, right]` as `count(right) - count(left - 1)`.

## First-principles derivation

Enumerating every number up to a huge limit is impossible, but many digit
prefixes have identical futures. The state records position, the property being
tracked, and whether the prefix still equals the limit.

Once a chosen digit is smaller than the limit digit, later digits are
unrestricted and that state can be reused.

## Pattern recognition

Use digit DP to count numbers up to very large limits subject to digit sum,
digit frequency, divisibility, forbidden pattern, or adjacency rules.

## Implementation: count numbers with a target digit sum

Leading zeroes are harmless. Number `0` is counted when the target sum is `0`.

### C++

```cpp
long long countDigitSum(long long limit, int target) {
    if (limit < 0) return 0;
    const std::string digits = std::to_string(limit);
    std::vector<std::vector<long long>> memo(digits.size(), std::vector<long long>(target + 1, -1));
    std::function<long long(int, int, bool)> solve = [&](int position, int sum, bool tight) -> long long {
        if (sum > target) return 0;
        if (position == static_cast<int>(digits.size())) return sum == target;
        if (!tight && memo[position][sum] != -1) return memo[position][sum];
        const int maximum = tight ? digits[position] - '0' : 9;
        long long answer = 0;
        for (int digit = 0; digit <= maximum; ++digit) {
            answer += solve(position + 1, sum + digit, tight && digit == maximum);
        }
        if (!tight) memo[position][sum] = answer;
        return answer;
    };
    return solve(0, 0, true);
}
```

### Python

```python
from functools import cache


def count_digit_sum(limit: int, target: int) -> int:
    if limit < 0:
        return 0
    digits = str(limit)

    @cache
    def solve(position: int, total: int, tight: bool) -> int:
        if total > target:
            return 0
        if position == len(digits):
            return int(total == target)
        maximum = int(digits[position]) if tight else 9
        return sum(
            solve(position + 1, total + digit, tight and digit == maximum)
            for digit in range(maximum + 1)
        )

    return solve(0, 0, True)
```

### Java

```java
static long countDigitSum(long limit, int target) {
    if (limit < 0) return 0;
    char[] digits = Long.toString(limit).toCharArray();
    long[][] memo = new long[digits.length][target + 1];
    for (long[] row : memo) Arrays.fill(row, -1);
    return countDigits(digits, 0, 0, true, target, memo);
}

static long countDigits(char[] digits, int position, int sum, boolean tight, int target, long[][] memo) {
    if (sum > target) return 0;
    if (position == digits.length) return sum == target ? 1 : 0;
    if (!tight && memo[position][sum] != -1) return memo[position][sum];
    int maximum = tight ? digits[position] - '0' : 9;
    long answer = 0;
    for (int digit = 0; digit <= maximum; digit++) {
        answer += countDigits(digits, position + 1, sum + digit, tight && digit == maximum, target, memo);
    }
    if (!tight) memo[position][sum] = answer;
    return answer;
}
```

## Why it works

Every number from `0` to the limit has one padded digit sequence. The tight
rule generates exactly those sequences without exceeding the limit.

## Complexity

For `D` digits and target sum `S`, time is `O(D * S * 10)` and memo space is
`O(D * S)`.

## Common mistakes

- Updating tightness against `9` instead of the current allowed digit.
- Forgetting a `started` state when leading zeroes affect the property.
- Counting an inclusive range without subtracting `count(left - 1)`.
