# 14 - Legacy Coverage Map (List Module)

This file maps old or fragmented list notes to the current complete module so cleanup/refactor can be done safely.

## 1) Coverage for `ArrayList` Legacy Notes

Mapped to:

- `01-list-basics.md`: list contract, mutability, method families
- `02-arraylist-core.md`: internals, complexity, capacity, overload traps
- `06-list-iteration-patterns.md`: iteration choices
- `07-sorting-searching-and-binarysearch.md`: sorting/searching integration
- `09-immutability-and-defensive-copy.md`: `Arrays.asList`, immutable snapshots
- `10-performance-and-memory.md`: workload-based performance selection
- `11-common-bugs-and-best-practices.md`: runtime bug patterns

## 2) Coverage for `LinkedList` Legacy Notes

Mapped to:

- `03-linkedlist-core.md`: node model, deque operations, complexity
- `06-list-iteration-patterns.md`: iterator/listIterator usage
- `10-performance-and-memory.md`: cache/memory and operation tradeoffs
- `11-common-bugs-and-best-practices.md`: index-loop pitfalls

## 3) Coverage for `Vector` / `Stack` Legacy Notes

Mapped to:

- `04-vector-and-stack-core.md`: legacy rationale, APIs, capacity behavior, modern replacement strategy
- `10-performance-and-memory.md`: synchronization and overhead notes
- `11-common-bugs-and-best-practices.md`: thread-safety misconceptions

## 4) Coverage for `CopyOnWriteArrayList` Legacy Notes

Mapped to:

- `05-copyonwritearraylist-core.md`: snapshot semantics, cost model, concurrent examples
- `06-list-iteration-patterns.md`: fail-fast vs snapshot iteration
- `10-performance-and-memory.md`: write amplification and allocation impact

## 5) Coverage for Sorting / Comparator Legacy Notes

Mapped to:

- `07-sorting-searching-and-binarysearch.md`: stable sort, comparator-aware binary search
- `13-comparable-vs-comparator.md`: contract, chaining, null handling, mistakes
- `12-interview-and-practice.md`: interview drill and solved problems

## 6) Coverage for List + Lambda / Streams Notes

Mapped to:

- `08-list-with-lambda-and-streams.md`: map/filter/reduce/grouping/partitioning/flatMap
- `06-list-iteration-patterns.md`: stream vs loop iteration strategy
- `12-interview-and-practice.md`: applied stream problems

## 7) Coverage for Immutability / API Contract Notes

Mapped to:

- `09-immutability-and-defensive-copy.md`: mutable vs fixed vs unmodifiable vs immutable
- `11-common-bugs-and-best-practices.md`: unsupported operation and exposure bugs
- `01-list-basics.md`: mutability overview at foundation level

## 8) Coverage for Performance / Tuning Notes

Mapped to:

- `10-performance-and-memory.md`: complexity table, memory model, JMH guidance
- `02-arraylist-core.md`: capacity tuning
- `03-linkedlist-core.md`: traversal tradeoffs
- `05-copyonwritearraylist-core.md`: read-heavy concurrency economics

## 9) Recommended Study Order

1. `01-list-basics.md`
2. `02-arraylist-core.md`
3. `03-linkedlist-core.md`
4. `04-vector-and-stack-core.md`
5. `05-copyonwritearraylist-core.md`
6. `06-list-iteration-patterns.md`
7. `07-sorting-searching-and-binarysearch.md`
8. `08-list-with-lambda-and-streams.md`
9. `09-immutability-and-defensive-copy.md`
10. `10-performance-and-memory.md`
11. `11-common-bugs-and-best-practices.md`
12. `13-comparable-vs-comparator.md`
13. `12-interview-and-practice.md`
14. `14-legacy-coverage-map.md`

## 10) Module Status

Current `list` module is now complete for beginner-to-advanced learning:

- concept coverage
- implementation tradeoffs
- code snippets with expected outputs
- interview + practice readiness
- migration mapping from legacy fragments
