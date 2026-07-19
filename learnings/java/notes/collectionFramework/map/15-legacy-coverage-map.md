# 15 - Legacy Coverage Map (Map Module)

This file maps old and fragmented notes to the current complete `map` learning path.

## 1) Basics Coverage

- map fundamentals, uniqueness, null overview, map vs list/set -> `01-map-basics.md`
- first program and API families -> `01-map-basics.md`

## 2) HashMap Core Coverage

- internals: hashing, buckets, collisions -> `02-hashmap-core.md`
- load factor/capacity/resize strategy -> `02-hashmap-core.md`, `11-performance-and-memory.md`
- key contracts (`equals/hashCode`) -> `02-hashmap-core.md`, `06-pitfalls-and-best-practices.md`

## 3) API Method Coverage

- read/write/query APIs -> `03-map-methods-with-output.md`
- compute/merge APIs -> `03-map-methods-with-output.md`, `12-map-design-patterns.md`
- backed views and iteration -> `03-map-methods-with-output.md`, `13-debugging-and-testing-maps.md`

## 4) Implementation Selection Coverage

- map selection matrix -> `04-map-implementations.md`
- ordered vs sorted behavior -> `08-ordered-sorted-and-sequenced-views.md`
- specialized map recommendations -> `10-specialized-maps-and-immutability.md`

## 5) Pattern Coverage

- counting/grouping/top-k/two-sum -> `05-common-patterns.md`, `14-map-practice-problems.md`
- multi-level aggregation -> `05-common-patterns.md`, `12-map-design-patterns.md`
- LRU cache pattern -> `05-common-patterns.md`, `01-linkedhashmap-core.md`

## 6) Reliability Coverage

- pitfalls and runtime bugs -> `06-pitfalls-and-best-practices.md`
- debugging and test strategies -> `13-debugging-and-testing-maps.md`
- thread-safety and atomic updates -> `09-thread-safety-and-concurrency.md`

## 7) Performance Coverage

- complexity and memory tradeoffs -> `11-performance-and-memory.md`
- pre-sizing and key hash quality -> `02-hashmap-core.md`, `11-performance-and-memory.md`

## 8) Interview + Practice Coverage

- rapid revision and speaking templates -> `07-interview-revision.md`
- graded practice from beginner to expert -> `14-map-practice-problems.md`

## 9) Specialized Deep-Dive Coverage

- `01-linkedhashmap-core.md`
- `02-treemap-core.md`
- `03-concurrenthashmap-core.md`
- `04-weakhashmap-core.md`
- `05-identityhashmap-core.md`
- `06-enummap-core.md`
- `07-immutable-map-core.md`
- `08-hashtable-core.md`

These files are retained as focused implementation references.

## 10) Module Status

`map` module now includes:

- complete conceptual progression
- implementation deep dives
- snippet-by-snippet teaching intent
- expected outputs and explanations
- practice + interview readiness
