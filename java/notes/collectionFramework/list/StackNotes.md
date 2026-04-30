# Stack Notes

## Imports

```java
import java.util.Stack;
import java.util.LinkedList;
import java.util.ArrayList;
import java.util.ArrayDeque;
import java.util.Deque;
```

Use `java.util.*` or exact `java.util` imports.  
`java.utils.*` is incorrect.

## What Is Stack

- Stack follows **LIFO** (Last In, First Out).
- Last inserted element is removed first.

## Stack Class (`java.util.Stack`)

`Stack` is a legacy class that extends `Vector`.

```java
Stack<Integer> stack = new Stack<>();
stack.push(1);      // add at top
stack.push(3);
int top = stack.peek();   // read top
int removed = stack.pop();// remove top
int pos = stack.search(1);// 1-based position from top, -1 if not found
boolean empty = stack.isEmpty();
```

### Notes

- Because it extends `Vector`, methods are synchronized.
- Thread-safe for individual calls, but has locking overhead.
- In modern code, `Stack` is usually not preferred.

## Method Behavior (In-Place vs Read)

- In-place (modifies stack): `push`, `pop`, `clear`
- Read/no structural change: `peek`, `search`, `isEmpty`, `size`

## Complexity (Typical)

- `push`: `O(1)` amortized
- `pop`: `O(1)`
- `peek`: `O(1)`
- `isEmpty`: `O(1)`
- `search`: `O(n)`

## Using LinkedList as Stack (via Deque Operations)

```java
LinkedList<Integer> ls = new LinkedList<>();
ls.addLast(1);      // push
int top = ls.getLast();   // peek
int x = ls.removeLast();  // pop
int n = ls.size();
```

Important correction:
- If you use `addLast` as push, then pop must be `removeLast` (not `removeFirst`).
- Keep both operations on the same end for correct LIFO behavior.

## Using ArrayList as Stack (Manual)

```java
ArrayList<Integer> arr = new ArrayList<>();
arr.add(10);                             // push
int top = arr.get(arr.size() - 1);       // peek
int x = arr.remove(arr.size() - 1);      // pop
```

- Works for stack behavior.
- Must guard against empty list before `get/remove(size - 1)`.

## Preferred Modern Option: ArrayDeque

`ArrayDeque` is generally preferred for stack behavior in single-threaded code.

```java
Deque<Integer> dq = new ArrayDeque<>();
dq.push(1);          // add first
dq.push(3);
int top = dq.peek(); // peek first
int x = dq.pop();    // remove first
```

Why preferred:
- No legacy `Vector` synchronization overhead
- Good performance and memory behavior
- Cleaner API for stack/queue use-cases

## Thread-Safety Summary

- `Stack`: synchronized methods (legacy thread-safe behavior)
- `LinkedList`, `ArrayList`, `ArrayDeque`: not thread-safe by default
- For concurrent scenarios, use external synchronization or concurrent collections as needed

## Common Mistakes

- Wrong import: `java.utils.*` (should be `java.util.*`)
- Mixing ends in linked list stack simulation (`addLast` with `removeFirst`) breaks LIFO
- Calling `pop/peek` on empty structure causes exception
