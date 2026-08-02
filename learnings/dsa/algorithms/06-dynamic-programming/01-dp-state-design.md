# Dynamic Programming State Design

## Idea

Dynamic programming (DP) solves overlapping subproblems once. A state stores
exactly the information the future needs—no less and no more.

## Visual model

```text
state -> smaller states -> store answer -> reuse instead of recomputing
```

## Classroom board: see repeated work

```text
ways(4) asks ways(3) and ways(2)
ways(3) asks ways(2) and ways(1)
ways(2) was requested twice

store ways(2) once -> reuse it
```

The state is just “how many steps remain/current step,” because no other past
detail changes future choices.

## Steps

Answer four questions before coding:

1. **State:** what does `dp[...]` mean in one sentence?
2. **Transition:** which smaller states produce it?
3. **Base case:** which states are known immediately?
4. **Order:** when a state is computed, are its dependencies ready?

## First-principles derivation

Start with a brute-force recursion and write the exact information that makes
two future subproblems identical. That information is the DP state.

```text
state meaning -> choices -> smaller states
              -> base cases -> evaluation order
```

Memoization is correct because equal states have equal remaining choices and
therefore equal answers.

## Pattern recognition

Use DP when a brute-force recursion repeats the same state and the optimal
answer can be built from optimal answers to smaller states.

## Implementation: number of ways to climb stairs

### C++

```cpp
long long climbWays(int steps) {
    if (steps <= 1) return 1;
    long long previousTwo = 1;
    long long previousOne = 1;
    for (int current = 2; current <= steps; ++current) {
        const long long ways = previousOne + previousTwo;
        previousTwo = previousOne;
        previousOne = ways;
    }
    return previousOne;
}
```

### Python

```python
def climb_ways(steps: int) -> int:
    if steps <= 1:
        return 1
    previous_two = previous_one = 1
    for _ in range(2, steps + 1):
        previous_two, previous_one = previous_one, previous_one + previous_two
    return previous_one
```

### Java

```java
static long climbWays(int steps) {
    if (steps <= 1) return 1;
    long previousTwo = 1;
    long previousOne = 1;
    for (int current = 2; current <= steps; current++) {
        long ways = previousOne + previousTwo;
        previousTwo = previousOne;
        previousOne = ways;
    }
    return previousOne;
}
```

## Why it works

Every final move came from exactly one or two steps below, so the two sets of
ways are disjoint and complete. Only the previous two states are needed.

## Complexity

Time is `O(steps)` and extra space is `O(1)`.

## Common mistakes

- Defining a state vaguely.
- Adding dimensions that the transition does not need.
- Updating compressed states in an order that reuses the current item.
- Confusing number of ways, minimum cost, and feasibility transitions.
