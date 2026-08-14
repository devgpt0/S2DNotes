# ICPC300 109: CSES - Christmas Party

**Source:** [CSES - Christmas Party](https://cses.fi/problemset/task/1717/)  
**Pattern:** derangement recurrence  
**Goal:** Count, modulo `1_000_000_007`, gift assignments in which no person
receives their own gift.

## 1. Problem in plain words

An assignment is a permutation. A valid Christmas-party assignment has no
fixed point. Such permutations are called derangements.

For three people, the two valid assignments are the two three-cycles, so the
answer is `2`.

## 2. First principles

Consider person `1`, who receives person `j`'s gift for one of `n-1` choices.

- If person `j` receives gift `1`, those two form a pair and the rest can be
  deranged in `D[n-2]` ways.
- Otherwise, merge the obligation involving gift `1` into person `j`; this is
  bijective with a derangement of `n-1` items, giving `D[n-1]` ways.

Therefore `D[n] = (n-1)(D[n-1] + D[n-2])`, with `D[0]=1`, `D[1]=0`.

## 3. Cases that decide correctness

| Case | Required result |
| --- | --- |
| Zero people in reusable recurrence | `1` empty assignment. |
| One person | `0`. |
| Two people | `1`: swap gifts. |
| Fixed point anywhere | Exclude the permutation. |
| Large `n` | Reduce each recurrence step modulo the source modulus. |

## 4. Brute force: test every assignment

```python
from itertools import permutations


def count_derangements_brute_force(size: int) -> int:
    if size < 0:
        raise ValueError("size must be nonnegative")
    return sum(
        all(person != gift for person, gift in enumerate(assignment))
        for assignment in permutations(range(size))
    )
```

**Complexity:** `O(n! n)` time and `O(n)` generated-permutation memory.

## 5. Better: inclusion-exclusion over fixed points

There are `C(n,k)(n-k)! = n!/k!` permutations fixing any chosen `k` people.
Alternating these counts gives the derangement number.

```python
MODULO = 1_000_000_007


def count_derangements_inclusion_exclusion(size: int) -> int:
    if size < 0:
        raise ValueError("size must be nonnegative")

    factorial = 1
    for value in range(2, size + 1):
        factorial = factorial * value % MODULO

    answer = 0
    inverse_factorial = 1
    for fixed_count in range(size + 1):
        term = factorial * inverse_factorial % MODULO
        answer += term if fixed_count % 2 == 0 else -term
        if fixed_count < size:
            inverse_factorial = (
                inverse_factorial * pow(fixed_count + 1, MODULO - 2, MODULO) % MODULO
            )
    return answer % MODULO
```

**Complexity:** `O(n log MODULO)` time as written and `O(1)` memory.

## 6. Expert solution: constant-memory recurrence

```python
MODULO = 1_000_000_007


def count_derangements(size: int) -> int:
    if size < 0:
        raise ValueError("size must be nonnegative")
    if size == 0:
        return 1

    two_back = 1
    one_back = 0
    for people in range(2, size + 1):
        current = (people - 1) * (one_back + two_back) % MODULO
        two_back, one_back = one_back, current
    return one_back
```

### Why the expert code is correct

- Person `1` has exactly `n-1` possible foreign gifts.
- For each choice, whether the gift owner receives gift `1` partitions valid
  assignments into disjoint `D[n-2]` and `D[n-1]` cases.
- The recurrence counts each derangement once through person `1`'s received
  gift and its corresponding case.
- Base cases match the empty and one-person assignments.

**Complexity:** `O(n)` time and `O(1)` memory.

## 7. What to remember

Derangements satisfy `D[n]=(n-1)(D[n-1]+D[n-2])`: choose the gift received by
one person, then split on whether a two-cycle is formed.
