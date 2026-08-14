# ICPC300 179: Codeforces 453B - Little Pony and Harmony Chest

**Source:** [Codeforces 453B - Little Pony and Harmony Chest](https://codeforces.com/problemset/problem/453/B)  
**Pattern:** minimum-cost DP over used prime-factor masks

## Exact contract

Given up to 100 integers in `[1, 30]`, choose replacement values in `[1, 59]`
that minimize `sum(abs(a[i] - b[i]))` and are pairwise coprime. Return any
minimum-cost replacement array.

## First principles

All prime factors of values up to 59 belong to the 17 primes up to 59. Encode a
candidate by the mask of its distinct prime factors. Two chosen values are
coprime exactly when their masks are disjoint, so a DP state needs only the
union of primes used by earlier positions.

Candidates with the same mask have identical future behavior. At one position,
keep only the value with minimum replacement cost for each distinct mask.

## Cases that decide correctness

- Value `1` has mask zero and may be selected repeatedly.
- Prime powers reserve their prime once, not once per exponent.
- Pairwise coprimality is equivalent to globally disjoint prime masks.
- Several optimal arrays may exist; any one is valid.
- Reconstruction must remove exactly the chosen value's mask.

## Brute force: enumerate a bounded candidate product

```python
from itertools import product
from math import gcd


def harmony_chest_brute(values: list[int], maximum: int) -> list[int]:
    if not values or any(type(value) is not int or value < 1 for value in values):
        raise ValueError("values must be positive integers")
    if type(maximum) is not int or maximum < 1:
        raise ValueError("maximum must be a positive integer")

    best: tuple[int, ...] | None = None
    best_cost: int | None = None
    for candidate in product(range(1, maximum + 1), repeat=len(values)):
        if any(
            gcd(candidate[first], candidate[second]) != 1
            for first in range(len(candidate))
            for second in range(first + 1, len(candidate))
        ):
            continue
        cost = sum(
            abs(original - replacement)
            for original, replacement in zip(values, candidate)
        )
        if best_cost is None or cost < best_cost:
            best = candidate
            best_cost = cost

    if best is None:
        raise ValueError("maximum does not permit a solution")
    return list(best)
```

The Cartesian product makes this suitable only for tiny differential tests.

## Better approach: no separate intermediate

Trying all 59 values from every used-prime mask is the same exact mask DP with
more duplicate transitions. Compressing equal candidate masks is an
implementation improvement inside the expert method, not a separate approach.

## Expert solution: prime-mask DP with compact reconstruction

```python
from array import array

PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59)
MAXIMUM_REPLACEMENT = 59


def harmony_chest(values: list[int]) -> list[int]:
    if (
        not values
        or len(values) > 100
        or any(type(value) is not int or not 1 <= value <= 30 for value in values)
    ):
        raise ValueError("values must contain 1 to 100 integers in [1, 30]")

    value_masks = [0] * (MAXIMUM_REPLACEMENT + 1)
    for value in range(2, MAXIMUM_REPLACEMENT + 1):
        for bit, prime in enumerate(PRIMES):
            if value % prime == 0:
                value_masks[value] |= 1 << bit

    state_count = 1 << len(PRIMES)
    full_mask = state_count - 1
    infinity = 10**9
    current = [infinity] * state_count
    current[0] = 0
    choices: list[array] = []

    for original in values:
        best_by_mask: dict[int, tuple[int, int]] = {}
        for replacement in range(1, MAXIMUM_REPLACEMENT + 1):
            mask = value_masks[replacement]
            candidate = abs(original - replacement), replacement
            previous = best_by_mask.get(mask)
            if previous is None or candidate < previous:
                best_by_mask[mask] = candidate

        following = [infinity] * state_count
        selected = array("b", [0]) * state_count
        for candidate_mask, (replacement_cost, replacement) in best_by_mask.items():
            available = full_mask ^ candidate_mask
            used_mask = available
            while True:
                previous_cost = current[used_mask]
                target_mask = used_mask | candidate_mask
                candidate_cost = previous_cost + replacement_cost
                if candidate_cost < following[target_mask]:
                    following[target_mask] = candidate_cost
                    selected[target_mask] = replacement
                if used_mask == 0:
                    break
                used_mask = (used_mask - 1) & available

        current = following
        choices.append(selected)

    final_mask = min(range(state_count), key=current.__getitem__)
    answer = [0] * len(values)
    for index in range(len(values) - 1, -1, -1):
        replacement = choices[index][final_mask]
        answer[index] = replacement
        final_mask ^= value_masks[replacement]
    return answer
```

Every transition appends one candidate whose prime mask is disjoint from the
used mask. Conversely, every pairwise-coprime prefix follows exactly one such
state path. Minimum-cost relaxation and parent choices therefore reconstruct a
globally optimal array.

**Complexity:** `O(n * 59 * 2^17)` worst-case time and `O(n * 2^17)` bytes for
compact choices plus `O(2^17)` integer costs.
