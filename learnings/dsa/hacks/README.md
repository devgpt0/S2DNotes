# Python Competitive-Programming Playbook

These notes turn Python knowledge into reliable contest execution. Read them in
order once, then use them as a pre-contest and wrong-answer checklist.

> [!IMPORTANT]
> “Hack” here means a legal competitive-programming technique: faster input,
> better testing, sharper reasoning, or safer implementation. It does not mean
> attacking systems or other contestants.

## Format

```text
First principle -> Why it matters -> Technique -> Python pattern
                -> Visual worked example -> Traps
```

Every note explains the runtime or correctness fact behind the technique. The
worked example then shows exactly what Python stores, copies, compares, or
executes. Learn the reason first; the short syntax becomes easy to remember.

## Stage 1 — Write fast, predictable Python

1. [Fast input and output](01-fast-input-output.md)
2. [A minimal contest template](02-minimal-contest-template.md)
3. [Turn constraints into an algorithm budget](03-constraints-to-complexity.md)
4. [Python complexity traps](04-python-complexity-traps.md)
5. [Recursion and stack safety](05-recursion-and-stack-safety.md)
6. [Integer and modular arithmetic](06-integer-and-modular-arithmetic.md)
7. [Floating-point safety](07-floating-point-safety.md)
8. [Choose the right built-in collection](08-efficient-collections.md)
9. [Sorting like a competitor](09-sorting-techniques.md)
10. [Bisect and boundary searches](10-bisect-boundaries.md)
11. [Heaps and lazy deletion](11-heap-lazy-deletion.md)
12. [Fast string construction and parsing](12-string-performance.md)
13. [Graph performance in Python](13-graph-performance.md)
14. [Dynamic-programming performance](14-dp-performance.md)
15. [Memory engineering](15-memory-engineering.md)

## Stage 2 — Make wrong answers unlikely

16. [The edge-case matrix](16-edge-case-matrix.md)
17. [Assertions and useful debugging](17-assertions-and-debugging.md)
18. [Brute-force oracles](18-brute-force-oracles.md)
19. [Randomized stress testing](19-randomized-stress-testing.md)
20. [Build adversarial tests](20-adversarial-tests.md)
21. [Benchmark before optimizing](21-benchmarking.md)

## Stage 3 — Think and compete at a high level

22. [A pattern-recognition decision tree](22-pattern-recognition.md)
23. [A compact proof toolkit](23-proof-toolkit.md)
24. [Contest time management](24-contest-strategy.md)
25. [Interactive-problem discipline](25-interactive-problems.md)

## Progression

```text
correct idea
   -> complexity fits
      -> Python implementation fits
         -> edge cases + oracle + stress test
            -> calm contest execution
```

Expertise still requires deliberate problem solving. Use the notes to shorten
the feedback loop: solve, test, submit, study the failure, and solve again.
