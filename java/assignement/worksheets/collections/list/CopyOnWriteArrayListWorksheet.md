# CopyOnWriteArrayList Worksheet

Source: CopyOnWriteArrayList Notes.md

## Level 1

### Tricky Predict the Output (15)

1.
```java
CopyOnWriteArrayList<Integer> l = new CopyOnWriteArrayList<>(List.of(1,2,3));
l.add(4);
System.out.println(l);
```

Answer: _____________

2.
```java
CopyOnWriteArrayList<Integer> l = new CopyOnWriteArrayList<>(List.of(1,2,3));
l.remove(Integer.valueOf(2));
System.out.println(l);
```

Answer: _____________

3.
```java
CopyOnWriteArrayList<Integer> l = new CopyOnWriteArrayList<>(List.of(1,2,3));
l.set(1,9);
System.out.println(l);
```

Answer: _____________

4.
```java
CopyOnWriteArrayList<String> l = new CopyOnWriteArrayList<>(List.of("a","b"));
System.out.println(l.contains("c"));
```

Answer: _____________

5.
```java
CopyOnWriteArrayList<Integer> l = new CopyOnWriteArrayList<>(List.of(1,2,3));
Iterator<Integer> it = l.iterator();
l.add(4);
while(it.hasNext()) System.out.print(it.next());
```

Answer: _____________

6.
```java
CopyOnWriteArrayList<Integer> l = new CopyOnWriteArrayList<>(List.of(1,2));
Iterator<Integer> it = l.iterator();
it.next();
it.remove();
```

Answer: _____________

7.
```java
CopyOnWriteArrayList<String> l = new CopyOnWriteArrayList<>();
l.add("x");
l.remove("y");
System.out.println(l.size());
```

Answer: _____________

8.
```java
CopyOnWriteArrayList<Integer> l = new CopyOnWriteArrayList<>(List.of(1,2,3,4));
l.removeIf(x -> x % 2 == 0);
System.out.println(l);
```

Answer: _____________

9.
```java
CopyOnWriteArrayList<Integer> l = new CopyOnWriteArrayList<>(List.of(1,2,3));
Object[] a = l.toArray();
System.out.println(a.length);
```

Answer: _____________

10.
```java
CopyOnWriteArrayList<String> l = new CopyOnWriteArrayList<>(List.of("a","b"));
l.addIfAbsent("b");
System.out.println(l);
```

Answer: _____________

11.
```java
CopyOnWriteArrayList<String> l = new CopyOnWriteArrayList<>(List.of("a","b"));
l.addIfAbsent("c");
System.out.println(l);
```

Answer: _____________

12.
```java
CopyOnWriteArrayList<Integer> l = new CopyOnWriteArrayList<>(List.of(1,2,3));
System.out.println(l.get(2));
```

Answer: _____________

13.
```java
CopyOnWriteArrayList<Integer> l = new CopyOnWriteArrayList<>(List.of(1,2,3));
System.out.println(l.size());
```

Answer: _____________

14.
```java
CopyOnWriteArrayList<Integer> l = new CopyOnWriteArrayList<>(List.of(1,2,3));
l.clear();
System.out.println(l.isEmpty());
```

Answer: _____________

15.
```java
CopyOnWriteArrayList<Integer> l = new CopyOnWriteArrayList<>(List.of(1,2,3));
for(Integer x : l){ if(x==2) l.add(99);
} System.out.println(l);
```

Answer: _____________

### MCQ Theory (15)

1. Copy-on-write means write operations:
```text
A) mutate same array directly
B) copy array then swap reference
C) are disallowed
D) are lock-free always
```

2. Best workload for `CopyOnWriteArrayList`:
```text
A) write-heavy
B) read-heavy concurrent
C) CPU-bound math
D) disk IO only
```

3. Iterator behavior is:
```text
A) fail-fast
B) snapshot-based
C) random
D) lock-step live
```

4. Write complexity is typically:
```text
A) O(1)
B) O(log n)
C) O(n)
D) O(n^2)
```

5. `iterator.remove()` on COW iterator:
```text
A) supported
B) unsupported
C) async
D) no-op
```

6. Read by index complexity is usually:
```text
A) O(1)
B) O(log n)
C) O(n)
D) O(n^2)
```

7. `addIfAbsent` does:
```text
A) always append
B) append only if absent
C) prepend only
D) remove duplicates fully
```

8. Main tradeoff of COW:
```text
A) low write cost
B) high write cost + safe iteration
C) no memory use
D) no reads allowed
```

9. `remove("missing")` generally returns:
```text
A) exception
B) false
C) null
D) -1
```

10. `toArray()` returns:
```text
A) same internal array
B) new array copy
C) map
D) set
```

11. Why no `ConcurrentModificationException` in normal iteration?
```text
A) no iterators exist
B) snapshot iterator over stable array
C) synchronized sort
D) immutable class
```

12. Compared to Vector in read-heavy cases, COW can be:
```text
A) worse always
B) better for low-contention reads
C) same always
D) not thread-safe
```

13. COW is poor when:
```text
A) reads dominate
B) writes are frequent and large
C) list is tiny
D) single thread only
```

14. `reversed()` returns:
```text
A) copied list
B) reverse-order view
C) sorted list
D) deque
```

15. `addFirst` / `addLast` in COW are generally:
```text
A) O(1)
B) O(log n)
C) O(n) due full copy
D) unsupported
```

## Level 2

### Tricky Predict the Output (15)

1.
```java
CopyOnWriteArrayList<Integer> l = new CopyOnWriteArrayList<>(List.of(1,2,3));
List<Integer> r = l.reversed();
System.out.println(r);
```

Answer: _____________

2.
```java
CopyOnWriteArrayList<Integer> l = new CopyOnWriteArrayList<>(List.of(1,2,3));
List<Integer> r = l.reversed();
l.set(0,99);
System.out.println(r.get(2));
```

Answer: _____________

3.
```java
CopyOnWriteArrayList<Integer> l = new CopyOnWriteArrayList<>(List.of(1,2,3));
l.addFirst(0);
System.out.println(l);
```

Answer: _____________

4.
```java
CopyOnWriteArrayList<Integer> l = new CopyOnWriteArrayList<>(List.of(1,2,3));
l.addLast(4);
System.out.println(l);
```

Answer: _____________

5.
```java
CopyOnWriteArrayList<Integer> l = new CopyOnWriteArrayList<>(List.of(1,2,3));
l.removeFirst();
System.out.println(l);
```

Answer: _____________

6.
```java
CopyOnWriteArrayList<Integer> l = new CopyOnWriteArrayList<>(List.of(1,2,3));
l.removeLast();
System.out.println(l);
```

Answer: _____________

7.
```java
CopyOnWriteArrayList<Integer> l = new CopyOnWriteArrayList<>(List.of(1,2,3));
System.out.println(l.getFirst() + ":" + l.getLast());
```

Answer: _____________

8.
```java
CopyOnWriteArrayList<String> l = new CopyOnWriteArrayList<>(List.of("a",null,"b"));
l.remove(null);
System.out.println(l);
```

Answer: _____________

9.
```java
CopyOnWriteArrayList<String> l = new CopyOnWriteArrayList<>(List.of("a","b"));
Object[] a = l.toArray();
l.add("c");
System.out.println(a.length + ":" + l.size());
```

Answer: _____________

10.
```java
CopyOnWriteArrayList<Integer> l = new CopyOnWriteArrayList<>(List.of(1,2,3));
Iterator<Integer> i1 = l.iterator();
l.add(4);
Iterator<Integer> i2 = l.iterator();
System.out.println(i1.next() + ":" + i2.next());
```

Answer: _____________

11.
```java
CopyOnWriteArrayList<Integer> l = new CopyOnWriteArrayList<>(List.of(1,2,3));
System.out.println(l.remove(Integer.valueOf(9)));
```

Answer: _____________

12.
```java
CopyOnWriteArrayList<Integer> l = new CopyOnWriteArrayList<>(List.of(1,2,3));
l.removeAll(List.of(2,5));
System.out.println(l);
```

Answer: _____________

13.
```java
CopyOnWriteArrayList<String> l = new CopyOnWriteArrayList<>(List.of("x","y"));
l.replaceAll(String::toUpperCase);
System.out.println(l);
```

Answer: _____________

14.
```java
CopyOnWriteArrayList<Integer> l = new CopyOnWriteArrayList<>(List.of(1,2,3,4));
l.removeIf(x -> x > 2);
System.out.println(l);
```

Answer: _____________

15.
```java
CopyOnWriteArrayList<Integer> l = new CopyOnWriteArrayList<>(List.of(1,2,3));
for(Integer x : l){ l.remove(Integer.valueOf(2));
} System.out.println(l);
```

Answer: _____________

### MCQ Theory (15)

1. Snapshot iterator sees:
```text
A) all future writes
B) list state at iterator creation
C) no elements
D) random updates
```

2. COW write path generally causes:
```text
A) no allocations
B) full-array copy allocation
C) disk write
D) recursion
```

3. Good use case:
```text
A) subscriber list with many readers
B) high-frequency writer queue
C) numeric matrix
D) LRU cache internals
```

4. Bad use case:
```text
A) 99% reads
B) huge list + frequent writes
C) mostly iteration
D) occasional append
```

5. `addFirst` in COW complexity:
```text
A) O(1)
B) O(log n)
C) O(n)
D) O(n^2)
```

6. `addLast` in COW complexity:
```text
A) O(1)
B) O(log n)
C) O(n)
D) O(n^2)
```

7. `removeFirst` in COW complexity:
```text
A) O(1)
B) O(log n)
C) O(n)
D) O(n^2)
```

8. `contains` complexity in COW is typically:
```text
A) O(1)
B) O(log n)
C) O(n)
D) O(n^2)
```

9. Why do readers scale better?
```text
A) no reads allowed
B) read path avoids structural locking conflicts
C) each read copies list
D) immutable JVM
```

10. `reversed` view updates when base list changes?
```text
A) never
B) yes, as view of current list
C) only once
D) only for primitives
```

11. `clear` in COW:
```text
A) not supported
B) writes new empty backing array
C) sets size to -1
D) blocks forever
```

12. `removeIf` in COW is generally:
```text
A) write operation with copy cost
B) read-only
C) unsupported
D) constant time
```

13. Compared with synchronized list wrappers, COW read behavior is often:
```text
A) worse always
B) competitive/better for read-heavy
C) identical always
D) not thread-safe
```

14. COW iterators are generally:
```text
A) mutation-friendly
B) read-focused snapshots
C) index-based only
D) fail-fast
```

15. Main interview point for COW:
```text
A) great for write-heavy
B) read scalability vs write cost tradeoff
C) no memory overhead
D) no iterator support
```
