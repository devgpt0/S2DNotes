# 08 - Grouping, Partitioning, and Downstream Collectors

## 1) Grouping

```java
record Employee(String department, String name, int salary) {}

List<Employee> employees = List.of(
        new Employee("IT", "Asha", 100),
        new Employee("HR", "Ravi", 80),
        new Employee("IT", "Anu", 120));

Map<String, List<Employee>> byDepartment = employees.stream()
        .collect(Collectors.groupingBy(Employee::department));
System.out.println(byDepartment.get("IT").stream().map(Employee::name).toList());
// Output: [Asha, Anu]
```

## 2) Downstream Mapping

```java
Map<String, List<String>> namesByDepartment = employees.stream()
        .collect(Collectors.groupingBy(
                Employee::department,
                Collectors.mapping(Employee::name, Collectors.toList())));
System.out.println(namesByDepartment.get("HR"));
// Output: [Ravi]
```

## 3) Aggregation per Group

```java
Map<String, Integer> salaryByDepartment = employees.stream()
        .collect(Collectors.groupingBy(
                Employee::department,
                Collectors.summingInt(Employee::salary)));
System.out.println(salaryByDepartment.get("IT"));
// Output: 220
```

## 4) Partitioning

```java
Map<Boolean, List<Integer>> partition = Stream.of(1, 2, 3, 4)
        .collect(Collectors.partitioningBy(value -> value % 2 == 0));
System.out.println(partition.get(true));
System.out.println(partition.get(false));
// Output:
// [2, 4]
// [1, 3]
```

Partitioning always has Boolean keys for true and false.

## 5) `teeing`

```java
record Range(int minimum, int maximum) {}

Range range = Stream.of(4, 9, 2)
        .collect(Collectors.teeing(
                Collectors.minBy(Integer::compareTo),
                Collectors.maxBy(Integer::compareTo),
                (minimum, maximum) -> new Range(minimum.orElseThrow(), maximum.orElseThrow())));
System.out.println(range);
// Output: Range[minimum=2, maximum=9]
```
