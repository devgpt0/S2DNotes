# Python Collection Framework - Mastery Roadmap

This roadmap makes `python/notes/collection_framework` a full coverage track for interviews and production use.

## 1) What "Collection Framework Mastery" Means

You can:
- choose the right collection by workload shape.
- reason about time and memory tradeoffs.
- avoid common mutation/copy/hashability bugs.
- use stdlib collection tools beyond basics (`collections`, `heapq`, `bisect`).
- design clean, testable APIs with collection abstractions.

## 2) Coverage Map in This Folder

1. `list.md`
2. `tuple.md`
3. `set.md`
4. `dict.md`
5. `10_collections_module_mastery.md`
6. `11_heapq_bisect_mastery.md`
7. `12_collections_abc_and_typing.md`
8. `13_specialized_sequence_types.md`
9. `14_itertools_for_collections.md`

## 3) Study Sequence

1. Start with `list.md` and `tuple.md`.
2. Move to `set.md` and `dict.md`.
3. Learn `collections` module special types.
4. Learn `heapq` and `bisect` for algorithmic problem-solving.
5. Finish with `collections.abc` and typing-oriented API design.

## 4) Concept Checklist (Must-Master)

- Mutable vs immutable containers
- Hashability and key safety
- Shallow vs deep copy
- Ordered behavior and iteration guarantees
- In-place vs functional-style operations
- Queue/stack/priority use-cases
- Mapping and set algebra patterns
- Custom containers via `collections.abc`

## 5) Interview Readiness Checklist

1. Explain why `deque` is preferred over list for queue front pops.
2. Explain `dict` insertion order guarantees and `OrderedDict` relevance.
3. Explain when to use `Counter`, `defaultdict`, and `ChainMap`.
4. Explain `heapq` top-k strategy and complexity.
5. Explain `bisect` for maintaining sorted lists.
6. Explain hashability constraints for dict/set keys.
7. Explain copy semantics for nested containers.

## 6) Production Readiness Checklist

1. Data-shape choices are deliberate and documented.
2. Mutation boundaries are explicit.
3. Memory hotspots are profiled, not guessed.
4. Collection operations in hot paths have expected complexity.
5. Boundary outputs are deterministic where needed (sorted order at APIs/reports).
