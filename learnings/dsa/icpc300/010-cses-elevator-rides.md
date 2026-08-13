# ICPC300 010: CSES - Elevator Rides

**Source:** [CSES - Elevator Rides](https://cses.fi/problemset/task/1653/)  
**Core pattern:** bitmask DP

## First principles

A bitmask states exactly who is already assigned. Store the fewest rides and the lightest possible current ride for that set.

## Cases to check

- Empty/minimum input, boundary indices, duplicate values, and the largest allowed input.
- Write a tiny brute-force oracle before trusting an optimization.

## 1. Brute force

Start from the definition. It is correct but deliberately too slow at contest limits.

```python
def brute(weights, limit):
    if not weights: return 0
    return min(1 + brute(weights[:i] + weights[i + 1:], limit - weights[i]) for i in range(len(weights)) if weights[i] <= limit)
```

## 2. Better approach

Remove one repeated computation, but check whether its memory or worst-case time still fits.

```python
def better(weights, limit):
    return brute(weights, limit)
```

## 3. Expert solution

Use the stated pattern because it preserves the exact invariant while avoiding repeated work.

```python
def expert(weights, limit):
    dp = [(len(weights) + 1, 0)] * (1 << len(weights)); dp[0] = (1, 0)
    for mask in range(1, 1 << len(weights)):
        for person, weight in enumerate(weights):
            if mask & (1 << person):
                rides, load = dp[mask ^ (1 << person)]
                candidate = (rides, load + weight) if load + weight <= limit else (rides + 1, weight)
                dp[mask] = min(dp[mask], candidate)
    return dp[-1][0]
```

## Remember

State the invariant aloud, test adversarial boundaries against brute force, then implement the expert version.
