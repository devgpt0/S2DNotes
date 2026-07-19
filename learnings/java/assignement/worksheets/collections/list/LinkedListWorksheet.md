# LinkedList Worksheet

Source: LinkedListNotes.md

## Level 1

### Tricky Predict the Output (15)

1.
```java
LinkedList<String> l = new LinkedList<>(Arrays.asList("a","b","c"));
l.addFirst("x");
System.out.println(l);
```

Answer: _____________

2.
```java
LinkedList<Integer> l = new LinkedList<>(Arrays.asList(1,2,3));
l.addLast(4);
System.out.println(l);
```

Answer: _____________

3.
```java
LinkedList<Integer> l = new LinkedList<>(Arrays.asList(1,2,3));
l.removeFirst();
System.out.println(l);
```

Answer: _____________

4.
```java
LinkedList<Integer> l = new LinkedList<>(Arrays.asList(1,2,3));
l.removeLast();
System.out.println(l);
```

Answer: _____________

5.
```java
LinkedList<String> l = new LinkedList<>(Arrays.asList("ad","raj","ad"));
l.removeFirstOccurrence("ad");
System.out.println(l);
```

Answer: _____________

6.
```java
LinkedList<String> l = new LinkedList<>(Arrays.asList("ad","raj","ad"));
l.removeLastOccurrence("ad");
System.out.println(l);
```

Answer: _____________

7.
```java
LinkedList<Integer> l = new LinkedList<>(Arrays.asList(1,2,3,4));
l.removeIf(x -> x % 2 == 0);
System.out.println(l);
```

Answer: _____________

8.
```java
LinkedList<Integer> l = new LinkedList<>(Arrays.asList(1,2,3));
l.add(1,9);
System.out.println(l);
```

Answer: _____________

9.
```java
LinkedList<Integer> l = new LinkedList<>(Arrays.asList(1,2,3));
l.remove(1);
System.out.println(l);
```

Answer: _____________

10.
```java
LinkedList<String> l = new LinkedList<>(Arrays.asList("k","r","m"));
System.out.println(l.get(1));
```

Answer: _____________

11.
```java
LinkedList<String> l = new LinkedList<>(Arrays.asList("k","r","m"));
System.out.println(l.contains("x"));
```

Answer: _____________

12.
```java
LinkedList<Integer> l = new LinkedList<>(Arrays.asList(1,2,3));
System.out.println(l.size());
```

Answer: _____________

13.
```java
LinkedList<Integer> l = new LinkedList<>(Arrays.asList(1,2,3));
l.clear();
System.out.println(l.isEmpty());
```

Answer: _____________

14.
```java
LinkedList<String> l = new LinkedList<>(Arrays.asList("a","b"));
Object[] a = l.toArray();
System.out.println(a.length);
```

Answer: _____________

15.
```java
LinkedList<Integer> l = new LinkedList<>();
l.removeFirst();
```

Answer: _____________

### MCQ Theory (15)

1. `LinkedList` internal model is:
```text
A) dynamic array
B) doubly linked nodes
C) balanced tree
D) hash buckets
```

2. Memory overhead is higher due to:
```text
A) next/prev references
B) sorting cache
C) gzip compression
D) finalizer queue
```

3. `get(index)` is usually:
```text
A) O(1)
B) O(log n)
C) O(n)
D) O(n^2)
```

4. `addFirst` is generally:
```text
A) O(1)
B) O(log n)
C) O(n)
D) O(n^2)
```

5. `removeLast` is generally:
```text
A) O(1)
B) O(log n)
C) O(n)
D) O(n^2)
```

6. `contains(x)` is typically:
```text
A) O(1)
B) O(log n)
C) O(n)
D) O(n log n)
```

7. `LinkedList` also implements:
```text
A) Map
B) Deque
C) SortedSet
D) Optional
```

8. `removeFirstOccurrence(x)` removes:
```text
A) all matches
B) first match only
C) last match only
D) none
```

9. `removeLastOccurrence(x)` removes:
```text
A) first match
B) last match
C) all matches
D) by index only
```

10. `new LinkedList<>(Arrays.asList(...))` creates:
```text
A) immutable list
B) mutable linked-list copy
C) vector
D) set
```

11. Better use case than random read-heavy work:
```text
A) frequent head/tail updates
B) binary search loops
C) heavy index random access
D) direct memory mapping
```

12. Potential O(n^2) anti-pattern on LinkedList:
```text
A) for-each loop
B) loop with repeated get(i)
C) iterator traversal
D) removeFirst loop
```

13. `toArray()` from LinkedList returns:
```text
A) linked nodes
B) new array copy
C) map view
D) queue view
```

14. `clear()` does:
```text
A) reverse list
B) remove all elements
C) sort list
D) lock list
```

15. True statement:
```text
A) LinkedList random index read is O(1)
B) LinkedList supports duplicates and nulls
C) LinkedList is immutable
D) LinkedList cannot be used as deque
```

## Level 2

### Tricky Predict the Output (15)

1.
```java
LinkedList<String> l = new LinkedList<>(Arrays.asList("A","B","C"));
l.push("X");
System.out.println(l);
```

Answer: _____________

2.
```java
LinkedList<String> l = new LinkedList<>(Arrays.asList("A","B","C"));
System.out.println(l.pop());
```

Answer: _____________

3.
```java
LinkedList<Integer> l = new LinkedList<>(Arrays.asList(1,2,3));
System.out.println(l.peek());
```

Answer: _____________

4.
```java
LinkedList<Integer> l = new LinkedList<>(Arrays.asList(1,2,3));
System.out.println(l.peekFirst() + ":" + l.peekLast());
```

Answer: _____________

5.
```java
LinkedList<Integer> l = new LinkedList<>(Arrays.asList(1,2,3));
l.offerFirst(0);
l.offerLast(4);
System.out.println(l);
```

Answer: _____________

6.
```java
LinkedList<Integer> l = new LinkedList<>(Arrays.asList(1,2,3));
l.pollFirst();
System.out.println(l);
```

Answer: _____________

7.
```java
LinkedList<Integer> l = new LinkedList<>(Arrays.asList(1,2,3));
l.pollLast();
System.out.println(l);
```

Answer: _____________

8.
```java
LinkedList<String> l = new LinkedList<>(Arrays.asList("k","a","r","a","n"));
System.out.println(l.indexOf("a"));
```

Answer: _____________

9.
```java
LinkedList<String> l = new LinkedList<>(Arrays.asList("k","a","r","a","n"));
System.out.println(l.lastIndexOf("a"));
```

Answer: _____________

10.
```java
LinkedList<Integer> l = new LinkedList<>(Arrays.asList(1,2,3));
l.addAll(Arrays.asList(4,5));
System.out.println(l);
```

Answer: _____________

11.
```java
LinkedList<Integer> l = new LinkedList<>(Arrays.asList(3,1,2));
Collections.sort(l);
System.out.println(l);
```

Answer: _____________

12.
```java
LinkedList<Integer> l = new LinkedList<>(Arrays.asList(3,1,2));
l.sort(Collections.reverseOrder());
System.out.println(l);
```

Answer: _____________

13.
```java
LinkedList<String> l = new LinkedList<>(Arrays.asList("x","yy","zzz"));
l.removeIf(s -> s.length() > 1);
System.out.println(l);
```

Answer: _____________

14.
```java
LinkedList<Integer> l = new LinkedList<>(Arrays.asList(1,2,3));
l.set(1,99);
System.out.println(l);
```

Answer: _____________

15.
```java
LinkedList<Integer> l = new LinkedList<>();
System.out.println(l.getFirst());
```

Answer: _____________

### MCQ Theory (15)

1. `push(x)` on LinkedList behaves like:
```text
A) addLast
B) addFirst
C) set(0,x)
D) insert middle
```

2. `pop()` on LinkedList behaves like:
```text
A) removeFirst
B) removeLast
C) peekFirst
D) clear
```

3. `peekFirst()` on empty list returns:
```text
A) exception
B) null
C) -1
D) false
```

4. `getFirst()` on empty list does:
```text
A) returns null
B) throws exception
C) returns -1
D) returns Optional
```

5. `pollFirst()` differs from `removeFirst()` by:
```text
A) time complexity
B) empty-case return vs exception
C) list mutability
D) comparator usage
```

6. `offerLast(x)` is queue-style:
```text
A) enqueue at tail
B) dequeue head
C) stack pop
D) reverse
```

7. `pollLast()` on empty list returns:
```text
A) exception
B) null
C) false
D) -1
```

8. `indexOf(x)` returns:
```text
A) first index
B) last index
C) frequency
D) boolean
```

9. `lastIndexOf(x)` returns:
```text
A) first index
B) last index
C) size
D) hash
```

10. `set(index, value)` complexity is usually dominated by:
```text
A) no-op
B) traversal to node
C) hashing
D) balancing
```

11. `add(index, value)` complexity is usually:
```text
A) O(1)
B) O(log n)
C) O(n)
D) O(n^2)
```

12. Queue-heavy workloads often prefer:
```text
A) ArrayDeque
B) Hashtable
C) TreeMap
D) CopyOnWriteArrayList
```

13. Efficient linked-list traversal usually uses:
```text
A) repeated get(i)
B) iterator/for-each
C) random index jumps
D) binary search
```

14. `removeIf` on LinkedList is:
```text
A) read-only
B) structural mutation
C) compile-time only
D) immutable transformation
```

15. Correct statement:
```text
A) LinkedList cannot act as stack
B) LinkedList cannot act as queue
C) LinkedList supports both stack and queue style methods
D) LinkedList forbids null
```
