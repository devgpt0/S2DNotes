# The Edge-Case Matrix

## First principles

Bugs cluster at boundaries created by the problem's dimensions: size, value,
order, duplication, answer position, and graph shape. Build tests by taking the
extreme of each relevant dimension instead of guessing random examples.

## Why it matters

Random examples rarely hit the boundary that breaks an otherwise correct idea.
A fixed checklist makes testing repeatable.

## Technique

Create one test from every relevant row before submission.

| Category | Tests |
| --- | --- |
| size | empty if allowed, one item, two items, maximum size |
| values | zero, negative, maximum magnitude, all equal |
| order | sorted, reverse sorted, alternating high/low |
| answer | absent, first position, last position, whole input |
| duplicates | none, some, all duplicates |
| graph | isolated vertex, disconnected, path, star, cycle, parallel edges |
| ranges | one point, full range, touching ranges, disjoint ranges |
| arithmetic | answer zero, modulo boundary, overflow-sized fixed-width result |

## Python pattern

Keep tiny direct tests beside the function while developing:

```python
def run_tests() -> None:
    assert lower_bound([], 4) == 0
    assert lower_bound([4], 4) == 0
    assert lower_bound([1, 4, 4, 9], 4) == 1
    assert lower_bound([1, 4, 4, 9], 10) == 4
```

Remove or guard large local test harnesses before submission.

## Pattern recognition

Derive tests from every branch and every assumption in the proof. If the proof
says “positive values,” test zero/negative input only if the statement permits
it; otherwise confirm the constraint is explicit.

## Expert habit

For each variable, ask for its minimum, maximum, and equality boundary. For
each data structure, ask when it is empty and when it contains duplicates.

## Visual worked example: binary-search test matrix

```text
dimension       cases
size            [] | [5] | many
target position before first | first | middle | last | after last
duplicates      none | all equal | duplicate boundary
values          negative | zero | positive

selected tests:
([], 3)
([5], 5)
([2,2,2], 2)
([-4,0,7], -5)
([-4,0,7], 8)
```

Each test attacks a different branch or interval boundary; samples usually
cover only one.

## Traps

- Testing only official samples.
- Inventing invalid tests and “fixing” correct code for them.
- Forgetting multiple test cases can leak state.
- Checking the result but not required ordering or formatting.
