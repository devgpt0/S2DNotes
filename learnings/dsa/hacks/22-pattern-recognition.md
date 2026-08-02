# A Pattern-Recognition Decision Tree

## First principles

Pattern recognition is constraint matching, not keyword matching. Start from
the required operations and structural guarantees, then eliminate algorithms
whose preconditions or complexity do not fit.

## Why it matters

Experts do not memorize a solution for every story. They translate the story
into a small set of structural signals.

## Decision tree

```text
Is the answer about a contiguous range?
  -> static sums/counts: prefix sums
  -> moving valid range: sliding window
  -> nearest greater/smaller: monotonic stack/deque

Is input sorted or a yes/no condition monotone?
  -> two pointers or binary search

Is it connectivity/path structure?
  -> equal weights: BFS
  -> weights 0/1: 0-1 BFS
  -> non-negative weights: Dijkstra
  -> negative weights: Bellman-Ford

Are choices repeated across the same state?
  -> dynamic programming
  -> n near 20: bitmask/subset methods
  -> n near 40: meet in the middle

Are ranges updated and queried?
  -> offline adds: difference array
  -> point updates + sums: Fenwick tree
  -> general associative query: segment tree
  -> range updates: lazy segment tree
```

## Technique

Write three lines before coding:

```text
constraint budget:
state/invariant:
candidate patterns and why their assumptions hold:
```

## Pattern recognition

The best clue is often a guarantee: positivity enables sliding windows,
non-negative weights enable Dijkstra, a tree removes cycles, and a DAG gives a
topological order.

## Expert habit

Practice classifying solved problems without rereading their solutions. Then
practice explaining why tempting alternatives fail.

## Visual worked example: derive the pattern

```text
problem facts:
- static array
- 200,000 queries
- each asks sum on [left,right)

required operation: many static range sums
repeated work: adding the same prefixes
useful stored fact: total before every index

decision:
prefix sum -> O(n) build, O(1) per query

not chosen:
sliding window -> query ranges are unrelated
Fenwick tree   -> supports updates that do not exist
```

The story may mention cities or scores; the operation signature is what reveals
the technique.

## Traps

- Keyword matching without checking assumptions.
- Forcing a favorite structure onto every range problem.
- Choosing an advanced algorithm when a simpler one fits.
- Ignoring output size; generating all answers can be exponential by itself.
