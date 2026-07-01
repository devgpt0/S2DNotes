# 05 - Generics and Type Safety

## 1) Why Generics

Generics provide compile-time type safety and remove manual casts.

Concept taught: Generic collection prevents wrong-type insertion.

```java
List<String> names = new ArrayList<>();
names.add("Ram");
System.out.println(names.get(0).toUpperCase());
```

Expected output:

```text
RAM
```

## 2) Raw Type Risk

Concept taught: Raw collections can produce runtime `ClassCastException`.

```java
List raw = new ArrayList();
raw.add("A");
raw.add(10);

try {
    String s = (String) raw.get(1);
    System.out.println(s);
} catch (ClassCastException ex) {
    System.out.println("ClassCastException");
}
```

Expected output:

```text
ClassCastException
```

## 3) Wildcards

- `? extends T`: producer/read-mostly
- `? super T`: consumer/write-friendly for subtype values

PECS: Producer Extends, Consumer Super.

Concept taught: Reading from extends list safely.

```java
List<Integer> ints = List.of(1, 2, 3);
List<? extends Number> nums = ints;
System.out.println(nums.get(0));
```

Expected output:

```text
1
```

## 4) Summary

Use strong generic typing everywhere in collection APIs; avoid raw types in production code.
