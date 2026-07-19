# Lambda Worksheet

Source: collectionFramework/lamdbaFunction (unified notes)

## Tricky Predict the Output (15)

1.
```java
Runnable r = () -> System.out.print("Hi");
r.run();
```
Answer: _____________

2.
```java
Function<Integer, Integer> f = x -> x * x;
System.out.println(f.apply(4));
```
Answer: _____________

3.
```java
Predicate<String> p = s -> !s.isBlank();
System.out.println(p.test("   "));
```
Answer: _____________

4.
```java
Supplier<String> s = () -> "java";
System.out.println(s.get().toUpperCase());
```
Answer: _____________

5.
```java
Consumer<String> c = x -> System.out.print(x + "!");
c.accept("Hi");
```
Answer: _____________

6.
```java
Function<Integer, Integer> t2 = x -> x * 2;
Function<Integer, Integer> p3 = x -> x + 3;
System.out.println(t2.andThen(p3).apply(5));
```
Answer: _____________

7.
```java
Function<Integer, Integer> t2 = x -> x * 2;
Function<Integer, Integer> p3 = x -> x + 3;
System.out.println(t2.compose(p3).apply(5));
```
Answer: _____________

8.
```java
List<String> l = new ArrayList<>(List.of("a", "bb", "ccc"));
l.removeIf(s -> s.length() == 2);
System.out.println(l);
```
Answer: _____________

9.
```java
List<String> out = List.of("a", "bb", "ccc").stream()
    .filter(s -> s.length() >= 2)
    .map(String::toUpperCase)
    .toList();
System.out.println(out);
```
Answer: _____________

10.
```java
Map<String, Integer> m = new HashMap<>();
m.merge("java", 1, Integer::sum);
m.merge("java", 1, Integer::sum);
System.out.println(m.get("java"));
```
Answer: _____________

11.
```java
Function<String, Integer> f = Integer::parseInt;
System.out.println(f.apply("42"));
```
Answer: _____________

12.
```java
int base = 10;
Function<Integer, Integer> add = x -> x + base;
System.out.println(add.apply(5));
```
Answer: _____________

13.
```java
int x = 10;
Function<Integer, Integer> f = y -> y + x;
x = 20;
System.out.println(f.apply(1));
```
Answer: _____________

14.
```java
List<Integer> l = new ArrayList<>(List.of(1, 2, 3));
l.forEach(n -> {
  if (n == 2) l.remove(Integer.valueOf(2));
});
System.out.println(l);
```
Answer: _____________

15.
```java
Function<Integer, Function<Integer, Integer>> adder = a -> b -> a + b;
System.out.println(adder.apply(10).apply(5));
```
Answer: _____________

## MCQ Theory (15)

1. Lambda can be assigned to:
```text
A) any interface
B) functional interface
C) abstract class only
D) enum only
```

2. Functional interface means:
```text
A) one abstract method
B) one default method
C) no methods
D) one static method only
```

3. `@FunctionalInterface` mainly:
```text
A) enables JIT
B) enforces SAM rule at compile time
C) makes class immutable
D) creates threads
```

4. `Predicate<T>` returns:
```text
A) T
B) boolean
C) int
D) void
```

5. `Supplier<T>` takes:
```text
A) one input
B) two inputs
C) no input
D) list input only
```

6. `Consumer<T>` returns:
```text
A) T
B) boolean
C) void
D) Optional<T>
```

7. `Function<T,R>` does:
```text
A) R -> T
B) T -> R
C) T -> boolean
D) no input
```

8. Method reference `Integer::parseInt` is:
```text
A) constructor ref
B) static method ref
C) instance method of object ref
D) invalid
```

9. Captured local variable in lambda must be:
```text
A) volatile
B) effectively final
C) static final only
D) mutable
```

10. `andThen` vs `compose` differ in:
```text
A) syntax only
B) application order
C) return type
D) thread safety
```

11. In streams, side effects in `map/filter` are:
```text
A) always recommended
B) usually discouraged
C) mandatory
D) compile error always
```

12. Primitive functional interfaces help:
```text
A) avoid boxing overhead
B) avoid exceptions
C) avoid streams
D) avoid lambdas
```

13. `Comparator.comparing(...)` with lambda is example of:
```text
A) recursion
B) higher-order API usage
C) reflection
D) serialization only
```

14. Checked exceptions in lambda are:
```text
A) always ignored
B) must follow target method signature constraints
C) never allowed by JVM
D) converted automatically
```

15. Better readability practice for long lambdas:
```text
A) keep growing inline
B) extract method and use method reference when possible
C) avoid naming
D) avoid tests
```

## Interview Questions (10)

1. What problem did lambdas solve in Java compared to anonymous classes?
2. Explain functional interface and why SAM matters.
3. Compare lambda and method reference with examples.
4. Explain effectively-final capture rule and why it exists.
5. Difference between `Function`, `Consumer`, `Supplier`, `Predicate`.
6. Explain `andThen` and `compose` with practical use.
7. What are common stream + lambda anti-patterns?
8. How do you handle checked exceptions inside lambda pipelines?
9. Why and when to use primitive specializations like `IntUnaryOperator`?
10. Show one real-world use of lambda in collections/map processing.

