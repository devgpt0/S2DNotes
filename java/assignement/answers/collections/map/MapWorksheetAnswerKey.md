# Answer Key - MapWorksheet

## Tricky Predict the Output

1. `null`, `1`, `5` (printed on separate lines)
2. `null` then `true`
3. `3`
4. `[10, 20]`
5. `{A=15}`
6. `{2=B, 1=A, 3=C}`
7. `{2=B, 3=C, 1=A}`
8. `30`
9. `UnsupportedOperationException`
10. `NullPointerException`
11. `{NEW=1, DONE=2}`
12. `a:b`
13. `B2`
14. `true`
15. `99`

## MCQ Answers

1. B  
2. C  
3. A  
4. B  
5. C  
6. B  
7. A  
8. C  
9. B  
10. C  
11. B  
12. B  
13. C  
14. B  
15. C

## Interview Key Points

1. Hash -> bucket index -> collision handling -> resize by threshold.
2. Equal keys must share hash; both methods required for lookup correctness.
3. HashMap unordered fast, LinkedHashMap ordered, TreeMap sorted `O(log n)`.
4. `compute*`/`merge` reduce boilerplate and avoid check-then-act errors.
5. `ConcurrentHashMap` scales better and has modern atomic APIs.
6. Null rules vary; especially strict in `ConcurrentHashMap` and immutable maps.
7. Access-order `LinkedHashMap` + `removeEldestEntry` gives LRU eviction.
8. EnumMap for enums, WeakHashMap for lifecycle metadata, IdentityHashMap for identity semantics.
9. Verify key mutability and `equals/hashCode`; log key/value/hash behavior.
10. Test overwrite, null handling, ordering, compute/merge behavior, and concurrent cases where relevant.

