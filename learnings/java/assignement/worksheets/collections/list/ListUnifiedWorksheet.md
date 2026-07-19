# Comprehensive List Worksheet (All Concepts)

**Source**: collectionFramework/list (all notes 01-14)  
**Weightage**: ArrayList (30%) | LinkedList (15%) | Vector/Stack (10%) | Immutable (15%) | Iteration/Streams (15%) | Sorting (10%) | CopyOnWriteArrayList (5%)

---

## LEVEL 1 - FUNDAMENTALS

### 1.1 Predict the Output (35 Questions)

#### ArrayList Basics (10 questions)
1.
```java
List<Integer> l = new ArrayList<>(List.of(10, 20, 30, 40));
l.add(1, 99);
System.out.println(l);
```
Answer: _____________

2.
```java
List<Integer> l = new ArrayList<>(List.of(10, 20, 30));
l.remove(Integer.valueOf(20));
System.out.println(l);
```
Answer: _____________

3.
```java
List<Integer> l = new ArrayList<>(List.of(1, 2, 3));
System.out.println(l.get(0) + l.get(2));
```
Answer: _____________

4.
```java
List<String> l = new ArrayList<>(List.of("a", "b", "c"));
l.set(1, "X");
System.out.println(l);
```
Answer: _____________

5.
```java
List<Integer> l = new ArrayList<>();
l.ensureCapacity(100);
System.out.println(l.size());
```
Answer: _____________

6.
```java
List<Integer> l = new ArrayList<>(List.of(1, 2, 3, 4, 5));
l.removeIf(x -> x % 2 == 0);
System.out.println(l);
```
Answer: _____________

7.
```java
List<Integer> l = new ArrayList<>(List.of(2, 4, 6));
l.replaceAll(x -> x / 2);
System.out.println(l);
```
Answer: _____________

8.
```java
List<String> l = new ArrayList<>(List.of("p", "q"));
System.out.println(l.contains("r"));
```
Answer: _____________

9.
```java
List<String> l = new ArrayList<>(List.of("a", "b"));
l.addAll(List.of("c", "d"));
System.out.println(l.size());
```
Answer: _____________

10.
```java
List<Integer> l = new ArrayList<>(List.of(1, 2, 3));
Object[] arr = l.toArray();
System.out.println(arr.length);
```
Answer: _____________

#### LinkedList & Deque Operations (8 questions)
11.
```java
LinkedList<Integer> l = new LinkedList<>(List.of(10, 20, 30));
l.addFirst(5);
System.out.println(l.getFirst());
```
Answer: _____________

12.
```java
LinkedList<Integer> l = new LinkedList<>(List.of(1, 2, 3));
l.addLast(99);
System.out.println(l.getLast());
```
Answer: _____________

13.
```java
LinkedList<Integer> l = new LinkedList<>(List.of(10, 20, 30));
l.removeFirst();
System.out.println(l);
```
Answer: _____________

14.
```java
LinkedList<String> l = new LinkedList<>(List.of("a", "b", "c"));
l.removeFirstOccurrence("b");
System.out.println(l);
```
Answer: _____________

15.
```java
LinkedList<Integer> l = new LinkedList<>(List.of(1, 1, 2, 1, 3));
l.removeLastOccurrence(1);
System.out.println(l);
```
Answer: _____________

16.
```java
LinkedList<Integer> l = new LinkedList<>(List.of(10, 20, 30));
System.out.println(l.get(1));
```
Answer: _____________

17.
```java
LinkedList<Integer> q = new LinkedList<>();
q.offerLast(10);
q.offerFirst(5);
System.out.println(q.pollFirst());
```
Answer: _____________

18.
```java
LinkedList<Integer> l = new LinkedList<>(Arrays.asList(1, 2, 3, 4));
LinkedList<Integer> toRemove = new LinkedList<>(Arrays.asList(2, 4));
l.removeAll(toRemove);
System.out.println(l);
```
Answer: _____________

#### Vector & Stack (5 questions)
19.
```java
Vector<Integer> v = new Vector<>();
v.add(1);
v.add(2);
v.add(3);
System.out.println(v.capacity() >= v.size());
```
Answer: _____________

20.
```java
Stack<Integer> st = new Stack<>();
st.push(10);
st.push(20);
System.out.println(st.pop());
```
Answer: _____________

21.
```java
Stack<Integer> st = new Stack<>();
st.push(1);
st.push(2);
st.push(3);
System.out.println(st.search(2));
```
Answer: _____________

22.
```java
Stack<String> st = new Stack<>();
st.push("a");
st.push("b");
System.out.println(st.peek());
st.pop();
System.out.println(st.peek());
```
Answer: _____________

23.
```java
Vector<Integer> v = new Vector<>(10, 5);
v.add(100);
System.out.println(v.capacity());
```
Answer: _____________

#### Immutable Collections (5 questions)
24.
```java
List<String> l = List.of("x", "y", "z");
l.set(1, "a");
```
Answer: _____________

25.
```java
List<String> l = List.of("a", "b");
l.add("c");
```
Answer: _____________

26.
```java
List<Integer> src = new ArrayList<>(List.of(1, 2, 3));
List<Integer> snap = List.copyOf(src);
src.set(0, 99);
System.out.println(snap);
```
Answer: _____________

27.
```java
List<Integer> base = new ArrayList<>(List.of(1, 2, 3));
List<Integer> ro = Collections.unmodifiableList(base);
base.set(1, 99);
System.out.println(ro);
```
Answer: _____________

28.
```java
List<Integer> l = Arrays.asList(1, 2, 3);
l.set(0, 9);
System.out.println(l);
```
Answer: _____________

#### Iteration (3 questions)
29.
```java
List<Integer> l = new ArrayList<>(List.of(1, 2, 3));
ListIterator<Integer> it = l.listIterator();
it.next();
it.add(99);
System.out.println(l);
```
Answer: _____________

30.
```java
List<Integer> l = new ArrayList<>(List.of(10, 20, 30));
ListIterator<Integer> it = l.listIterator(l.size());
System.out.println(it.previous());
```
Answer: _____________

31.
```java
List<String> l = new ArrayList<>(List.of("a", "b", "c"));
for (String s : l) {
    if (s.equals("b")) l.remove(s);
}
System.out.println(l);
```
Answer: _____________

#### Sorting & Searching (3 questions)
32.
```java
List<Integer> l = new ArrayList<>(List.of(5, 1, 3));
Collections.sort(l);
System.out.println(l);
```
Answer: _____________

33.
```java
List<Integer> l = new ArrayList<>(List.of(1, 2, 3, 4, 5));
System.out.println(Collections.binarySearch(l, 3));
```
Answer: _____________

34.
```java
List<Integer> l = new ArrayList<>(List.of(1, 2, 3, 4, 5));
System.out.println(Collections.binarySearch(l, 3) >= 0);
```
Answer: _____________

35.
```java
List<Integer> l = new ArrayList<>(List.of(3, 1, 4, 1, 5));
Collections.sort(l, Collections.reverseOrder());
System.out.println(l);
```
Answer: _____________

---

### 1.2 MCQ Theory (35 Questions)

#### ArrayList Concepts (10 questions)
1. `ArrayList` internal data structure is:
```text
A) doubly linked list
B) dynamic resizable array
C) hash table with buckets
D) tree structure
```

2. Time complexity of `get(index)` in `ArrayList`:
```text
A) O(1)
B) O(log n)
C) O(n)
D) O(n^2)
```

3. Time complexity of `add(index, element)` in `ArrayList`:
```text
A) O(1) amortized
B) O(log n)
C) O(n) - due to shifting
D) O(n^2)
```

4. `ArrayList` growth factor upon reaching capacity is typically:
```text
A) 1.5x
B) 2x
C) 3x
D) 4x
```

5. `set(index, element)` in `ArrayList` is:
```text
A) O(1) - replacement only
B) O(n) - requires shift
C) O(log n)
D) O(n^2)
```

6. Difference between `remove(int)` and `remove(Object)`:
```text
A) same operation
B) first removes by index, second by value
C) first removes by value, second by index
D) completely different implementations
```

7. `ensureCapacity(n)`:
```text
A) increases logical size
B) guarantees minimum internal capacity
C) creates new ArrayList
D) throws exception if n < current size
```

8. Allowed operations on `Arrays.asList(1, 2, 3)`:
```text
A) only get/size/contains
B) add, set, remove all allowed
C) set allowed, add/remove not allowed
D) no operations allowed
```

9. `trimToSize()` does:
```text
A) reduces logical size
B) shrinks internal array to match logical size
C) clears all elements
D) increases capacity
```

10. `new ArrayList<>(List.of("a","b"))` creates:
```text
A) unmodifiable list
B) mutable ArrayList backed by immutable list
C) independent mutable copy
D) fixed-size view
```

#### LinkedList Concepts (7 questions)
11. `LinkedList` internal structure:
```text
A) contiguous array
B) doubly linked nodes (prev, data, next)
C) singly linked nodes
D) tree structure
```

12. Advantage of `LinkedList` over `ArrayList`:
```text
A) faster random access
B) better memory locality
C) O(1) insertion/deletion at ends
D) lower memory footprint
```

13. `get(index)` complexity in `LinkedList`:
```text
A) O(1)
B) O(log n)
C) O(n)
D) O(n^2)
```

14. `LinkedList` implements which interface:
```text
A) List only
B) Deque interface also
C) Set interface also
D) Queue interface only
```

15. `addFirst()` and `addLast()` in `LinkedList`:
```text
A) both O(n)
B) both O(log n)
C) both O(1)
D) addFirst O(1), addLast O(n)
```

16. `removeLastOccurrence(obj)` searches:
```text
A) from beginning
B) from end backward
C) random order
D) doesn't search, throws exception
```

17. `LinkedList` as Queue operations:
```text
A) push/pop only
B) offer/poll/peek available
C) no queue operations
D) stack operations only
```

#### Vector & Stack Concepts (5 questions)
18. `Vector` thread-safety mechanism:
```text
A) not thread-safe
B) method-level synchronization
C) lock-free implementation
D) no synchronization
```

19. `Stack` internal structure:
```text
A) array-based like ArrayList
B) extends Vector (legacy)
C) linked list
D) tree-based
```

20. `Stack.search(element)`:
```text
A) returns index from 0
B) returns 1-based position from top, -1 if absent
C) returns boolean
D) throws exception if not found
```

21. Capacity growth behavior in `Vector`:
```text
A) always 1.5x
B) can be controlled via capacityIncrement
C) fixed size always
D) doubles always
```

22. Complexity of Stack operations `push/pop/peek`:
```text
A) all O(1)
B) all O(n)
C) all O(log n)
D) mixed complexity
```

#### Immutable Collections (5 questions)
23. `List.of()` creates:
```text
A) mutable ArrayList
B) immutable fixed-size list
C) fixed-size view
D) thread-safe synchronized list
```

24. `List.copyOf()` on immutable list:
```text
A) creates mutable copy
B) returns same reference
C) creates new immutable copy
D) throws exception
```

25. Key difference between `List.of()` and `Arrays.asList()`:
```text
A) no difference
B) List.of immutable, Arrays.asList fixed-size mutable view
C) same behavior
D) Arrays.asList is immutable
```

26. Defensive copy pattern (receiving list):
```text
A) List<T> items;
B) this.items = new ArrayList<>(items);
C) this.items = items;
D) this.items = Collections.unmodifiableList(items);
```

27. Collections.unmodifiableList() creates:
```text
A) independent copy
B) view that throws exception on modification
C) defensive copy
D) fully mutable list
```

#### Iteration & Streams (3 questions)
28. `ListIterator` key difference from `Iterator`:
```text
A) no difference
B) can iterate backward, add/set during iteration
C) faster performance
D) thread-safe
```

29. ConcurrentModificationException occurs when:
```text
A) modifying list during enhanced for loop
B) using Iterator correctly
C) calling size() multiple times
D) never occurs
```

30. Streams `toList()` creates:
```text
A) mutable ArrayList
B) immutable List (Java 16+)
C) fixed-size view
D) synchronized list
```

#### Sorting & Searching (3 questions)
31. `binarySearch()` requires:
```text
A) no precondition
B) list must be sorted
C) ascending order only
D) descending order mandatory
```

32. `binarySearch()` returns:
```text
A) true/false
B) element if found, null otherwise
C) index if found, negative index-1 if not found
D) always positive
```

33. Natural ordering uses:
```text
A) Comparator interface
B) Comparable interface
C) compareTo() method
D) both B and C
```

---

### 1.3 Interview Questions (15 Questions)

1. **Explain ArrayList resizing mechanism and load factor concept.** What happens when capacity is exceeded?

2. **Why is `ArrayList` fast for get() but slow for middle insertions/deletions? Explain the O(n) cost.**

3. **When would you use `LinkedList` over `ArrayList`? Provide real-world scenarios.**

4. **What are the trade-offs between ArrayList and LinkedList in terms of memory and time complexity?**

5. **Explain the difference between `List.of()`, `Arrays.asList()`, and `new ArrayList<>()` in terms of mutability and backing.**

6. **What is the defensive copy pattern? Why use `List.copyOf()` when returning lists?**

7. **How does `Collections.unmodifiableList()` prevent modifications? What happens if you try to add?**

8. **Explain the variable capture issue when removing elements during iteration. How to fix it?**

9. **What is `ListIterator` and how is it different from `Iterator`? Provide a use case.**

10. **Explain the `binarySearch()` contract: why must list be sorted? What if not sorted?**

11. **Stack vs LinkedList as stack implementation: which is better and why?**

12. **In `Vector`, how does capacity and capacityIncrement work? When to use `trimToSize()`?**

13. **Explain `subList()` behavior: is it a view or independent copy? What happens when backing list changes?**

14. **What is `forEach()` loop and how is it different from traditional for loops regarding modification?**

15. **Design a custom cache using LinkedHashMap with access-order. Explain eviction strategy.**

---

## LEVEL 2 - ADVANCED

### 2.1 Predict the Output (35 Questions)

#### Complex ArrayList Scenarios (10 questions)
1.
```java
List<Integer> l = new ArrayList<>(List.of(1, 2, 3));
List<Integer> sub = l.subList(1, 3);
sub.set(0, 99);
System.out.println(l);
```
Answer: _____________

2.
```java
List<String> l = new ArrayList<>(List.of("a", "b", "c"));
List<String> sub = l.subList(1, 3);
l.remove(1);
System.out.println(sub);
```
Answer: _____________

3.
```java
List<Integer> l = new ArrayList<>(List.of(1, 1, 2, 1, 3));
while (l.contains(1)) {
    l.remove(Integer.valueOf(1));
}
System.out.println(l);
```
Answer: _____________

4.
```java
List<String> l = Stream.of("a", "bb", "ccc")
    .map(String::toUpperCase)
    .toList();
System.out.println(l);
```
Answer: _____________

5.
```java
List<Integer> l = new ArrayList<>(List.of(1, 2, 3));
List<Integer> r = l.reversed();
l.set(0, 99);
System.out.println(r);
```
Answer: _____________

6.
```java
List<String> l = new ArrayList<>(List.of("apple", "banana", "cherry"));
l.sort((a, b) -> a.length() - b.length());
System.out.println(l);
```
Answer: _____________

7.
```java
List<Integer> l = new ArrayList<>(List.of(10, 20, 30, 40, 50));
l.removeRange(1, 3); // removeRange is protected, but conceptually
System.out.println(l);
```
Answer: _____________

8.
```java
List<String> l = new ArrayList<>(List.of("x", "y", "z"));
List<String> m = new ArrayList<>(l);
l.clear();
System.out.println(m);
```
Answer: _____________

9.
```java
List<Integer> l = new ArrayList<>(List.of(1, 2, 3));
List<Integer> u = Collections.unmodifiableList(l);
l.add(4);
System.out.println(u);
```
Answer: _____________

10.
```java
List<Integer> l = List.copyOf(Arrays.asList(1, 2, 3, null));
System.out.println(l);
```
Answer: _____________

#### Advanced LinkedList & Deque (8 questions)
11.
```java
LinkedList<Integer> q = new LinkedList<>();
q.offerLast(1);
q.offerLast(2);
q.offerLast(3);
while (!q.isEmpty()) {
    System.out.print(q.pollFirst() + " ");
}
```
Answer: _____________

12.
```java
Deque<String> d = new LinkedList<>();
d.addFirst("a");
d.addLast("b");
d.addFirst("z");
System.out.println(d);
```
Answer: _____________

13.
```java
LinkedList<Integer> l = new LinkedList<>(List.of(1, 2, 3, 2, 4, 2));
l.removeAll(List.of(2));
System.out.println(l);
```
Answer: _____________

14.
```java
LinkedList<String> l = new LinkedList<>(List.of("a", "b", "c"));
Iterator<String> it = l.iterator();
it.next();
l.add("x"); // structural modification
it.next(); // will this throw?
```
Answer: _____________

15.
```java
LinkedList<Integer> stack = new LinkedList<>();
stack.push(1);
stack.push(2);
stack.push(3);
System.out.println(stack.pop() + " " + stack.pop());
```
Answer: _____________

16.
```java
LinkedList<Character> l = new LinkedList<>();
for (char c : "abcabc".toCharArray()) {
    l.add(c);
}
l.removeFirstOccurrence('a');
l.removeLastOccurrence('c');
System.out.println(l);
```
Answer: _____________

17.
```java
Deque<Integer> dq = new LinkedList<>(List.of(1, 2, 3, 4));
dq.removeFirst();
dq.removeLast();
System.out.println(dq);
```
Answer: _____________

18.
```java
LinkedList<String> l = new LinkedList<>(List.of("x", "y", "z"));
ListIterator<String> it = l.listIterator(l.size());
it.previous();
it.set("modified");
System.out.println(l);
```
Answer: _____________

#### Vector, Stack, and CopyOnWriteArrayList (5 questions)
19.
```java
Stack<Integer> st = new Stack<>();
st.push(1);
st.push(2);
st.push(3);
int x = st.search(1);
System.out.println(x);
```
Answer: _____________

20.
```java
Vector<String> v = new Vector<>(5, 2);
for (int i = 0; i < 8; i++) {
    v.add("" + i);
}
System.out.println(v.capacity());
```
Answer: _____________

21.
```java
CopyOnWriteArrayList<Integer> l = new CopyOnWriteArrayList<>(List.of(1, 2, 3));
Iterator<Integer> it1 = l.iterator();
l.add(4);
Iterator<Integer> it2 = l.iterator();
System.out.println(it1.hasNext() + " " + it2.hasNext());
```
Answer: _____________

22.
```java
Stack<Character> st = new Stack<>();
String s = "hello";
for (char c : s.toCharArray()) st.push(c);
while (!st.isEmpty()) System.out.print(st.pop());
```
Answer: _____________

23.
```java
CopyOnWriteArrayList<String> l = new CopyOnWriteArrayList<>(List.of("a", "b", "c"));
for (String s : l) {
    l.add("x");
}
System.out.println(l);
```
Answer: _____________

#### Complex Iteration & ListIterator (5 questions)
24.
```java
List<Integer> l = new ArrayList<>(List.of(1, 2, 3, 4, 5));
ListIterator<Integer> it = l.listIterator(l.size());
it.previous();
it.remove();
System.out.println(l);
```
Answer: _____________

25.
```java
List<String> l = new ArrayList<>(List.of("a", "b", "c", "d"));
ListIterator<String> it = l.listIterator(1);
it.next();
it.set("X");
it.previous();
it.add("Y");
System.out.println(l);
```
Answer: _____________

26.
```java
List<Integer> l = new ArrayList<>(List.of(1, 2, 3));
ListIterator<Integer> lit = l.listIterator();
while (lit.hasNext()) {
    if (lit.next() == 2) lit.remove();
}
System.out.println(l);
```
Answer: _____________

27.
```java
List<Integer> l = new ArrayList<>(List.of(1, 2, 3, 4));
for (Iterator<Integer> it = l.iterator(); it.hasNext();) {
    Integer val = it.next();
    if (val % 2 == 0) it.remove();
}
System.out.println(l);
```
Answer: _____________

28.
```java
List<String> l = new ArrayList<>(List.of("p", "q", "r"));
ListIterator<String> it = l.listIterator(l.size());
while (it.hasPrevious()) {
    System.out.print(it.previous());
}
```
Answer: _____________

#### Sorting, Searching, Comparator (4 questions)
29.
```java
List<String> l = new ArrayList<>(List.of("apple", "pie", "a"));
l.sort(Comparator.comparingInt(String::length));
System.out.println(l);
```
Answer: _____________

30.
```java
List<Integer> l = new ArrayList<>(List.of(1, 3, 5, 7, 9));
int idx = Collections.binarySearch(l, 5);
System.out.println(idx);
```
Answer: _____________

31.
```java
List<Integer> l = new ArrayList<>(List.of(9, 5, 3, 1));
Collections.binarySearch(l, 5); // unsorted list
System.out.println("works");
```
Answer: _____________

32.
```java
List<String> l = new ArrayList<>(List.of("c", "a", "b"));
Collections.sort(l, Collections.reverseOrder());
System.out.println(l);
```
Answer: _____________

33.
```java
List<Employee> l = new ArrayList<>();
l.add(new Employee("Alice", 25));
l.add(new Employee("Bob", 20));
l.sort(Comparator.comparingInt(Employee::getAge));
System.out.println(l.get(0).getName());
```
Answer: _____________

34.
```java
List<Integer> l = new ArrayList<>(List.of(3, 1, 4, 1, 5));
l.sort(null); // natural order
System.out.println(l);
```
Answer: _____________

35.
```java
List<String> l = Stream.of("5", "3", "1", "4", "2")
    .sorted()
    .toList();
System.out.println(l);
```
Answer: _____________

---

### 2.2 MCQ Advanced (35 Questions)

#### subList and Structural Modifications (5 questions)
1. `subList()` returns:
```text
A) independent copy
B) view backed by original
C) immutable snapshot
D) new ArrayList
```

2. Modifying original list affects subList:
```text
A) never
B) only if using removeRange
C) yes, immediately
D) only if concurrent
```

3. ConcurrentModificationException from subList happens:
```text
A) only with subList modifications
B) if original modified structurally after subList creation
C) never occurs
D) always occurs
```

4. `subList` performance characteristics:
```text
A) always O(n)
B) set/get O(1), add/remove O(n)
C) all operations O(log n)
D) optimized always
```

5. Correct usage pattern for subList:
```text
A) create, then modify original
B) create, then use subList only
C) use immediately in same scope
D) store for later always
```

#### Comparator & Comparable (7 questions)
6. `Comparable` interface:
```text
A) compares two external objects
B) defines natural ordering within class
C) thread-safe comparison
D) faster than Comparator
```

7. `Comparator` implementation:
```text
A) inside comparable class
B) external comparison logic
C) built into List
D) cannot use with sort
```

8. `compareTo()` return value:
```text
A) true/false
B) < 0, 0, > 0 for less, equal, greater
C) 0/1/-1 always
D) boolean
```

9. `Collections.reverseOrder()` without argument:
```text
A) throws exception
B) reverse current list
C) natural order reversal
D) invalid usage
```

10. Chaining comparators:
```text
A) not possible
B) using .thenComparing()
C) by creating new Comparator each time
D) impossible with lambda
```

11. Custom Comparator for objects:
```java
List<Student> l = new ArrayList<>(students);
l.sort(Comparator.comparingInt(Student::getAge)
    .thenComparing(Student::getName));
```
This sorts by:
```text
A) name first, then age
B) age first, then name
C) randomly
D) alphabetically always
```

12. Performance: sort with custom Comparator:
```text
A) always slower than no Comparator
B) depends on Comparator complexity
C) same speed as natural order
D) can be O(1)
```

#### Immutability & Defensive Copy (6 questions)
13. `List.of()` vs `List.copyOf()`:
```text
A) same behavior
B) both immutable, but copyOf defensively copies
C) List.of faster
D) List.copyOf throws on null
```

14. Returning internal list safely:
```text
A) return list directly
B) return Collections.unmodifiableList(list)
C) return List.copyOf(list)
D) return new ArrayList<>(list)
```

15. Defensive copy rationale:
```text
A) always needed
B) prevents external modification of internal state
C) performance optimization
D) legacy requirement
```

16. `Arrays.asList()` structural modification:
```text
A) add always works
B) remove always works
C) size is fixed, add/remove throws
D) all operations work
```

17. Collection returned by `List.of()`:
```text
A) can be modified via underlying array
B) truly immutable, no backdoor
C) thread-safe but mutable
D) uses Arrays.asList internally
```

18. When to use `Collections.unmodifiableList()`:
```text
A) always
B) when view of mutable list needed
C) to create immutable copy
D) for performance
```

#### Streams and Functional Operations (6 questions)
19. `.toList()` on Stream (Java 16+):
```text
A) immutable list
B) mutable ArrayList
C) fixed-size list
D) synchronized list
```

20. `List.removeIf()` with lambda:
```text
A) creates new list
B) modifies original list in-place
C) returns filtered result
D) thread-safe
```

21. `List.forEach()` vs for-each loop:
```text
A) same behavior always
B) forEach cannot modify list structurally
C) for-each faster
D) forEach prevents ConcurrentModificationException
```

22. `List.replaceAll()`:
```text
A) functional operation, returns new list
B) in-place replacement using UnaryOperator
C) creates stream
D) immutable operation
```

23. Stream distinct() on List of objects:
```text
A) uses == for comparison
B) uses equals() method
C) uses hashCode()
D) cannot call on custom objects
```

24. `sorted(Comparator)` on Stream:
```text
A) returns stream in place
B) terminal operation
C) returns new list directly
D) lazy evaluation maintains
```

#### CopyOnWriteArrayList Behavior (5 questions)
25. `CopyOnWriteArrayList` best use case:
```text
A) frequent writes
B) read-heavy concurrent workloads
C) single-threaded performance
D) memory efficiency
```

26. Iterator on `CopyOnWriteArrayList`:
```text
A) reflects concurrent modifications
B) snapshot at iteration start
C) throws ConcurrentModificationException
D) blocks other threads
```

27. Write operation on `CopyOnWriteArrayList`:
```text
A) modifies in-place
B) creates copy of entire array
C) uses copy-on-write semantics
D) uses lock-free data structure
```

28. `CopyOnWriteArrayList.add()` complexity:
```text
A) O(1)
B) O(n) due to array copy
C) O(log n)
D) unpredictable
```

29. When NOT to use `CopyOnWriteArrayList`:
```text
A) concurrent reads
B) frequent concurrent writes
C) thread-safe iteration needed
D) immutable snapshots needed
```

#### Advanced Iteration (3 questions)
30. `ListIterator.nextIndex()`:
```text
A) index of element just returned
B) index of next element to return
C) size of list
D) current position from end
```

31. Using `ListIterator` for safe removal:
```text
A) not recommended
B) safe because using iterator method
C) must use concurrent structure
D) not possible
```

32. Reverse iteration with `ListIterator`:
```java
ListIterator<String> it = l.listIterator(l.size());
while (it.hasPrevious()) {
    it.previous();
}
```
This is:
```text
A) O(1)
B) O(n)
C) O(n^2)
D) O(log n)
```

#### Vector & Legacy Behavior (3 questions)
33. When `Vector` preferred over `ArrayList`:
```text
A) never in new code
B) legacy codebase integration
C) better performance
D) automatic synchronization
```

34. Capacity increment in Vector:
```text
A) always fixed
B) configurable constructor parameter
C) always doubles
D) random
```

35. Synchronization overhead in Vector:
```text
A) none
B) can impact concurrent performance
C) invisible to developer
D) only on reads
```

---

### 2.2 Advanced Interview Questions (15 Questions)

1. **Design a thread-safe mutable cache using CopyOnWriteArrayList. When is this better than ArrayList with synchronization?**

2. **Explain the ConcurrentModificationException: why does it occur with subList and how to prevent it safely?**

3. **subList creates a view, not a copy. What are the implications of this design? Show a code example where this causes bugs.**

4. **Compare three ways of defensive copying when returning lists: new ArrayList<>(), List.copyOf(), and Collections.unmodifiableList(). Use cases for each.**

5. **Implement a reverse() function using ListIterator. Compare efficiency with Collections.reverse().**

6. **Explain why binarySearch() requires a sorted list. What's the worst-case behavior if list is unsorted?**

7. **Design a multi-key sort using Comparator.thenComparing(). Handle null values properly.**

8. **Streams provide functional operations like filter/map/sorted. How do they differ from imperative list operations? Performance implications?**

9. **When removing elements during iteration, why is Iterator.remove() preferred over list.remove()? Demonstrate the bug without it.**

10. **LinkedList implements Deque. Show practical use cases where Deque operations are cleaner than List operations.**

11. **Stack extends Vector (legacy design issue). How would you implement a modern Stack? What about ArrayDeque alternative?**

12. **Explain the interaction between reversed() view and structural modifications. Is it a view or copy?**

13. **Implement a LRU (Least Recently Used) cache using LinkedHashMap access-order behavior. Show eviction logic.**

14. **Compare ArrayList, LinkedList, Vector, and CopyOnWriteArrayList for a scenario with 1M elements, read-heavy, multi-threaded workload.**

15. **Explain the equals() contract for lists: [1,2] equals [1,2] but equals check also considers type. Why this design?**

---

## LEVEL 3 - EDGE CASES & EXPERT PATTERNS

### 3.1 Predict Behavior - Edge Cases (20 Questions)

1. Empty list operations:
```java
List<Integer> l = new ArrayList<>();
System.out.println(l.get(0));
```
Answer: _____________

2. Null in immutable list:
```java
List<Integer> l = List.of(1, null, 3);
```
Answer: _____________

3. Modifying list view:
```java
List<Integer> l = new ArrayList<>(List.of(1, 2, 3, 4, 5));
List<Integer> view = l.subList(1, 4);
l.removeIf(x -> x > 2);
System.out.println(view);
```
Answer: _____________

4. Iterator on concurrent modification:
```java
List<String> l = new ArrayList<>(List.of("a", "b", "c"));
for (String s : l) {
    l.add("x");
}
```
Answer: _____________

5. Stack on empty:
```java
Stack<Integer> st = new Stack<>();
System.out.println(st.pop());
```
Answer: _____________

6. binarySearch on unsorted:
```java
List<Integer> l = new ArrayList<>(List.of(3, 1, 2));
System.out.println(Collections.binarySearch(l, 1));
```
Answer: _____________

7. LinkedList.get(0) on large list:
```java
LinkedList<Integer> l = new LinkedList<>();
for (int i = 0; i < 1000000; i++) l.add(i);
long start = System.nanoTime();
System.out.println(l.get(999999)); // O(n) access
```
Answer: _____________

8. ListIterator add then remove:
```java
List<Integer> l = new ArrayList<>(List.of(1, 2, 3));
ListIterator<Integer> it = l.listIterator();
it.add(0);
System.out.println(it.next());
```
Answer: _____________

9. subList then remove from original:
```java
List<Integer> l = new ArrayList<>(List.of(1, 2, 3, 4, 5));
List<Integer> sub = l.subList(1, 4);
l.clear();
System.out.println(sub);
```
Answer: _____________

10. CopyOnWriteArrayList concurrent add:
```java
CopyOnWriteArrayList<Integer> l = new CopyOnWriteArrayList<>();
Iterator<Integer> it = l.iterator();
l.add(1);
System.out.println(it.hasNext());
```
Answer: _____________

11. Collections.unmodifiableList with null value:
```java
List<String> inner = new ArrayList<>();
inner.add(null);
List<String> unmod = Collections.unmodifiableList(inner);
System.out.println(unmod.get(0));
```
Answer: _____________

12. Stack.search() on absent element:
```java
Stack<String> st = new Stack<>();
st.push("a");
st.push("b");
System.out.println(st.search("x"));
```
Answer: _____________

13. reversed() multiple times:
```java
List<Integer> l = new ArrayList<>(List.of(1, 2, 3));
List<Integer> r1 = l.reversed();
List<Integer> r2 = r1.reversed();
System.out.println(r2);
```
Answer: _____________

14. forEach on list with stream:
```java
List<String> l = List.of("a", "b");
l.stream().forEach(s -> System.out.println(s));
System.out.println("done");
```
Answer: _____________

15. Comparator chain with null:
```java
List<String> l = new ArrayList<>(Arrays.asList("b", null, "a"));
l.sort(Comparator.nullsLast(Comparator.naturalOrder()));
System.out.println(l);
```
Answer: _____________

16. Vector growth with large capacityIncrement:
```java
Vector<Integer> v = new Vector<>(1, 1000000);
for (int i = 0; i < 10; i++) v.add(i);
System.out.println(v.capacity());
```
Answer: _____________

17. removeIf on filtered stream list:
```java
List<Integer> l = Stream.of(1, 2, 3, 4, 5)
    .filter(x -> x > 2)
    .toList();
l.removeIf(x -> x == 4);
```
Answer: _____________

18. ListIterator during remove/set:
```java
List<String> l = new ArrayList<>(List.of("a", "b", "c"));
ListIterator<String> it = l.listIterator();
it.next();
it.next();
it.remove();
it.set("X");
```
Answer: _____________

19. LinkedList capacity method:
```java
LinkedList<Integer> l = new LinkedList<>(List.of(1, 2, 3));
System.out.println(l.capacity()); // no such method
```
Answer: _____________

20. Arrays.asList structural operations:
```java
List<Integer> l = Arrays.asList(1, 2, 3);
l.clear();
System.out.println(l);
```
Answer: _____________

---

## EXPERT PATTERNS (Design & Optimization)

### Pattern 1: Efficient Bulk Operations
```java
// Instead of: for loop with add()
List<Integer> result = new ArrayList<>();
for (Integer x : list) result.add(x * 2);

// Better: use addAll with collection
List<Integer> data = List.of(1, 2, 3);
List<Integer> result = new ArrayList<>(data.size());
result.addAll(data.stream().map(x -> x * 2).toList());
```

### Pattern 2: Defensive List Copying
```java
// Receiving
public void setItems(List<String> items) {
    this.items = new ArrayList<>(items); // independent mutable copy
}

// Returning
public List<String> getItems() {
    return List.copyOf(items); // immutable snapshot
}
```

### Pattern 3: Safe Concurrent Access with CopyOnWriteArrayList
```java
CopyOnWriteArrayList<String> listeners = new CopyOnWriteArrayList<>();
// Writer thread
listeners.add("listener1");
// Reader thread
for (String listener : listeners) { // safe iteration, doesn't see new adds
    process(listener);
}
```

### Pattern 4: Efficient Sorting with Multiple Keys
```java
l.sort(Comparator.comparingInt(Person::getAge)
    .reversed()
    .thenComparing(Person::getName)
    .thenComparingInt(Person::getId));
```

### Pattern 5: Stream Processing Pipelines
```java
List<String> result = largeList.stream()
    .filter(s -> s.length() > 5)
    .map(String::toUpperCase)
    .distinct()
    .sorted()
    .toList(); // immutable result
```

---

## ANSWERS KEY

### Level 1 Answers

#### 1.1 Predict Output
1. [10, 99, 20, 30, 40]
2. [10, 30]
3. 4
4. [a, X, c]
5. 0
6. [1, 3, 5]
7. [1, 2, 3]
8. false
9. 4
10. 3
11. 5
12. 99
13. [10, 20]
14. [a, c]
15. [1, 1, 2, 3]
16. 20
17. 5
18. [1, 3]
19. true
20. 20
21. 2
22. b, a
23. capacity >= 10 (default or set)
24. UnsupportedOperationException
25. UnsupportedOperationException
26. [1, 2, 3]
27. [1, 99, 3]
28. [9, 2, 3]
29. [1, 99, 2, 3]
30. 30
31. [a, c] (safely removes "b" using iterator)
32. [1, 3, 5]
33. 2
34. true
35. [5, 4, 3, 1, 1]

#### 1.2 MCQ (Sample Answers - Every letter has answer)
1. B, 2. A, 3. C, 4. A, 5. A, 6. B, 7. B, 8. C, 9. B, 10. C
11. B, 12. C, 13. C, 14. B, 15. C, 16. B, 17. B
18. B, 19. B, 20. B, 21. B, 22. A
23. B, 24. B, 25. B, 26. B, 27. B
28. B, 29. A, 30. B
31. B, 32. C, 33. D

---

