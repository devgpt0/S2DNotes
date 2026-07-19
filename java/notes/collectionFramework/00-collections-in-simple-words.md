# Java Collections in Simple Words

Read this before List, Set, Map, Queue, lambda, and stream details.

## Why Do Collections Exist?

A variable holds one value. A collection holds a group of values.

```java
List<String> courses = new ArrayList<>();
courses.add("Java");
courses.add("SQL");
System.out.println(courses);
// Output: [Java, SQL]
```

## Choose by the Question You Need to Answer

| Need | Start with | Simple meaning |
|---|---|---|
| ordered values, duplicates allowed | `List` | numbered sequence |
| unique values | `Set` | membership group |
| find a value by a key | `Map` | key-to-value lookup |
| process in waiting order | `Queue` | next item to handle |
| add/remove at both ends | `Deque` | double-ended queue |

Do not choose by habit. Choose from the behavior the program needs.

## List

```java
List<String> names = new ArrayList<>();
names.add("Asha");
names.add("Ravi");
names.add("Asha");
System.out.println(names.get(1));
System.out.println(names);
// Output:
// Ravi
// [Asha, Ravi, Asha]
```

A list keeps order and allows duplicates. Positions start at zero.

## Set

```java
Set<String> skills = new HashSet<>();
skills.add("Java");
skills.add("Java");
System.out.println(skills.size());
// Output: 1
```

A set keeps unique values. A `HashSet` does not promise display order.

## Map

```java
Map<String, Integer> scores = new HashMap<>();
scores.put("Asha", 90);
scores.put("Ravi", 85);
System.out.println(scores.get("Asha"));
// Output: 90
```

A map connects each unique key to one value. It is not a subtype of `Collection` because it stores entries, not single elements.

## Queue

```java
Queue<String> jobs = new ArrayDeque<>();
jobs.add("email");
jobs.add("report");
System.out.println(jobs.remove());
System.out.println(jobs);
// Output:
// email
// [report]
```

A queue normally removes the item that has waited longest.

## Interface and Implementation

```java
List<String> names = new ArrayList<>();
```

- `List`: behavior the rest of the code needs
- `ArrayList`: object that provides that behavior

Declaring the useful interface keeps callers focused on the required operations.

## Generics

`List<String>` means only `String` values belong in this list.

```java
List<String> names = new ArrayList<>();
// names.add(10); // compile-time error
```

## Equality Matters

Sets and map keys need to decide when two objects represent the same value. For custom value objects, `equals` and `hashCode` must agree.

Read that chapter before placing mutable custom objects in a hash-based set or using them as map keys.

## Mutable vs Unmodifiable

```java
List<String> fixedList = List.of("Java", "SQL");
System.out.println(fixedList);
// fixedList.add("HTML"); // UnsupportedOperationException
```

`List.of` does not allow element changes. A final variable alone does not make a mutable list unmodifiable.

## Performance in Plain Language

- `ArrayList.get(index)` is usually fast
- searching a list is usually linear
- `HashSet.contains(value)` and `HashMap.get(key)` are usually constant-time on average with good keys
- sorted collections do extra work to maintain order

Correct behavior comes before small performance differences.

## Thread Safety

Most common mutable collections are not safe for shared writes from several threads. Prefer one owner, immutable snapshots, or a collection designed for the real access pattern.

## Beginner to Expert Path

1. **Beginner:** add, read, update, remove, iterate, and print.
2. **Developer:** choose by required behavior and mutability.
3. **Senior:** understand equality, views, complexity, and API ownership.
4. **Expert:** reason about memory, concurrency, ordering, and workload tradeoffs.

Given “unique email addresses,” choose a `Set`. Given “course by ID,” choose a `Map`. Given “tasks in display order,” choose a `List`. If you can explain why, continue to the focused chapters.
