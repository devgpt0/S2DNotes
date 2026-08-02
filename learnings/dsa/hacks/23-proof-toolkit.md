# A Compact Proof Toolkit

## First principles

A proof explains why each discarded choice is safe and why the remaining state
still contains an optimum. Choose the proof shape that matches the algorithm:
invariant for loops, induction for recursive states, and exchange for greedy
choices.

## Why it matters

A proof is a debugging tool. It tells you which facts the code must preserve
and exposes unsafe optimizations before submission.

## Technique

Choose the smallest proof style that fits.

### Loop invariant

State what is true before and after every iteration.

```text
binary search: the first feasible answer always remains in [left, right]
```

### Induction

Prove base states, then show smaller correct states make the next state correct.
This fits recursion, trees, and DP.

### Exchange argument

Show an optimal answer can replace its first differing choice with the greedy
choice without becoming worse.

### Cut argument

Show the cheapest safe edge across a partition belongs to some optimal spanning
tree.

### Contradiction

Assume the returned answer is not optimal and use the algorithm's invariant to
derive an impossible better candidate.

## Three-sentence proof template

```text
Invariant: ...
Each step preserves it because ...
At termination it implies the requested answer because ...
```

## Expert habit

Write the proof before implementation. Match variable names to the proof's
objects so code review is almost mechanical.

## Visual worked example: exchange an interval choice

Goal: attend the maximum number of non-overlapping activities.

```text
greedy chooses G, the activity ending earliest
an optimal schedule starts with O

G ends no later than O:
time ----G|
time --------O|

replace O with G
every later activity that fit after O also fits after G
schedule size does not decrease
```

After the exchange, the remaining problem has the same form, so the argument
repeats inductively.

## Traps

- Saying “obviously optimal” instead of proving a discarded choice is safe.
- Proving a recurrence but not its base cases or evaluation order.
- Proving correctness under an unstated assumption such as positive values.
