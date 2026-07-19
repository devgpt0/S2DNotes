# 07 - Sorting, Searching, and Binary Search (Complete)

## 1) Sorting Fundamentals

Java list sorting is stable (equal elements keep original relative order) for standard object sorting.

Common APIs:

- `Collections.sort(list)`
- `list.sort(comparator)`

## 2) Natural Order Sort

Concept taught: Demonstrates 2) Natural Order Sort in practice.

```java
List<Integer> nums = new ArrayList<>(List.of(40, 10, 30, 20));
Collections.sort(nums);
System.out.println(nums);
```

Expected output:

```text
[10, 20, 30, 40]
```

Equivalent modern style:

Concept taught: Demonstrates 2) Natural Order Sort in practice.

```java
nums.sort(Comparator.naturalOrder());
```

## 3) Descending and Custom Sort

Concept taught: Demonstrates 3) Descending and Custom Sort in practice.

```java
List<Integer> nums = new ArrayList<>(List.of(40, 10, 30, 20));
nums.sort(Comparator.reverseOrder());
System.out.println(nums);
```

Expected output:

```text
[40, 30, 20, 10]
```

For strings (case-insensitive):

Concept taught: Demonstrates 3) Descending and Custom Sort in practice.

```java
List<String> names = new ArrayList<>(List.of("ram", "Aman", "shyam"));
names.sort(String.CASE_INSENSITIVE_ORDER);
System.out.println(names);
```

Output:

```text
[Aman, ram, shyam]
```

## 4) Sorting Objects with Comparator Chains

Concept taught: Demonstrates 4) Sorting Objects with Comparator Chains in practice.

```java
class Employee {
    private final String name;
    private final int age;
    private final double salary;

    Employee(String name, int age, double salary) {
        this.name = name;
        this.age = age;
        this.salary = salary;
    }

    String getName() { return name; }
    int getAge() { return age; }
    double getSalary() { return salary; }

    @Override
    public String toString() {
        return name + "(" + age + "," + salary + ")";
    }
}

List<Employee> emps = new ArrayList<>(List.of(
    new Employee("Ravi", 30, 70000),
    new Employee("Aman", 30, 90000),
    new Employee("Neha", 25, 90000)
));

emps.sort(
    Comparator.comparingDouble(Employee::getSalary).reversed()
              .thenComparingInt(Employee::getAge)
              .thenComparing(Employee::getName)
);

System.out.println(emps);
```

Expected output:

```text
[Neha(25,90000.0), Aman(30,90000.0), Ravi(30,70000.0)]
```

## 5) Binary Search Correct Usage

`Collections.binarySearch` requires list sorted with same ordering logic used for search.

Concept taught: Demonstrates 5) Binary Search Correct Usage in practice.

```java
List<Integer> nums = new ArrayList<>(List.of(40, 10, 30, 20));
Collections.sort(nums); // [10,20,30,40]

int idx1 = Collections.binarySearch(nums, 30);
int idx2 = Collections.binarySearch(nums, 25);

System.out.println(idx1);
System.out.println(idx2);
```

Expected output:

```text
2
-3
```

Meaning of negative result:

- insertion point = `-(result + 1)`
- here `-3` means insertion point `2`

## 6) Binary Search with Comparator

Concept taught: Demonstrates 6) Binary Search with Comparator in practice.

```java
List<String> names = new ArrayList<>(List.of("ram", "Aman", "shyam"));
names.sort(String.CASE_INSENSITIVE_ORDER);
int idx = Collections.binarySearch(names, "RAM", String.CASE_INSENSITIVE_ORDER);
System.out.println(names);
System.out.println(idx);
```

Expected output:

```text
[Aman, ram, shyam]
1
```

If sort comparator and search comparator mismatch, result is undefined.

## 7) Utility Operations

Concept taught: Demonstrates 7) Utility Operations in practice.

```java
List<Integer> nums = new ArrayList<>(List.of(10, 20, 30, 40));
System.out.println(Collections.min(nums));
System.out.println(Collections.max(nums));

Collections.reverse(nums);
System.out.println(nums);

Collections.shuffle(nums);
System.out.println(nums);
```

Possible output:

```text
10
40
[40, 30, 20, 10]
[random order each run]
```

## 8) Partial Sort / Top-K Pattern

For top few elements:

Concept taught: Demonstrates 8) Partial Sort / Top-K Pattern in practice.

```java
List<Integer> nums = new ArrayList<>(List.of(5, 1, 9, 7, 2, 8));
nums.sort(Comparator.reverseOrder());
List<Integer> top3 = nums.subList(0, Math.min(3, nums.size()));
System.out.println(top3);
```

Expected output:

```text
[9, 8, 7]
```

For very large data + small K, heap-based approach is better than full sort.

## 9) Common Mistakes

- calling `binarySearch` on unsorted list
- sorting with one comparator and searching with another
- comparator returning subtraction (`a - b`) for large integers (overflow risk)
- forgetting null handling when comparator touches nullable fields

Safer compare style:

Concept taught: Demonstrates 9) Common Mistakes in practice.

```java
Comparator<Integer> c = Integer::compare;
```

## 10) Summary

Master these three pieces together:

- stable sorting strategy (`Comparable`/`Comparator`)
- consistent comparator chain
- binary-search preconditions and negative-index decoding
