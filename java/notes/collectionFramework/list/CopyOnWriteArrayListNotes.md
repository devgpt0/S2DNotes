# CopyOnWriteArrayList Notes

## Imports

```java
import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;
```

`CopyOnWriteArrayList` is a thread-safe `List` implementation from `java.util.concurrent`.

## Why It Exists

- `ArrayList` and `LinkedList` are not thread-safe.
- `Vector` is thread-safe but uses coarse-grained synchronization on many operations.
- `CopyOnWriteArrayList` gives safe concurrent reads with very low read-side contention.

Core idea:
- On each write (`add`, `set`, `remove`, etc.), it creates a new internal array copy.
- It applies the change to the new array.
- Then it atomically switches the internal reference to this new array.

## Best Use Case

Use it when:
- Reads are much more frequent than writes.
- Iteration must be safe while other threads may modify the list.
- You can accept higher memory and write cost.

Avoid it when:
- Writes are frequent or list is very large.

## Read vs Write Cost

- Reads (`get`, iteration, `contains`) are lock-light and fast.
- Writes are expensive (`O(n)` copy per write) and create extra garbage.

## Iterator Behavior (Very Important)

- Iterator is **snapshot-based**.
- It sees the array state at iterator creation time.
- Later modifications are not visible in that iterator.
- `ConcurrentModificationException` is not thrown during normal concurrent iteration.
- Iterator mutation methods like `remove()` are not supported.

## In-Place vs New View / Copy

- `add`, `addIfAbsent`, `addAll`, `set`, `remove`, `clear`: update this same list object (internally swaps array reference).
- `reversed()` (Java 21 `List` API): returns a reverse-order view, not a copied list.
- `toArray(...)`: returns a new array copy.


`CopyOnWriteArrayList` implements `List`, and in Java 21 `List` includes sequenced methods:

- `addFirst(e)` and `addLast(e)` -> supported, each write copies array.
- `getFirst()` and `getLast()` -> supported reads.
- `removeFirst()` and `removeLast()` -> supported writes (copy on write).
- `reversed()` -> reverse-order view via `List` API.

Complexity (practical):
- Reads by index: `O(1)`
- Writes (`add/remove/set`): `O(n)` due to full copy
- `addFirst/removeFirst`: `O(n)`
- `addLast/removeLast`: still `O(n)` here (because copy-on-write), unlike `ArrayList` amortized-end behavior

## Correct Demo (Thread-Safe Iteration + Write)

```java
import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;

public class CopyOnWriteArrayListDemo {
    public static void main(String[] args) {
        List<String> sharedList = new CopyOnWriteArrayList<>();
        sharedList.add("item1");
        sharedList.add("item2");
        sharedList.add("item3");

        Thread readerThread = new Thread(() -> {
            try {
                while (true) {
                    for (String s : sharedList) {
                        System.out.println("Reading: " + s);
                        Thread.sleep(100);
                    }
                }
            } catch (InterruptedException ex) {
                Thread.currentThread().interrupt();
            }
        });

        Thread writerThread = new Thread(() -> {
            try {
                Thread.sleep(500);
                sharedList.add("item4");
                System.out.println("Added item4");

                Thread.sleep(500);
                sharedList.remove("item2");
                System.out.println("Removed item2");
            } catch (InterruptedException ex) {
                Thread.currentThread().interrupt();
            }
        });

        readerThread.start();
        writerThread.start();
    }
}
```

## Common Mistakes to Avoid

- Do not use `if (item == "milk")` for `String`; use `"milk".equals(item)`.
- `remove("item5")` does nothing if item is absent (returns `false`).
- Do not expect iterators to reflect real-time updates; each iterator is a snapshot.