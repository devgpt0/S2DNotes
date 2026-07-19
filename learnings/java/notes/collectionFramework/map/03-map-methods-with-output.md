# 03 - Map Methods With Output (Complete)

This chapter is a method lab: each snippet teaches one API family with expected output.

## 1) `put` and Overwrite Return Value

Concept taught: `put` returns old value for existing key, else `null`.

```java
Map<String, Integer> map = new HashMap<>();
System.out.println(map.put("Ram", 80));
System.out.println(map.put("Sita", 92));
System.out.println(map.put("Ram", 95));
System.out.println(map);
```

Expected output (order may vary):

```text
null
null
80
{Ram=95, Sita=92}
```

## 2) Read Methods

Concept taught: Difference between `get` and `getOrDefault`.

```java
Map<String, Integer> map = Map.of("A", 10, "B", 20);
System.out.println(map.get("A"));
System.out.println(map.get("Z"));
System.out.println(map.getOrDefault("Z", 0));
```

Expected output:

```text
10
null
0
```

## 3) Existence Checks

Concept taught: `containsKey` is exact key existence; `containsValue` scans values.

```java
Map<String, Integer> map = new HashMap<>();
map.put("x", 1);
map.put("y", 2);

System.out.println(map.containsKey("x"));
System.out.println(map.containsValue(2));
```

Expected output:

```text
true
true
```

## 4) `putIfAbsent`

Concept taught: Insert only when key missing.

```java
Map<String, Integer> map = new HashMap<>();
map.put("A", 1);

System.out.println(map.putIfAbsent("A", 999));
System.out.println(map.putIfAbsent("B", 2));
System.out.println(map);
```

Expected output:

```text
1
null
{A=1, B=2}
```

## 5) `replace` Variants

Concept taught: unconditional and conditional replace.

```java
Map<String, Integer> map = new HashMap<>();
map.put("A", 1);

System.out.println(map.replace("A", 10));
System.out.println(map.replace("A", 1, 99));
System.out.println(map.replace("A", 10, 99));
System.out.println(map);
```

Expected output:

```text
1
false
true
{A=99}
```

## 6) `remove` Variants

Concept taught: remove by key and remove by key+value.

```java
Map<String, Integer> map = new HashMap<>();
map.put("A", 1);
map.put("B", 2);

System.out.println(map.remove("A"));
System.out.println(map.remove("B", 999));
System.out.println(map.remove("B", 2));
System.out.println(map);
```

Expected output:

```text
1
false
true
{}
```

## 7) `computeIfAbsent`

Concept taught: lazy value creation only when key absent.

```java
Map<String, List<String>> groups = new HashMap<>();
groups.computeIfAbsent("teamA", k -> new ArrayList<>()).add("Ram");
groups.computeIfAbsent("teamA", k -> new ArrayList<>()).add("Sita");

System.out.println(groups);
```

Expected output:

```text
{teamA=[Ram, Sita]}
```

## 8) `computeIfPresent`

Concept taught: update only if key exists.

```java
Map<String, Integer> map = new HashMap<>();
map.put("count", 5);
map.computeIfPresent("count", (k, v) -> v + 1);
map.computeIfPresent("missing", (k, v) -> 1);

System.out.println(map);
```

Expected output:

```text
{count=6}
```

## 9) `compute`

Concept taught: full control for insert/update/delete based on old value.

```java
Map<String, Integer> map = new HashMap<>();
map.compute("x", (k, v) -> v == null ? 1 : v + 1);
map.compute("x", (k, v) -> v == null ? 1 : v + 1);
map.compute("x", (k, v) -> null); // removes key

System.out.println(map);
```

Expected output:

```text
{}
```

## 10) `merge`

Concept taught: best API for counters and aggregations.

```java
Map<String, Integer> freq = new HashMap<>();
freq.merge("java", 1, Integer::sum);
freq.merge("java", 1, Integer::sum);
freq.merge("python", 1, Integer::sum);

System.out.println(freq);
```

Expected output:

```text
{python=1, java=2}
```

## 11) Views: `keySet`, `values`, `entrySet`

Concept taught: backed views reflect map changes.

```java
Map<String, Integer> map = new LinkedHashMap<>();
map.put("A", 1);
map.put("B", 2);

Set<String> keys = map.keySet();
Collection<Integer> values = map.values();
Set<Map.Entry<String, Integer>> entries = map.entrySet();

System.out.println(keys);
System.out.println(values);
System.out.println(entries);

map.put("C", 3);
System.out.println(keys);
```

Expected output:

```text
[A, B]
[1, 2]
[A=1, B=2]
[A, B, C]
```

## 12) `replaceAll`

Concept taught: bulk value transformation.

```java
Map<String, Integer> map = new HashMap<>();
map.put("A", 10);
map.put("B", 20);
map.replaceAll((k, v) -> v + 5);
System.out.println(map);
```

Possible output:

```text
{A=15, B=25}
```

## 13) `forEach`

Concept taught: concise iteration over entries.

```java
Map<String, Integer> map = new LinkedHashMap<>();
map.put("Ram", 95);
map.put("Sita", 92);
map.forEach((k, v) -> System.out.println(k + " -> " + v));
```

Expected output:

```text
Ram -> 95
Sita -> 92
```

## 14) Method Family Recap

- read/query: `get`, `getOrDefault`, `containsKey`, `containsValue`, `size`, `isEmpty`
- write: `put`, `putIfAbsent`, `replace`, `remove`, `clear`, `replaceAll`
- compute/update: `computeIfAbsent`, `computeIfPresent`, `compute`, `merge`
- traversal/views: `forEach`, `keySet`, `values`, `entrySet`

## 15) Summary

If you master `put/get/remove` + `merge` + `computeIfAbsent`, you can solve most real map problems cleanly.
