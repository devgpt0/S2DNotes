# 13 - Comparable vs Comparator (List Sorting Expert)

## 1) Core Difference

- `Comparable<T>` defines natural/default ordering inside class.
- `Comparator<T>` defines external/custom ordering logic.

| Feature | Comparable | Comparator |
|---|---|---|
| Package | `java.lang` | `java.util` |
| Method | `compareTo(T other)` | `compare(T a, T b)` |
| Sorting API | `Collections.sort(list)` | `list.sort(cmp)` |
| Number of possible orderings | one natural | many custom |
| Logic location | model class | separate strategy object |

## 2) `Comparable` Example (Natural Order)

Concept taught: Demonstrates 2) `Comparable` Example (Natural Order) in practice.

```java
class Student implements Comparable<Student> {
    private final String name;
    private final int rollNo;

    Student(String name, int rollNo) {
        this.name = name;
        this.rollNo = rollNo;
    }

    String getName() { return name; }
    int getRollNo() { return rollNo; }

    @Override
    public int compareTo(Student o) {
        int byRoll = Integer.compare(this.rollNo, o.rollNo);
        if (byRoll != 0) return byRoll;
        return this.name.compareTo(o.name);
    }

    @Override
    public String toString() {
        return name + "(" + rollNo + ")";
    }
}

List<Student> list = new ArrayList<>(List.of(
    new Student("Amit", 3),
    new Student("Riya", 1),
    new Student("Aman", 1)
));

Collections.sort(list);
System.out.println(list);
```

Expected output:

```text
[Aman(1), Riya(1), Amit(3)]
```

## 3) `Comparator` Example (Custom Order)

Concept taught: Demonstrates 3) `Comparator` Example (Custom Order) in practice.

```java
List<Student> list = new ArrayList<>(List.of(
    new Student("Amit", 3),
    new Student("Riya", 1),
    new Student("Aman", 1)
));

list.sort(Comparator.comparing(Student::getName));
System.out.println(list);

list.sort(Comparator.comparingInt(Student::getRollNo).reversed());
System.out.println(list);
```

Expected output:

```text
[Aman(1), Amit(3), Riya(1)]
[Amit(3), Aman(1), Riya(1)]
```

## 4) Comparator Chaining Patterns

Concept taught: Demonstrates 4) Comparator Chaining Patterns in practice.

```java
Comparator<Student> cmp = Comparator
    .comparingInt(Student::getRollNo)
    .thenComparing(Student::getName);

list.sort(cmp);
System.out.println(list);
```

Expected output:

```text
[Aman(1), Riya(1), Amit(3)]
```

Reverse only one key:

Concept taught: Demonstrates 4) Comparator Chaining Patterns in practice.

```java
Comparator<Student> cmp2 = Comparator
    .comparing(Student::getName)
    .thenComparing(Comparator.comparingInt(Student::getRollNo).reversed());
```

## 5) Null-Safe Comparator

Concept taught: Demonstrates 5) Null-Safe Comparator in practice.

```java
List<String> names = new ArrayList<>(Arrays.asList("ram", null, "aman"));
names.sort(Comparator.nullsLast(String.CASE_INSENSITIVE_ORDER));
System.out.println(names);
```

Expected output:

```text
[aman, ram, null]
```

## 6) Compare Contract Rules (Very Important)

Good comparator must be:

- anti-symmetric: `sign(compare(a,b)) == -sign(compare(b,a))`
- transitive
- consistent on repeated calls
- preferably consistent with `equals` for sorted set/map behavior

Broken comparators cause unstable sorting and collection anomalies.

## 7) Avoid Subtraction Compare

Bad:

Concept taught: Demonstrates 7) Avoid Subtraction Compare in practice.

```java
Comparator<Integer> bad = (a, b) -> a - b;
```

Risk: integer overflow.

Good:

Concept taught: Demonstrates 7) Avoid Subtraction Compare in practice.

```java
Comparator<Integer> good = Integer::compare;
```

## 8) APIs You Must Remember

Concept taught: Demonstrates 8) APIs You Must Remember in practice.

```java
Collections.sort(list);      // natural order via Comparable
list.sort(null);             // same meaning
list.sort(customComparator); // custom order
Collections.sort(list, customComparator);
```

## 9) `equals` / `hashCode` and Ordering

Sorting uses comparator/compareTo, not hash code.
But consistency matters when objects are also used in sorted sets/maps.

Guideline:

- if two objects are considered equal in business logic, comparator should usually return `0` for them

## 10) Common Mistakes

- implementing `compare` instead of `compareTo` in `Comparable`
- forgetting tie-breakers (`thenComparing`)
- writing inconsistent comparator logic
- using mutable fields for sorting keys and mutating after insertion into sorted collections
- not handling nulls in comparator when null possible

## 11) Interview-Ready One-Liners

- `Comparable` = default order, `Comparator` = custom order.
- For multi-field sort, chain comparators.
- Use `Integer.compare`, not subtraction.
- Binary search must use same comparator as sort.

## 12) Practice Tasks

1. Define `Comparable<Employee>` by employee id.
2. Sort by salary desc then name asc using `Comparator`.
3. Add null-safe name sorting.
4. Build reusable comparator constants (`BY_NAME`, `BY_SALARY_DESC`).
5. Write unit tests validating comparator transitivity.

## 13) Summary

Use `Comparable` for model-level natural order and `Comparator` for business-level sorting strategies. Strong comparator design is critical for correct list sorting and sorted collections.
