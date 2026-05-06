# 07 - Sorting, Searching, and Binary Search

## 1) Natural Sort

```java
Collections.sort(list);
```

or:

```java
list.sort(Comparator.naturalOrder());
```

## 2) Custom Sort

```java
list.sort((a, b) -> b.compareTo(a)); // descending
Collections.sort(list, Collections.reverseOrder()); // descending alternative
```

For objects:

```java
employees.sort(Comparator.comparing(Employee::getSalary).reversed());
```

## 3) Binary Search

`Collections.binarySearch` needs sorted list first.

```java
Collections.sort(nums);
int idx = Collections.binarySearch(nums, 40);
```

If not found, returns negative insertion point formula:
`-(insertionPoint) - 1`

## 4) Min/Max and Reverse

```java
int min = Collections.min(nums);
int max = Collections.max(nums);
Collections.reverse(nums);
Collections.shuffle(nums);
```
