# Comparators and Comparables Notes

## Why This Topic Matters
Sorting is one of the most common interview and production tasks.
In Java, sorting custom objects is mainly done in two ways:

- `Comparable<T>`: default (natural) ordering inside the class
- `Comparator<T>`: custom/external ordering outside the class

Use both together in real projects:

- Keep one sensible default order in `Comparable`
- Build many use-case-specific orders using `Comparator`

## Quick Difference: Comparable vs Comparator

| Feature | Comparable | Comparator |
|---|---|---|
| Package | `java.lang` | `java.util` |
| Method | `compareTo(T o)` | `compare(T a, T b)` |
| Where logic lives | Inside model class | Outside model class |
| Purpose | Natural/default order | Custom/multiple orders |
| How used | `Collections.sort(list)` / `list.sort(null)` | `list.sort(comparator)` |

## Fixing Your First Snippet (Important Corrections)

You had this pattern:

```java
List<Student> ls = new Student();
ls.add("Ad",03);
```

Problems:

- `new Student()` is a single object, not a list
- `ls.add("Ad",03)` is invalid for `List<Student>`
- `list.sort(null);` variable name mismatch (`list` vs `ls`)

Correct version:

```java
import java.util.*;

public class ComparableDemo {
    static class Student implements Comparable<Student> {
        private final String name;
        private final int rollNo;

        Student(String name, int rollNo) {
            this.name = name;
            this.rollNo = rollNo;
        }

        public String getName() {
            return name;
        }

        public int getRollNo() {
            return rollNo;
        }

        @Override
        public int compareTo(Student other) {
            // Natural order: by roll number ascending
            return Integer.compare(this.rollNo, other.rollNo);
        }

        @Override
        public String toString() {
            return name + "(" + rollNo + ")";
        }
    }

    public static void main(String[] args) {
        List<Student> ls = new ArrayList<>();
        ls.add(new Student("Ad", 3));
        ls.add(new Student("Bod", 7));
        ls.add(new Student("Ad", 1));
        ls.add(new Student("Bod", 2));

        // Uses Comparable (natural order)
        ls.sort(null);
        System.out.println(ls);
    }
}
```

## Comparable: Complete Guide

### Rule
Implement `Comparable<T>` when your class has one obvious default order.

### Method Contract

```java
int compareTo(T o)
```

Return value meaning:

- `< 0`: this object comes before `o`
- `0`: both are equal for ordering
- `> 0`: this object comes after `o`

### Correct `Students` Class (based on your file)

```java
import java.util.Objects;

public class Students implements Comparable<Students> {
    private String name;
    private Integer rollNo;

    public Students(String name, Integer rollNo) {
        this.name = name;
        this.rollNo = rollNo;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Integer getRollNo() {
        return rollNo;
    }

    public void setRollNo(Integer rollNo) {
        this.rollNo = rollNo;
    }

    @Override
    public String toString() {
        return "Students{name='" + name + "', rollNo=" + rollNo + "}";
    }

    @Override
    public int compareTo(Students o) {
        // Natural order: roll number ascending, then name ascending
        int byRoll = Integer.compare(this.rollNo, o.rollNo);
        if (byRoll != 0) {
            return byRoll;
        }
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
}
```

### Why Your `toString()` Needed Fix
You had `return Object.hash(name,RollNo);` which is wrong because:

- `Object.hash(...)` is invalid (correct utility is `Objects.hash(...)`)
- `toString()` must return `String`, not hash `int`

## Comparator: Complete Guide

Use `Comparator<T>` when:

- You cannot modify model class
- You need multiple sort orders
- You need per-screen/per-feature sorting

### Basic Examples

```java
import java.util.*;

public class ComparatorBasics {
    public static void main(String[] args) {
        List<Integer> nums = new ArrayList<>(List.of(3, 6, 1, 2, 5));

        // Ascending
        nums.sort(Integer::compareTo);

        // Descending
        nums.sort((a, b) -> Integer.compare(b, a));

        System.out.println(nums);
    }
}
```

### Student Comparator (from your style, simplified)

```java
import java.util.*;

public class ComparatorsMethods {
    public static class Student {
        private final String name;
        private final float gpa;

        public Student(String name, float gpa) {
            this.name = name;
            this.gpa = gpa;
        }

        public String getName() {
            return name;
        }

        public float getGpa() {
            return gpa;
        }

        @Override
        public String toString() {
            return name + ":" + gpa;
        }
    }

    public static void main(String[] args) {
        List<Student> list = new ArrayList<>();
        list.add(new Student("Adarsh", 8.5f));
        list.add(new Student("Raj", 9.5f));
        list.add(new Student("Rajiv", 7.5f));
        list.add(new Student("Raja", 6.5f));
        list.add(new Student("Rama", 5.5f));

        // GPA ascending, then name ascending
        list.sort(
            Comparator.comparingDouble(Student::getGpa)
                      .thenComparing(Student::getName)
        );

        list.forEach(System.out::println);
    }
}
```

## Best Practice: Avoid `o1 - o2` Pattern

Risky:

```java
(a, b) -> a - b
```

Better:

```java
Integer.compare(a, b)
Long.compare(a, b)
Float.compare(a, b)
Double.compare(a, b)
```

Reason: subtraction can overflow for large values.

## Comparator Utility Methods You Should Know

```java
Comparator.comparing(Student::getName)
Comparator.comparingInt(Student::getAge)
Comparator.comparingDouble(Student::getGpa)
Comparator.naturalOrder()
Comparator.reverseOrder()
Comparator.nullsFirst(Comparator.naturalOrder())
Comparator.nullsLast(Comparator.naturalOrder())
```

Chaining:

```java
Comparator<Students> cmp = Comparator
    .comparing(Students::getName)
    .thenComparing(Students::getRollNo);
```

Reverse whole chain:

```java
cmp = cmp.reversed();
```

Reverse only one key:

```java
Comparator<Students> cmp2 = Comparator
    .comparing(Students::getName)
    .thenComparing(Comparator.comparing(Students::getRollNo).reversed());
```

## Sorting APIs

```java
Collections.sort(list);              // Uses Comparable
Collections.sort(list, comparator);  // Uses Comparator
list.sort(null);                     // Uses Comparable
list.sort(comparator);               // Uses Comparator
```

## Comparator Contract (Very Important)
Good comparator should be:

- Anti-symmetric
- Transitive
- Consistent for repeated calls
- Preferably consistent with `equals` for sorted sets/maps

Bad comparators can produce unpredictable order and bugs in `TreeSet`/`TreeMap`.

## Comparable + Comparator Together (Real Project Pattern)

```java
// In model class: natural order
@Override
public int compareTo(Students o) {
    return Integer.compare(this.rollNo, o.rollNo);
}

// In service/controller: custom order for specific view
list.sort(Comparator.comparing(Students::getName));
```

## Interview-Ready Talking Points

- `Comparable` = default order in class; single natural order
- `Comparator` = external custom order; unlimited strategies
- Use `Integer.compare`-style methods, not subtraction compare
- Chain comparators with `thenComparing`
- Use null-safe helpers for nullable fields
- Ensure comparator contract to avoid sorted-collection bugs

## Common Mistakes Checklist

- Creating list incorrectly (`List<T> list = new T()`)
- Wrong method name (`compare` instead of `compareTo` in `Comparable`)
- Returning wrong type in `toString()`
- Using subtraction for comparison on large integers
- Forgetting tie-breaker in comparator
- Inconsistent comparator causing unstable business behavior

## Practice Tasks

1. Implement `Comparable<Students>` by `rollNo` ascending.
2. Sort same list by `name` ascending using `Comparator`.
3. Sort by `name` descending, then `rollNo` ascending.
4. Add null-safe sorting for names.
5. Build two comparator constants and reuse across classes.
