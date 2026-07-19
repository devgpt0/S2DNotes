# Vector List Worksheet

Source: VectorListNotes.md

## Level 1

### Tricky Predict the Output (15)

1.
```java
Vector<Integer> v = new Vector<>();
v.add(1);
v.add(2);
v.add(3);
System.out.println(v);
```

Answer: _____________

2.
```java
Vector<Integer> v = new Vector<>(List.of(1,2,3));
v.remove(1);
System.out.println(v);
```

Answer: _____________

3.
```java
Vector<Integer> v = new Vector<>(List.of(1,2,3));
v.remove(Integer.valueOf(2));
System.out.println(v);
```

Answer: _____________

4.
```java
Vector<Integer> v = new Vector<>(List.of(1,2,3));
v.add(1,9);
System.out.println(v);
```

Answer: _____________

5.
```java
Vector<Integer> v = new Vector<>(List.of(1,2,3));
v.set(2,99);
System.out.println(v);
```

Answer: _____________

6.
```java
Vector<Integer> v = new Vector<>(List.of(1,2,3));
System.out.println(v.get(0));
```

Answer: _____________

7.
```java
Vector<Integer> v = new Vector<>(List.of(1,2,3));
System.out.println(v.contains(4));
```

Answer: _____________

8.
```java
Vector<Integer> v = new Vector<>(List.of(1,2,2,3));
System.out.println(v.indexOf(2));
```

Answer: _____________

9.
```java
Vector<Integer> v = new Vector<>(List.of(1,2,2,3));
System.out.println(v.lastIndexOf(2));
```

Answer: _____________

10.
```java
Vector<Integer> v = new Vector<>();
System.out.println(v.capacity());
```

Answer: _____________

11.
```java
Vector<Integer> v = new Vector<>();
v.add(1);
System.out.println(v.size());
```

Answer: _____________

12.
```java
Vector<Integer> v = new Vector<>(List.of(1,2,3));
v.clear();
System.out.println(v.isEmpty());
```

Answer: _____________

13.
```java
Vector<Integer> v = new Vector<>(List.of(5,1,3));
Collections.sort(v);
System.out.println(v);
```

Answer: _____________

14.
```java
Vector<Integer> v = new Vector<>(List.of(5,1,3));
v.sort(Collections.reverseOrder());
System.out.println(v);
```

Answer: _____________

15.
```java
Vector<Integer> v = new Vector<>(List.of(1,2,3));
Object[] a = v.toArray();
System.out.println(a.length);
```

Answer: _____________

### MCQ Theory (15)

1. `Vector` is:
```text
A) unsynchronized
B) synchronized dynamic array
C) linked list
D) immutable
```

2. `get(i)` complexity is:
```text
A) O(1)
B) O(n)
C) O(log n)
D) O(n^2)
```

3. `add(i, e)` is typically:
```text
A) O(1)
B) O(log n)
C) O(n)
D) O(n^2)
```

4. Single-threaded performance can be slower than `ArrayList` due to:
```text
A) hashing
B) lock overhead
C) tree balancing
D) recursion
```

5. `ensureCapacity` affects:
```text
A) logical size
B) internal capacity target
C) both size and values
D) sorting order
```

6. `trimToSize` does:
```text
A) reverse list
B) shrink capacity to current size
C) clear list
D) deduplicate
```

7. `capacity()` returns:
```text
A) element count
B) internal array capacity
C) max int
D) thread count
```

8. `size()` returns:
```text
A) internal array length
B) number of stored elements
C) free slots
D) lock count
```

9. `Vector` is legacy mainly because:
```text
A) no generics
B) old synchronized design pattern
C) no iterator
D) cannot grow
```

10. `toArray()` returns:
```text
A) same backing store
B) new array object
C) map view
D) deque
```

11. `reversed()` returns:
```text
A) copied list
B) reverse-order view
C) immutable copy
D) tree set
```

12. Compound action `if(!v.contains(x)) v.add(x)` is:
```text
A) always atomic
B) not atomic as a pair
C) compile-time error
D) impossible
```

13. Better default for non-concurrent list:
```text
A) Vector
B) ArrayList
C) Stack
D) Hashtable
```

14. `indexOf` complexity is typically:
```text
A) O(1)
B) O(log n)
C) O(n)
D) O(n^2)
```

15. `remove(value)` in Vector is typically:
```text
A) O(1)
B) O(log n)
C) O(n)
D) O(n^2)
```

## Level 2

### Tricky Predict the Output (15)

1.
```java
Vector<Integer> v = new Vector<>(2);
v.add(1);
v.add(2);
System.out.println(v.capacity());
```

Answer: _____________

2.
```java
Vector<Integer> v = new Vector<>(2);
v.add(1);
v.add(2);
v.add(3);
System.out.println(v.capacity());
```

Answer: _____________

3.
```java
Vector<Integer> v = new Vector<>(10,5);
for(int i=0;i<11;i++) v.add(i);
System.out.println(v.capacity());
```

Answer: _____________

4.
```java
Vector<Integer> v = new Vector<>(List.of(1,2,3));
v.addFirst(0);
System.out.println(v);
```

Answer: _____________

5.
```java
Vector<Integer> v = new Vector<>(List.of(1,2,3));
v.addLast(4);
System.out.println(v);
```

Answer: _____________

6.
```java
Vector<Integer> v = new Vector<>(List.of(1,2,3));
System.out.println(v.getFirst() + ":" + v.getLast());
```

Answer: _____________

7.
```java
Vector<Integer> v = new Vector<>(List.of(1,2,3));
v.removeFirst();
System.out.println(v);
```

Answer: _____________

8.
```java
Vector<Integer> v = new Vector<>(List.of(1,2,3));
v.removeLast();
System.out.println(v);
```

Answer: _____________

9.
```java
Vector<Integer> v = new Vector<>(List.of(1,2,3));
List<Integer> r = v.reversed();
System.out.println(r);
```

Answer: _____________

10.
```java
Vector<Integer> v = new Vector<>(List.of(1,2,3));
List<Integer> r = v.reversed();
v.set(0,99);
System.out.println(r.get(2));
```

Answer: _____________

11.
```java
Vector<Integer> v = new Vector<>(List.of(1,2,3));
v.ensureCapacity(50);
System.out.println(v.size());
```

Answer: _____________

12.
```java
Vector<Integer> v = new Vector<>(List.of(1,2,3));
v.trimToSize();
System.out.println(v.size());
```

Answer: _____________

13.
```java
Vector<Integer> v = new Vector<>(List.of(1,2,3));
System.out.println(v.remove(Integer.valueOf(9)));
```

Answer: _____________

14.
```java
Vector<Integer> v = new Vector<>(List.of(1,2,3));
v.clear();
System.out.println(v.isEmpty());
```

Answer: _____________

15.
```java
Vector<Integer> v = new Vector<>();
Thread t1=new Thread(()->{for(int i=0;i<1000;i++)v.add(i);});
Thread t2=new Thread(()->{for(int i=0;i<1000;i++)v.add(i);});
t1.start();
t2.start();
t1.join();
t2.join();
System.out.println(v.size());
```

Answer: _____________

### MCQ Theory (15)

1. If `capacityIncrement > 0`, Vector growth is usually:
```text
A) doubling always
B) fixed-step increment
C) no growth
D) random growth
```

2. If `capacityIncrement <= 0`, growth is usually:
```text
A) fixed +1
B) roughly doubled
C) no resize
D) halved
```

3. `addFirst` on Vector is generally:
```text
A) O(1)
B) O(n)
C) O(log n)
D) O(n^2)
```

4. `addLast` on Vector is generally:
```text
A) O(1) amortized
B) O(n)
C) O(log n)
D) O(n^2)
```

5. `removeFirst` on Vector is generally:
```text
A) O(1)
B) O(log n)
C) O(n)
D) O(n^2)
```

6. Individual synchronized methods guarantee:
```text
A) all multi-step thread safety
B) per-call mutual exclusion
C) lock-free behavior
D) immutability
```

7. Best concurrent read-heavy list candidate (from notes):
```text
A) ArrayList
B) CopyOnWriteArrayList
C) Stack
D) HashSet
```

8. `capacity` differs from `size` because capacity is:
```text
A) current logical elements
B) current max before resize
C) sorted elements
D) last index
```

9. `clear` changes:
```text
A) capacity only
B) size to 0
C) type of list
D) comparator
```

10. `contains` complexity in Vector is usually:
```text
A) O(1)
B) O(log n)
C) O(n)
D) O(n^2)
```

11. `lastIndexOf` complexity is usually:
```text
A) O(1)
B) O(log n)
C) O(n)
D) O(n^2)
```

12. Which statement is true?
```text
A) Vector methods are unsynchronized
B) Vector cannot store duplicates
C) Vector supports random access
D) Vector is immutable
```

13. Which is not atomic as a compound step?
```text
A) `v.add(x)`
B) `v.get(i)`
C) `if(!v.contains(x)) v.add(x)`
D) `v.size()`
```

14. Good replacement for legacy stack usage:
```text
A) ArrayDeque
B) Hashtable
C) TreeMap
D) CopyOnWriteArraySet
```

15. In interview prep, major Vector tradeoff is:
```text
A) speed with no locks
B) thread-safe calls vs overhead
C) immutability
D) no resizing
```
