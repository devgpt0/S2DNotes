# Algorithms and Data Structures: Beginner to Expert

This is a concept-first competitive-programming course. Read it in order the
first time. Every implementation uses a small, explicit API so the algorithm
is visible instead of being buried in input parsing.

## Start here if you are new

1. If loops, functions, lists, and indexes are still difficult, finish
   [Python Starter 100](../python-starter-100/README.md) or [Java Starter 100](../java-starter-100/README.md) first.
2. Read [How to learn from a classroom note](00-classroom-learning-guide.md).
3. Keep the [simple DSA glossary](00-simple-glossary.md) open.
4. Follow the stages in order. Do not jump to graphs or DP because a problem
   name sounds interesting.

## Format used in every algorithm note

```text
Problem definition -> slow obvious method -> repeated work / useful fact
        -> invariant -> visual classroom trace -> steps
        -> pattern recognition -> C++ / Python / Java
        -> proof -> complexity -> mistakes
```

Every note contains an explicit **First-principles derivation** and a
**Classroom board** with a solved state-by-state example. The wording is
intentionally simple. Later topics become more advanced, but they keep the
same reasoning model so you can derive instead of memorize.

Every algorithm note now includes a **Classroom board** section. Cover the
algorithm and code, trace the example yourself, then compare your trace.

Reference code targets C++17, Python 3.12+, and Java 17+. Snippets focus on the
algorithm API; add the normal standard-library imports required by your judge.

## How to study each concept

1. Write the slow obvious solution before reading the derivation.
2. Identify its repeated work and compare it with the useful fact in the note.
3. Trace every line of the classroom board by hand.
4. State the invariant: what is guaranteed to be true at each step?
5. Derive the complexity from the operations; do not memorize it blindly.
6. Hide the code and implement it in your contest language.
7. Test the smallest case, boundaries, duplicates, and the largest shape.
8. Solve one direct problem, one disguised problem, and one timed problem.

> [!IMPORTANT]
> The code assumes valid, typed function arguments. In a contest, input is
> trusted to follow the statement. In production, validate external input
> before calling these algorithms.

## Stage 0 — Thinking like a problem solver

**Before this stage:** you can write a loop and a function. **Move on when:**
you can explain `O(n)`, trace recursion, and state what an invariant means.

1. [A repeatable problem-solving process](00-foundations/01-problem-solving-process.md)
2. [Time and space complexity](00-foundations/02-complexity.md)
3. [Correctness, invariants, and proofs](00-foundations/03-correctness-and-invariants.md)
4. [Recursion and the call stack](00-foundations/04-recursion.md)
5. [Bitmasks and subset enumeration](00-foundations/05-bitmasks.md)

## Stage 1 — Arrays, ranges, and searching

**Before this stage:** indexes and complexity feel comfortable. **Move on
when:** you can recognize prefix sum, two pointers, sliding window, and binary
search without seeing their names.

1. [Prefix sums](01-arrays-searching/01-prefix-sums.md)
2. [Difference arrays](01-arrays-searching/02-difference-arrays.md)
3. [Two pointers](01-arrays-searching/03-two-pointers.md)
4. [Sliding windows](01-arrays-searching/04-sliding-window.md)
5. [Binary search](01-arrays-searching/05-binary-search.md)
6. [Binary search on the answer](01-arrays-searching/06-binary-search-on-answer.md)
7. [Coordinate compression](01-arrays-searching/07-coordinate-compression.md)
8. [Meet in the middle](01-arrays-searching/08-meet-in-the-middle.md)

## Stage 2 — Sorting and selection

**Move on when:** you can explain stability, trace a merge, and choose between
library sort, counting sort, and selection without guessing.

1. [Sorting fundamentals and comparators](02-sorting/01-sorting-fundamentals.md)
2. [Merge sort](02-sorting/02-merge-sort.md)
3. [Quicksort](02-sorting/03-quicksort.md)
4. [Quickselect](02-sorting/04-quickselect.md)
5. [Counting sort](02-sorting/05-counting-sort.md)
6. [Radix sort](02-sorting/06-radix-sort.md)

## Stage 3 — Core data structures

**Move on when:** you can say what each structure stores, what operation is
fast, and what invariant keeps its answer correct.

1. [Stacks](03-data-structures/01-stack.md)
2. [Queues](03-data-structures/02-queue.md)
3. [Deques](03-data-structures/03-deque.md)
4. [Hash tables and frequency maps](03-data-structures/04-hashing.md)
5. [Heaps and priority queues](03-data-structures/05-heaps.md)
6. [Monotonic stacks](03-data-structures/06-monotonic-stack.md)
7. [Monotonic queues](03-data-structures/07-monotonic-queue.md)
8. [Disjoint-set union](03-data-structures/08-disjoint-set-union.md)
9. [Fenwick trees](03-data-structures/09-fenwick-tree.md)
10. [Segment trees](03-data-structures/10-segment-tree.md)
11. [Lazy propagation](03-data-structures/11-lazy-segment-tree.md)
12. [Sparse tables](03-data-structures/12-sparse-table.md)
13. [Tries](03-data-structures/13-trie.md)
14. [Square-root decomposition](03-data-structures/14-square-root-decomposition.md)

## Stage 4 — Graphs and trees

**Before this stage:** stack, queue, heap, and DSU are comfortable. **Move on
when:** you can choose BFS/0-1 BFS/Dijkstra/Bellman-Ford from edge weights and
can explain visited state precisely.

1. [Graph representation](04-graphs-trees/01-graph-representation.md)
2. [Breadth-first search](04-graphs-trees/02-breadth-first-search.md)
3. [Depth-first search](04-graphs-trees/03-depth-first-search.md)
4. [Cycle detection](04-graphs-trees/04-cycle-detection.md)
5. [Topological sorting](04-graphs-trees/05-topological-sort.md)
6. [0-1 BFS](04-graphs-trees/06-zero-one-bfs.md)
7. [Dijkstra's algorithm](04-graphs-trees/07-dijkstra.md)
8. [Bellman-Ford](04-graphs-trees/08-bellman-ford.md)
9. [Floyd-Warshall](04-graphs-trees/09-floyd-warshall.md)
10. [Kruskal's minimum spanning tree](04-graphs-trees/10-kruskal.md)
11. [Prim's minimum spanning tree](04-graphs-trees/11-prim.md)
12. [Strongly connected components](04-graphs-trees/12-strongly-connected-components.md)
13. [Bridges](04-graphs-trees/13-bridges.md)
14. [Articulation points](04-graphs-trees/14-articulation-points.md)
15. [Eulerian paths and circuits](04-graphs-trees/15-eulerian-paths.md)
16. [Tree diameter](04-graphs-trees/16-tree-diameter.md)
17. [Lowest common ancestor and binary lifting](04-graphs-trees/17-lowest-common-ancestor.md)
18. [Tree DP](04-graphs-trees/18-tree-dp.md)
19. [Rerooting DP](04-graphs-trees/19-rerooting-dp.md)
20. [Maximum flow](04-graphs-trees/20-maximum-flow.md)
21. [Bipartite matching](04-graphs-trees/21-bipartite-matching.md)
22. [2-SAT](04-graphs-trees/22-two-sat.md)

## Stage 5 — Greedy search and exhaustive search

**Move on when:** you can prove a greedy choice with an exchange argument and
undo every backtracking choice correctly.

1. [Greedy choice and exchange proofs](05-greedy-backtracking/01-greedy-and-exchange-arguments.md)
2. [Merging intervals](05-greedy-backtracking/02-merging-intervals.md)
3. [Sweep lines](05-greedy-backtracking/03-sweep-line.md)
4. [Backtracking](05-greedy-backtracking/04-backtracking.md)
5. [Branch and bound](05-greedy-backtracking/05-branch-and-bound.md)

## Stage 6 — Dynamic programming

**Before this stage:** recursion and brute force are comfortable. **Move on
when:** you can write the state meaning, transition, base case, and evaluation
order before writing code.

1. [DP state design](06-dynamic-programming/01-dp-state-design.md)
2. [0/1 knapsack](06-dynamic-programming/02-zero-one-knapsack.md)
3. [Unbounded knapsack](06-dynamic-programming/03-unbounded-knapsack.md)
4. [Longest increasing subsequence](06-dynamic-programming/04-longest-increasing-subsequence.md)
5. [Grid DP](06-dynamic-programming/05-grid-dp.md)
6. [Longest common subsequence](06-dynamic-programming/06-longest-common-subsequence.md)
7. [Edit distance](06-dynamic-programming/07-edit-distance.md)
8. [Interval DP](06-dynamic-programming/08-interval-dp.md)
9. [Bitmask DP](06-dynamic-programming/09-bitmask-dp.md)
10. [Digit DP](06-dynamic-programming/10-digit-dp.md)
11. [Sum over subsets DP](06-dynamic-programming/11-sos-dp.md)

## Stage 7 — Number theory and combinatorics

**Move on when:** you can derive—not only memorize—GCD, modular inverse,
combinations, and the prime preprocessing needed by a problem.

1. [Greatest common divisor](07-mathematics/01-greatest-common-divisor.md)
2. [Extended Euclidean algorithm](07-mathematics/02-extended-euclid.md)
3. [Modular arithmetic](07-mathematics/03-modular-arithmetic.md)
4. [Fast exponentiation](07-mathematics/04-fast-exponentiation.md)
5. [Sieve of Eratosthenes](07-mathematics/05-sieve-of-eratosthenes.md)
6. [Prime factorization](07-mathematics/06-prime-factorization.md)
7. [Euler's totient function](07-mathematics/07-euler-totient.md)
8. [Combinations modulo a prime](07-mathematics/08-combinatorics.md)
9. [Inclusion-exclusion](07-mathematics/09-inclusion-exclusion.md)
10. [Chinese remainder theorem](07-mathematics/10-chinese-remainder-theorem.md)
11. [Matrix exponentiation](07-mathematics/11-matrix-exponentiation.md)
12. [Probability and expected value](07-mathematics/12-probability-and-expectation.md)
13. [Game theory and Nim](07-mathematics/13-game-theory.md)

## Stage 8 — String algorithms

**Before this stage:** arrays and prefix ideas are comfortable. **Move on
when:** you can trace fallback links/ranks and explain which repeated character
comparisons are avoided.

1. [KMP prefix function](08-strings/01-kmp-prefix-function.md)
2. [Z algorithm](08-strings/02-z-algorithm.md)
3. [Rolling hash](08-strings/03-rolling-hash.md)
4. [Manacher's algorithm](08-strings/04-manacher.md)
5. [Suffix arrays](08-strings/05-suffix-array.md)
6. [Longest common prefix array](08-strings/06-lcp-array.md)
7. [Aho-Corasick](08-strings/07-aho-corasick.md)
8. [Suffix automaton](08-strings/08-suffix-automaton.md)

## Stage 9 — Geometry and advanced techniques

**Do not rush here.** These notes assume every earlier stage is usable under
time pressure. Read one advanced topic only when a problem or practice set
needs it.

1. [Geometry primitives](09-advanced/01-geometry-primitives.md)
2. [Convex hull](09-advanced/02-convex-hull.md)
3. [Mo's algorithm](09-advanced/03-mos-algorithm.md)
4. [Heavy-light decomposition](09-advanced/04-heavy-light-decomposition.md)
5. [Centroid decomposition](09-advanced/05-centroid-decomposition.md)
6. [Persistent segment trees](09-advanced/06-persistent-segment-tree.md)
7. [Number-theoretic transform](09-advanced/07-number-theoretic-transform.md)

## Mastery checkpoints

| Level | You can reliably do this |
| --- | --- |
| Beginner | Derive complexity; use prefix sums, two pointers, binary search, BFS, and DFS |
| Intermediate | Select the right data structure; solve shortest path, MST, greedy, and standard DP problems |
| Advanced | Combine techniques; prove correctness; use range trees, string algorithms, flow, and tree decompositions |
| Expert | Recognize reductions, derive new states/invariants, stress-test solutions, and execute under time pressure |

The [competitive-programming hacks](../hacks/README.md) are part of the course,
not optional polish. Most wrong answers come from implementation and reasoning
failures rather than missing an advanced algorithm.
