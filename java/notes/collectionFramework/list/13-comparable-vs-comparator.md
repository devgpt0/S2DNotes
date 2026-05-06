# 13 - Comparable vs Comparator (List Sorting Expert)

## 1) Core Difference

- `Comparable<T>`: default order inside class (`compareTo`)
- `Comparator<T>`: custom external order (`compare`)

Quick table:

| Feature | Comparable | Comparator |
|---|---|---|
| Package | `java.lang` | `java.util` |
| Method | `compareTo(T o)` | `compare(T a, T b)` |
| Logic location | inside model class | outside model class |
| Purpose | natural/default order | custom/multiple orders |
| Usage | `Collections.sort(list)` / `list.sort(null)` | `list.sort(comparator)` |

## 2) When To Use

- use `Comparable` for one natural order
- use `Comparator` for multiple business-specific orders

Real-project pattern:

- keep one sensible default in `Comparable`
- build use-case-specific orders with `Comparator`

## 3) Comparable Example

```java
class Student implements Comparable<Student> {
    private final String name;
    private final int rollNo;

    Student(String name, int rollNo) {
        this.name = name;
        this.rollNo = rollNo;
    }

    public String getName() { return name; }
    public int getRollNo() { return rollNo; }

    @Override
    public int compareTo(Student o) {
        int byRoll = Integer.compare(this.rollNo, o.rollNo);
        if (byRoll != 0) return byRoll;
        return this.name.compareTo(o.name);
    }
}
```

Full model example with `equals/hashCode`:

```java
import java.util.Objects;

class Students implements Comparable<Students> {
    private String name;
    private Integer rollNo;

    Students(String name, Integer rollNo) {
        this.name = name;
        this.rollNo = rollNo;
    }

    public String getName() { return name; }
    public Integer getRollNo() { return rollNo; }

    @Override
    public int compareTo(Students o) {
        int byRoll = Integer.compare(this.rollNo, o.rollNo);
        if (byRoll != 0) return byRoll;
        return this.name.compareTo(o.name);
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (!(obj instanceof Students other)) return false;
        return Objects.equals(name, other.name) && Objects.equals(rollNo, other.rollNo);
    }

    @Override
    public int hashCode() {
        return Objects.hash(name, rollNo);
    }

    @Override
    public String toString() {
        return "Students{name='" + name + "', rollNo=" + rollNo + "}";
    }
}
```

`compareTo` return contract:

- `< 0`: current object comes before other
- `0`: equal in ordering
- `> 0`: current object comes after other

Correct `toString` note:

- `toString()` must return `String`
- `Objects.hash(...)` is for hash code, not string output

## 4) Comparator Example

```java
list.sort(
    Comparator.comparingInt(Student::getRollNo)
              .thenComparing(Student::getName)
);
```

Reverse:

```java
list.sort(Comparator.comparingInt(Student::getRollNo).reversed());
```

More utility methods:

```java
Comparator.comparing(Student::getName);
Comparator.comparingInt(Student::getRollNo);
Comparator.comparingDouble(Student::getGpa);
Comparator.naturalOrder();
Comparator.reverseOrder();
Comparator.nullsFirst(Comparator.naturalOrder());
Comparator.nullsLast(Comparator.naturalOrder());
```

Reverse only one key:

```java
Comparator<Student> cmp = Comparator
    .comparing(Student::getName)
    .thenComparing(Comparator.comparingInt(Student::getRollNo).reversed());
```

## 5) Important Best Practices

- avoid subtraction compare: `(a, b) -> a - b`
- use `Integer.compare`, `Long.compare`, etc.
- for nullable fields use `Comparator.nullsFirst/nullsLast`

Better numeric compare helpers:

```java
Integer.compare(a, b);
Long.compare(a, b);
Float.compare(a, b);
Double.compare(a, b);
```

## 6) APIs You Should Remember

```java
Collections.sort(list);            // Comparable
list.sort(null);                   // Comparable
Collections.sort(list, cmp);       // Comparator
list.sort(cmp);                    // Comparator
```

Also valid:

```java
Collections.sort(list, cmp);
```

## 7) Interview Points

- `Comparable` gives one natural ordering
- `Comparator` enables unlimited sorting strategies
- tie-breakers via `thenComparing`
- comparator contract quality matters for `TreeSet`/`TreeMap`

Comparator contract essentials:

- anti-symmetric
- transitive
- consistent on repeated calls
- preferably consistent with `equals` for sorted set/map behavior

## 8) Common Mistakes

- wrong list creation: `List<T> list = new T()`
- wrong method name: using `compare` instead of `compareTo` in `Comparable`
- variable mismatch while sorting (for example calling `list.sort(...)` when variable is `ls`)
- subtraction compare risk on large values
- missing tie-breaker for stable business ordering
- inconsistent comparator leading to unstable sorted collection behavior

## 9) Corrected Beginner Snippet

```java
List<Student> ls = new ArrayList<>();
ls.add(new Student("Ad", 3));
ls.add(new Student("Bod", 7));
ls.add(new Student("Ad", 1));
ls.sort(null); // natural order via Comparable
```

## 10) Practice Tasks

1. Implement `Comparable<Student>` by `rollNo` ascending.
2. Sort same list by `name` ascending using `Comparator`.
3. Sort by `name` descending, then `rollNo` ascending.
4. Add null-safe sorting for names.
5. Build reusable comparator constants.
