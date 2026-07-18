# 07 - Collectors

## Beginner Meaning

A collector gathers the values coming out of a stream. Think of it as the final container or summary: a list, set, map, joined string, group, count, or numeric statistics.

## 1) Lists, Sets, and Specific Collections

```java
List<String> list = Stream.of("A", "B").toList();
Set<String> set = Stream.of("A", "B", "A").collect(Collectors.toSet());
TreeSet<String> sorted = Stream.of("B", "A").collect(Collectors.toCollection(TreeSet::new));
System.out.println(list);
System.out.println(set.size());
System.out.println(sorted);
// Output:
// [A, B]
// 2
// [A, B]
```

`Stream.toList()` returns an unmodifiable list. Collector implementation types are not guaranteed unless you request one.

## 2) Joining

```java
String joined = Stream.of("Java", "Spring")
        .collect(Collectors.joining(", ", "[", "]"));
System.out.println(joined);
// Output: [Java, Spring]
```

## 3) Maps and Duplicate Keys

```java
record Product(long id, String name) {}

Map<Long, String> products = Stream.of(new Product(1, "Book"), new Product(2, "Pen"))
        .collect(Collectors.toMap(Product::id, Product::name));
System.out.println(products.get(2L));
// Output: Pen
```

Duplicate keys throw `IllegalStateException` unless an explicit merge rule is supplied.

```java
Map<String, Integer> totals = Stream.of("A:2", "A:3")
        .collect(Collectors.toMap(
                value -> value.substring(0, 1),
                value -> Integer.parseInt(value.substring(2)),
                Integer::sum));
System.out.println(totals);
// Output: {A=5}
```

## 4) Summaries

```java
IntSummaryStatistics stats = Stream.of(10, 20, 30)
        .collect(Collectors.summarizingInt(Integer::intValue));
System.out.println(stats.getCount() + ", " + stats.getSum() + ", " + stats.getMax());
// Output: 3, 60, 30
```
