# 09 - Immutability and Defensive Copy in Lists (Complete)

## 1) Why This Topic Is Critical

Many production bugs happen because one part of code modifies a list that another part assumes is stable.

Immutability + defensive copying prevents:

- accidental mutation
- hidden shared-state bugs
- thread-visibility surprises
- API contract confusion

## 2) Four Common List Forms

### 2.1 Fully mutable list

Concept taught: Demonstrates 2.1 Fully mutable list in practice.

```java
List<String> a = new ArrayList<>(List.of("x", "y"));
a.add("z");
System.out.println(a);
```

Output:

```text
[x, y, z]
```

### 2.2 Fixed-size view (`Arrays.asList`)

Concept taught: Demonstrates 2.2 Fixed-size view (`Arrays.asList`) in practice.

```java
List<String> b = Arrays.asList("x", "y");
b.set(0, "X");
System.out.println(b);
```

Output:

```text
[X, y]
```

`b.add("z")` and `b.remove(0)` throw `UnsupportedOperationException`.

### 2.3 Unmodifiable wrapper (`Collections.unmodifiableList`)

Concept taught: Demonstrates 2.3 Unmodifiable wrapper (`Collections.unmodifiableList`) in practice.

```java
List<String> base = new ArrayList<>(List.of("a", "b"));
List<String> view = Collections.unmodifiableList(base);
System.out.println(view);
base.add("c");
System.out.println(view);
```

Expected output:

```text
[a, b]
[a, b, c]
```

Important:

- wrapper is read-only through `view`
- but if underlying `base` changes, `view` reflects it

### 2.4 Immutable snapshot (`List.of`, `List.copyOf`)

Concept taught: Demonstrates 2.4 Immutable snapshot (`List.of`, `List.copyOf`) in practice.

```java
List<String> src = new ArrayList<>(List.of("p", "q"));
List<String> snap = List.copyOf(src);
System.out.println(snap);
src.add("r");
System.out.println(snap);
```

Expected output:

```text
[p, q]
[p, q]
```

Snapshot does not change when source changes.

## 3) `List.of` Rules

Concept taught: Demonstrates 3) `List.of` Rules in practice.

```java
List<String> list = List.of("A", "B", "C");
System.out.println(list);
```

Output:

```text
[A, B, C]
```

Rules:

- immutable
- rejects `null` elements (throws `NullPointerException`)

## 4) Defensive Copy in Constructors

Concept taught: Demonstrates 4) Defensive Copy in Constructors in practice.

```java
class Course {
    private final List<String> students;

    Course(List<String> students) {
        this.students = new ArrayList<>(students); // defensive copy in
    }

    List<String> getStudents() {
        return List.copyOf(students); // defensive copy out (immutable)
    }
}

List<String> ext = new ArrayList<>(List.of("A", "B"));
Course c = new Course(ext);
ext.add("C");
System.out.println(c.getStudents());
```

Expected output:

```text
[A, B]
```

Why it matters:

- external mutations cannot corrupt internal state

## 5) Defensive Copy in Setters

Concept taught: Demonstrates 5) Defensive Copy in Setters in practice.

```java
class Team {
    private List<String> members = new ArrayList<>();

    void setMembers(List<String> members) {
        this.members = new ArrayList<>(members);
    }

    List<String> membersView() {
        return Collections.unmodifiableList(members);
    }
}
```

Pattern:

- copy inputs
- expose controlled read access

## 6) Deep vs Shallow Immutability

`List.copyOf` freezes list structure, not mutable objects inside list.

Concept taught: Demonstrates 6) Deep vs Shallow Immutability in practice.

```java
class Box {
    String value;
    Box(String value) { this.value = value; }
    public String toString() { return value; }
}

List<Box> src = new ArrayList<>(List.of(new Box("A")));
List<Box> snap = List.copyOf(src);
src.get(0).value = "B";
System.out.println(snap);
```

Expected output:

```text
[B]
```

Meaning:

- list structure immutable
- element object can still mutate

For deep immutability, elements must also be immutable.

## 7) Common API Contract Choices

When returning a list from public API, choose one and document it clearly:

- mutable independent copy: `new ArrayList<>(internal)`
- unmodifiable live view: `Collections.unmodifiableList(internal)`
- immutable snapshot: `List.copyOf(internal)`

## 8) UnsupportedOperationException Hotspots

These often fail at runtime:

- `List.of(...).add(...)`
- `Arrays.asList(...).remove(...)`
- `Collections.unmodifiableList(...).set(...)`

Always know mutability contract before modifying list.

## 9) Null Handling Differences

- `ArrayList`: allows null
- `Arrays.asList`: allows null values in source array
- `List.of`/`List.copyOf`: reject null

## 10) Practical Safe Recipe

If input may be external and you need safe read-only output:

Concept taught: Demonstrates 10) Practical Safe Recipe in practice.

```java
this.items = new ArrayList<>(input);
return List.copyOf(this.items);
```

This is one of the best default patterns for domain models.

## 11) Summary

Immutability is not one thing in Java lists. Always distinguish between fixed-size view, unmodifiable view, and immutable snapshot, then use defensive copying to protect object boundaries.
