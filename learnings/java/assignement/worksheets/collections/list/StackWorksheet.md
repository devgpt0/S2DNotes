# Stack Worksheet

Source: StackNotes.md

## Level 1

### Tricky Predict the Output (15)

1.
```java
Stack<Integer> s = new Stack<>();
s.push(1);
s.push(2);
s.push(3);
System.out.println(s.peek());
```

Answer: _____________

2.
```java
Stack<Integer> s = new Stack<>();
s.push(1);
s.push(2);
System.out.println(s.pop());
```

Answer: _____________

3.
```java
Stack<Integer> s = new Stack<>();
s.push(1);
s.push(2);
s.pop();
System.out.println(s.peek());
```

Answer: _____________

4.
```java
Stack<String> s = new Stack<>();
s.push("A");
s.push("B");
System.out.println(s.search("A"));
```

Answer: _____________

5.
```java
Stack<String> s = new Stack<>();
s.push("A");
s.push("B");
System.out.println(s.search("Z"));
```

Answer: _____________

6.
```java
Stack<Integer> s = new Stack<>();
System.out.println(s.isEmpty());
```

Answer: _____________

7.
```java
Stack<Integer> s = new Stack<>();
s.push(10);
s.push(20);
System.out.println(s.size());
```

Answer: _____________

8.
```java
Stack<Integer> s = new Stack<>();
s.pop();
```

Answer: _____________

9.
```java
Stack<Integer> s = new Stack<>();
s.peek();
```

Answer: _____________

10.
```java
Deque<Integer> d = new ArrayDeque<>();
d.push(1);
d.push(2);
d.push(3);
System.out.println(d.pop());
```

Answer: _____________

11.
```java
Deque<Integer> d = new ArrayDeque<>();
d.push(1);
d.push(2);
System.out.println(d.peek());
```

Answer: _____________

12.
```java
LinkedList<Integer> l = new LinkedList<>();
l.addLast(1);
l.addLast(2);
System.out.println(l.removeLast());
```

Answer: _____________

13.
```java
ArrayList<Integer> a = new ArrayList<>();
a.add(1);
a.add(2);
System.out.println(a.remove(a.size()-1));
```

Answer: _____________

14.
```java
Deque<Integer> d = new ArrayDeque<>();
d.push(5);
d.pop();
System.out.println(d.isEmpty());
```

Answer: _____________

15.
```java
Stack<Integer> s = new Stack<>();
s.push(1);
s.clear();
System.out.println(s.isEmpty());
```

Answer: _____________

### MCQ Theory (15)

1. Stack follows:
```text
A) FIFO
B) LIFO
C) random
D) sorted
```

2. `push(x)` means:
```text
A) remove top
B) insert at top
C) insert at bottom
D) sort stack
```

3. `pop()` means:
```text
A) read top only
B) remove and return top
C) remove bottom
D) return size
```

4. `peek()` means:
```text
A) remove top
B) read top without removal
C) clear stack
D) reverse stack
```

5. `search(x)` in Stack returns:
```text
A) zero-based from bottom
B) one-based from top
C) boolean
D) hash
```

6. `search(x)` not found value is:
```text
A) 0
B) -1
C) null
D) exception
```

7. Preferred modern stack implementation is often:
```text
A) Stack
B) ArrayDeque
C) Vector
D) Hashtable
```

8. Legacy Stack concern in modern code:
```text
A) no generics
B) Vector-based synchronization overhead
C) immutability
D) no push method
```

9. Correct package root is:
```text
A) java.utils
B) java.util
C) java.utility
D) util.java
```

10. `pop()` on empty Stack causes:
```text
A) silent ignore
B) runtime exception
C) false return
D) -1 return
```

11. `peek()` on empty Stack causes:
```text
A) null return always
B) runtime exception
C) compile error
D) empty string
```

12. LinkedList stack simulation must use:
```text
A) opposite ends for push/pop
B) same end for push/pop
C) middle operations
D) random ends
```

13. ArrayList stack top is usually:
```text
A) index 0
B) index size-1
C) index size/2
D) random index
```

14. Desired complexity for stack push/pop/peek is:
```text
A) O(1)
B) O(log n)
C) O(n)
D) O(n^2)
```

15. Best underflow guard before pop is:
```text
A) sort check
B) isEmpty check
C) reverse check
D) trim check
```

## Level 2

### Tricky Predict the Output (15)

1.
```java
Deque<Integer> d = new ArrayDeque<>();
d.push(1);
d.push(2);
d.push(3);
System.out.println(d);
```

Answer: _____________

2.
```java
Deque<Integer> d = new ArrayDeque<>();
d.push(1);
d.push(2);
d.pop();
System.out.println(d.peek());
```

Answer: _____________

3.
```java
Deque<Integer> d = new ArrayDeque<>();
d.push(1);
d.push(2);
d.push(3);
d.pop();
d.pop();
System.out.println(d.peek());
```

Answer: _____________

4.
```java
Deque<Integer> d = new ArrayDeque<>();
d.pop();
```

Answer: _____________

5.
```java
LinkedList<Integer> l = new LinkedList<>();
l.addLast(10);
l.addLast(20);
l.addLast(30);
System.out.println(l.getLast());
```

Answer: _____________

6.
```java
LinkedList<Integer> l = new LinkedList<>();
l.addLast(10);
l.addLast(20);
l.removeLast();
System.out.println(l);
```

Answer: _____________

7.
```java
ArrayList<Integer> a = new ArrayList<>();
a.add(10);
a.add(20);
a.add(30);
int x = a.get(a.size()-1);
System.out.println(x);
```

Answer: _____________

8.
```java
ArrayList<Integer> a = new ArrayList<>();
a.add(10);
a.add(20);
a.remove(a.size()-1);
System.out.println(a);
```

Answer: _____________

9.
```java
Stack<Integer> s = new Stack<>();
s.push(1);
s.push(2);
s.push(3);
while(!s.isEmpty()) System.out.print(s.pop());
```

Answer: _____________

10.
```java
Stack<String> s = new Stack<>();
s.push("x");
s.push("y");
s.push("z");
System.out.println(s.search("z"));
```

Answer: _____________

11.
```java
Stack<String> s = new Stack<>();
s.push("x");
s.push("y");
s.push("z");
System.out.println(s.search("x"));
```

Answer: _____________

12.
```java
Deque<Integer> d = new ArrayDeque<>();
d.push(1);
d.push(2);
d.push(3);
d.clear();
System.out.println(d.isEmpty());
```

Answer: _____________

13.
```java
Deque<Integer> d = new ArrayDeque<>();
d.push(1);
d.push(2);
System.out.println(d.size());
```

Answer: _____________

14.
```java
Deque<Integer> d = new ArrayDeque<>();
d.push(1);
d.push(2);
d.push(3);
System.out.println(d.peek() + ":" + d.pop());
```

Answer: _____________

15.
```java
LinkedList<Integer> l = new LinkedList<>();
l.addLast(1);
l.addLast(2);
System.out.println(l.removeFirst());
```

Answer: _____________

### MCQ Theory (15)

1. In `Deque`, stack-style push maps to:
```text
A) addLast
B) push/addFirst
C) offerLast only
D) removeFirst
```

2. In `Deque`, stack-style pop maps to:
```text
A) pop/removeFirst
B) removeLast
C) pollLast only
D) clear
```

3. In `Deque`, stack-style peek maps to:
```text
A) peek/peekFirst
B) peekLast only
C) size
D) contains
```

4. `ArrayDeque` allows null values?
```text
A) yes
B) no
C) one null only
D) only with lock
```

5. `ArrayDeque` is thread-safe by default?
```text
A) yes
B) no
C) only in static methods
D) only for primitives
```

6. Legacy `Stack` thread behavior:
```text
A) unsynchronized always
B) synchronized method-level calls
C) immutable object
D) lock-free CAS
```

7. `if(!s.empty()) s.pop();` in multi-threading is:
```text
A) atomic pair
B) non-atomic pair without extra sync
C) compile error
D) always safe
```

8. Iterative DFS commonly uses:
```text
A) queue
B) stack/deque
C) set
D) map only
```

9. Undo feature maps naturally to:
```text
A) queue
B) stack
C) heap
D) tree map
```

10. Browser back history is conceptually:
```text
A) hash table
B) stack-like behavior
C) binary tree
D) graph traversal queue
```

11. If using `addLast` as push in LinkedList, pop should be:
```text
A) removeFirst
B) removeLast
C) pop both
D) clear
```

12. `clear()` on stack-like collection does:
```text
A) sort ascending
B) remove all elements
C) remove top only
D) compact only
```

13. Key advantage of `ArrayDeque` over legacy `Stack`:
```text
A) map semantics
B) modern API with strong stack/queue performance profile
C) immutability
D) no generics
```

14. `size()` on stack collections is generally:
```text
A) O(1)
B) O(log n)
C) O(n)
D) O(n^2)
```

15. Interview red-flag stack bug is:
```text
A) same-end operations
B) mixing opposite ends for push/pop
C) empty checks
D) LIFO understanding
```
