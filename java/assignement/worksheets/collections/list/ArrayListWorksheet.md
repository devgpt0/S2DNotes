# ArrayList Worksheet

Source: ArrayListNotes.md

## Level 1

### Tricky Predict the Output (15)

1.
```java
List<Integer> l = new ArrayList<>(List.of(1,2,3));
l.add(1,9);
System.out.println(l);
```

Answer: _____________

2.
```java
List<Integer> l = new ArrayList<>(List.of(1,2,3));
l.remove(1);
System.out.println(l);
```

Answer: _____________

3.
```java
List<Integer> l = new ArrayList<>(List.of(1,2,3));
l.remove(Integer.valueOf(2));
System.out.println(l);
```

Answer: _____________

4.
```java
List<String> l = new ArrayList<>(List.of("a","b","c"));
l.set(2,"x");
System.out.println(l);
```

Answer: _____________

5.
```java
List<Integer> l = new ArrayList<>(List.of(1,2,3,4));
l.removeIf(x -> x % 2 == 0);
System.out.println(l);
```

Answer: _____________

6.
```java
List<Integer> l = new ArrayList<>(List.of(1,2,3));
l.replaceAll(x -> x * 2);
System.out.println(l);
```

Answer: _____________

7.
```java
List<Integer> l = new ArrayList<>();
l.ensureCapacity(100);
System.out.println(l.size());
```

Answer: _____________

8.
```java
List<String> l = new ArrayList<>(List.of("p","q"));
System.out.println(l.contains("r"));
```

Answer: _____________

9.
```java
List<String> l = new ArrayList<>(List.of("p","q","r"));
System.out.println(l.get(0) + l.get(2));
```

Answer: _____________

10.
```java
List<String> l = new ArrayList<>(List.of("a","b"));
l.addAll(List.of("c","d"));
System.out.println(l);
```

Answer: _____________

11.
```java
List<Integer> l = new ArrayList<>(List.of(5,1,3));
Collections.sort(l);
System.out.println(l);
```

Answer: _____________

12.
```java
List<Integer> l = new ArrayList<>(List.of(5,1,3));
Collections.sort(l, Collections.reverseOrder());
System.out.println(l);
```

Answer: _____________

13.
```java
List<Integer> l = new ArrayList<>(List.of(1,2,3));
Object[] a = l.toArray();
System.out.println(a.length);
```

Answer: _____________

14.
```java
List<String> l = List.of("x","y");
l.add("z");
```

Answer: _____________

15.
```java
List<String> l = new ArrayList<>(List.of("x","y"));
List<String> r = l.reversed();
l.set(0,"z");
System.out.println(r.get(1));
```

Answer: _____________

### MCQ Theory (15)

1. `ArrayList` internal structure is:
```text
A) doubly linked nodes
B) dynamic array
C) heap tree
D) hash buckets
```

2. Fastest common operation in `ArrayList` is typically:
```text
A) get(index)
B) add at index 0
C) remove index 0
D) contains(x)
```

3. End append `add(e)` is usually:
```text
A) O(1) amortized
B) O(log n)
C) O(n)
D) O(n^2)
```

4. `add(index, e)` can be expensive due to:
```text
A) hashing
B) shifting elements
C) recursion
D) locking
```

5. `set(index, v)` does:
```text
A) insert and shift
B) replace existing element
C) remove element
D) append only
```

6. `remove(int)` vs `remove(Integer)` differs by:
```text
A) package
B) overload target (index vs value)
C) capacity
D) iterator type
```

7. Which factory makes immutable list?
```text
A) new ArrayList<>()
B) List.of(...)
C) Arrays.asList(...)
D) Collections.sort(...)
```

8. `Arrays.asList(...)` returns:
```text
A) fully mutable ArrayList
B) fixed-size backed view
C) immutable list
D) linked list
```

9. Allowed on `Arrays.asList(...)` list:
```text
A) add
B) remove
C) set
D) clear
```

10. `contains(x)` complexity is usually:
```text
A) O(1)
B) O(log n)
C) O(n)
D) O(n^2)
```

11. `size()` gives:
```text
A) capacity
B) number of elements
C) free slots
D) bytes used
```

12. Best declaration style:
```text
A) ArrayList<T> ref = ...
B) List<T> ref = new ArrayList<>()
C) raw List ref
D) T[] always
```

13. `toArray(...)` creates:
```text
A) same backing storage
B) new array object
C) map view
D) set view
```

14. Why is `ArrayList` often cache-friendly?
```text
A) contiguous memory locality
B) per-node pointers
C) random hash spread
D) recursion
```

15. True statement:
```text
A) ArrayList is thread-safe by default
B) ArrayList permits duplicates and nulls
C) ArrayList forbids null
D) ArrayList has fixed capacity only
```

## Level 2

### Tricky Predict the Output (15)

1.
```java
List<Integer> l = new ArrayList<>(List.of(1,2,3,4,5));
l.removeIf(x -> x > 3);
System.out.println(l);
```

Answer: _____________

2.
```java
List<String> f = List.of("a","b");
List<String> m = new ArrayList<>(f);
m.add("c");
System.out.println(m);
```

Answer: _____________

3.
```java
List<Integer> l = Arrays.asList(1,2,3);
l.add(4);
```

Answer: _____________

4.
```java
List<Integer> l = Arrays.asList(1,2,3);
l.set(1,9);
System.out.println(l);
```

Answer: _____________

5.
```java
ArrayList<Integer> l = new ArrayList<>(15);
l.add(1);
l.trimToSize();
System.out.println(l.size());
```

Answer: _____________

6.
```java
List<Integer> l = new ArrayList<>(List.of(1,2,3));
l.addFirst(0);
System.out.println(l.getFirst());
```

Answer: _____________

7.
```java
List<Integer> l = new ArrayList<>(List.of(1,2,3));
l.addLast(4);
System.out.println(l.getLast());
```

Answer: _____________

8.
```java
List<Integer> l = new ArrayList<>(List.of(1,2,3));
l.removeFirst();
System.out.println(l);
```

Answer: _____________

9.
```java
List<Integer> l = new ArrayList<>(List.of(1,2,3));
l.removeLast();
System.out.println(l);
```

Answer: _____________

10.
```java
List<Integer> l = new ArrayList<>(List.of(1,2,3));
List<Integer> r = l.reversed();
System.out.println(r);
```

Answer: _____________

11.
```java
List<String> l = new ArrayList<>(List.of("a","b","c"));
l.clear();
System.out.println(l.isEmpty());
```

Answer: _____________

12.
```java
List<Integer> l = new ArrayList<>(List.of(3,1,2));
System.out.println(Collections.max(l));
```

Answer: _____________

13.
```java
List<Integer> l = new ArrayList<>(List.of(3,1,2));
System.out.println(Collections.min(l));
```

Answer: _____________

14.
```java
List<Integer> l = new ArrayList<>(List.of(1,2,3));
System.out.println(l.indexOf(2));
```

Answer: _____________

15.
```java
List<Integer> l = new ArrayList<>(List.of(1,2,2,3));
System.out.println(l.lastIndexOf(2));
```

Answer: _____________

### MCQ Theory (15)

1. `ensureCapacity(n)` affects:
```text
A) logical size
B) internal capacity target
C) sort order
D) element values
```

2. `trimToSize()` is mainly for:
```text
A) reducing unused internal capacity
B) sorting list
C) deduping list
D) making list immutable
```

3. `reversed()` returns:
```text
A) deep copy
B) reverse-order view
C) sorted list
D) set
```

4. `addFirst` on array-backed list is generally:
```text
A) O(1)
B) O(log n)
C) O(n)
D) O(n^2)
```

5. `addLast` on array-backed list is generally:
```text
A) O(1) amortized
B) O(n)
C) O(log n)
D) O(n^2)
```

6. `removeFirst` on array-backed list is generally:
```text
A) O(1)
B) O(log n)
C) O(n)
D) O(n^2)
```

7. `removeLast` on array-backed list is generally:
```text
A) near O(1)
B) O(n)
C) O(log n)
D) O(n^2)
```

8. `List.copyOf(list)` returns:
```text
A) mutable copy
B) immutable copy
C) linked list
D) synchronized wrapper
```

9. `new ArrayList<>(someList)` returns:
```text
A) immutable list
B) mutable copy
C) fixed-size view
D) sorted copy always
```

10. `removeIf(predicate)` is:
```text
A) non-modifying read
B) in-place structural modification
C) compile-time filter
D) map transform
```

11. `replaceAll(op)` is:
```text
A) element-wise in-place replacement
B) remove-by-condition
C) sort alias
D) synchronization helper
```

12. Raw type `List l = ...` risk:
```text
A) no resizing
B) no generic type safety
C) immutability
D) no iteration
```

13. For predictable bulk append performance, prefer:
```text
A) frequent trimToSize
B) pre-sizing via ensureCapacity
C) repeated contains
D) repeated reverse
```

14. In multithreaded code, plain ArrayList is:
```text
A) thread-safe
B) not thread-safe by default
C) immutable
D) lock-free and safe
```

15. `List.of(...)` elements can be structurally modified?
```text
A) yes
B) no
C) only add allowed
D) only remove allowed
```
