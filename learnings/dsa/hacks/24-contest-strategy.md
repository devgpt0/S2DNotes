# Contest Time Management

## First principles

Contest score comes from solved problems under a fixed clock. Time spent has an
opportunity cost, so decisions should use evidence: progress made, remaining
implementation risk, and the availability of easier problems.

## Why it matters

Contest rank depends on correct submissions under limited time, not the hardest
idea you can eventually solve.

## Technique

### First pass

1. Read every problem's constraints and output.
2. Mark likely complexity and confidence.
3. Solve the highest-confidence, shortest implementation first.

### During a problem

```text
understand -> derive -> prove -> code -> edge tests -> submit
```

Set a checkpoint. If no new concrete progress appears for a long block of time,
write down what is missing and switch problems.

### After a wrong answer

Classify before editing:

- misunderstood statement;
- wrong algorithm/proof;
- missing edge case;
- implementation bug;
- overflow/precision;
- complexity/resource failure;
- output format.

## Expert habit

Keep a short contest log: problem, failed assumption, smallest counterexample,
and lesson. Re-solve missed problems later without looking at the editorial.

## Submission checklist

- correct test-case loop;
- correct indexing conversion;
- no debug output;
- complexity fits maximum constraints;
- empty/single/boundary tests checked;
- output format exact.

## Visual worked example: a controlled first hour

```text
00-10  read all problems; record constraints and likely patterns
10-30  solve the clearest low-risk problem
30-45  solve or code the next best candidate
45-50  if stuck with no new invariant, leave a short note and switch
50-60  test and submit completed work

after every wrong answer:
classify -> idea | complexity | implementation | edge case
then change one justified thing
```

A time box is a decision checkpoint, not an automatic surrender when one more
clear step is available.

## Traps

- Coding before the invariant is clear.
- Spending the entire contest protecting sunk time on one problem.
- Making several speculative edits after a wrong answer.
- Reading editorials without later implementing the idea from memory.
