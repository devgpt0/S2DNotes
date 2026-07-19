# 05 - Method References, from First Look to Expert Use

## Start with the Smallest Idea

Look at these two lines:

```java
names.forEach(name -> System.out.println(name));
names.forEach(System.out::println);
```

They do the same work. The second line is a **method reference**.

A method reference is a short way to say:

> “For each value, call this existing method.”

Use it only when it makes the code easier to read.

## Why Does It Exist?

This lambda only passes its input to another method:

```java
text -> Integer.parseInt(text)
```

We are not adding new logic. We can point directly to the existing method:

```java
Integer::parseInt
```

The `::` symbol means “refer to this method.” It does **not** run the method immediately.

## First Runnable Example

Save this as `MethodReferenceDemo.java`:

```java
import java.util.List;

public class MethodReferenceDemo {
    public static void main(String[] args) {
        List<String> courses = List.of("Java", "Spring", "SQL");

        courses.forEach(System.out::println);
    }
}
// Output:
// Java
// Spring
// SQL
```

Read the main line like this:

> For every course, call `println` on `System.out`.

## Lambda and Method Reference Side by Side

```java
Function<String, Integer> withLambda = text -> Integer.parseInt(text);
Function<String, Integer> withReference = Integer::parseInt;

System.out.println(withLambda.apply("42"));
System.out.println(withReference.apply("42"));
// Output:
// 42
// 42
```

Both variables contain behavior. Calling `.apply("42")` runs that behavior.

## The Four Forms

You do not need to memorize all four at once. Learn them in this order.

### 1. Static Method

```java
Function<String, Integer> parse = Integer::parseInt;
System.out.println(parse.apply("25"));
// Output: 25
```

Long form: `text -> Integer.parseInt(text)`

### 2. Method on One Particular Object

```java
String prefix = "Course: ";
Function<String, String> label = prefix::concat;
System.out.println(label.apply("Java"));
// Output: Course: Java
```

Long form: `text -> prefix.concat(text)`

The object is already known: it is the string stored in `prefix`.

### 3. Method on the Value That Arrives

```java
Function<String, String> upper = String::toUpperCase;
System.out.println(upper.apply("java"));
// Output: JAVA
```

Long form: `text -> text.toUpperCase()`

The object is not known until `.apply(...)` receives it.

### 4. Constructor

```java
Supplier<ArrayList<String>> createList = ArrayList::new;
ArrayList<String> courses = createList.get();
courses.add("Java");
System.out.println(courses);
// Output: [Java]
```

Long form: `() -> new ArrayList<>()`

## Complete Example Using All Four

```java
import java.util.ArrayList;
import java.util.function.Function;
import java.util.function.Supplier;

public class AllMethodReferences {
    public static void main(String[] args) {
        Function<String, Integer> parse = Integer::parseInt;

        String prefix = "Score: ";
        Function<String, String> label = prefix::concat;

        Function<String, String> trim = String::trim;
        Supplier<ArrayList<String>> createList = ArrayList::new;

        ArrayList<String> results = createList.get();
        results.add(label.apply(trim.apply("  95  ")));

        System.out.println(parse.apply("42"));
        System.out.println(results);
    }
}
// Output:
// 42
// [Score: 95]
```

## Common Confusion: When Does It Run?

```java
Supplier<Long> clock = System::currentTimeMillis;
```

This line does not read the time. It stores a way to read the time.

```java
System.out.println(clock.get());
```

The call to `.get()` runs it.

## When a Normal Lambda Is Better

Do not force a method reference when you need extra work:

```java
Function<String, String> cleanLabel = text -> {
    String cleaned = text.trim().toUpperCase();
    return "Course: " + cleaned;
};
System.out.println(cleanLabel.apply("  java  "));
// Output: Course: JAVA
```

That reads more clearly than trying to hide several steps behind a method reference.

## Developer-Level Rules

- compare the method reference with its lambda form; keep the clearer one
- check the functional interface to know the input and result types
- prefer a named domain method over a chain of clever references
- be careful when a method name has several overloads; the surrounding type must select one

## Expert Understanding

Experts use two terms for the middle forms:

- **bound receiver:** the object is already chosen, such as `prefix::concat`
- **unbound receiver:** the arriving value becomes the object, such as `String::trim`

These names explain why `String::trim` fits `Function<String, String>`: the input string becomes the object on which `trim()` runs.

## Quick Memory Card

- `::` points to existing behavior
- it stores behavior; it does not run it immediately
- `Class::staticMethod`
- `object::instanceMethod`
- `Class::instanceMethod`
- `Class::new`
- use the form that a reader understands fastest

## Practice

Change the lambda to a method reference:

```java
List<String> names = List.of("Asha", "Ravi");
names.forEach(System.out::println);
// Output:
// Asha
// Ravi
```
