# Comprehensive Lambda Worksheet (All Concepts)

**Source**: collectionFramework/lambda (all notes 01-12)  
**Weightage**: Basics (20%) | Functional Interfaces (20%) | Method References (15%) | Variable Capture (10%) | With Collections/Streams (20%) | Composition (10%) | Advanced (5%)

---

## LEVEL 1 - FUNDAMENTALS

### 1.1 Predict the Output (35 Questions)

#### Basic Lambda Syntax (10 questions)
1.
```java
Runnable r = () -> System.out.println("Hello");
r.run();
```
Answer: _____________

2.
```java
Function<Integer, Integer> f = x -> x * x;
System.out.println(f.apply(5));
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
Function<Integer, Integer> f = x -> x;
System.out.println(f.apply(42));
```
Answer: _____________

7.
```java
Predicate<Integer> even = x -> x % 2 == 0;
System.out.println(even.test(4));
```
Answer: _____________

8.
```java
BiFunction<Integer, Integer, Integer> add = (a, b) -> a + b;
System.out.println(add.apply(3, 5));
```
Answer: _____________

9.
```java
UnaryOperator<String> upper = s -> s.toUpperCase();
System.out.println(upper.apply("hello"));
```
Answer: _____________

10.
```java
BinaryOperator<Integer> multiply = (a, b) -> a * b;
System.out.println(multiply.apply(4, 5));
```
Answer: _____________

#### Functional Interfaces & Type Inference (8 questions)
11.
```java
Function<String, Integer> len = s -> s.length();
System.out.println(len.apply("lambda"));
```
Answer: _____________

12.
```java
BiPredicate<Integer, Integer> greater = (a, b) -> a > b;
System.out.println(greater.test(10, 5));
```
Answer: _____________

13.
```java
IntPredicate isPos = x -> x > 0;
System.out.println(isPos.test(-5));
```
Answer: _____________

14.
```java
IntUnaryOperator increment = x -> x + 1;
System.out.println(increment.applyAsInt(9));
```
Answer: _____________

15.
```java
ToIntFunction<String> len = s -> s.length();
System.out.println(len.applyAsInt("test"));
```
Answer: _____________

16.
```java
BiConsumer<String, String> print = (a, b) -> System.out.print(a + b);
print.accept("Hello", "World");
```
Answer: _____________

17.
```java
@FunctionalInterface
interface MathOp { int calc(int a, int b); }
MathOp sub = (a, b) -> a - b;
System.out.println(sub.calc(10, 3));
```
Answer: _____________

18.
```java
Supplier<Double> random = () -> Math.random();
double d1 = random.get();
double d2 = random.get();
System.out.println(d1 == d2);
```
Answer: _____________

#### Method References (7 questions)
19.
```java
Function<String, Integer> parse = Integer::parseInt;
System.out.println(parse.apply("42"));
```
Answer: _____________

20.
```java
Consumer<String> print = System.out::println;
print.accept("method reference");
```
Answer: _____________

21.
```java
Function<String, String> upper = String::toUpperCase;
System.out.println(upper.apply("hello"));
```
Answer: _____________

22.
```java
Supplier<ArrayList<String>> supplier = ArrayList::new;
List<String> l = supplier.get();
System.out.println(l.size());
```
Answer: _____________

23.
```java
BiConsumer<List<String>, String> add = List::add;
List<String> l = new ArrayList<>();
add.accept(l, "java");
System.out.println(l);
```
Answer: _____________

24.
```java
Function<String[], Integer> len = String[]::length;
String[] arr = {"a", "b", "c"};
System.out.println(len.apply(arr));
```
Answer: _____________

25.
```java
Comparator<String> comp = String::compareTo;
System.out.println(comp.compare("a", "b"));
```
Answer: _____________

#### Variable Capture & Scope (5 questions)
26.
```java
int base = 10;
Function<Integer, Integer> addBase = x -> x + base;
System.out.println(addBase.apply(5));
```
Answer: _____________

27.
```java
int x = 10;
Function<Integer, Integer> f = a -> {
    // x = 20; // compile error: x not final
    return a + x;
};
System.out.println(f.apply(5));
```
Answer: _____________

28.
```java
class Counter {
    int count = 0;
    void increment() {
        Runnable r = () -> count++;
        r.run();
        r.run();
    }
}
Counter c = new Counter();
c.increment();
System.out.println(c.count);
```
Answer: _____________

29.
```java
List<Integer> list = new ArrayList<>(List.of(1, 2, 3));
Consumer<Integer> print = x -> System.out.print(x + " ");
list.forEach(print);
```
Answer: _____________

30.
```java
int val = 5;
Supplier<Integer> s = () -> val * 2;
System.out.println(s.get());
```
Answer: _____________

#### With Collections & Streams (5 questions)
31.
```java
List<String> l = new ArrayList<>(List.of("a", "bb", "ccc"));
l.removeIf(s -> s.length() == 2);
System.out.println(l);
```
Answer: _____________

32.
```java
List<String> out = List.of("a", "bb", "ccc").stream()
    .filter(s -> s.length() >= 2)
    .map(String::toUpperCase)
    .toList();
System.out.println(out);
```
Answer: _____________

33.
```java
List<Integer> l = new ArrayList<>(List.of(1, 2, 3));
l.replaceAll(x -> x * 2);
System.out.println(l);
```
Answer: _____________

34.
```java
Map<String, Integer> m = new HashMap<>();
m.merge("java", 1, Integer::sum);
m.merge("java", 1, Integer::sum);
System.out.println(m.get("java"));
```
Answer: _____________

35.
```java
List<Integer> nums = new ArrayList<>(List.of(3, 1, 4, 1, 5));
nums.sort((a, b) -> a - b);
System.out.println(nums);
```
Answer: _____________

---

### 1.2 MCQ Theory (35 Questions)

#### Lambda Basics & Syntax (10 questions)
1. Lambda expression is:
```text
A) named inner class
B) anonymous function implementing single abstract method
C) regular method
D) class inheritance
```

2. Syntax variants of lambda:
```text
A) only () -> expr
B) x -> expr, (x, y) -> expr, (x, y) -> { ... }
C) only (params) -> { statements }
D) no variants, fixed format
```

3. Parameter type in lambda can be:
```text
A) always explicit
B) always inferred from context
C) explicit or implicit
D) not allowed
```

4. Return in lambda:
```text
A) always explicit with `return`
B) implicit for single expression, explicit for block
C) not used
D) optional
```

5. Lambda can access:
```text
A) local variables always
B) local variables if final or effectively final
C) static fields
D) both B and C
```

6. Functional interface requirement:
```text
A) any interface
B) interface with exactly one abstract method
C) interface extending other interfaces
D) no interface needed
```

7. `@FunctionalInterface` annotation:
```text
A) required for compilation
B) optional, documentation + compiler check
C) not recommended
D) only for built-in interfaces
```

8. Lambda this reference:
```text
A) refers to lambda object
B) refers to enclosing instance
C) throws compile error
D) refers to null
```

9. Cannot do in lambda:
```text
A) call other methods
B) modify captured final variables
C) return value
D) use ternary operator
```

10. Best practice for lambda length:
```text
A) no length limit
B) keep short, extract complex logic
C) use method reference when clearer
D) both B and C
```

#### Functional Interfaces (8 questions)
11. `Predicate<T>` is:
```text
A) T -> boolean
B) void -> T
C) T -> void
D) T -> T
```

12. `Function<T, R>` is:
```text
A) T -> T
B) T -> R
C) () -> R
D) T -> void
```

13. `Consumer<T>` is:
```text
A) T -> boolean
B) T -> R
C) T -> void (side effects)
D) () -> T
```

14. `Supplier<T>` is:
```text
A) T -> void
B) void -> T
C) T -> T
D) T -> boolean
```

15. `UnaryOperator<T>` is:
```text
A) T -> T
B) (T, T) -> T
C) T -> void
D) () -> T
```

16. `BinaryOperator<T>` is:
```text
A) T -> T
B) (T, T) -> T
C) () -> T
D) T -> boolean
```

17. Primitive specialization benefit:
```text
A) no benefit
B) avoids boxing overhead
C) always required
D) only for performance tuning
```

18. `BiPredicate<T, U>` is:
```text
A) (T) -> boolean
B) (T, U) -> boolean
C) () -> boolean
D) T -> U
```

#### Method References (5 questions)
19. Method reference type - static method:
```text
A) instance::method
B) ClassName::staticMethod
C) ClassName::method
D) new ClassName()::method
```

20. Method reference for instance method:
```text
A) ClassName::method
B) instance::method
C) static context only
D) cannot do
```

21. Constructor reference:
```text
A) ClassName::class
B) ClassName::new
C) new::ClassName
D) ClassName()
```

22. Method reference vs lambda:
```text
A) method reference always better
B) use method reference for clarity, lambda for logic
C) always same performance
D) lambda is subset of method reference
```

23. This in method reference:
```text
A) refers to reference object
B) refers to enclosing instance
C) not available
D) implementation dependent
```

#### Collection Lambda Operations (5 questions)
24. `List.forEach()` loop:
```text
A) can modify list structure safely
B) may throw ConcurrentModificationException
C) is terminal stream operation
D) works only with immutable lists
```

25. `List.removeIf()`:
```text
A) returns new list
B) modifies original in-place
C) creates stream
D) thread-safe
```

26. `List.replaceAll()`:
```text
A) returns new list
B) in-place replacement with UnaryOperator
C) functional
D) creates stream
```

27. `Map.forEach()`:
```text
A) only accepts Consumer
B) accepts BiConsumer of key, value
C) creates new map
D) cannot use lambda
```

28. `Map.merge()`:
```text
A) combines two maps
B) combines value for key using lambda function
C) replaces entire value
D) cannot use lambda
```

29. Stream `filter()`:
```text
A) terminal operation
B) intermediate operation, returns Stream
C) requires explicit collect
D) modifies source
```

#### Variable Capture (2 questions)
30. Effectively final variable:
```text
A) marked with final keyword
B) assigned once, never modified after
C) always local scope
D) field reference
```

31. Capturing mutable object in lambda:
```text
A) always safe
B) value captured, mutations visible
C) creates copy
D) not allowed
```

---

### 1.3 Interview Questions (15 Questions)

1. **What is a lambda expression? How does it relate to functional interfaces?**

2. **Explain the difference between lambda and anonymous inner classes. When would you still use anonymous classes?**

3. **What is a functional interface? Show an example with @FunctionalInterface annotation.**

4. **Explain the variable capture rule: why must local variables be final or effectively final?**

5. **What are the built-in functional interfaces in java.util.function? Provide a practical use case for each.**

6. **How are primitive specializations (IntPredicate, IntFunction) better than generic alternatives?**

7. **What is a method reference? Show all 4 types with examples.**

8. **When is a method reference preferred over a lambda expression?**

9. **Explain how lambda captures `this` from the enclosing class. Provide a use case.**

10. **What happens when you use removeIf() with lambda on a list? Is it safe? Why/why not?**

11. **Show how to use lambda with Collections.sort() to sort objects by multiple criteria.**

12. **Explain Map.merge() with a lambda remapping function. Provide a frequency counting example.**

13. **What are the performance implications of using lambda in hot loops?**

14. **Design a custom comparator using lambda for sorting complex objects.**

15. **Explain the functional programming paradigm benefits: immutability, composition, and purity with lambda examples.**

---

## LEVEL 2 - ADVANCED

### 2.1 Predict the Output (35 Questions)

#### Complex Function Composition (8 questions)
1.
```java
Function<Integer, Integer> f = x -> x * 2;
Function<Integer, Integer> g = x -> x + 3;
System.out.println(f.andThen(g).apply(5));
```
Answer: _____________

2.
```java
Function<Integer, Integer> f = x -> x * 2;
Function<Integer, Integer> g = x -> x + 3;
System.out.println(f.compose(g).apply(5));
```
Answer: _____________

3.
```java
Predicate<Integer> p1 = x -> x > 0;
Predicate<Integer> p2 = x -> x < 10;
System.out.println(p1.and(p2).test(5));
```
Answer: _____________

4.
```java
Predicate<Integer> p = x -> x > 5;
System.out.println(p.negate().test(3));
```
Answer: _____________

5.
```java
Predicate<String> p1 = String::isEmpty;
Predicate<String> p2 = s -> s.length() > 5;
System.out.println(p1.or(p2).test("hello"));
```
Answer: _____________

6.
```java
Function<String, Integer> parse = Integer::parseInt;
Function<Integer, String> toStr = Object::toString;
System.out.println(parse.andThen(toStr).apply("42"));
```
Answer: _____________

7.
```java
Comparator<Integer> c = Integer::compareTo;
Comparator<Integer> rev = c.reversed();
System.out.println(rev.compare(5, 3));
```
Answer: _____________

8.
```java
Supplier<Integer> s = () -> (int)(Math.random() * 10);
System.out.println(s.get() == s.get());
```
Answer: _____________

#### Stream & Lambda Integration (8 questions)
9.
```java
List<Integer> nums = new ArrayList<>(List.of(1, 2, 3, 4, 5));
long count = nums.stream()
    .filter(x -> x % 2 == 0)
    .count();
System.out.println(count);
```
Answer: _____________

10.
```java
List<String> words = new ArrayList<>(List.of("a", "bb", "ccc"));
List<Integer> lengths = words.stream()
    .map(String::length)
    .toList();
System.out.println(lengths);
```
Answer: _____________

11.
```java
List<Integer> nums = Arrays.asList(1, 2, 3, 4, 5);
int sum = nums.stream()
    .filter(x -> x > 2)
    .map(x -> x * 2)
    .mapToInt(Integer::intValue)
    .sum();
System.out.println(sum);
```
Answer: _____________

12.
```java
List<String> words = List.of("apple", "app", "application");
String longest = words.stream()
    .max(Comparator.comparingInt(String::length))
    .orElse("");
System.out.println(longest);
```
Answer: _____________

13.
```java
List<Integer> nums = new ArrayList<>(List.of(1, 2, 2, 3, 3, 3));
List<Integer> distinct = nums.stream()
    .distinct()
    .toList();
System.out.println(distinct);
```
Answer: _____________

14.
```java
List<String> words = List.of("a", "bb", "ccc", "aa");
words.stream()
    .sorted(Comparator.comparingInt(String::length))
    .forEach(System.out::print);
```
Answer: _____________

15.
```java
List<List<Integer>> matrix = List.of(
    List.of(1, 2),
    List.of(3, 4)
);
int sum = matrix.stream()
    .flatMap(List::stream)
    .mapToInt(Integer::intValue)
    .sum();
System.out.println(sum);
```
Answer: _____________

16.
```java
List<String> words = new ArrayList<>(List.of("a", "bb", "ccc"));
Map<Integer, Long> lenCount = words.stream()
    .collect(Collectors.groupingBy(
        String::length,
        Collectors.counting()
    ));
System.out.println(lenCount);
```
Answer: _____________

#### Map Operations with Lambda (7 questions)
17.
```java
Map<String, Integer> m = new HashMap<>();
m.put("a", 1);
m.put("b", 2);
m.forEach((k, v) -> System.out.print(k + v));
```
Answer: _____________

18.
```java
Map<String, Integer> m = new HashMap<>();
m.put("java", 1);
m.computeIfAbsent("java", k -> 10);
m.computeIfAbsent("python", k -> 5);
System.out.println(m);
```
Answer: _____________

19.
```java
Map<String, Integer> m = new HashMap<>();
m.put("a", 1);
m.put("b", 2);
m.replaceAll((k, v) -> v * 2);
System.out.println(m);
```
Answer: _____________

20.
```java
Map<String, Integer> freq = new HashMap<>();
String s = "aabbc";
for (char c : s.toCharArray()) {
    freq.merge(String.valueOf(c), 1, Integer::sum);
}
System.out.println(freq);
```
Answer: _____________

21.
```java
Map<String, List<Integer>> m = new HashMap<>();
m.computeIfAbsent("key", k -> new ArrayList<>())
    .add(10);
m.computeIfAbsent("key", k -> new ArrayList<>())
    .add(20);
System.out.println(m);
```
Answer: _____________

22.
```java
Map<String, Integer> m = new HashMap<>();
m.put("a", 5);
m.computeIfPresent("a", (k, v) -> v + 10);
m.computeIfPresent("b", (k, v) -> 1);
System.out.println(m);
```
Answer: _____________

23.
```java
Map<String, String> m = new HashMap<>();
m.put("name", "John");
String value = m.getOrDefault("age", "unknown");
System.out.println(value);
```
Answer: _____________

#### Custom Functional Interfaces (5 questions)
24.
```java
@FunctionalInterface
interface Transformer<T> {
    T transform(T input);
}
Transformer<String> upper = s -> s.toUpperCase();
System.out.println(upper.transform("hello"));
```
Answer: _____________

25.
```java
@FunctionalInterface
interface Combiner<T> {
    T combine(T a, T b);
    default T combine(T a, T b, T c) {
        return combine(combine(a, b), c);
    }
}
Combiner<Integer> sum = (a, b) -> a + b;
System.out.println(sum.combine(1, 2, 3));
```
Answer: _____________

26.
```java
@FunctionalInterface
interface Validator<T> {
    boolean validate(T value);
}
List<String> words = List.of("a", "bb", "ccc");
Validator<String> longWord = s -> s.length() > 1;
long count = words.stream()
    .filter(longWord::validate)
    .count();
System.out.println(count);
```
Answer: _____________

27.
```java
@FunctionalInterface
interface Pipe<T> {
    T apply(T input);
    default <U> Pipe<U> andThen(Pipe<? super T> next) {
        return i -> next.apply(apply(i));
    }
}
Pipe<Integer> f = x -> x * 2;
Pipe<Integer> g = x -> x + 1;
System.out.println(f.andThen(g).apply(5));
```
Answer: _____________

28.
```java
@FunctionalInterface
interface CheckedSupplier<T> {
    T get() throws Exception;
}
CheckedSupplier<Integer> s = () -> Integer.parseInt("42");
System.out.println(s.get());
```
Answer: _____________

#### Variable Capture Scenarios (4 questions)
29.
```java
List<Function<Integer, Integer>> fns = new ArrayList<>();
for (int i = 0; i < 3; i++) {
    final int val = i; // must be effectively final
    fns.add(x -> x + val);
}
System.out.println(fns.get(0).apply(10));
```
Answer: _____________

30.
```java
List<Supplier<Integer>> suppliers = new ArrayList<>();
int[] arr = {1, 2, 3};
for (int v : arr) {
    suppliers.add(() -> v); // tries to capture
}
System.out.println(suppliers.get(0).get());
```
Answer: _____________

31.
```java
class Container {
    int value = 10;
    Supplier<Integer> supplier = () -> value;
    void changeValue() { value = 20; }
}
Container c = new Container();
System.out.println(c.supplier.get());
c.changeValue();
System.out.println(c.supplier.get());
```
Answer: _____________

32.
```java
Supplier<String> s;
{
    String msg = "captured";
    s = () -> msg;
}
System.out.println(s.get());
```
Answer: _____________

#### Method Reference Variants (3 questions)
33.
```java
List<String> words = List.of("a", "bb", "ccc");
List<Integer> lens = words.stream()
    .map(String::length)
    .toList();
System.out.println(lens);
```
Answer: _____________

34.
```java
List<String> words = List.of("apple", "banana", "cherry");
words.stream()
    .filter(w -> w.startsWith("a"))
    .map(String::toUpperCase)
    .forEach(System.out::println);
```
Answer: _____________

35.
```java
Supplier<List<String>> newList = ArrayList::new;
List<String> l = newList.get();
System.out.println(l instanceof ArrayList);
```
Answer: _____________

---

### 2.2 MCQ Advanced (35 Questions)

#### Function Composition (7 questions)
1. `Function.andThen()`:
```text
A) f.andThen(g) applies f then g
B) f.andThen(g) applies g then f
C) creates sequential pipe
D) both A and C
```

2. `Function.compose()`:
```text
A) f.compose(g) applies f then g
B) f.compose(g) applies g then f
C) reverse of andThen
D) both B and C
```

3. Composition signature:
```java
Function<Integer, Integer> add3 = x -> x + 3;
Function<Integer, Integer> mul2 = x -> x * 2;
int result = add3.compose(mul2).apply(5);
```
Result is:
```text
A) 13 (5*2+3)
B) 16 ((5+3)*2)
C) 26
D) error
```

4. Chaining operations:
```text
A) only Function supports
B) Predicate, Comparator also support
C) all functional interfaces
D) custom only
```

5. `Predicate.and()`:
```text
A) short-circuit AND logic
B) always evaluates both
C) returns boolean
D) returns new Predicate
```

6. `Predicate.or()`:
```text
A) short-circuit OR logic
B) evaluates both always
C) returns boolean
D) returns new Predicate
```

7. Performance of composition:
```text
A) same as separate calls
B) can be optimized by JIT
C) always slower
D) unpredictable
```

#### Stream Terminal Operations (7 questions)
8. Terminal operation:
```text
A) filter, map (intermediate)
B) toList, collect, forEach (terminal)
C) sorted, distinct (terminal)
D) all are intermediate
```

9. Stream once consumed:
```text
A) can be reused
B) must be recreated
C) throws IllegalStateException
D) optional behavior
```

10. Lazy evaluation in Streams:
```text
A) computed immediately
B) computed only on terminal operation
C) cached and reused
D) never computed
```

11. `.toList()` in Java 16+:
```text
A) mutable ArrayList
B) immutable List
C) same as collect(toList())
D) returns null on empty
```

12. `collect(Collectors.toMap())`:
```text
A) creates List
B) creates Map with key/value
C) creates Set
D) cannot use with lambda
```

13. `collect(Collectors.groupingBy())`:
```text
A) groups by key function
B) counts occurrences
C) both A and B possible
D) creates Set
```

14. `findFirst()` vs `findAny()`:
```text
A) same behavior
B) findFirst deterministic, findAny not
C) findAny faster in parallel
D) both B and C
```

#### Advanced Stream Operations (8 questions)
15. `flatMap()`:
```text
A) flattens nested collections
B) maps then flattens result
C) creates Set
D) both A and B
```

16. `peek()` operation:
```text
A) terminal operation
B) intermediate, for debugging
C) always evaluates
D) creates list
```

17. `reduce()` operation:
```text
A) collects into list
B) combines elements with function
C) creates map
D) groups elements
```

18. `boxed()` on primitive stream:
```text
A) creates primitive array
B) wraps into Object stream
C) filters elements
D) sorts stream
```

19. Optional best practice:
```text
A) check with isPresent() then get()
B) use ifPresent(), orElse(), etc.
C) both valid
D) never use Optional
```

20. `orElseThrow()`:
```text
A) always throws
B) throws only if empty
C) returns value if present
D) both B and C
```

21. Stream performance considerations:
```text
A) always faster than loops
B) depends on operations and data size
C) parallelStream() always better
D) same performance always
```

22. Collection source efficiency:
```text
A) List most efficient
B) Set more efficient
C) depends on size and operations
D) no difference
```

#### Lambda with Collections (5 questions)
23. `replaceAll()` with lambda:
```text
A) creates new list
B) modifies in-place
C) returns new list
D) cannot use lambda
```

24. `removeIf()` behavior:
```text
A) safe during iteration
B) uses iterator internally
C) both A and B
D) cannot use
```

25. `forEach()` in Map:
```text
A) accepts Consumer only
B) accepts BiConsumer
C) cannot modify
D) throws exception always
```

26. `computeIfAbsent()`:
```text
A) always computes
B) computes only if key absent
C) replaces always
D) cannot use lambda
```

27. `computeIfPresent()`:
```text
A) always computes
B) computes if key present
C) never computes
D) cannot use lambda
```

#### Custom Functional Interfaces (5 questions)
28. Functional interface rules:
```text
A) exactly one abstract method
B) can have default methods
C) can have static methods
D) all above
```

29. Multiple inheritance of SAM:
```text
A) not allowed
B) allowed if only one abstract
C) not possible
D) requires @FunctionalInterface
```

30. Extending functional interface:
```java
@FunctionalInterface
interface A { void method(); }
@FunctionalInterface
interface B extends A { void method2(); }
```
This is:
```text
A) valid
B) invalid - B has 2 abstract methods
C) valid - extends allowed
D) requires default implementation
```

31. Generic functional interface:
```text
A) not allowed
B) allowed with type parameter
C) only for built-in
D) requires raw types
```

32. Checked exceptions in functional interface:
```text
A) not allowed
B) allowed, but lambda cannot throw
C) allowed with throws clause
D) requires wrapper
```

#### Variable Capture Advanced (3 questions)
33. Capturing in lambda from method:
```text
A) any local variable
B) final or effectively final only
C) instance fields always
D) static fields only
```

34. Shadowing in lambda:
```text
A) allowed always
B) cannot redeclare same name
C) different type allowed
D) no restriction
```

35. Memory implications of capture:
```text
A) lambda holds reference to variables
B) captures copy of value
C) captures reference to object
D) no memory overhead
```

---

### 2.2 Advanced Interview Questions (15 Questions)

1. **Explain function composition: andThen vs compose. Provide a practical pipeline example.**

2. **Design a fluent builder API using lambda and method references.**

3. **How does lazy evaluation in Streams work? Show an example where intermediate operations are not evaluated.**

4. **Compare eager (list.forEach) vs lazy (stream.forEach): when use each and why?**

5. **Explain terminal vs intermediate operations. Why does toList() need explicit call?**

6. **Design a frequency counter using Map.merge() and explain why it's better than get/put pattern.**

7. **What are checked exceptions and why can't lambda throw them directly? Show workaround patterns.**

8. **Explain variable capture memory implications: does lambda hold reference or copy? Show ConcurrentModificationException scenario.**

9. **Design a custom Validator interface with composition (chaining validators). Implement and() and or().**

10. **Show how to implement Decorator pattern using functional interfaces and method references.**

11. **Explain performance tuning: when to use parallelStream()? Pitfalls with shared state?**

12. **Design a callback mechanism using Consumer/Supplier. When is this pattern better than inheritance?**

13. **Explain the Observer pattern using BiConsumer for event handling. Show subscription/notification mechanism.**

14. **Compare lambda, anonymous class, method reference in terms of bytecode and performance.**

15. **Design a DSL (Domain Specific Language) using lambda and functional interfaces for query building.**

---

## LEVEL 3 - EXPERT PATTERNS

### Advanced Lambda Patterns

#### Pattern 1: Function Composition Pipeline
```java
Function<String, String> trim = String::trim;
Function<String, String> upper = String::toUpperCase;
Function<String, String> appendDot = s -> s + ".";

Function<String, String> pipeline = trim
    .andThen(upper)
    .andThen(appendDot);

String result = pipeline.apply("  hello  "); // "HELLO."
```

#### Pattern 2: Conditional Predicate Composition
```java
Predicate<String> isNotEmpty = s -> !s.isEmpty();
Predicate<String> hasLength = s -> s.length() > 3;
Predicate<String> startsWithA = s -> s.startsWith("a");

Predicate<String> combined = isNotEmpty
    .and(hasLength)
    .and(startsWithA);

List<String> filtered = words.stream()
    .filter(combined)
    .toList();
```

#### Pattern 3: Map Frequency Counter
```java
Map<String, Integer> freqMap = new HashMap<>();
words.forEach(word ->
    freqMap.merge(word, 1, Integer::sum)
);
```

#### Pattern 4: Stream Transformation Pipeline
```java
List<String> result = rawData.stream()
    .filter(s -> !s.isBlank())
    .map(String::trim)
    .map(String::toUpperCase)
    .distinct()
    .sorted()
    .toList();
```

#### Pattern 5: BiConsumer Event Handler
```java
BiConsumer<String, Throwable> errorHandler = (msg, ex) -> {
    System.err.println(msg);
    ex.printStackTrace();
};

try {
    // code
} catch (Exception e) {
    errorHandler.accept("Error occurred", e);
}
```

---

## ANSWERS KEY

### Level 1 Answers
1. Hello
2. 25
3. false
4. JAVA
5. Hi!
6. 42
7. true
8. 8
9. HELLO
10. 20
11. 6
12. true
13. false
14. 10
15. 4
16. HelloWorld
17. 7
18. false (extremely unlikely to be equal)
19. 42
20. method reference
21. HELLO
22. 0 (empty list)
23. [java]
24. 3
25. -1
26. 15
27. 15
28. 2
29. 1 2 3
30. 10
31. [a, ccc]
32. [BB, CCC]
33. [2, 4, 6]
34. 2
35. [1, 1, 3, 4, 5]

### Level 2 Answers
1. 13 (5*2=10, then 10+3=13)
2. 16 ((5+3)=8, then 8*2=16)
3. true
4. true
5. true (p1.or(p2) on "hello": length is 5, > 5 is false, but or means either works)
6. "42"
7. -1 (reversed reverses comparison: 5 vs 3 becomes 3 vs 5, so negative)
8. false (random values different)
9. 2
10. [1, 2, 3]
11. 16 ((3+5)*2 = 16)
12. application
13. [1, 2, 3]
14. aabbcccaa
15. 10 (1+2+3+4)
16. {1=3, 2=1, 3=3}
17. a1b2 (forEach prints key+value for each entry)
18. {java=1, python=5}
19. {a=2, b=4}
20. {a=2, b=2, c=1}
21. {key=[10, 20]}
22. {a=15}
23. unknown
24. HELLO
25. 6
26. 2
27. (compile error or result depends on implementation)
28. "42"
29. 10
30. 1
31. 10, 20 (captures reference to field)
32. "captured"
33. [1, 2, 3]
34. APPLE (only "apple" starts with "a")
35. true

---

