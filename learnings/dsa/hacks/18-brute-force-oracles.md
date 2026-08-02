# Brute-Force Oracles

## First principles

A brute-force solution explores the definition directly. It may be too slow
for the judge, but on tiny inputs it is easier to trust than an optimized
solution. Comparing both turns correctness into an executable check.

## Why it matters

A simple slow solution is often easier to trust than the optimized solution.
On small inputs it becomes an oracle that tells you whether optimization
changed the answer.

## Technique

Write the direct definition first and keep it separate from optimized code.

```python
def pair_count_brute(values: list[int], target: int) -> int:
    return sum(
        values[first] + values[second] == target
        for first in range(len(values))
        for second in range(first + 1, len(values))
    )


def pair_count_fast(values: list[int], target: int) -> int:
    frequency: dict[int, int] = {}
    answer = 0
    for value in values:
        answer += frequency.get(target - value, 0)
        frequency[value] = frequency.get(value, 0) + 1
    return answer
```

## Oracle design rules

- Follow the statement literally.
- Prefer enumeration over a second clever algorithm.
- Limit it to small input.
- Return a canonical result: sort unordered answer sets before comparing.

## Pattern recognition

Oracles are especially useful for greedy claims, optimized DP, graph
algorithms, range structures, and any solution with complex case analysis.

## Expert habit

Keep the oracle during development even after samples pass. Connect it to the
stress-testing loop in the next note.

## Visual worked example: pair-count oracle

For `values=[1,2,3,3]`, target `4`:

```text
brute index pairs:
(0,1): 1+2=3
(0,2): 1+3=4 yes
(0,3): 1+3=4 yes
(1,2): 2+3=5
(1,3): 2+3=5
(2,3): 3+3=6
expected = 2

fast frequency solution returns 2 -> agrees
```

Keep the oracle structurally different from the optimized algorithm so they
are unlikely to share the same bug.

## Traps

- Sharing helper logic with the fast solution; one bug can infect both.
- Comparing lists when answer order is irrelevant.
- Using the oracle at maximum constraints.
- Assuming the brute solution is correct without testing its own tiny cases.
