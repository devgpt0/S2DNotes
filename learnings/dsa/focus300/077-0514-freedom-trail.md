# Focus300 077: LeetCode 514 - Freedom Trail

**Source:** [LeetCode 514](https://leetcode.com/problems/freedom-trail/)  
**Difficulty:** Hard  
**Pattern:** dynamic programming over repeated ring positions

## Exact contract

A circular ring starts with index zero aligned at twelve o'clock. For every
character of a nonempty key, rotate the ring clockwise or counterclockwise to
align an equal character, then press the button once. Each one-position rotation
and each press costs one step. Return the minimum total; every key character is
guaranteed to occur in the ring.

## First principles

After spelling a key prefix, only the ring index currently aligned at twelve
o'clock matters. For each occurrence of the next character, combine the best
cost at every previous aligned index with the shorter circular rotation distance
and one button press.


## Classroom board: store the repeated state once

```text
brute force recomputes the same subproblem many times.
dp keeps the smallest useful state and extends it one step at a time.
```



## Step-by-step transformation

1. Turn the input into subproblems, prefixes, or states that can be reused.
2. Fill the base cases first so later states have something correct to build on.
3. Update each new state from earlier states while keeping the recurrence valid.
4. Read the answer from the final table entry or the best state collected at the end.

Dynamic-programming style notes transform the input by compressing many repeated choices into a small set of reusable states.


## Diagram: state table to answer

```text

            input
                |
                v
            base states
                |
                v
            reuse smaller states
                |
                v
            final dp answer
```

These notes compress repeated choices into reusable states, then read the answer from the last state that matters.

## Cases that decide correctness

- The ring may contain repeated copies of a key character.
- Clockwise and counterclockwise distances wrap around.
- Staying on the same index costs zero rotation but still one press.
- Greedily choosing the nearest current occurrence can hurt later characters.
- The initial aligned index is zero.

## Brute force: recurse through every occurrence sequence

```python
def freedom_trail_steps_brute(ring: str, key: str) -> int:
    if not ring or not key or any(character not in ring for character in key):
        raise ValueError("ring and key must be nonempty and spellable")

    positions = {
        character: [index for index, value in enumerate(ring) if value == character]
        for character in set(ring)
    }

    def search(ring_index: int, key_index: int) -> int:
        if key_index == len(key):
            return 0
        answer = 10**9
        for target in positions[key[key_index]]:
            difference = abs(target - ring_index)
            rotation = min(difference, len(ring) - difference)
            answer = min(answer, rotation + 1 + search(target, key_index + 1))
        return answer

    return search(0, 0)
```

This revisits the same `(ring_index, key_index)` states exponentially often.

## Better approach: memoize aligned index and key offset

```python
from functools import cache


def freedom_trail_steps_memoized(ring: str, key: str) -> int:
    if not ring or not key or any(character not in ring for character in key):
        raise ValueError("ring and key must be nonempty and spellable")

    positions = {
        character: [index for index, value in enumerate(ring) if value == character]
        for character in set(ring)
    }

    @cache
    def search(ring_index: int, key_index: int) -> int:
        if key_index == len(key):
            return 0
        return min(
            min(
                abs(target - ring_index),
                len(ring) - abs(target - ring_index),
            )
            + 1
            + search(target, key_index + 1)
            for target in positions[key[key_index]]
        )

    return search(0, 0)
```

Memoization evaluates each reachable state once.

## Expert solution: iterative costs on relevant positions

```python
def freedom_trail_steps(ring: str, key: str) -> int:
    if not ring or not key or any(character not in ring for character in key):
        raise ValueError("ring and key must be nonempty and spellable")

    positions = {
        character: [index for index, value in enumerate(ring) if value == character]
        for character in set(ring)
    }
    costs = {0: 0}
    for character in key:
        next_costs: dict[int, int] = {}
        for target in positions[character]:
            next_costs[target] = min(
                cost
                + min(
                    abs(target - previous),
                    len(ring) - abs(target - previous),
                )
                + 1
                for previous, cost in costs.items()
            )
        costs = next_costs
    return min(costs.values())
```

`costs[position]` is exactly the minimum cost for the processed key prefix
ending at that aligned occurrence. The transition tries every possible previous
occurrence and the exact shorter rotation, so induction over key characters
proves optimality.

**Complexity:** `O(len(key) * len(ring)^2)` worst-case time and `O(len(ring))`
space.
