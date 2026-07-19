# Answer Key - ListUnifiedWorksheet_Additional

## Tricky Predict the Output

1. `2`
2. `-3`
3. `[a, X, c]`
4. `[1, 99, 3]`
5. `[1, 2, 3]`
6. `UnsupportedOperationException`
7. `ConcurrentModificationException`
8. `[1, 99, 2, 3]`
9. `3`
10. `[1]`
11. `[a, b]`
12. `UnsupportedOperationException`
13. `false`
14. `[1, 3, 5]`
15. `[z, y, x]`

## MCQ Answers

1. B  
2. B  
3. B  
4. B  
5. B  
6. B  
7. B  
8. B  
9. B  
10. B  
11. B  
12. A  
13. B  
14. B  
15. B

## Interview Key Points

1. `unmodifiableList` is view, `copyOf` is immutable snapshot.
2. For-each remove causes fail-fast; use `Iterator.remove` or `removeIf`.
3. `ListIterator` supports bidirectional traversal and add/set during iteration.
4. Non-found binary search returns `-(insertionPoint)-1`.
5. Immutable returns protect internal state and API contracts.
6. `ArrayList` random reads fast; `LinkedList` better at ends.
7. `Arrays.asList` fixed-size view; `set` works, `add/remove` fail.
8. `subList` is backed view; structural changes can invalidate iterators/views.
9. Missing `equals/hashCode` breaks semantic contains/remove for custom objects.
10. Example: `ArrayList` general storage, `LinkedList` deque workflows, `CopyOnWriteArrayList` read-heavy listeners.

