# Randomized Stress Testing

## First principles

A stress test repeatedly samples the small input space where an oracle is
affordable. A fixed seed makes the generated sequence deterministic, so the
first failure can be replayed exactly.

## Why it matters

Stress testing generates thousands of small cases and compares the fast answer
with a trusted oracle. It finds combinations humans do not think to write.

## Technique

Use a fixed seed so every failure is reproducible.

```python
from random import Random


def stress() -> None:
    random = Random(0)
    for case_index in range(20_000):
        size = random.randint(0, 9)
        values = [random.randint(-5, 5) for _ in range(size)]
        target = random.randint(-10, 10)
        expected = pair_count_brute(values, target)
        actual = pair_count_fast(values, target)
        if actual != expected:
            raise AssertionError(
                f'case={case_index} values={values} target={target} '
                f'expected={expected} actual={actual}'
            )
```

## Steps

1. Generate only valid inputs.
2. Bias generation toward boundaries and duplicates.
3. Compare canonical outputs.
4. Stop at the first failure and print every detail needed to replay it.
5. Minimize the failing case before changing code.

## Pattern recognition

Stress-test whenever a brute oracle exists and the optimized solution has a
non-obvious invariant or many branches.

## Expert habit

After fixing a bug, add the minimized input as a permanent regression test,
then run the same seed and new seeds.

## Visual worked example: find and shrink a failure

```text
seed 0
case 0 -> agree
case 1 -> agree
...
case 37:
values=[0,-1,0,2], target=0
expected=1, actual=2  -> stop

shrink while failure remains:
remove 2      -> [0,-1,0] still fails
remove -1     -> [0,0]    still fails
minimal case  -> [0,0], target=0
```

The minimized case usually exposes the missing rule—in this example, counting
one element with itself or mishandling duplicates.

## Traps

- Using the global random generator without recording a seed.
- Generating mostly easy uniform cases.
- Continuing after failure and flooding the useful first counterexample.
- Comparing floating values with exact equality.
