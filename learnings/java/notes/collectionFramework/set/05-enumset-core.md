# 05 - EnumSet Core (Complete)

## 1) Internal Idea

`EnumSet` is a specialized high-performance set for enum constants.

- very compact bit-vector style representation
- extremely fast operations
- iteration follows enum declaration order

## 2) Basic Usage

Concept taught: Enum-only set with declaration-order iteration.

```java
enum Role { USER, MODERATOR, ADMIN }
EnumSet<Role> roles = EnumSet.of(Role.USER, Role.ADMIN);
System.out.println(roles);
```

Expected output:

```text
[USER, ADMIN]
```

## 3) Range and All Helpers

Concept taught: Efficient enum range and complement operations.

```java
enum Day { MON, TUE, WED, THU, FRI, SAT, SUN }
EnumSet<Day> weekdays = EnumSet.range(Day.MON, Day.FRI);
EnumSet<Day> weekend = EnumSet.complementOf(weekdays);
System.out.println(weekdays);
System.out.println(weekend);
```

Expected output:

```text
[MON, TUE, WED, THU, FRI]
[SAT, SUN]
```

## 4) When to Use

- permission/role sets
- finite state flags
- frequent membership checks over enum domain

## 5) Summary

If elements are enum constants, `EnumSet` is usually the best set choice.
