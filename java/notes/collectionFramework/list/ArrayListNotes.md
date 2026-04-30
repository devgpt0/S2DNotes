# ArrayList Notes

## Imports

```java
import java.util.*;
import java.util.ArrayList;
```

`ArrayList` is a resizable-array implementation of the `List` interface.

## Time Complexity (Important Correction)

- `add(e)` at end: `O(1)` amortized
- `add(index, e)`: `O(n)`
- `remove(index)`: `O(n)`
- `remove(value)`: `O(n)` (search + shift)
- `get(index)`: `O(1)`
- `set(index, value)`: `O(1)`
- `contains(value)`: `O(n)`
- `size()`: `O(1)`

Note: inserting/removing in the middle is costly because elements are shifted.

## Ways to Iterate a List

```java
List<String> list = new ArrayList<>();

// 1) for loop
for (int i = 0; i < list.size(); i++) {
    System.out.println(list.get(i));
}

// 2) enhanced for-each
for (String s : list) {
    System.out.println(s);
}

// 3) Iterator
Iterator<String> itr = list.iterator();
while (itr.hasNext()) {
    System.out.println(itr.next());
}
```

## Common ArrayList Methods

```java
List<Integer> list = new ArrayList<>();
list.add(3);
list.add(4);
list.add(1);
list.add(2);
list.add(5);
```

- `add(value)`: append at end (`in-place`, mutates same list)
- `add(index, value)`: insert at position (`in-place`)
- `addFirst(value)`: insert at beginning (`in-place`, Java 21+)
- `addLast(value)`: insert at end (`in-place`, Java 21+)
- `set(index, value)`: replace value (`in-place`, size does not increase)
- `get(index)`: fetch element (`no modification`)
- `getFirst()` / `getLast()`: read first/last element (`no modification`, Java 21+)
- `contains(value)`: returns `true`/`false` (`no modification`)
- `remove(index)`: remove by index (`in-place`)
- `remove(Integer.valueOf(x))`: remove by value (`in-place`)
- `removeFirst()` / `removeLast()`: remove first/last (`in-place`, Java 21+)
- `addAll(otherList)`: append all elements from another collection (`in-place`)
- `removeIf(predicate)`: remove matching elements (`in-place`)
- `replaceAll(op)`: replace each element (`in-place`)
- `reversed()`: returns reverse-order view (`new view`, not copied list, Java 21+)
- `toArray(new Integer[0])`: returns a new array (`new array`)

## Sorting

```java
Collections.sort(list); // ascending
Collections.sort(list, Collections.reverseOrder()); // descending
```

## Immutable vs Mutable Lists

```java
List<String> fixed = List.of("R", "A", "M"); // immutable
```

- `List.of(...)` creates an immutable list.
- `List.copyOf(list)` also creates an immutable copy.
- To modify it, create a new `ArrayList<>(thatList)`.

Convert immutable to mutable and update:

```java
List<String> fixed = List.of("R", "A", "M");    // immutable
List<String> mutable = new ArrayList<>(fixed);  // new mutable copy
mutable.add("Ji");                              // in-place on mutable
mutable.set(0, "Ram");                          // in-place on mutable
```

```java
List<String> copy = List.copyOf(mutable); // immutable copy
```

## Arrays.asList Notes

```java
List<Integer> arrList = Arrays.asList(1, 2, 3, 4, 5);
arrList.set(2, 5); // allowed
```

- Fixed-size list view backed by array.
- You can use `set`, but not `add` or `remove`.

## Declarations

```java
List<Integer> a = new ArrayList<>();
ArrayList<Integer> b = new ArrayList<>();
List c = new ArrayList(); // raw type (avoid in production code)
```

- Prefer `List<Type> var = new ArrayList<>();` for flexibility.

`forEach(...)` only reads/iterates unless your lambda explicitly mutates external state.

```java
ArrayList<Integer> data = new ArrayList<>();
data.ensureCapacity(1000); // pre-allocate to reduce resizes
```

`ensureCapacity(...)` may expand internal capacity, but logical `size` does not change.

## Size vs Capacity

- `size`: number of elements currently stored.
- `capacity`: internal array length (how many can fit before resize).
- Default capacity is usually `10` (on first insertion in modern JDK behavior).
- Growth is roughly `1.5x` when resizing.

```java
ArrayList<Integer> list3 = new ArrayList<>(15); // initial capacity 15
list3.trimToSize(); // reduce capacity to current size
```

Use `trimToSize()` only when you are sure the list will not grow soon, to reduce memory overhead.

Complexity notes for Java first/last methods on `ArrayList`:
- `addFirst` / `removeFirst`: `O(n)` (shifting needed)
- `addLast` / `removeLast`: `O(1)` amortized at end
- `getFirst` / `getLast`: `O(1)`
