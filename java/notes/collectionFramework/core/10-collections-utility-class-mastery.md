# 10 - Collections Utility Class Mastery

`java.util.Collections` provides useful algorithms and wrappers.

## 1) Sorting and Reversing

Concept taught: Utility algorithms on list data.

```java
List<Integer> nums = new ArrayList<>(List.of(4, 1, 3, 2));
Collections.sort(nums);
Collections.reverse(nums);
System.out.println(nums);
```

Expected output:

```text
[4, 3, 2, 1]
```

## 2) Binary Search

Concept taught: `binarySearch` requires sorted list.

```java
List<Integer> nums = new ArrayList<>(List.of(10, 20, 30, 40));
int idx = Collections.binarySearch(nums, 30);
System.out.println(idx);
```

Expected output:

```text
2
```

## 3) Unmodifiable Wrappers

Concept taught: Read-only view wrappers.

```java
List<String> src = new ArrayList<>(List.of("A", "B"));
List<String> ro = Collections.unmodifiableList(src);
src.add("C");
System.out.println(ro);
```

Expected output:

```text
[A, B, C]
```

## 4) Synchronized Wrappers

Concept taught: Wrapper-based synchronization for legacy adaptation.

```java
List<Integer> syncList = Collections.synchronizedList(new ArrayList<>());
syncList.add(1);
System.out.println(syncList);
```

Expected output:

```text
[1]
```

## 5) Summary

`Collections` utilities help with algorithms and wrappers without changing data structure classes.
