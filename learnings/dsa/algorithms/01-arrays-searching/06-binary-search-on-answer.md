# Binary Search on the Answer

## Idea

Sometimes the answer is not stored in an array, but “is candidate `x`
feasible?” is monotone:

## Visual model

```text
false false false | true true true
                  ^ first feasible answer
```

## Example: minimum ship capacity

Given positive package weights in order and `days`, find the smallest capacity
that ships them within the limit. If capacity works, every larger capacity
works.

## Classroom board: ship `[3, 2, 2]` in two days

```text
minimum possible capacity = 3 (largest package)
maximum possible capacity = 7 (all packages together)

candidate 5 -> day 1: 3+2, day 2: 2 -> works
candidate 4 -> day 1: 3,   day 2: 2+2 -> works
candidate 3 -> day 1: 3,   day 2: 2, day 3: 2 -> fails

false false | true true ...
              first true = 4
```

We binary-search capacities, not array positions.

## Steps

1. Write a `feasible(candidate)` function.
2. Prove feasibility changes only once.
3. Find safe lower and upper answer bounds.
4. Binary-search the first feasible candidate.

## First-principles derivation

Sometimes constructing the optimum is hard, but checking “can answer `x`
work?” is easy. If feasibility changes only once, the answers form:

```text
impossible impossible ... possible possible
                         ^
                    first feasible
```

Binary search finds that boundary without testing every answer.

## Pattern recognition

Look for “minimum possible maximum,” “maximum possible minimum,” or a numeric
answer whose candidate can be checked faster than it can be constructed.

## Implementation

### C++

```cpp
long long minimumCapacity(const std::vector<int>& weights, int days) {
    auto feasible = [&](long long capacity) {
        int usedDays = 1;
        long long load = 0;
        for (int weight : weights) {
            if (load + weight > capacity) {
                ++usedDays;
                load = 0;
            }
            load += weight;
        }
        return usedDays <= days;
    };

    long long left = *std::max_element(weights.begin(), weights.end());
    long long right = std::accumulate(weights.begin(), weights.end(), 0LL);
    while (left < right) {
        const long long middle = left + (right - left) / 2;
        if (feasible(middle)) {
            right = middle;
        } else {
            left = middle + 1;
        }
    }
    return left;
}
```

### Python

```python
def minimum_capacity(weights: list[int], days: int) -> int:
    def feasible(capacity: int) -> bool:
        used_days = 1
        load = 0
        for weight in weights:
            if load + weight > capacity:
                used_days += 1
                load = 0
            load += weight
        return used_days <= days

    left, right = max(weights), sum(weights)
    while left < right:
        middle = left + (right - left) // 2
        if feasible(middle):
            right = middle
        else:
            left = middle + 1
    return left
```

### Java

```java
static long minimumCapacity(int[] weights, int days) {
    long left = 0;
    long right = 0;
    for (int weight : weights) {
        left = Math.max(left, weight);
        right += weight;
    }
    while (left < right) {
        long middle = left + (right - left) / 2;
        if (canShip(weights, days, middle)) {
            right = middle;
        } else {
            left = middle + 1;
        }
    }
    return left;
}

static boolean canShip(int[] weights, int days, long capacity) {
    int usedDays = 1;
    long load = 0;
    for (int weight : weights) {
        if (load + weight > capacity) {
            usedDays++;
            load = 0;
        }
        load += weight;
    }
    return usedDays <= days;
}
```

## Why it works

Feasible capacities form one continuous suffix. Binary search keeps the first
feasible value inside its range until both boundaries meet there.

## Complexity

If feasibility is `O(n)` and the answer range has width `R`, time is
`O(n log R)`.

## Derivation checklist

1. Define exactly what a candidate means.
2. Prove feasibility is monotone.
3. Find one guaranteed impossible/possible boundary or a tight closed range.
4. Decide whether you need the first true or last true.

## Common mistakes

- Searching before proving monotonicity.
- Using bounds that do not contain the answer.
- Returning the last failed value instead of the first successful one.
- Letting sums or midpoint arithmetic overflow.
