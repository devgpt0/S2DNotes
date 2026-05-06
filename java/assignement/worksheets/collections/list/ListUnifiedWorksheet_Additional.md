# List Unified Worksheet (Additional Concepts Only)

Source: collectionFramework/list (unified notes)

## Tricky Predict the Output (15)

1.
```java
List<Integer> l = new ArrayList<>(List.of(10, 20, 30, 40));
System.out.println(Collections.binarySearch(l, 30));
```
Answer: _____________

2.
```java
List<Integer> l = new ArrayList<>(List.of(10, 20, 30, 40));
System.out.println(Collections.binarySearch(l, 25));
```
Answer: _____________

3.
```java
List<String> l = new ArrayList<>(List.of("a", "b", "c"));
List<String> s = l.subList(1, 3);
s.set(0, "X");
System.out.println(l);
```
Answer: _____________

4.
```java
List<Integer> base = new ArrayList<>(List.of(1, 2, 3));
List<Integer> ro = Collections.unmodifiableList(base);
base.set(1, 99);
System.out.println(ro);
```
Answer: _____________

5.
```java
List<Integer> src = new ArrayList<>(List.of(1, 2, 3));
List<Integer> snap = List.copyOf(src);
src.set(0, 99);
System.out.println(snap);
```
Answer: _____________

6.
```java
List<String> l = List.of("a", "b", "c");
l.set(1, "x");
```
Answer: _____________

7.
```java
List<String> l = new ArrayList<>(List.of("a", "b", "c"));
for (String s : l) {
    if (s.equals("b")) l.remove(s);
}
System.out.println(l);
```
Answer: _____________

8.
```java
List<Integer> l = new ArrayList<>(List.of(1, 2, 3));
ListIterator<Integer> it = l.listIterator();
it.next();
it.add(99);
System.out.println(l);
```
Answer: _____________

9.
```java
List<Integer> l = new ArrayList<>(List.of(1, 2, 3));
ListIterator<Integer> it = l.listIterator(l.size());
System.out.println(it.previous());
```
Answer: _____________

10.
```java
List<Integer> l = Arrays.asList(1, 2, 3);
List<Integer> c = new ArrayList<>(l);
c.removeIf(x -> x >= 2);
System.out.println(c);
```
Answer: _____________

11.
```java
List<String> l = Stream.of(" a ", "b ", " a ")
    .map(String::trim)
    .distinct()
    .sorted()
    .toList();
System.out.println(l);
```
Answer: _____________

12.
```java
List<Integer> l = Stream.of(1, 2, 3).toList();
l.add(4);
```
Answer: _____________

13.
```java
class P {
  int id;
  P(int id){ this.id = id; }
}
List<P> l = new ArrayList<>();
l.add(new P(1));
System.out.println(l.contains(new P(1)));
```
Answer: _____________

14.
```java
List<Integer> l = new ArrayList<>(List.of(1, 2, 3, 4, 5));
Iterator<Integer> it = l.iterator();
while (it.hasNext()) {
  if (it.next() % 2 == 0) it.remove();
}
System.out.println(l);
```
Answer: _____________

15.
```java
List<String> l = new ArrayList<>(List.of("x", "y", "z"));
Collections.swap(l, 0, 2);
System.out.println(l);
```
Answer: _____________

## MCQ Theory (15)

1. `Collections.binarySearch(list, key)` requires:
```text
A) linked list only
B) list sorted according to same ordering
C) immutable list
D) synchronized list
```

2. `subList(from, to)` is:
```text
A) deep copy
B) view backed by original list
C) immutable snapshot
D) set conversion
```

3. `Collections.unmodifiableList(base)`:
```text
A) copies base deeply
B) prevents writes through wrapper view
C) freezes base object entirely
D) sorts list
```

4. `List.copyOf(base)` returns:
```text
A) mutable view
B) immutable snapshot copy
C) synchronized wrapper
D) linked list
```

5. Structural remove inside enhanced for-loop usually causes:
```text
A) silent ignore
B) ConcurrentModificationException
C) ClassCastException
D) EOFException
```

6. Safe removal during iteration is via:
```text
A) for-each + list.remove
B) Iterator.remove
C) stream().forEach(remove)
D) random index only
```

7. `Stream.toList()` in modern Java typically returns:
```text
A) mutable ArrayList
B) unmodifiable list
C) LinkedList
D) Vector
```

8. `ListIterator` can:
```text
A) move only forward
B) move forward and backward
C) work only on linked list
D) sort automatically
```

9. For custom object `contains` correctness, you usually need:
```text
A) clone
B) equals/hashCode
C) finalizer
D) synchronized
```

10. `Collections.unmodifiableList(base)` reflects later base mutations?
```text
A) no, never
B) yes, because it is a view
C) only in debug mode
D) only for integers
```

11. Binary search non-found return is:
```text
A) always -1
B) negative insertion-point encoding
C) null
D) exception
```

12. Best declaration style remains:
```text
A) List<T> ref = concreteImplementation
B) raw List only
C) concrete type always on left
D) array first
```

13. `removeIf` is:
```text
A) read-only operation
B) structural mutation
C) compile-time transform
D) immutable projection
```

14. `Collections.swap` does:
```text
A) sort ascending
B) exchange two indexed elements
C) reverse all
D) deduplicate
```

15. Defensive copy in constructor typically uses:
```text
A) this.items = items;
B) this.items = new ArrayList<>(items);
C) this.items = Collections.unmodifiableList(items);
D) this.items = null;
```

## Interview Questions (10)

1. Explain difference between `Collections.unmodifiableList` and `List.copyOf`.
2. Why can for-each + `list.remove(...)` fail, and what are safe alternatives?
3. When should you use `ListIterator` instead of `Iterator`?
4. Explain binary search insertion-point result with example.
5. Why should API methods return immutable list views/copies in many designs?
6. Compare `ArrayList` and `LinkedList` for random reads vs middle inserts.
7. What are common mistakes with `Arrays.asList`?
8. How does `subList` behave and what pitfalls come with structural changes?
9. Explain effect of missing `equals/hashCode` on list operations.
10. Give one production use case each for `ArrayList`, `LinkedList`, `CopyOnWriteArrayList`.

