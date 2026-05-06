# 02 - ArrayList Core

## 1) Internal Idea

`ArrayList` uses a dynamic array.

- fast random access
- resize when capacity is full

## 2) Complexity

- `get(index)`: `O(1)`
- `set(index, e)`: `O(1)`
- `add(e)` at end: `O(1)` amortized
- `add(index, e)`: `O(n)`
- `remove(index)`: `O(n)`
- `remove(value)`: `O(n)` (search + shift)
- `contains`: `O(n)`
- `size()`: `O(1)`

## 3) Capacity vs Size

- `size`: number of elements present
- `capacity`: internal array length
- growth is typically around `1.5x`

```java
ArrayList<Integer> list = new ArrayList<>(100);
list.ensureCapacity(200);
list.trimToSize();
```

Java 21 list methods also available:

```java
list.addFirst(10);   // O(n)
list.addLast(20);    // O(1) amortized
int first = list.getFirst(); // O(1)
int last = list.getLast();   // O(1)
list.removeFirst();  // O(n)
list.removeLast();   // O(1)
```

## 4) When To Use

- frequent reads by index
- append-heavy workloads
- memory-efficient compared to linked nodes

## 5) Pitfall

Inserting/removing frequently at start or middle is expensive due to shifting.

## 6) Useful Extra Notes

`Arrays.asList` is fixed-size view:

```java
List<Integer> a = Arrays.asList(1, 2, 3);
a.set(0, 9); // allowed
// a.add(4); // UnsupportedOperationException
```

`List.of(...)` is immutable.

`List.copyOf(list)` creates immutable copy.

Convert immutable to mutable:

```java
List<String> fixed = List.of("R", "A", "M");
List<String> mutable = new ArrayList<>(fixed);
mutable.add("Ji");
mutable.set(0, "Ram");
List<String> copy = List.copyOf(mutable);
```

## 7) Method Behavior (In-Place vs Read vs New Object)

- in-place: `add`, `add(index, e)`, `addFirst`, `addLast`, `set`, `remove`, `removeIf`, `replaceAll`, `addAll`
- read/no structural modification: `get`, `getFirst`, `getLast`, `contains`, `size`, `isEmpty`
- new object/view: `toArray(...)` (new array), `reversed()` (view)

Overload reminder:

```java
list.remove(2);                  // remove by index
list.remove(Integer.valueOf(2)); // remove by value
```

## 8) Important Practical Notes

- default internal capacity is usually `10` after first insertion in modern JDK behavior
- `ensureCapacity(...)` may increase capacity but does not change logical size
- use `trimToSize()` only when you are sure list will not grow soon
- `forEach(...)` reads/iterates unless lambda mutates external state

## 9) Declarations

```java
List<Integer> a = new ArrayList<>();
ArrayList<Integer> b = new ArrayList<>();
List c = new ArrayList(); // raw type: avoid in production
```
