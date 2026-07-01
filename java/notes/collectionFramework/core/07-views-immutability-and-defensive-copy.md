# 07 - Views, Immutability, and Defensive Copy

## 1) Mutable vs Fixed vs Immutable

- mutable: full structural updates allowed
- fixed-size view: no add/remove
- immutable: no structural or replacement mutation

## 2) `Arrays.asList` Trap

Concept taught: Fixed-size list allows `set`, rejects `add/remove`.

```java
List<String> fixed = Arrays.asList("A", "B");
fixed.set(0, "X");
System.out.println(fixed);
```

Expected output:

```text
[X, B]
```

## 3) `List.of` Immutability

Concept taught: Immutable factory list throws on structural modification.

```java
List<String> imm = List.of("A", "B");
System.out.println(imm);
// imm.add("C"); // UnsupportedOperationException
```

Expected output:

```text
[A, B]
```

## 4) Unmodifiable View vs Snapshot

Concept taught: Unmodifiable view reflects source changes; copy snapshot does not.

```java
List<String> src = new ArrayList<>(List.of("A"));
List<String> view = Collections.unmodifiableList(src);
List<String> snap = List.copyOf(src);
src.add("B");
System.out.println(view);
System.out.println(snap);
```

Expected output:

```text
[A, B]
[A]
```

## 5) Defensive Copy Pattern

Concept taught: Protect class boundaries with copy-in and immutable copy-out.

```java
class Course {
    private final List<String> students;
    Course(List<String> students) { this.students = new ArrayList<>(students); }
    List<String> students() { return List.copyOf(students); }
}

List<String> ext = new ArrayList<>(List.of("R"));
Course c = new Course(ext);
ext.add("S");
System.out.println(c.students());
```

Expected output:

```text
[R]
```

## 6) Summary

For robust APIs, prefer immutable snapshots at boundaries unless live views are explicitly required.
