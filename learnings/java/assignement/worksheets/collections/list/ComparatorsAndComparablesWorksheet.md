# Comparators and Comparables Worksheet

Source: ComparatorsAndComparablesNotes.md

## Level 1

### Tricky Predict the Output (15)

1.
```java
List<Integer> l = new ArrayList<>(List.of(4, 1, 3, 2));
l.sort(Comparator.naturalOrder());
System.out.println(l);
```

Answer: _____________

2.
```java
List<Integer> l = new ArrayList<>(List.of(4, 1, 3, 2));
l.sort(Comparator.reverseOrder());
System.out.println(l);
```

Answer: _____________

3.
```java
List<String> l = new ArrayList<>(List.of("aa", "b", "cccc"));
l.sort(Comparator.comparingInt(String::length));
System.out.println(l);
```

Answer: _____________

4.
```java
List<String> l = new ArrayList<>(List.of("B", "a", "C"));
l.sort(String.CASE_INSENSITIVE_ORDER);
System.out.println(l);
```

Answer: _____________

5.
```java
class S implements Comparable<S> {
  int roll;
  S(int roll){ this.roll = roll; }
  public int compareTo(S o){ return Integer.compare(this.roll, o.roll); }
  public String toString(){ return String.valueOf(roll); }
}
List<S> l = new ArrayList<>(List.of(new S(3), new S(1), new S(2)));
Collections.sort(l);
System.out.println(l);
```

Answer: _____________

6.
```java
class S implements Comparable<S> {
  int roll;
  S(int roll){ this.roll = roll; }
  public int compareTo(S o){ return Integer.compare(this.roll, o.roll); }
  public String toString(){ return String.valueOf(roll); }
}
List<S> l = new ArrayList<>(List.of(new S(3), new S(1), new S(2)));
l.sort(null);
System.out.println(l);
```

Answer: _____________

7.
```java
record E(String n, int a) {}
List<E> l = new ArrayList<>(List.of(new E("A", 30), new E("B", 25)));
l.sort(Comparator.comparingInt(E::a));
System.out.println(l);
```

Answer: _____________

8.
```java
List<Integer> l = new ArrayList<>(List.of(1, 2, 3));
l.sort((a, b) -> 0);
System.out.println(l);
```

Answer: _____________

9.
```java
List<Integer> l = new ArrayList<>(List.of(3, 1, 2));
Collections.sort(l, Comparator.reverseOrder());
System.out.println(l);
```

Answer: _____________

10.
```java
List<String> l = new ArrayList<>(List.of("a", null, "b"));
l.sort(Comparator.nullsFirst(String::compareTo));
System.out.println(l);
```

Answer: _____________

11.
```java
List<String> l = new ArrayList<>(List.of("a", null, "b"));
l.sort(Comparator.nullsLast(String::compareTo));
System.out.println(l);
```

Answer: _____________

12.
```java
List<String> l = new ArrayList<>(List.of("a10", "a2", "a1"));
l.sort(Comparator.naturalOrder());
System.out.println(l);
```

Answer: _____________

13.
```java
List<Integer> l = new ArrayList<>(List.of(2, 4, 1, 3));
l.sort((x, y) -> x % 2 - y % 2);
System.out.println(l);
```

Answer: _____________

14.
```java
List<Integer> l = new ArrayList<>(List.of(2, 4, 1, 3));
l.sort(Comparator.comparingInt(x -> x % 2).thenComparingInt(x -> x));
System.out.println(l);
```

Answer: _____________

15.
```java
class S implements Comparable<S> {
  int roll;
  S(int roll){ this.roll = roll; }
  public int compareTo(S o){ return Integer.compare(this.roll, o.roll); }
  public String toString(){ return String.valueOf(roll); }
}
List<S> l = new ArrayList<>(List.of(new S(2), new S(1)));
l.sort(Comparator.comparingInt(s -> s.roll).reversed());
System.out.println(l);
```

Answer: _____________

### MCQ Theory (15)

1. `Comparable<T>` defines:
```text
A) external sort rules
B) natural/default order in class
C) hash rules
D) synchronization rules
```

2. `Comparator<T>` defines:
```text
A) one fixed class order only
B) external/custom order
C) equals override
D) constructor order
```

3. Correct `Comparable` method is:
```text
A) compare(a,b)
B) compareTo(o)
C) sort(o)
D) order(o)
```

4. Compare result `< 0` means:
```text
A) left comes after right
B) left comes before right
C) equal always
D) invalid
```

5. Compare result `0` means:
```text
A) remove element
B) equal in ordering
C) compile warning
D) null case only
```

6. Safer integer comparison is:
```text
A) a-b always
B) Integer.compare(a,b)
C) a==b?0:1
D) Math.abs(a-b)
```

7. Why avoid `a-b` comparison?
```text
A) no lambda support
B) overflow risk
C) no generics
D) slow JVM startup
```

8. `Collections.sort(list)` uses:
```text
A) comparator always
B) natural order
C) random order
D) insertion order only
```

9. `list.sort(null)` means:
```text
A) no sorting
B) natural order sorting
C) reverse order
D) unstable order
```

10. `list.sort(comparator)` means:
```text
A) ignore comparator
B) use provided comparator
C) use hashCode
D) use toString
```

11. `thenComparing` is used for:
```text
A) tie-break key
B) null removal
C) filtering
D) cloning
```

12. `nullsFirst/nullsLast` provide:
```text
A) null-safe ordering
B) thread safety
C) immutability
D) dedupe
```

13. One model class can have:
```text
A) one comparator max
B) many comparators
C) no comparator
D) only static comparator
```

14. Default business-wide order usually belongs in:
```text
A) compareTo
B) toString
C) equals only
D) constructor
```

15. Feature-specific sort should usually be in:
```text
A) compareTo only
B) dedicated comparator
C) hashCode
D) record header
```

## Level 2

### Tricky Predict the Output (15)

1.
```java
record Emp(String n, int age, double sal) {}
List<Emp> l = new ArrayList<>(List.of(
    new Emp("A", 30, 1000),
    new Emp("B", 25, 2000),
    new Emp("C", 25, 1500)
));
l.sort(Comparator.comparingInt(Emp::age).thenComparingDouble(Emp::sal));
System.out.println(l);
```

Answer: _____________

2.
```java
List<String> l = new ArrayList<>(List.of("z", "aa", "b"));
l.sort(Comparator.comparingInt(String::length).reversed());
System.out.println(l);
```

Answer: _____________

3.
```java
List<String> l = new ArrayList<>(List.of("z", "aa", "b"));
l.sort(Comparator.comparingInt(String::length).reversed().thenComparing(Comparator.naturalOrder()));
System.out.println(l);
```

Answer: _____________

4.
```java
List<Integer> l = new ArrayList<>(List.of(5, 4, 3, 2, 1));
l.sort((a, b) -> a - b);
System.out.println(l);
```

Answer: _____________

5.
```java
List<Integer> l = new ArrayList<>(List.of(5, 4, 3, 2, 1));
l.sort((a, b) -> b - a);
System.out.println(l);
```

Answer: _____________

6.
```java
class Students implements Comparable<Students> {
  String name; int roll;
  Students(String n, int r){ name=n; roll=r; }
  public int compareTo(Students o){ return Integer.compare(this.roll, o.roll); }
  public String toString(){ return name + "-" + roll; }
}
List<Students> l = new ArrayList<>(List.of(
  new Students("Bod", 7),
  new Students("Ad", 3),
  new Students("Ad", 1)
));
Collections.sort(l);
System.out.println(l);
```

Answer: _____________

7.
```java
class Students implements Comparable<Students> {
  String name; int roll;
  Students(String n, int r){ name=n; roll=r; }
  public int compareTo(Students o){
    int byRoll = Integer.compare(this.roll, o.roll);
    return byRoll != 0 ? byRoll : this.name.compareTo(o.name);
  }
  public String toString(){ return name + "-" + roll; }
}
List<Students> l = new ArrayList<>(List.of(
  new Students("B", 1),
  new Students("A", 1),
  new Students("C", 1)
));
Collections.sort(l);
System.out.println(l);
```

Answer: _____________

8.
```java
class Students {
  String name; int roll;
  Students(String n, int r){ name=n; roll=r; }
  public String toString(){ return name + "-" + roll; }
}
List<Students> l = new ArrayList<>(List.of(
  new Students("B", 1),
  new Students("A", 1),
  new Students("C", 1)
));
l.sort(Comparator.comparing((Students s) -> s.name).thenComparingInt(s -> s.roll));
System.out.println(l);
```

Answer: _____________

9.
```java
List<String> l = new ArrayList<>(List.of("Bob", "alice", "ALAN"));
l.sort(String.CASE_INSENSITIVE_ORDER);
System.out.println(l);
```

Answer: _____________

10.
```java
List<Integer> l = new ArrayList<>(List.of(11, 2, 30, 4));
l.sort(Comparator.comparingInt(String::valueOf));
System.out.println(l);
```

Answer: _____________

11.
```java
List<String> l = new ArrayList<>(List.of("a", null, "c", null, "b"));
l.sort(Comparator.nullsLast(Comparator.naturalOrder()));
System.out.println(l);
```

Answer: _____________

12.
```java
List<String> l = new ArrayList<>(List.of("a", null, "c", null, "b"));
l.sort(Comparator.nullsFirst(Comparator.reverseOrder()));
System.out.println(l);
```

Answer: _____________

13.
```java
record P(String city, int p) {}
List<P> l = new ArrayList<>(List.of(
  new P("X", 5),
  new P("A", 5),
  new P("B", 2)
));
l.sort(Comparator.comparingInt(P::p).thenComparing(P::city));
System.out.println(l);
```

Answer: _____________

14.
```java
class S implements Comparable<S> {
  int roll;
  S(int r){ roll=r; }
  public int compareTo(S o){ return 0; }
}
List<S> l = new ArrayList<>(List.of(new S(3), new S(1), new S(2)));
Collections.sort(l);
System.out.println(l.size());
```

Answer: _____________

15.
```java
class S implements Comparable<S> {
  int roll;
  S(int r){ roll=r; }
  public int compareTo(S o){ return Integer.compare(this.roll, o.roll); }
}
TreeSet<S> set = new TreeSet<>();
set.add(new S(1));
set.add(new S(1));
System.out.println(set.size());
```

Answer: _____________

### MCQ Theory (15)

1. Comparator transitivity is important for:
```text
A) random output
B) predictable sorted behavior
C) faster JVM boot
D) hash seed
```

2. Comparator inconsistent with equals can affect:
```text
A) ArrayList memory
B) TreeSet/TreeMap semantics
C) GC pauses only
D) string interning
```

3. In sorted sets/maps, element uniqueness depends mostly on:
```text
A) toString
B) compare/compareTo result
C) field order
D) object identity only
```

4. Stable sorting means:
```text
A) equal-key relative order preserved
B) no comparisons happen
C) descending only
D) immutable output
```

5. `comparingInt` expects:
```text
A) int key extractor
B) boolean predicate
C) collector
D) supplier
```

6. `comparingDouble` is useful for:
```text
A) floating-point key sort
B) string collation
C) null removal
D) lock handling
```

7. `reversed()` on comparator does:
```text
A) reverse comparator ordering
B) reverse list in-place now
C) clear list
D) disable nulls
```

8. Reverse only secondary key correctly by:
```text
A) reversing full chain blindly
B) reversing that secondary comparator only
C) sorting twice random
D) using hashCode
```

9. Case-insensitive ordering helper is:
```text
A) String.CASE_INSENSITIVE_ORDER
B) String::toUpperCase only
C) equalsIgnoreCase
D) compareTo only
```

10. Null-safe descending string comparator can be:
```text
A) nullsLast(reverseOrder())
B) comparingInt(length) only
C) equals only
D) hash compare
```

11. Compare always returning 0 implies:
```text
A) strict total order
B) all elements equal in ordering
C) reverse sorting
D) compile error
```

12. Compare always returning positive for unequal pairs is:
```text
A) valid order
B) contract violation
C) stable by definition
D) optimized order
```

13. `Collections.sort(list, cmp)` vs `list.sort(cmp)`:
```text
A) both valid comparator-based APIs
B) one is invalid
C) both array-only
D) both deprecated
```

14. Production sorting design often uses:
```text
A) Comparable only
B) Comparator only
C) Comparable + feature-specific comparators
D) no contracts
```

15. Interview-ready understanding includes:
```text
A) syntax only
B) contracts, nulls, chaining, correctness
C) imports only
D) IDE shortcuts only
```
