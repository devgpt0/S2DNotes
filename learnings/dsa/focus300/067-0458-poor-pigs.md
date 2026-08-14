# Focus300 067: LeetCode 458 - Poor Pigs

**Source:** [LeetCode 458](https://leetcode.com/problems/poor-pigs/)  
**Difficulty:** Hard  
**Pattern:** encode buckets with multi-state experiment outcomes

## Exact contract

Exactly one bucket is poisonous. A pig dies `minutesToDie` minutes after
drinking. Tests last `minutesToTest` minutes and may be run in parallel rounds.
Return the minimum pigs needed to identify the poisoned bucket with certainty.

## First principles

There are `rounds = floor(minutesToTest/minutesToDie)` observable drinking
rounds. One pig has `rounds+1` final states: it dies after any one round or
survives. With `p` pigs, independent outcome tuples distinguish
`(rounds+1)^p` buckets.

Assign each bucket a base-`rounds+1` code; pig positions are code digits. The
smallest `p` whose capacity reaches the bucket count is both sufficient and
necessary.

## Cases that decide correctness

- One bucket needs zero pigs.
- Survival is an additional observable state.
- Partial final rounds do not create another state.
- Pigs act in parallel, so capacities multiply.
- Positive timing values are required.

## Brute force: materialize outcome tuples for increasing pig counts

```python
from itertools import product


def poor_pigs_brute(buckets: int, minutes_to_die: int, minutes_to_test: int) -> int:
    if buckets <= 0 or minutes_to_die <= 0 or minutes_to_test < 0:
        raise ValueError("bucket and timing values are invalid")
    states = minutes_to_test // minutes_to_die + 1
    if states == 1 and buckets > 1:
        raise ValueError("no informative test round is available")
    for pigs in range(buckets + 1):
        if sum(1 for _ in product(range(states), repeat=pigs)) >= buckets:
            return pigs
    raise RuntimeError("finite bucket count must be representable")
```

This explicitly enumerates exponentially many outcome tuples.

## Better insight: only the number of distinguishable outcome codes matters

The testing schedule is a positional numeral system. Capacity multiplies by
the state count for each added pig.

## Expert solution: grow multi-state capacity

```python
def poor_pigs(buckets: int, minutes_to_die: int, minutes_to_test: int) -> int:
    if buckets <= 0 or minutes_to_die <= 0 or minutes_to_test < 0:
        raise ValueError("bucket and timing values are invalid")
    states = minutes_to_test // minutes_to_die + 1
    if states == 1 and buckets > 1:
        raise ValueError("no informative test round is available")
    pigs = 0
    capacity = 1
    while capacity < buckets:
        capacity *= states
        pigs += 1
    return pigs
```

The loop returns the smallest exponent satisfying the information-capacity
lower bound, and the base-code construction shows it is achievable.

**Complexity:** `O(log_states(buckets))` time and `O(1)` space.
