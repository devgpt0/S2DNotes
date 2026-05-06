# 06 - List Iteration Patterns

## 1) For Loop (Index Based)

```java
for (int i = 0; i < list.size(); i++) {
    System.out.println(list.get(i));
}
```

Good when index is required.

## 2) Enhanced For Loop

```java
for (String s : list) {
    System.out.println(s);
}
```

Simple read-only iteration.

## 3) Iterator

```java
Iterator<String> it = list.iterator();
while (it.hasNext()) {
    String s = it.next();
    if (s.isBlank()) it.remove(); // safe removal
}
```

## 4) ListIterator

Supports bidirectional traversal and in-place add/set.

```java
ListIterator<String> li = list.listIterator();
while (li.hasNext()) {
    String v = li.next();
    if (v.equals("a")) li.set("A");
}
```

## 5) `forEach`

```java
list.forEach(System.out::println);
```

Avoid mutating same list structure inside `forEach`.

