# 05 - CopyOnWriteArrayList Core

## 1) Internal Idea

On every write (`add/remove/set`), it creates a new copied array.

Reads happen on stable snapshot.

Then it atomically switches internal reference to the new array.

## 2) Why Useful

- iteration is safe without external synchronization
- no `ConcurrentModificationException` during iteration

Why it exists:

- `ArrayList`/`LinkedList` are not thread-safe
- `Vector` is synchronized but coarse-grained
- `CopyOnWriteArrayList` provides very low read-side contention

## 3) Cost Model

- read: fast
- write: expensive (copy whole array)
- write complexity: usually `O(n)` per update
- writes create extra garbage (new arrays)

## 4) Use Case

Best for:

- read-heavy, write-rare collections
- listener lists, subscriber registries

## 5) Example

```java
CopyOnWriteArrayList<String> listeners = new CopyOnWriteArrayList<>();
listeners.add("L1");
for (String l : listeners) {
    listeners.add("L2"); // safe, iterator sees snapshot
}
```

## 6) Iterator Behavior

- snapshot at iterator creation
- no `ConcurrentModificationException` for normal concurrent iteration
- iterator `remove()` is unsupported
- later updates are not visible to already-created iterator

## 7) In-Place vs New View/Copy

- in-place update of same list object: `add`, `addIfAbsent`, `addAll`, `set`, `remove`, `clear`
- new array copy returned: `toArray(...)`
- new view: `reversed()`

## 8) Java 21 Sequenced Methods

- `addFirst/addLast`: supported, each write still copies array
- `getFirst/getLast`: supported reads
- `removeFirst/removeLast`: supported writes with copy-on-write behavior

Practical complexity:

- `get(index)`: `O(1)`
- `add/remove/set`: `O(n)`
- `addFirst/removeFirst`: `O(n)`
- `addLast/removeLast`: also `O(n)` here (copy-on-write), unlike amortized end behavior in `ArrayList`

## 9) Threaded Demo

```java
List<String> sharedList = new CopyOnWriteArrayList<>();
sharedList.add("item1");
sharedList.add("item2");
sharedList.add("item3");

Thread readerThread = new Thread(() -> {
    for (String s : sharedList) {
        System.out.println("Reading: " + s);
    }
});

Thread writerThread = new Thread(() -> {
    sharedList.add("item4");
    sharedList.remove("item2");
});

readerThread.start();
writerThread.start();
```

Full version with pacing and interruption handling:

```java
Thread readerThread2 = new Thread(() -> {
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

Thread writerThread2 = new Thread(() -> {
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
```

## 10) Common Mistakes

- use `"milk".equals(item)`, not `item == "milk"` for string value compare
- `remove("absent")` returns `false` and does nothing
