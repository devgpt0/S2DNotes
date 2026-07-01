# 10 - Specialized Maps and Immutability (Complete)

## 1) `EnumMap`

Use when keys are from one enum type.

- compact and fast
- iteration follows enum declaration order

Concept taught: Enum-key map with predictable order.

```java
enum Status { NEW, IN_PROGRESS, DONE }
Map<Status, Integer> count = new EnumMap<>(Status.class);
count.put(Status.NEW, 5);
count.put(Status.DONE, 2);
System.out.println(count);
```

Expected output:

```text
{NEW=5, DONE=2}
```

## 2) `WeakHashMap`

Stores keys as weak references.

- if key has no strong reference elsewhere, entry can be GC-removed
- cleanup timing is nondeterministic

Concept taught: Entry lifecycle tied to key reachability.

```java
Map<Object, String> map = new WeakHashMap<>();
Object key = new Object();
map.put(key, "meta");
System.out.println("before gc=" + map.size());
key = null;
System.gc();
System.out.println("after gc=" + map.size());
```

Possible output:

```text
before gc=1
after gc=0
```

## 3) `IdentityHashMap`

Compares keys with `==` not `equals`.

Concept taught: Identity semantics can treat equal-looking objects as different keys.

```java
Map<String, Integer> map = new IdentityHashMap<>();
String a = new String("x");
String b = new String("x");
map.put(a, 1);
map.put(b, 2);
System.out.println(map.size());
```

Expected output:

```text
2
```

## 4) `Hashtable` (Legacy)

- synchronized legacy hash map
- no null key/value
- usually replaced by `ConcurrentHashMap`

Concept taught: Basic `Hashtable` usage and null restrictions.

```java
Map<Integer, String> table = new Hashtable<>();
table.put(1, "A");
System.out.println(table);
// table.put(null, "X"); // NullPointerException
```

Expected output:

```text
{1=A}
```

## 5) Immutable Maps (`Map.of`, `Map.copyOf`)

Concept taught: Create immutable map safely.

```java
Map<String, Integer> a = Map.of("A", 1, "B", 2);
Map<String, Integer> b = Map.copyOf(a);
System.out.println(a);
System.out.println(b);
// b.put("C", 3); // UnsupportedOperationException
```

Expected output:

```text
{A=1, B=2}
{A=1, B=2}
```

Rules:

- null keys/values rejected
- duplicate keys rejected at creation

## 6) Unmodifiable View vs Immutable Snapshot

Concept taught: `Collections.unmodifiableMap` reflects source changes; `Map.copyOf` does not.

```java
Map<String, Integer> src = new HashMap<>();
src.put("A", 1);
Map<String, Integer> view = Collections.unmodifiableMap(src);
Map<String, Integer> snap = Map.copyOf(src);

src.put("B", 2);
System.out.println(view);
System.out.println(snap);
```

Expected output:

```text
{A=1, B=2}
{A=1}
```

## 7) When to Choose What

- enum keys -> `EnumMap`
- object-lifecycle metadata -> `WeakHashMap`
- identity-based framework internals -> `IdentityHashMap`
- immutable constants/defensive returns -> `Map.of` / `Map.copyOf`
- legacy APIs only -> `Hashtable`

## 8) Summary

Specialized maps solve very specific problems. Use them intentionally, not as defaults.
