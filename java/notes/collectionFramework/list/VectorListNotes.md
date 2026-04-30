# Vector List Notes

## Imports

```java
import java.util.*;
import java.util.Vector;
```

`Vector` is a legacy, synchronized, dynamic-array implementation of `List`.

## Core Properties

- Dynamic array (grows automatically)
- Index-based random access
- Thread-safe for individual method calls (because methods are synchronized)
- Usually slower than `ArrayList` in single-threaded use due to lock overhead

## Time Complexity

- `get(index)`: `O(1)`
- `set(index, value)`: `O(1)`
- `add(value)`: `O(1)` amortized
- `add(index, value)`: `O(n)`
- `remove(index)`: `O(n)`
- `remove(value)`: `O(n)`
- `contains(value)`: `O(n)`
- `indexOf/lastIndexOf`: `O(n)`

## Common Methods (Correct Names)

```java
Vector<Integer> vector = new Vector<>();
vector.add(3);
vector.add(5);
vector.add(6);
vector.add(7);

vector.remove(2);              // remove by index
vector.add(2, 4);              // insert at index
vector.set(2, 6);              // replace at index
int x = vector.get(3);         // read
int n = vector.size();         // current element count
int c = vector.capacity();     // internal capacity
boolean e = vector.isEmpty();
boolean ok = vector.contains(3);
int i1 = vector.indexOf(3);
int i2 = vector.lastIndexOf(3);

vector.ensureCapacity(50);     // increase capacity if needed
vector.trimToSize();           // shrink capacity to current size
Object[] arr = vector.toArray();
vector.clear();
```

## Modern List Additions Available on Vector

```java
vector.addFirst(10);       // insert at beginning
vector.addLast(20);        // insert at end
int first = vector.getFirst();
int last = vector.getLast();
vector.removeFirst();
vector.removeLast();

List<Integer> rev = vector.reversed(); // reverse-order view
```

- `reversed()` returns a view, not a copied list.
- Changes in the original list are reflected in the view.

## In-Place vs New Object

- In-place (mutates same vector): `add`, `addFirst`, `addLast`, `set`, `remove`, `removeFirst`, `removeLast`, `clear`, `ensureCapacity`, `trimToSize`
- Read-only/no structural change: `get`, `getFirst`, `getLast`, `size`, `capacity`, `contains`, `indexOf`, `lastIndexOf`, `isEmpty`
- New object returned: `toArray()` (new array), `reversed()` (new view object)

## Capacity Behavior

- Default initial capacity: `10` (if default constructor is used)
- When full, capacity typically grows to about `2x`
- You can control growth:

```java
Vector<Integer> v1 = new Vector<>(20);      // initial capacity
Vector<Integer> v2 = new Vector<>(10, 5);   // initial capacity + capacityIncrement
```

If `capacityIncrement > 0`, growth happens by that fixed increment; otherwise, growth is doubled.

## Thread-Safety Notes

- `Vector` is safe for concurrent single operations (`add`, `get`, etc.).
- Compound actions are still not automatically atomic.

Example:
- `if (!vector.contains(x)) { vector.add(x); }` is not atomic as a pair.

For heavy-read concurrent scenarios, prefer `CopyOnWriteArrayList`.
For most non-concurrent cases, prefer `ArrayList`.

## Correct Concurrent Example

```java
import java.util.Vector;

public class VectorDemo {
    public static void main(String[] args) throws InterruptedException {
        Vector<Integer> vector = new Vector<>();

        Thread t1 = new Thread(() -> {
            for (int i = 0; i < 1000; i++) {
                vector.add(i);
            }
        });

        Thread t2 = new Thread(() -> {
            for (int i = 0; i < 1000; i++) {
                vector.add(i);
            }
        });

        t1.start();
        t2.start();
        t1.join();
        t2.join();

        System.out.println(vector.size()); // expected 2000
    }
}
```

